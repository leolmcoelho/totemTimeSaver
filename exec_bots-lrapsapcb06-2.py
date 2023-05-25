import sys
import os
import requests
import json

import time
from urllib.parse import quote
from unidecode import unidecode
from src.bot.unimed import Unimed
from src.bot.stenci import Stenci
from src.bot.amil import Amil
from src.bot.medsenior import MedSenior
from src.bot.sulAmerica import sulAmerica
from src.bot.parana_clinicas import ParanaClinicas
from src.models.user import *

from src.bot.my_logger import get_logger


logging = get_logger()

id = 1
empresa = 'Unimed'
host = 'timesaver.com.br'


def status(code):
    with open('status.json', 'w') as f:
        f.write(json.dumps({'code': code}))


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

    url = f'https://{host}/controller/read/senhas?empresa={empresa}&id={id}'
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
    url = f'https://{host}/controller/read/medicos?medico={medico}&id={id}'
    logging.info(url)

    j = requests.get(url).json()
    logging.info(j)
    
    if len(j) > 0:
        r = j['result'][0]
        r = Medico(**r)
        
    return r


def unimed(carteira, medico):
    medico = unidecode(medico)
    for _ in range(3):
        try:

            senha = get_password('Unimed')
            u = Unimed(senha.user, senha.password, teste=True)

            u.select(medico)

            u.set_beneficiary(carteira)

            try:
                u.set_value(medico)
            except Exception as e:
                logging.error(e)
            u.click_final()

            return u.verify_conclusion()

        except Exception as e:
            logging.exception(e)
            continue


def escolher_convenio(data:IStenci):
    result = None

    convenio = data.convenio
    logging.info(f'convenio utilizado: {convenio}')

    if convenio == "Unimed Curitiba":
        result = unimed(data.carteira, data.medico)

    if convenio == "Amil (Planos)":
        result = exec_amil(data)

    if convenio == "MedSênior":
        result = exec_medSenior(data)

    if convenio == 'Sul América Serviços de Saúde (Sulamérica Serviços de Saúde)':
        result = exec_sulAmerica(data)

    if convenio == "Paraná Clínicas":
        result = exec_parana_clinicas(data)

    logging.info(result)

    if result:
        pass
    else:
        status(300)

    return result


def exec_amil(data:IStenci):
    zerar_token()
    senha = get_password('Amil (Planos)')

    medico = get_medico(data.medico)

    amil = Amil(senha.user, senha.password)

    amil.click_autorization_previa()
    amil.verificar_load_page()
    amil.insert_CPF(data.carteira)
    amil.insert_atendimento('consulta')

    amil.insert_data()
    # input('esperar')
    amil.inserir_solicitante(medico.name, medico.cbo)
    amil.inserir_servico()
    amil.click_incluir()

    status(400)

    token = get_token()
    for _ in range(3):
        senha = amil.get_senha()
        if senha:
            break

    zerar_token()
    amil.inserir_token(token)

    if amil.verify_token():
        senha = False
    logging.info('erro no token')

    # input('sair')
    return senha


def exec_medSenior(data:IStenci):

    senha = get_password('MedSênior')
    med = MedSenior(senha.user, senha.password)
    med.inserir_beneficiario(data.carteira)
    med.inserir_cel('2199999999')
    result = med.final()
    logging.info(result)
    # input('aperte enter para continuar')
    #status(200)
    #status(400)
    return result


def exec_sulAmerica(data:IStenci):
    try:
        logging.info('iniciou')
        senha = get_password('sulamerica')
        medico = get_medico(data.medico)
        medico.name = unidecode(medico.name)
        
        try:
            sul = sulAmerica(
                senha.code, senha.user, senha.password)
        except Exception as e:
            logging.error(e)
        
        logging.info('iniciou o driver')
        
        sul.insert_code(data.carteira)
        logging.info(data)
        logging.info(medico)
        
        code = sul.exec_dados_atendimento(
            medico.name, medico.conselho, medico.registro, medico.cbo, uf="PR")
        logging.info('terminou a execução do sulamerica')
        #input('\n\nterminou\n\n\n\n')
        return code 

    except Exception as e:
        logging.error(e)
        input('\n\n\ndeu erro\n\n\n')
        return False


def exec_parana_clinicas(data:IStenci):
    
    senha = get_password('parana clinicas')
    parana = ParanaClinicas(senha.user, senha.password)
    parana.exec(data.carteira, data.medico, 5171288)


if __name__ == '__main__':
    data = {'medico': 'André Matos de Oliveira',
            'carteira': '072327862'}
    # r = exec_amil(data:IStenci)
    #data.medico = unidecode(data.medico)
    #r = get_medico(data.medico)
    r = get_password('unimed')

    print(r.user)
