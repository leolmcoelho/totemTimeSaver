from urllib.parse import quote
from unidecode import unidecode
from src.models.user import *

from app import Amil, Unimed, MedSenior, SulAmerica, ParanaClinicas, status
from src.bot.my_logger import get_logger

logging = get_logger()


def escolher_convenio(data: IStenci):
    convenios = {
        "Unimed Curitiba": Unimed,
        "Amil (Planos)": Amil,
        "MedSênior": MedSenior,
        "Sul América Serviços de Saúde (Sulamérica Serviços de Saúde)": SulAmerica,
        "Paraná Clínicas": ParanaClinicas
    }

    convenio = data.convenio
    logging.info(f"Convênio utilizado: {convenio}")

    result = convenios.get(convenio)

    if result:
        try:
            result = result(data)
            logging.info(result)
        except Exception as e:
            logging.error(f"Erro ao criar instância da classe de convênio: {e}")
            result = None
    else:
        logging.error("Convênio não encontrado.")

    if not result:
        status(300)

    logging.info(f"Procedimento no convênio {convenio} finalizado")

    return result


if __name__ == '__main__':
    data = {'medico': 'Bruno Luis Duda',
            'carteira': '072327862'}
    # r = exec_amil(data:IStenci)
    #data.medico = unidecode(data.medico)
    #r = get_medico(data['medico'])
    #status(300, 'Amil: Erro no token')
    #r = get_medico(')

    #print(r.cbo)
