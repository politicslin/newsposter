import json
import logging

from google.appengine.api import taskqueue

import webapp2

from commonutil import stringutil
from configmanager import cmapi
import globalconfig
from contentposter import cpapi

_MAX_TRY_COUNT = 5

def isItemInCache(item):
    hashkey = '.itemhash'
    hashes = cmapi.getItemValue(hashkey, [])
    lines = []
    url = item.get('url')
    if url:
        lines.append(url)
    title = item.get('title')
    if title:
        lines.append(title)
    hvalue = stringutil.calculateHash(lines)
    if hvalue in hashes:
        return True
    hashes.insert(0, hvalue)
    hashcount = globalconfig.getMaxItemHash4Cache()
    hashes = hashes[:hashcount]
    cmapi.saveItem(hashkey, hashes)
    return False


class PosterRequest(webapp2.RequestHandler):
    def post(self):
        rawdata = self.request.body
        # Use queue so we have a longer deadline.
        taskqueue.add(queue_name='default', payload=rawdata, url='/poster/response/')
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Request is accepted.')


class PosterResponse(webapp2.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        datasource = data['datasource']
        items = data['items']

        topic = datasource.get('topic')
        sourceSlug = '.'.join([topic, datasource.get('slug')])
        sourcetags = datasource.get('tags')
        posters = cpapi.getPosters(topic, sourceSlug, sourcetags)
        newItems = []

        for item in items:
            if isItemInCache(item):
                logging.info('Item/%s is already in cache.' % (item, ))
                continue
            newItems.append(item)

        for poster in posters:
            if poster.isOnlyNew():
                poster.publish(datasource, newItems)
            else:
                poster.publish(datasource, items)

        message = 'Publish %s to %s posters.' % (sourceSlug, len(posters), )
        logging.info(message)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(message)

