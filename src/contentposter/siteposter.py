import logging
import urllib2

import jsonpickle

from .baseposter import BasePoster

_URL_TIMEOUT = 30

class SitePoster(BasePoster):

    def __init__(self, url):
        self.url = url

    def isOnlyNew(self):
        return False

    def publish(self, datasource, items):
        data = {
                'origin': datasource,
                'items': items,
            }
        try:
            f = urllib2.urlopen(self.url, jsonpickle.encode(data),
                                timeout=_URL_TIMEOUT)
            f.read()
            f.close()
        except Exception:
            message = 'Failed to publish data to "%s".' % (self.url, )
            logging.exception(message)
        return True

