from src.models.user import *
from src.bot import ParanaClinicas as paranaClinicas
from app.data import *


def ParanaClinicas(data:IStenci):
    
    senha = get_password('parana clinicas')
    parana = paranaClinicas(senha.user, senha.password)
    senha = parana.exec(data.carteira, data.medico)
    
    return senha