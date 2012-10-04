import logging
import urllib2
import oauth2 as oauth

class TwitterPoster(object):

    def __init__(self, slug, name, comsumerkey, comsumersecret,
                 accesstoken, accesssecret):
        self.slug = slug
        self.name = name
        self.comsumerkey = comsumerkey
        self.comsumersecret = comsumersecret
        self.accesstoken = accesstoken
        self.accesssecret = accesssecret

    def _getContent(self, datasouce, item):
        # max len is counted as unicode,
        # which means it can send 140 Chinese character
        maxcontentlen = 140
        reserved4url = 20
        reserved4separator = 5
        sourcename = datasouce.get('name')
        itemtitle = item.get('title', '')
        maxTitleLen = maxcontentlen - len(sourcename) - maxcontentlen - separator
        return "%s: %s %s" % (
            sourcename,
            itemtitle[:maxTitleLen],
            item.get('url', ''),
        )

    def publish(self, datasouce, item):
        url = 'http://api.twitter.com/1/statuses/update.json'
        httpmethod = 'POST'
        proxyinfo = None

        content = self._getContent(datasouce, item)
        postbody = 'status=' +  urllib2.quote(content.encode('utf-8'))

        consumer = oauth.Consumer(key=self.comsumerkey, secret=self.comsumersecret)
        token = oauth.Token(key=self.accesstoken, secret=self.accesssecret)
        client = oauth.Client(consumer, token, proxy_info=proxyinfo)
        success = True
        try:
            result = client.request(
                           url,
                           method=httpmethod,
                           body=postbody,
                           headers=None
            )
            logging.info('return value: %s' % (result, ))
        except:
            success = False
            logging.exception('Failed to pubsh content to %s.' % (self.slug, ))
        return success

