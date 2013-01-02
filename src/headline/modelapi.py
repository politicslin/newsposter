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

def _getItemHashesKey():
    return 'item.hash'

def getItemHash():
    key = _getItemHashesKey()
    return cmapi.getItemValue(key, [], modelname=RuntimeStatus)

def saveItemHash(hashes):
    key = _getItemHashesKey()
    return cmapi.saveItem(key, hashes, modelname=RuntimeStatus)


