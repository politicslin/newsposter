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

def _matchBySource(source, targetsources):
    if targetsources:
        return source in targetsources.split(',')
    return True

def _matchByTopic(topic, targettopics):
    if targettopics:
        return topic in targettopics.split(',')
    return True

def _matchByTag(tags, targettags):
    if targettags:
        items = targettags.split(',')
        for item in items:
            grouptags = set(item.split('+'))
            if grouptags.issubset(tags):
                return True
        return False
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

def getPosters(topic, datasource, tags):
    if tags:
        tags = set(tags)
    else:
        tags = set()
    posters = _getPosters()
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
    posters = _getPosters()
    for poster in posters:
        if poster.get('slug') == posterslug:
            return _getRealPoster(poster)
    return None

