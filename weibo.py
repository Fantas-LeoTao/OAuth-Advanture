# -*- coding: utf-8 -*-
# weibo oauth flow

CLIENT_ID = '1814846457'
CLIENT_SECRET = '164733c9f63e4912dbe05c0a820480a5'
AUTHORIZE_URL = 'https://api.weibo.com/oauth2/authorize?'
ACCESS_TOKEN_URL = 'https://api.weibo.com/oauth2/access_token'
SOURCE_URL = 'https://api.weibo.com/oauth2/get_token_info'
REDIRECT_URI = 'http://taolei.com:5000/callback/'

import urllib
import requests

from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def home():
    url = make_authorization_url()
    print url
    return '<a href="%s">Authenticate with weibo</a>' % url


@app.route('/callback/')
def callback():
    error = request.args.get('error', '')
    if error:
        return error
    code = request.args.get('code')
    token = get_token(code)
    print token, 'token'
    post_data = {'access_token': token}
    response = requests.post(SOURCE_URL, data=post_data)
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
        'redirect_uri': REDIRECT_URI,
        'code': code,
        'grant_type': 'authorization_code'
    }
    response = requests.post(
        ACCESS_TOKEN_URL,
        data=post_data)
    print response.content
    return response.json().get('access_token')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
