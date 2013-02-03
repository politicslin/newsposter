import datetime

from configmanager import cmapi

import configmanager.models

class RuntimeStatus(configmanager.models.ConfigItem):
    pass

cmapi.registerModel(RuntimeStatus)

def _getPosterListKey():
    return 'poster-list'

def getPosters():
    return cmapi.getItemValue(_getPosterListKey(), [])

def savePosters(posters):
    return cmapi.saveItem(_getPosterListKey(), posters)

def isPageInHistory(url):
    pages = cmapi.getItemValue('page.history', [], modelname=RuntimeStatus)
    for page in pages:
        if page.get('url') == url:
            return True
    return False

def savePageHistory(url):
    pages = cmapi.getItemValue('page.history', [], modelname=RuntimeStatus)
    found = None
    for page in pages:
        if page.get('url') == url:
            found = page
            break
    if found:
        found['count'] += 1
    else:
        found = {}
        found['count'] = 1
        found['url'] = url
        pages.append(found)
    found['updated'] = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
    pages.sort(key=lambda page: page['updated'], reverse=True)
    pages.sort(key=lambda page: page['count'], reverse=True)
    MAX_COUNT = 1000
    RESET_COUNT = 200
    if len(pages) > MAX_COUNT:
        pages = pages[:RESET_COUNT]
    cmapi.saveItem('page.history', pages, modelname=RuntimeStatus)

