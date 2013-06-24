import logging

from commonutil import collectionutil, stringutil

from contentposter.twitterposter import TwitterPoster
from contentposter.siteposter import SitePoster
from . import models

def _matchByTag(pageTags, targettags):
    matched = False
    for tag in targettags:
        if collectionutil.fullContains(pageTags, tag.split('+')):
            matched = True
            break
    return matched

def _getRealPoster(poster):
    if poster.get('type') == 'twitter':
        return TwitterPoster(
            poster.get('slug'),
            poster.get('name'),
            poster.get('comsumerkey'),
            poster.get('comsumersecret'),
            poster.get('accesstoken'),
            poster.get('accesssecret')
          )
    elif poster.get('type') == 'site':
        return SitePoster(
            poster.get('url')
          )
    return None

def getAllPosters(onlyActive):
    result = []
    posters = models.getPosters()
    if not posters:
        return result
    if not onlyActive:
        return posters
    for poster in posters:
        if poster.get('active', True):
            result.append(poster)
    return result

def _getPosters(topic, datasource, tags):
    if tags:
        tags = set(tags)
    else:
        tags = set()
    posters = getAllPosters(True)
    result = []
    for poster in posters:
        matched = False
        targettags = poster.get('tags')
        if not targettags or _matchByTag(tags, targettags):
            matched = True
        if matched:
            realposter = _getRealPoster(poster)
            if realposter:
                result.append(realposter)
    return result

def getPoster(posterslug):
    posters = getAllPosters(False)
    for poster in posters:
        if poster.get('slug') == posterslug:
            return _getRealPoster(poster)
    return None

def savePosters(posters):
    return models.savePosters(posters)

def _populatedDuplicatedFlag(item):
    monitorPage = item.get('monitor')
    if not monitorPage:
        return
    itemUrl = monitorPage.get('url')
    if not itemUrl:
        return
    if models.isPageInHistory(itemUrl):
        item['duplicated'] = True
    models.savePageHistory(itemUrl)

def publishItems(datasource, items):
    topic = datasource.get('topic')
    sourceSlug = datasource.get('slug')
    sourcetags = datasource.get('tags')
    posters = _getPosters(topic, sourceSlug, sourcetags)

    for item in items:
        _populatedDuplicatedFlag(item)

    for poster in posters:
        poster.publish(datasource, items)

