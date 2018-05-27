#!/usr/bin/env python
import os
import time
from urllib import quote_plus

from plexapi.server import PlexServer
import yaml
from requests.exceptions import ConnectionError

plex_server = 'http://' + os.environ.get('PLEX_SERVER', 'localhost') + ':32400'
plex_auth = open('/.plex.auth', 'r').read()

print('plex_server: ' + plex_server)
print('plex auth: ' + plex_auth)


while True:
    try:
        plex = PlexServer(plex_server, plex_auth)
        break
    except ConnectionError:
        time.sleep(1)

sections_to_add = yaml.load(open('/etc/plex-setup/plex.conf.yml', 'r'))
print(sections_to_add)


def add_with_locations(title='', type='', agent='', scanner='', locations='', language='en', **kwargs):
    locations = '&'.join('location=%s' % quote_plus(loc) for loc in locations)
    part = '/library/sections?name=%s&type=%s&agent=%s&scanner=%s&language=%s&%s' % (
        quote_plus(title), type, agent, quote_plus(scanner), language, locations)  # noqa E126
    return plex.query(part, method=plex._session.post, **kwargs)


for section_name, section_to_add in sections_to_add.items():
    section_to_add['title'] = section_name
    found = False
    print('to_add: ' + str(section_to_add.items()))
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
        print('Adding Section %s' % section_name)
        add_with_locations(**section_to_add)
    else:
        print('Section %s already present' % section_name)

