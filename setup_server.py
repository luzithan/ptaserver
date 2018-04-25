#!/usr/bin/env python
import os
from string import Template

import requests
from dotenv import find_dotenv
from dotenv import load_dotenv

from tokens import getClaimToken, getAuthToken

load_dotenv(find_dotenv())

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

with open('docker-compose.template.yml', 'r') as template_file:
    template = Template(template_file.read())

    env = os.environ.copy()
    env['TZ'] = str(local_tz)
    env['ADVERTISE_IP'] = advertise_ip
    env['PLEX_CLAIM'] = claim_token
    env['PLEX_AUTH'] = auth_token
    env['PWD'] = os.path.dirname(__file__)
    env['dl_data_movies'] = '/share/Movies'
    env['dl_data_tv'] = '/share/TV'
    treated = template.substitute(env)
    with open('docker-compose.yml', 'w') as yml_file:
        yml_file.write(treated)
