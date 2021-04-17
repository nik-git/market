from pylib.logger import logger
from config.kiteconf import kiteconf
from kiteconnect import KiteConnect
import os
from pathlib import Path

this_file_path = Path(os.path.abspath(__file__))
api_key = kiteconf.get('api_key')
secret_key = kiteconf.get('secret_key')

with open(os.path.join(this_file_path.parent, '..', 'config', 'access_token.txt'), 'r') as fp:
    access_token = fp.read()
access_token = access_token

KITE = KiteConnect(api_key=api_key)
KITE.set_access_token(access_token)


def get_kite_connection():
    return KiteConnect(api_key=api_key)


def get_request_token():
    print(get_kite_connection().login_url())
    ## copy the login URL in browser and login from UI
    ## copy request_token from URL


# refresh once in a day
def save_access_token(request_token):
    data = get_kite_connection().generate_session(request_token,
                                                    api_secret=secret_key)
    access_token = data['access_token']
    with open(os.path.join(this_file_path.parent, '..', 'config', 'access_token.txt'),
              'w') as fp:
        fp.write(access_token)


def get_access_token():
    with open(os.path.join(this_file_path.parent, '..', 'config', 'access_token.txt'),
              'r') as fp:
        access_token = fp.read()
    return access_token

