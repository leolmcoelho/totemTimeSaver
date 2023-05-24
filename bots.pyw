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
from src.bot.my_logger import get_logger

from exec_bots import *

id = 1
empresa = 'Unimed'
host = 'timesaver.com.br'

paciente = False

def exec(paciente):
    logging = get_logger()
    
    status(100)
    set_error()
    try:
        for _ in range(2):

            senha = get_password('Stenci')
            stenci = Stenci(senha.user, senha.password, teste=True)
            stenci.set_client(paciente)

            for _ in range(5):
                data = stenci.get_infos()
                print(data)
                if data.carteira:
                    break

            result = escolher_convenio(data)
            convenio = data.convenio
            logging.info(result)
            stenci.finalizar_amil(result)
            try:
                stenci.finalizar_amil(result)
                if result == False:
                    status(300)
                else:
                    
                    ### mais qual??? ####
                    if convenio == 'Unimed Curitiba':
                        stenci.finalizar()
                    
                    else:
                        if result:
                            stenci.finalizar_amil(result)
                        else:
                            status(300)
                    
                status(200)
                return True

            except Exception as e:
                status(300)
                set_error('Stenci: Erro ao finalizar no Stenci')
                logging.exception(e)
                return False

    except Exception as e:
        logging.exception(e)
        status(300)
        return False

    finally:
        stenci.driver.close()

    
if len(sys.argv) > 1:
    print(sys.argv[1])
    exec(sys.argv[1])
    
    
# print(get_password('Unimed'))
    # print(sys.argv)
