from src.models.user import IStenci
from src.bot.sulAmerica import sulAmerica
from src.bot import sulAmericaSF
from app.data import get_password, get_medico
from unidecode import unidecode
from src.bot.my_logger import get_logger

logging = get_logger()

def SulAmerica(data: IStenci):
    medicos_Sales_Force = [
        'Marcos de Abreu Bonardi',
        'Olival de Oliveira Junior',
        'Dilermando Pereira de Almeida Neto'
    ]

    try:
        logging.info('Iniciou')
        senha = get_password('sulamerica')
        medico = get_medico(data.medico)
        medico.name = unidecode(medico.name)
        logging.info(data)

        if medico.name in medicos_Sales_Force:
            sul_america = sulAmericaSF()
            pass
        
        else:
            try:
                sul_america = sulAmerica(
                    senha.code, senha.user, senha.password)
            except Exception as e:
                logging.error(e)
                return False
            logging.info('Iniciou o driver')

            sul_america.insert_code(data.carteira)
            
            code = sul_america.exec_dados_atendimento(medico.name, 
                                                      medico.conselho, 
                                                      medico.registro, 
                                                      medico.cbo, 
                                                      uf="PR"
                                                      )
            logging.info('Terminou a execução do sulamerica')
            return code

    except Exception as e:
        logging.error(e)
        return False
