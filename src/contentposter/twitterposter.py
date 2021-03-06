import logging
import urllib2
import oauth2 as oauth
import json

from .baseposter import BasePoster

class TwitterPoster(BasePoster):

    def __init__(self, slug, name, comsumerkey, comsumersecret,
                 accesstoken, accesssecret):
        self.slug = slug
        self.name = name
        self.comsumerkey = comsumerkey
        self.comsumersecret = comsumersecret
        self.accesstoken = accesstoken
        self.accesssecret = accesssecret

    def _getContent(self, datasource, item):
        # max len is counted as unicode,
        # which means it can send 140 Chinese character
        maxcontentlen = 140
        reserved4url = 20
        reserved4separator = 5
        sourcename = datasource.get('name')
        itemtitle = None
        if 'monitor' in item:
            itemtitle = item['monitor'].get('title')
        if not itemtitle and 'editor' in item:
            itemtitle = item['editor'].get('title')
        if itemtitle is None:
            itemtitle = ''
        maxTitleLen = maxcontentlen - len(sourcename) - reserved4url - reserved4separator
        return "%s: %s %s" % (
            sourcename,
            itemtitle[:maxTitleLen],
            item.get('url', ''),
        )

    def _publishItem(self, datasource, item):
        url = 'http://api.twitter.com/1/statuses/update.json'
        httpmethod = 'POST'
        proxyinfo = None

        content = self._getContent(datasource, item)
        postbody = 'status=' +  urllib2.quote(content.encode('utf-8'))

        consumer = oauth.Consumer(key=self.comsumerkey, secret=self.comsumersecret)
        token = oauth.Token(key=self.accesstoken, secret=self.accesssecret)
        client = oauth.Client(consumer, token, proxy_info=proxyinfo)
        success = True
        try:
            responsehead, responsebody = client.request(
                           url,
                           method=httpmethod,
                           body=postbody,
                           headers=None
            )
            # I do not know when should the request be retried.
            published = True
            if responsehead.get('reason') != 'OK':
                published = False
            else:
                responsebodyItem = json.loads(responsebody)
                if responsebodyItem.get('error'):
                    published = False
            if not published:
                logging.error('Content: %s, return value: %s, %s. ' % (
                                content, responsehead, responsebody,))
        except:
            success = False
            logging.exception('Failed to pubsh %s to %s.' % (content, self.slug, ))
        if success and responsebody:
            return responsebody
        return success

    def publish(self, datasource, items):
        for item in items:
            if item.get('duplicated'):
                continue
            self._publishItem(datasource, item)
        return True

