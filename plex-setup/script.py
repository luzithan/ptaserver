import os

from plexapi.server import PlexServer
from attrdict import AttrDict


plex_server = 'http://' + os.environ['PLEX_SERVER'] + ':32400'
plex_auth = os.environ['PLEX_AUTH']

print('plex_server ' + plex_server)
print('plex auth' + plex_auth)


plex = PlexServer(plex_server, plex_auth)

movie_section = AttrDict(scanner="Plex Movie Scanner", language="en", type="movie", agent="com.plexapp.agents.imdb",
                         location="/movies", name="Movies")

movies_data_section = AttrDict(scanner="Plex Movie Scanner", language="en", type="movie", agent="com.plexapp.agents.imdb",
                         location="/data/movies", name="Data Movies")

tv_section = AttrDict(scanner="Plex Series Scanner", language="en", type="show", agent="com.plexapp.agents.thetvdb",
                      location="/tv", name="TV Shows")

tv_data_section = AttrDict(scanner="Plex Movie Scanner", language="en", type="movie", agent="com.plexapp.agents.imdb",
                         location="/data/tv", name="Data TV Shows")

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
