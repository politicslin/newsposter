import webapp2
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'library'))

import headline.handlersapi
import headline.handlersadmin

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')


app = webapp2.WSGIApplication([
('/', MainPage),
('/api/poster/request/', headline.handlersapi.PosterRequest),
('/poster/response/', headline.handlersapi.PosterResponse),
('/admin/poster/test/', headline.handlersadmin.TestPage),
('/admin/poster/', headline.handlersadmin.AdminPage),
],
                              debug=True)

