import os

from google.appengine.ext.webapp import template
import webapp2

from contentposter import cpapi

class TestPage(webapp2.RequestHandler):
    def _render(self, templateValues):
        self.response.headers['Content-Type'] = 'text/html'
        path = os.path.join(os.path.dirname(__file__), 'templates', 'test.html')
        self.response.out.write(template.render(path, templateValues))

    def get(self, message=None):
        posterSlug = self.request.get('poster')
        posters = cpapi.getAllPosters(onlyActive=False)
        templateValues = {
            'posterSlug': posterSlug,
            'posters': posters,
            'datasource': self.request.get('datasource'),
            'title': self.request.get('title'),
            'url': self.request.get('url'),
            'message': message,
        }
        self._render(templateValues)

    def post(self):
        datasourceName = self.request.get('datasource')
        title = self.request.get('title')
        url = self.request.get('url')
        posterSlug = self.request.get('poster')
        poster = cpapi.getPoster(posterSlug)
        datasouce = {'name': datasourceName}
        item = {'title': title, 'url': url}
        message = poster.publish(datasouce, item)
        return self.get(message='Message is published: %s.' % message)

