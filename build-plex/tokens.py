import os

import requests

URL_LOGIN = 'https://plex.tv/users/sign_in.json'
URL_CLAIM_TOKEN = 'https://plex.tv/api/claim/token.json'

PlexClientIdentifier = '4a745ae7-1839-e44e-1e42-aebfa578c865'


def getHeaders():
    return {
        'X-Plex-Client-Identifier': PlexClientIdentifier,
        'X-Plex-Product': 'Plex SSO',
    }


def getAuthToken(user, password):
    headers = getHeaders()

    data = 'user[login]=%s&user[password]=%s&user[remember_me]=1' % (user, password)

    response = requests.post(URL_LOGIN, headers=headers, data=data)
    data = response.json()

    return data['user']['authentication_token']


def getClaimToken(authToken=None):
    headers = getHeaders()
    headers['X-Plex-Token'] = authToken

    response = requests.get(URL_CLAIM_TOKEN, headers=headers)
    data = response.json()

    return data['token']
