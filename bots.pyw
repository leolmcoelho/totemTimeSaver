import sys

from src.bot.my_logger import get_logger
from exec_bots import escolher_convenio
from app import get_password, status, set_error
from src.bot import Stenci

def exec(paciente):
    
    SADT = ["Amil (Planos)"]

    CONSULTA = [
                "MedSênior",
                "Paraná Clínicas",
                "Paraná Clínicas"
                ]
    logging = get_logger()

    status(100)
    set_error()
    senha = get_password('Stenci')
    stenci = Stenci(senha.user, senha.password, teste=True)
            
    try:
        for _ in range(2):

            stenci.set_client(paciente)

            for _ in range(5):
                data = stenci.get_infos()
                # print(data)
                if data.carteira:
                    break

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
