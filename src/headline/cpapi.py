import logging

from commonutil import stringutil
import globalconfig

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

def _isItemInCache(item):
    hashes = modelapi.getItemHash()
    lines = []
    url = item.get('url')
    if url:
        lines.append(url)
    title = item.get('title')
    if title:
        lines.append(title)
    hvalue = stringutil.calculateHash(lines)
    if hvalue in hashes:
        return True
    hashes.insert(0, hvalue)
    hashcount = globalconfig.getMaxItemHash4Cache()
    hashes = hashes[:hashcount]
    modelapi.saveItemHash(hashes)
    return False


def publishItems(datasource, items):
    topic = datasource.get('topic')
    sourceSlug = datasource.get('slug')
    sourcetags = datasource.get('tags')
    posters = _getPosters(topic, sourceSlug, sourcetags)
    newItems = []

    for item in items:
        if _isItemInCache(item):
            logging.info('Item/%s is already in cache.' % (item, ))
            continue
        newItems.append(item)

    for poster in posters:
        if poster.isOnlyNew():
            if newItems:
                poster.publish(datasource, newItems)
        else:
            poster.publish(datasource, items)

