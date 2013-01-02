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

class AdminPage(webapp2.RequestHandler):
    def _render(self, templateValues):
        self.response.headers['Content-Type'] = 'text/html'
        path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
        self.response.out.write(template.render(path, templateValues))

    def get(self):
        return self.post()

    def post(self):
        message = ''
        posterTypes = ['twitter', 'site']
        posters = cpapi.getAllPosters(onlyActive=False)

        action = self.request.get('action')

        selectedslug = self.request.get('selectedslug')
        slug = self.request.get('slug')

        if not selectedslug and action == 'Save':
            selectedslug = slug

        poster = None
        for item in posters:
            if selectedslug == item.get('slug'):
                poster = item
        if not poster:
            poster = {}

        if action == 'Save':
            poster['name'] = self.request.get('name')
            poster['active'] = bool(self.request.get('active'))
            poster['type'] = self.request.get('type')
            if poster['type'] == 'site':
                poster['url'] = self.request.get('url')
            elif poster['type'] == 'twitter':
                poster['accesstoken'] = self.request.get('accesstoken')
                poster['accesssecret'] = self.request.get('accesssecret')
                poster['comsumerkey'] = self.request.get('comsumerkey')
                poster['comsumersecret'] = self.request.get('comsumersecret')
            poster['targetsource'] = self.request.get('targetsource')
            poster['targettag'] = self.request.get('targettag')
            poster['targettopic'] = self.request.get('targettopic')
            if selectedslug and slug and selectedslug != slug:
                message = ('Error: select slug'
                        ' and input slug have different values.')
            else:
                if 'slug' not in poster:
                    poster['slug'] = slug
                    if poster['slug']:
                        posters.append(poster)
                cpapi.savePosters(posters)
        elif action == 'Remove':
            if poster:
                posters.remove(poster)
                cpapi.savePosters(posters)
                poster = {}
        templateValues = {
            'posterTypes': posterTypes,
            'posters': posters,
            'poster': poster,
            'message': message,
        }
        self._render(templateValues)

