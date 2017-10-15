from datetime import timedelta
import omdb


class OmdbService(object):
    def search_title(self,value):
        result=omdb.search_series(value)
        if len(result)>=1:
            return result[0]['imdb_id']

    def getmovie_country(self,imdbid):
        obj = omdb.imdbid(imdbid)
        return obj['country'].lower()


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False