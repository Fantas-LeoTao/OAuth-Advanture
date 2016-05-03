# -*- coding: utf-8 -*-
# dummy oauth and resource server

CLIENT_ID = 'c943cb7b9b8a209bacee'
CLIENT_SECRET = '49e239697cb6d8093576b6a104659614b12e42b1'
CLIENTS_POOL = {CLIENT_ID: CLIENT_SECRET}
CODES_POOL = {}
TOKENS_POOL = {}
USER_INFO = {
    'account': '123456@gmail.com',
    'password': '123456',
    'uid': '1024',
    'name': 'taolei',
    'gender': 'unknown'
}
AUTHS_POOL = {'123456@gmail.com': USER_INFO}
USERS_POOL = {'1024': USER_INFO}


import uuid
def generate_code(uid):
    code = uuid.uuid1().hex
    CODES_POOL[code] = uid
    return code
def generate_token(uid):
    token = uuid.uuid1().hex
    TOKENS_POOL[token] = uid
    return token


from flask import (
    Flask, request, redirect, render_template,
    jsonify, url_for)
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField

app = Flask(__name__)
app.secret_key = 'dummy'


class LoginForm(Form):

    account = StringField('account')
    password = PasswordField('password')

    def validate(self):
        base = super(LoginForm, self).validate()
        if not base:
            return False
        return True


@app.route('/login/oauth/authorize')
def enter():
    if request.args.get('client_id') in CLIENTS_POOL:
        # TODO 通常还要检验redirect_uri是否合法
        redirect_uri = request.args.get('redirect_uri')
        return redirect(url_for('login', redirect_uri=redirect_uri))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()
        return render_template('login.html', form=form)
    elif request.method == 'POST':
        form = LoginForm()
        if not form.validate_on_submit():
            return render_template('login.html', form=form)
        # 用户和应用信息到这一步都会获取完毕
        user = AUTHS_POOL.get(form.account.data)
        if user:
            code = generate_code(user['uid'])
            redirect_uri = request.args.get('redirect_uri')
            if redirect_uri:
                redirect_uri = redirect_uri + '?' + 'code=%s' % code
            return redirect(redirect_uri)


@app.route('/login/oauth/access_token', methods=['POST'])
def token():
    req_info = request.get_json()
    # TODO 校验过程
    client_id = req_info['client_id']
    client_secret = req_info['client_secret']
    code = req_info['code']
    if CLIENTS_POOL.get(client_id) == client_secret:
        uid = CODES_POOL.get(code)
        token = generate_token(uid)
        return jsonify({'access_token': token}), 201


@app.route('/user')
def user_info():
    token = request.args.get('access_token')
    uid = TOKENS_POOL.get(token)
    return jsonify(USERS_POOL.get(uid)), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
