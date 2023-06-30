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
                # print(data)
                if data.carteira:
                    break
                #colocar erro pro user final

            result = escolher_convenio(data)
            convenio = data.convenio
            logging.info(result)
            try:
                print('\n\n\n\n')
                print(result)
                print('\n\n\n\n')
                """Copel- guia de consulta
                    Medsenior- consulta
                    Bradesco- consulta
                    Amil- SADT 
                    Cassi – consulta
                    Unimed – consulta
                    Paraná Clinicas – SADT
                    Sanepar – consulta 
                    Itaú – consulta
                    Sul América – consulta
                    Saude caixa – consulta"""
                SADT = [
                    "Amil (Planos)"
                ]

                CONSULTA = [
                    "MedSênior",
                    "Paraná Clínicas",
                    "Paraná Clínicas"
                ]
                if result == False:
                    status(300)
                    set_error(f'{convenio}: Erro ao finalizar no {convenio}')
                    return False
                else:
                    #SADT

                    ### mais qual??? ####
                    if convenio == 'Unimed Curitiba':
                        stenci.finalizar()

                    elif convenio == 'Fundação Copel':
                        # TEM QUE TER UM DIFERENTEEEEEEEEE
                        # stenci.finalizar()
                        # clicka na guia de consulta, ao inves de guia spd
                        pass

                    elif convenio in SADT:
                        stenci.finalizar_amil(result)

                    else:
                        print('\n\n\n\n')
                        print(result)
                        if result:
                            stenci.finalizar_geral(result)
                        else:
                            status(300)
                            return False

                status(200)
                logging.info('Finalizado no Stenci')
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
    #print(sys.argv[1])
    exec(sys.argv[1])


# print(get_password('Unimed'))
    # print(sys.argv)
