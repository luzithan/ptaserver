#!/usr/bin/env python
import os
from string import Template

import requests

from tokens import getClaimToken, getAuthToken

user = os.environ.get('PLEX_USERNAME', None)
password = os.environ.get('PLEX_PASSWORD', None)

if user is None:
    print('Error we need a PLEX_USERNAME environement variable')
    exit(-1)
if password is None:
    print('Error we need a PLEX_PASSWORD environement variable')
    exit(-1)

auth_token = getAuthToken(user,password)
claim_token = getClaimToken(auth_token)

from tzlocal import get_localzone
from datetime import datetime

try:
    local_tz = get_localzone()
    local_datetime = datetime.now(local_tz)
except:
    local_tz = 'Europe/Paris'

ip = requests.get('http://ipecho.net/plain').text

advertise_ip='http://%s:32400/'%ip

print('claim_token %s' % claim_token)
print('auth_token %s' % auth_token)
print('ip %s' % ip)
print('tz %s' % local_tz)


with open('/config/plex.env', 'w') as plex_env:
    plex_env.write("PLEX_CLAIM=%s\n" % claim_token)
    plex_env.write("PLEX_AUTH=%s\n" % auth_token)
    plex_env.write("ADVERTISE_IP=%s\n" % advertise_ip)
    plex_env.write("TZ=%s\n" % advertise_ip)
