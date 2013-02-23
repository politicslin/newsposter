import logging

from commonutil import networkutil

from .baseposter import BasePoster

_URL_TIMEOUT = 30
_POST_TRY_COUNT = 3

class SitePoster(BasePoster):

    def __init__(self, url):
        self.url = url

    def publish(self, datasource, items):
        data = {
                'datasource': datasource,
                'items': items,
            }
        success = networkutil.postData(self.url, data,
                    trycount=_POST_TRY_COUNT, timeout=_URL_TIMEOUT)
        return success

