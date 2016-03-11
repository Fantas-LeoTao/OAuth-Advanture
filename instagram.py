# -*- coding: utf-8 -*-
# github oauth flow

CLIENT_ID = '8b956ef9a0b6424199568894ea4903e0'
CLIENT_SECRET = '36598f45283b4b3c85dc7821528b1d63'
AUTHORIZE_URL = 'https://api.instagram.com/oauth/authorize?'
ACCESS_TOKEN_URL = 'https://api.instagram.com/oauth/access_token?'
REDIRECT_URI = 'http://taolei.com/callback'

import urllib
import requests

from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def home():
    url = make_authorization_url()
    return '<a href="%s">Authenticate with instagram</a>' % url


@app.route('/callback/')
def callback():
    error = request.args.get('error', '')
    if error:
        return error
    code = request.args.get('code')
    token = get_token(code)
    source_url = 'https://api.instagram.com/v1/users/self/?access_token=%s' % token
    response = requests.get(source_url)
    return response.text


def make_authorization_url():
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code'
    }
    url = AUTHORIZE_URL + urllib.urlencode(params)
    return url


def get_token(code):
    post_data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'code': code
    }
    response = requests.post(ACCESS_TOKEN_URL, data=post_data)
    return response.json().get('access_token')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
