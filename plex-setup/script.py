import os

from plexapi.server import PlexServer
from attrdict import AttrDict


plex_server = 'http://' + os.environ.get('PLEX_SERVER', 'plex') + ':32400'

print('plex_server ' + plex_server)

plex = PlexServer(plex_server, os.environ.get('PLEX_AUTH'))

movie_section = AttrDict(scanner="Plex Movie Scanner", language="en", type="movie", agent="com.plexapp.agents.imdb",
                         location="/movies", name="Movies")

music_section = AttrDict(scanner="Plex Music Scanner", language="en", type="artist", agent="com.plexapp.agents.lastfm",
                         location="/music", name="Music")

tv_section = AttrDict(scanner="Plex Series Scanner", language="en", type="show", agent="com.plexapp.agents.thetvdb",
                      location="/tv", name="TV Shows")

photo_section = AttrDict(scanner="Plex Photo Scanner", language="en", type="photo", agent="com.plexapp.agents.none",
                         location="/photos", name="Photos")

sections_to_add = [movie_section, tv_section]

for section_to_add in sections_to_add:
    found = False
    for section in plex.library.sections():
        second = vars(section)
        # section_to_add found completely inside secod
        if all(k in second and second[k] == v for k, v in section_to_add.items()):
            # found the same section
            found = True
            print('Found section already added %s' % section_to_add)
    if not found:
        print('Add section %s' % section_to_add)
        plex.library.add(**section_to_add)
