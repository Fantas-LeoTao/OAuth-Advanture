# -*- coding: utf-8 -*-
# dummy web server

CLIENT_ID = 'c943cb7b9b8a209bacee'
CLIENT_SECRET = '49e239697cb6d8093576b6a104659614b12e42b1'
AUTHORIZE_URL = 'http://open.com:8888/login/oauth/authorize?'
ACCESS_TOKEN_URL = 'http://open.com:8888/login/oauth/access_token'
REDIRECT_URI = 'http://taolei.com:5000/callback/'

import urllib
import requests

from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def home():
    url = make_authorization_url()
    return '<a href="%s">Authenticate with dummy</a>' % url


@app.route('/callback/')
def callback():
    error = request.args.get('error', '')
    if error:
        return error
    code = request.args.get('code')
    if not code:
        return
    token = get_token(code)
    source_url = 'http://open.com:8888/user?access_token=%s' % token
    response = requests.get(source_url)
    return response.text


def make_authorization_url():
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
    }
    url = AUTHORIZE_URL + urllib.urlencode(params)
    return url


def get_token(code):
    post_data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code
    }
    response = requests.post(
        ACCESS_TOKEN_URL,
        json=post_data)
    return response.json().get('access_token')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
