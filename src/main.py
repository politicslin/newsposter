import webapp2
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'library'))

import configmanager.handlers

import headline.handlersapi

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')


app = webapp2.WSGIApplication([
('/', MainPage),
('/configitem', configmanager.handlers.MainPage),
('/api/headline/poster/request', headline.handlersapi.PosterRequest),
('/api/headline/poster/response', headline.handlersapi.PosterResponse),
('/api/headline/poster/fail', headline.handlersapi.PosterFail),
],
                              debug=True)

