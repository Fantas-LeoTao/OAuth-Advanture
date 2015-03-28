# -*- coding: utf-8 -*-
# douban oauth flow

CLIENT_ID = '0f0abeedbb0535112d203cc9310f9f33'
CLIENT_SECRET = 'fccfc157bb243f61'
AUTHORIZE_URL = 'https://www.douban.com/service/auth2/auth?'
ACCESS_TOKEN_URL = 'https://www.douban.com/service/auth2/token'
SOURCE_URL = ''
REDIRECT_URI = 'http://taolei.com:5000/callback/'

import urllib
import requests

from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def home():
    url = make_authorization_url()
    return '<a href="%s">Authenticate with douban</a>' % url


@app.route('/callback/')
def callback():
    error = request.args.get('error', '')
    if error:
        return error
    code = request.args.get('code')
    token = get_token(code)
    source_url = 'https://api.douban.com/v2/user/~me'
    headers = {'Authorization': 'Bearer %s' % token}
    response = requests.get(source_url, headers=headers)
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
