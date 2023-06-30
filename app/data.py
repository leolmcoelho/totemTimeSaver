import json
import sys
import os
import time
import requests
from dotenv import dotenv_values
from urllib.parse import quote

sys.path.append(os.getcwd())
from src.models.user import *
from src.bot.my_logger import get_logger
from models.medicos import Medico

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
    with open('tmp/senha.json', 'r') as file:
            senhas = json.load(file)
    for item in senhas:
            if item['empresa_name'] == empresa:
                return User(**item)
    
    return False


def atualizar_password():
    url = f'https://{HOST}/controller/read/senhas?id={ID}'
    response = requests.get(url).json()['result']
    key = 'empresa_name'
    file_path = 'tmp/senha.json'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    for item in response:
        item[key] = item[key].lower()
         
    with open(file_path, 'w') as file:
        json.dump(response, file)
        
    return True


def get_medico(medico):
    
    medico = medico.lower() 
    with open('tmp/medicos.json', 'r') as file:
        medicos = json.load(file)
    for item in medicos:
        
        if item['name'] == medico:
            return Medico(**item)
    return True


def atualizar_medico():
    r = False

    url = f'https://{HOST}/controller/read/medicos?id={ID}'
    logging.info(url)

    j = requests.get(url).json()
    logging.info(j)

    if len(j) > 0:
        j = j['result']

        # Converter o nome para letras minúsculas
        for item in j:
            item['name'] = item['name'].lower()

        # Salvar JSON no arquivo
        filepath = os.path.join('tmp', 'medicos.json')
        with open(filepath, 'w') as file:
            json.dump(j, file)

    return r



if __name__ == '__main__':

    #medico = get_medico('Marcos de abreu bonardi')
    medico = get_password('medsÊnior')
    #medico = atualizar_medico()
    print(medico)
