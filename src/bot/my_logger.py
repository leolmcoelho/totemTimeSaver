import sys, os
import getpass
import logging
sys.path.append(os.getcwd())


def get_logger(name = getpass.getuser()):
    # Define o formato de saída do log
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format, datefmt='%Y/%m/%d %I:%M:%S')

    # Cria um handler para salvar as mensagens do log em um arquivo
    file_handler = logging.FileHandler(f'{name}.log', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Cria um handler para imprimir as mensagens do log no console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Cria o logger e adiciona os handlers
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
