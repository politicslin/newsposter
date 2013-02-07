import logging

from commonutil import stringutil

from contentposter.twitterposter import TwitterPoster
from contentposter.siteposter import SitePoster
from . import modelapi

def _matchBySource(source, targetsources):
    if targetsources:
        return source in targetsources.split(',')
    return False

def _matchByTopic(topic, targettopics):
    if targettopics:
        if targettopics == 'all':
            return True
        return topic in targettopics.split(',')
    return False

def _matchByTag(tags, targettags):
    if targettags:
        items = targettags.split(',')
        for item in items:
            grouptags = set(item.split('+'))
            if grouptags.issubset(tags):
                return True
    return False

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
    posters = modelapi.getPosters()
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
        targettopics = poster.get('targettopic')
        matched = False
        if _matchByTopic(topic, targettopics):
            matched = True
        if not matched:
            targetsources = poster.get('targetsource')
            if _matchBySource(datasource, targetsources):
                matched = True
        if not matched:
            targettags = poster.get('targettag')
            if _matchByTag(tags, targettags):
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
    return modelapi.savePosters(posters)

def _populatedDuplicatedFlag(item):
    monitorPage = item.get('monitor')
    if not monitorPage:
        return
    itemUrl = monitorPage.get('url')
    if not itemUrl:
        return
    if modelapi.isPageInHistory(itemUrl):
        item['duplicated'] = True
    modelapi.savePageHistory(itemUrl)

def publishItems(datasource, items):
    topic = datasource.get('topic')
    sourceSlug = datasource.get('slug')
    sourcetags = datasource.get('tags')
    posters = _getPosters(topic, sourceSlug, sourcetags)

    for item in items:
        _populatedDuplicatedFlag(item)

    for poster in posters:
        poster.publish(datasource, items)

