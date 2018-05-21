import os

from plexapi.server import PlexServer
from attrdict import AttrDict


plex_server = 'http://' + os.environ['PLEX_SERVER'] + ':32400'
plex_auth = os.environ['PLEX_AUTH']

print('plex_server ' + plex_server)
print('plex auth' + plex_auth)


plex = PlexServer(plex_server, plex_auth)

movie_section = AttrDict(scanner="Plex Movie Scanner", language="en", type="movie", agent="com.plexapp.agents.imdb",
                         locations=["/movies"], title="Movies")

movies_data_section = AttrDict(scanner="Plex Movie Scanner", language="en", type="movie", agent="com.plexapp.agents.imdb",
                         locations=["/data/movies"], title="Data Movies")

tv_section = AttrDict(scanner="Plex Series Scanner", language="en", type="show", agent="com.plexapp.agents.thetvdb",
                      locations=["/tv"], title="TV Shows")

tv_data_section = AttrDict(scanner="Plex Movie Scanner", language="en", type="movie", agent="com.plexapp.agents.imdb",
                         locations=["/data/tv"], title="Data TV Shows")

sections_to_add = [movie_section, tv_section]

for section_to_add in sections_to_add:
    found = False
    print('to_add: ' + str(list(section_to_add.items())))
    for section in plex.library.sections():
        second = vars(section)
        # section_to_add found completely inside secod
        print('present: ' + str(list(second.items())))
        if all(k in second and second[k] == v for k, v in section_to_add.items()):
            # found the same section
            found = True
            print('Found section already added %s' % section_to_add)
    print('---------------')
    if not found:
        print('Addin Section %s' % section_to_add.title)
#        plex.library.add(**section_to_add)
    else:
        print('Section %s already present' % section_to_add.title)

