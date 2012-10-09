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

def _isMatched(slug, tags, targetslugs, targettags):
    if targetslugs:
        targetslugs = targetslugs.split(',')
        if 'all' in targetslugs:
            return True
        for targetslug in targetslugs:
            if targetslug in slug:
                return True
    if targettags:
        targettags = targettags.split(',')
        if 'all' in targettags:
            return True
        for targettag in targettags:
            if targettag in tags:
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
    return None

def getPosters(slug, tags):
    posters = _getPosters()
    result = []
    for poster in posters:
        targetslugs = poster.get('targetslugs')
        targettags = poster.get('targettags')
        if not _isMatched(slug, tags, targetslugs, targettags):
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

