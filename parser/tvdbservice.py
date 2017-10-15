import os
import tvdb_api

from flask import current_app


class TvdbSeasonnotfound(tvdb_api.tvdb_seasonnotfound):
    pass


class TvdbShownotfound(tvdb_api.tvdb_shownotfound):
    pass


from pyswagger import App, Security
from pyswagger.contrib.client.requests import Client

# load Swagger resource file into App object
#app = App._create_('https://api.thetvdb.com/swagger.json')
app = App._create_('file://%s/swagger.json' % os.path.dirname(__file__))


class TvdbService(object):
    def __init__(self, config=None):
        config = current_app.config
        auth = Security(app)
        def get_jwt_token():
            apikey = config['TVDBAPI_KEY']
            userkey = config['TVDBAPI_USERKEY']
            username = config['TVDBAPI_USERNAME']
            pass

        os.environ['TVDBAPI_JWT'] = os.environ.get('TVDBAPI_JWT', get_jwt_token())

        auth.update_with('jwtToken', os.environ['TVDBAPI_JWT'])  # api key

        # init swagger client
        client = Client(auth)



        langs = open('langs', 'r').readlines()


        tvdbapi = tvdb_api.Tvdb()
        self.tvdbapis = {}
        langs_tvdb = tvdbapi.config['valid_languages']
        for lg in langs_tvdb:
            self.tvdbapis[lg] = tvdb_api.Tvdb(apikey=config.TVDBAPI_KEY, language=lg,
                                              cache=True, forceConnect=True, banners=True)
        for lg in langs:
            try:
                self.tvdbapis[lg] = tvdb_api.Tvdb(apikey=config.TVDBAPI_KEY, language=str(lg.audio),
                                                  cache=True, forceConnect=True, banners=True)
            except ValueError:
                pass

    def getshow_info(self, show):
        try:
            return self.tvdbapis[show.lang.audio][show.seriesname]
        except tvdb_api.tvdb_seasonnotfound:
            raise TvdbSeasonnotfound()

    def getepisode(self, lang, showtitle, season, episode):
        return self.tvdbapis[lang][showtitle][season][episode]

    def getepisode_info(self, episode):
        return self.tvdbapis[episode.lang][episode.seriesname][episode.seasonnumber][episode.episodenumber]

    def get_allepisodes(self, show):
        show_info = self.tvdbapis[show.lang][show.seriesname]
        for season_number in show_info:
            if season_number != 0:
                season = show_info[season_number]
                for episode_number in season:
                    episode = season[episode_number]
                    yield episode

    def getshow(self, lang, seriesname):
        pass


