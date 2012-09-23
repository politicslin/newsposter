import webapp2
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'library'))

import headline.handlersapi

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')


app = webapp2.WSGIApplication([
('/', MainPage),
('/api/headline/poster/request', headline.handlersapi.PosterRequest),
('/api/headline/poster/response', headline.handlersapi.PosterResponse),
],
                              debug=True)

