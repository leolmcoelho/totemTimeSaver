
import json
import sys
import os
import time
import requests
from dotenv import dotenv_values
from urllib.parse import quote

sys.path.append(os.getcwd())
from src.bot.my_logger import get_logger
from src.models.user import *

logging = get_logger()


config = dotenv_values('config/SITE.env')
config_user = dotenv_values('config/USER.env')
HOST = config['HOST']
ID = config_user['ID']


def status(code, error=False):
    with open('status.json', 'w') as f:
        f.write(json.dumps({'code': code}))


def set_error(error=False):
    with open('config/error.json', 'w') as f:
        f.write(json.dumps({'error': error}))


def get_error():
    with open('config/token.json', 'r') as f:
        error = f.read()
        error = json.loads(error)
    return error


def get_token():
    while True:
        with open('config/token.json', 'r') as f:
            token = f.read()
            token = json.loads(token)

        if token['token']:
            return token['token']

        time.sleep(4)


def zerar_token():
    with open('config/token.json', 'w') as f:
        f.write(json.dumps({'token': None}))


def get_password(empresa):
    empresa = empresa.lower()

    url = f'https://{HOST}/controller/read/senhas?empresa={empresa}&id={ID}'
    print(url)
    r = requests.get(url).json()['result'][0]
    print('vai vir o print do json')
    print(r)
    # if r['code']:
    # {'user': r['user'], 'password': r['password'], 'code': r['code']}
    user = User(**r)
    return user


def get_medico(medico):
    r = False
    medico = quote(medico)
    url = f'https://{HOST}/controller/read/medicos?medico={medico}&id={ID}'
    logging.info(url)

    j = requests.get(url).json()
    logging.info(j)

    if len(j) > 0:
        r = j['result'][0]
        r = Medico(**r)

    return r


if __name__ == '__main__':

    medico = get_medico('Marcos de abreu bonardi')
    print(medico.name)
