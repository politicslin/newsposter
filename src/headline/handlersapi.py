import json
import logging

from google.appengine.api import taskqueue

import webapp2

from commonutil import networkutil

from . import cpapi

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

        uuid = data.get('uuid')
        if networkutil.isUuidHandled(uuid):
            message = 'PosterResponse: %s is already handled.' % (uuid, )
            logging.warn(message)
            self.response.out.write(message)
            return
        networkutil.updateUuids(uuid)

        datasource = data['datasource']
        items = data['items']
        cpapi.publishItems(datasource, items)

        message = 'Publish %s.' % (datasource, )
        logging.info(message)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(message)

