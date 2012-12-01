import webapp2
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'library'))

import configmanager.handlers

import headline.handlersapi
import headline.handlersadmin

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')


app = webapp2.WSGIApplication([
('/', MainPage),
('/configitem/', configmanager.handlers.MainPage),
('/api/poster/request/', headline.handlersapi.PosterRequest),
('/poster/response/', headline.handlersapi.PosterResponse),
('/poster/fail/', headline.handlersapi.PosterFail),
('/admin/poster/test/', headline.handlersadmin.TestPage),
('/admin/poster/', headline.handlersadmin.AdminPage),
],
                              debug=True)

