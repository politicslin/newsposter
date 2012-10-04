import httplib2
import json
import logging
import urllib2

from google.appengine.api import taskqueue

import webapp2
import oauth2 as oauth

from contentposter import cpapi

_MAX_TRY_COUNT = 5

def _put2FailQueue(triedcount, posterslug, datasource, item):
    if triedcount >= _MAX_TRY_COUNT:
        logging.error('Failed to publish %s to %s for %s.' % (item.get('url'),
             posterslug, datasource.get('slug')))
        return
    data = {
        'posterslug': posterslug,
        'datasource': datasource,
        'item': item,
        'tredcount': triedcount,
      }
    taskqueue.add(queue_name='fail', payload=json.dumps(data), url='/api/headline/poster/fail')

class PosterRequest(webapp2.RequestHandler):
    def post(self):
        rawdata = self.request.body
        # Use queue so we have a longer deadline.
        taskqueue.add(queue_name='headline', payload=rawdata, url='/api/headline/poster/response')
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Request is accepted.')


class PosterResponse(webapp2.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        datasouce = data['datasource']
        items = data['items']

        sourceslug = datasouce.get('slug')
        sourcetags = datasouce.get('tags')
        posters = cpapi.getPosters(sourceslug, sourcetags)
        for item in items:
            for poster in posters:
                if not poster.publish(datasouce, item):
                    _put2FailQueue(1, poster.slug, datasouce, item)
        message = 'Publish %s to %s posters.' % (sourceslug, len(posters), )
        logging.info(message)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(message)


class PosterFail(webapp2.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        posterslug = data['posterslug']
        datasource = data['datasource']
        item = data['item']
        tredcount = data['tredcount']
        poster = cpapi.getPoster(posterslug)
        if poster:
            if poster.publish(datasource, item):
                message = 'Publish %s to %s.' % (datasource.get('slug'), posterslug, )
            else:
                _put2FailQueue(tredcount + 1, poster.slug, datasource, item)
                message = 'Failed to publish %s to %s.' % (datasource.get('slug'), posterslug, )
        else:
            message = '%s is not available.' % (posterslug, )
        logging.info(message)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(message)

