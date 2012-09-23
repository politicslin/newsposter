import httplib2
import json
import logging
import urllib2

import oauth2 as oauth

from google.appengine.api import taskqueue

import webapp2

def _distribute(url, self_comsumer_key, self_comsumer_secret, self_access_token, self_access_token_secret, 
             http_method='GET', post_body='', proxy_info=None):
    consumer = oauth.Consumer(key=self_comsumer_key, secret=self_comsumer_secret)
    token = oauth.Token(key=self_access_token, secret=self_access_token_secret)
    client = oauth.Client(consumer, token, proxy_info=proxy_info)
    resp, content = client.request(
        url,
        method=http_method,
        body=post_body,
        headers=None
    )
    return content

def _distribute2twitter(content):
    url = 'http://api.twitter.com/1/statuses/update.json'
    comsumerkey = 'Z0gscpxJz4Jz8kGDmielxA'
    comsumersecret = 'aXGuWtLK3WhZcg0xuzn4ldQpNBdLNavuAFNvefN6Pc'
    accesstoken = '17037491-ZgFJGdCC8DJNoN8VvNZ9CVhWBiLSrUSYNZsSc7eY'
    accesssecret = 'lKCqFnSY4c7PiIJVZ3iXe4Sp7V9bbP3wDIcMhdsCZ3I'

    httpmethod = 'POST'
    postbody = 'status=' +  urllib2.quote(content.encode('utf-8'))

    proxyinfo = None

    _distribute(url, comsumerkey, comsumersecret, accesstoken, accesssecret, httpmethod, postbody, proxyinfo)

def _distributeItem(item):
    lines = []
    itemtitle = item.get('title')
    if itemtitle:
        lines.append(itemtitle)
    itemurl = item.get('url')
    if itemurl:
        lines.append(itemurl)
    content = ' '.join(lines)
    _distribute2twitter(content) 

class PosterRequest(webapp2.RequestHandler):
    def post(self):
        rawdata = self.request.body
        # Use queue so we have a longer deadline.
        taskqueue.add(queue_name='headline', payload=rawdata, url='/api/headline/poster/response')
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Request is accepted.')


class PosterResponse(webapp2.RequestHandler):
    def post(self):
        items = json.loads(self.request.body)
        for item in items:
            _distributeItem(item)

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Response is generated.')

