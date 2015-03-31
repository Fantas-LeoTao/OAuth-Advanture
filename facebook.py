# -*- coding: utf-8 -*-
# fackbook oauth flow

CLIENT_ID = '759843707467725'
CLIENT_SECRET = 'd2a518f0e2709545728d44613ea0422d'
AUTHORIZE_URL = 'https://www.facebook.com/dialog/oauth?'
ACCESS_TOKEN_URL = 'https://graph.facebook.com/v2.3/oauth/access_token?'
REDIRECT_URI = 'http://taolei.com:5000/callback/'

import urllib
import requests

from flask import Flask, request, abort

app = Flask(__name__)


@app.route('/')
def home():
    url = make_authorization_url()
    return '<a href="%s">Authenticate with fackbook</a>' % url


@app.route('/callback/')
def callback():
    error = request.args.get('error', '')
    if error:
        return error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        abort(403)
    code = request.args.get('code')
    token = get_token(code)

    params = {
        'access_token': token,
        'input_token': token
    }
    source_url = 'https://graph.facebook.com/debug_token?' + urllib.urlencode(params)
    response = requests.get(source_url)
    return response.text


def generate_state():
    from uuid import uuid4
    return str(uuid4())


def save_state(state):
    pass


def is_valid_state(state):
    return True 


def make_authorization_url():
    state = generate_state()
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'state': state
    }
    url = AUTHORIZE_URL + urllib.urlencode(params)
    return url


def get_token(code):
    params = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'code': code
    }
    url = ACCESS_TOKEN_URL + urllib.urlencode(params)
    response = requests.get(url)
    return response.json().get('access_token')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
