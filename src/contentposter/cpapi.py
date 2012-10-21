from configmanager import cmapi
from .twitterposter import TwitterPoster

def _getPosters():
    result = []
    posters = cmapi.getItemValue('poster-list')
    if not posters:
        return result
    for poster in posters:
        if poster.get('active', True):
            result.append(poster)
    return result

def _matchByTopic(topic, targettopics):
    if targettopics:
        return topic in targettopics.split(',')
    return True

def _matchByTag(tags, targettags):
    if targettags:
        targettags = set(targettags.split(','))
        return not targettags.isdisjoint(tags)
    return True

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
    return None

def getPosters(topic, tags):
    if tags:
        tags = set(tags)
    else:
        tags = set()
    posters = _getPosters()
    result = []
    for poster in posters:
        targettopics = poster.get('targettopics')
        if not _matchByTopic(topic, targettopics):
            continue
        targettags = poster.get('targettags')
        if not _matchByTag(tags, targettags):
            continue
        realposter = _getRealPoster(poster)
        if realposter:
            result.append(realposter)
    return result

def getPoster(posterslug):
    posters = _getPosters()
    for poster in posters:
        if poster.get('slug') == posterslug:
            return _getRealPoster(poster)
    return None

