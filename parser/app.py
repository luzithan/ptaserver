import json
import os
import re
from collections import namedtuple

import PTN
import tvnamer
import tvnamer.config
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, Response
from tvdb_exceptions import *
from tvnamer.tvnamer_exceptions import DataRetrievalError, UserAbort, InvalidFilename
from tvnamer.utils import FileParser, DatedEpisodeInfo, AnimeEpisodeInfo

fileparser = FileParser('')
resplit = re.compile('[ \._\-\+\(\)\}\{\[\]]')


class ParserException(Exception):
    pass


Lang = namedtuple('Lang', ['audio', 'subtitles'])
Show = namedtuple('Show', ['seriesname', 'lang'])
Episode = namedtuple('Episode', ['show', 'seasonnumber', 'episodenumber'])


def get_Lang(audio, subtitles=None):
    return Lang(audio=audio, subtitles=subtitles)


class ParserService(object):
    def __init__(self, tvdb, omdb):
        self.tvdb = tvdb
        self.omdb = omdb

    def parse(self, string):
        episodedict = self.parseraw(string)
        if not episodedict:
            raise ParserException('Can\'t parse ' + string)
        lang = Lang(audio=episodedict['lang'].audio,
                    subtitles=episodedict['lang'].subtitles)
        show = Show(seriesname=episodedict['seriesname'], lang=lang)

        episode = Episode(show=show, seasonnumber=episodedict['seasonnumber'],
                          episodenumber=episodedict['episodenumber'])
        if not episode:
            return
        return episode

    def parseraw(self, string):
        ei0 = self.initialparse(string)
        if ei0 is None:
            return None
        spl = self.split(string)
        spl, lang = self.detectlanguage(string, spl, ei0)

        if lang is None:
            # spl,langdetect=self.detectlanguage()
            return

        ei0 = self.parseonelanguage(string, lang)
        if ei0 is None:
            return

        if isinstance(ei0, DatedEpisodeInfo):
            return
        if isinstance(ei0, AnimeEpisodeInfo):
            return
        if len(ei0.episodenumbers) == 1:
            return dict(lang=lang, seriesname=ei0.seriesname,
                        seasonnumber=ei0.seasonnumber,
                        episodenumber=ei0.episodenumbers[0])

    def parseonelanguage(self, string, lang):
        lang = lang.audio
        fileparser.path = string
        tvnamer.config.Config['language'] = lang
        ei0 = fileparser.parse()
        try:
            ei0.populateFromTvdb(self.tvdb.tvdbapis[lang])
        except (DataRetrievalError, AttributeError, UserAbort, InvalidFilename, KeyError) as ex:
            pass
        except tvdb_attributenotfound:
            pass
        if type(ei0) == tvnamer.utils.NoSeasonEpisodeInfo:
            pass
        return ei0

    def initialparse(self, string):
        return self.parseonelanguage(string, Lang(audio='en', subtitles=None))

    def split(self, string):
        spl = []
        for idx, cmatch in enumerate(fileparser.compiled_regexs):
            if '([\\._ -]|$|[^\\/]*$)' in cmatch.pattern:
                newpattern = cmatch.pattern.replace('([\\._ -]|$|[^\\/]*$)', '(?P<extra>[\\._ -]|$|[^\\/]*$)')
            else:
                newpattern = cmatch.pattern.replace('[^\\/]*', '(?P<extra>[^\\/]*)')
            newcmatch = re.compile(newpattern, re.VERBOSE)
            match = newcmatch.match(string)
            if match:
                # namedgroups = match.groupdict().keys()
                matchgroupextra = match.group('extra')
                spl = resplit.split(matchgroupextra)
                spl = [x.lower() for x in spl if x != '']
                break
        return spl

    def detectlanguage(self, string, spl, ei0):
        toparsestring = string
        toparsestring, ext = tvnamer.utils.split_extension(toparsestring)
        # splittokens=re.compile('\.| |-|_')

        fileparser.path = toparsestring

        # eis=[]
        # infoarray=[]

        def _search(forward, source, target, start=0, end=None):
            """Naive search for target in source."""
            m = len(source)
            n = len(target)
            if end is None:
                end = m
            else:
                end = min(end, m)
            if n == 0 or (end - start) < n:
                # target is empty, or longer than source, so obviously can't be found.
                return False
            if forward:
                x = range(start, end - n + 1)
            else:
                x = range(end - n, start - 1, -1)
            for i in x:
                if source[i:i + n] == target:
                    return True
            return False

        import functools

        search = functools.partial(_search, True)
        # rsearch = functools.partial(_search, False)

        thislang = 'en'
        show = self.tvdb.tvdbapis[thislang][ei0.seriesname]

        lang = [0, 0]

        try:
            imdbid = show.data['imdb_id']
            if imdbid:
                country = self.omdb.getmovie_country(imdbid)
                if 'us' in country or 'uk' in country:
                    lang = get_Lang(audio='en')
                elif 'france' in country:
                    lang = get_Lang(audio='fr')
                elif 'sweden' in country:
                    lang = get_Lang(audio='sv')
        except KeyError:
            pass
        # network=show.data['network']

        if 'ita' in spl:
            lang = get_Lang(audio='it')
        elif 'french' in spl:
            lang = get_Lang(audio='fr')
        elif 'german' in spl:
            lang = get_Lang(audio='de')
        elif search(spl, ['thor', 'pl']):
            lang = get_Lang(audio='pl')
        elif search(spl, ['german', 'ws']) or search(spl, ['ws', 'german']):
            lang = get_Lang(audio='de')
        if search(spl, ['subtitulado', 'esp']) or search(spl, ['esp', 'subtitulado']):
            lang.subtitles = 'es'
        if search(spl, ['arabic', 'subtitles']):
            lang.subtitles = 'ar'
        if search(spl, ['nl', 'sub']) or search(spl, ['nl', 'subs']):
            lang.subtitles = 'nl'
        if search(spl, ['pl', 'sub']) or search(spl, ['pl', 'subs']):
            lang.subtitles = 'pl'
        if 'rus' in spl:
            lang.subtitles = 'ru'
        if 'swesub' in spl:
            lang.subtitles = 'se'
        if 'napisypl' in spl:
            lang.subtitles = 'pl'
        if 'subtitulado' in spl:
            lang.subtitles = 'es'
        if 'vostfr' in spl:
            lang.subtitles = 'fr'

        if lang is [0, 0]:
            return spl, None
        return spl, lang


try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


load_dotenv(find_dotenv())


def create_app():
    app = Flask("TV shows file names parser")

    @app.route('/', methods=['GET'])
    def root_parser():
        result = PTN.parse(request.data)
        return Response(json.dumps(result), mimetype='text/json')
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=os.environ.get('PARSER_PORT', 8081), host='0.0.0.0')
