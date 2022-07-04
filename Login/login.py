from .crypto import make_key, encrypt
import requests

URL_GET_RSA_KEY = 'https://store.steampowered.com/login/getrsakey/'
URL_LOGIN = 'https://store.steampowered.com/login/dologin/'
URL_STORE_TRANSFER = 'https://steamcommunity.com/login/transfer'


def get_rsa_key(jar, username):

    resp = requests.post(URL_GET_RSA_KEY, params={
                         'username': username}, cookies=jar)
    assert resp.status_code == 200, "Invalid response code: {}".format(
        resp.status_code)
    data = resp.json()

    mod = int(data['publickey_mod'], 16)
    exp = int(data['publickey_exp'], 16)

    return {
        'key': make_key(mod, exp),
        'timestamp': data['timestamp']
    }


def login(jar, username, password):
    rsa = get_rsa_key(jar, username)

    params = {
        'captcha_text': '',
        'captchagid': -1,
        'emailauth': '',
        'emailsteamid': '',
        'loginfriendlyname': '',
        'captcha_text': '',
        'remember_login': False,
        'username': username,
        'rsatimestamp': rsa['timestamp'],
        'password': encrypt(rsa['key'], password)
    }

    resp = requests.post(URL_LOGIN, data=params, cookies=jar)
    assert resp.status_code == 200, "Login failed."

    data = resp.json()
    jar.update(resp.cookies)

    if data['success'] and 'transfer_parameters' in data:
        return data['transfer_parameters']

    elif data.get('emailauth_needed'):
        code = input("Enter the code you received in your email: ")
        params['emailauth'] = code.upper()
        params['emailsteamid'] = data['emailsteamid']

        resp = requests.post(URL_LOGIN, data=params, cookies=jar)
        assert resp.status_code == 200, "Login failed."

        data = resp.json()
        assert data['success'], "Login failed."

        jar.update(resp.cookies)
        return data['transfer_parameters']

    elif data.get('requires_twofactor'):
        code = input(
            "Enter the code you received from the Authenticator app: ")
        params['twofactorcode'] = code.upper()
        resp = requests.post(URL_LOGIN, data=params, cookies=jar)
        assert resp.status_code == 200, "Login failed."

        data = resp.json()
        assert data['success'], "Login failed."

        jar.update(resp.cookies)
        return data['transfer_parameters']

    else:
        logger.info("Login failed.")
        logger.info(data)
        assert False, "Could not log in. Sorry."


def transfer_login(jar, auth_ctx):
    resp = requests.post(URL_STORE_TRANSFER, auth_ctx, cookies=jar)
    jar.update(resp.cookies)
    return jar
