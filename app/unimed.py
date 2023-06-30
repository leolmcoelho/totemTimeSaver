from unidecode import unidecode

from src.models.user import *
from src.bot import Unimed as UNIMED
from app.data import *


def Unimed(carteira, medico):
    medico = unidecode(medico)
    for _ in range(3):
        try:

            senha = get_password('Unimed')
            u = UNIMED(senha.user, senha.password, teste=True)

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
