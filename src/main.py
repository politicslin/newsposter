import webapp2
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'library'))

import router.handlersapi
import router.handlersadmin

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')


app = webapp2.WSGIApplication([
('/', MainPage),
('/api/poster/request/', router.handlersapi.PosterRequest),
('/poster/response/', router.handlersapi.PosterResponse),
('/admin/poster/test/', router.handlersadmin.TestPage),
('/admin/poster/', router.handlersadmin.AdminPage),
],
                              debug=True)

