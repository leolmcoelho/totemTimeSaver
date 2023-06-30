from src.models.user import *
from src.bot import Amil as AMIL
from app.data import *

def Amil(data:IStenci):
    zerar_token()
    senha = get_password('Amil (Planos)')

    medico = get_medico(data.medico)
    
    amil = AMIL(senha.user, senha.password)

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
    
    amil.inserir_token(token)

    if amil.verify_token():
        senha = False
        set_error('Amil: erro no token')
        logging.info('erro no token')

    # input('sair')
    return senha