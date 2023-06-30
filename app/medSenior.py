from src.models.user import *
from src.bot import MedSenior as MEDSENIOR
from app.data import *


logging = get_logger()

def MedSenior(data:IStenci):

    senha = get_password('MedSênior')
    med = MEDSENIOR(senha.user, senha.password)
    med.inserir_beneficiario(data.carteira)
    med.inserir_cel('2199999999')
    result = med.final()
    #input("tirar isso aqui")
    logging.info(f'Resultado no MEDSENIOR {result}')
    
    return result