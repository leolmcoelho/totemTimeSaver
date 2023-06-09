import sys
import os
import getpass
import logging

def get_logger(name=getpass.getuser()):
    # Define o formato de saída do log
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format, datefmt='%Y/%m/%d %I:%M:%S')

    # Obtém o caminho absoluto para o diretório de logs
    logs_dir = os.path.abspath('logs')

    # Verifica se o diretório de logs existe e cria-o, se necessário
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Cria um handler para salvar as mensagens do log em um arquivo
    file_handler = logging.FileHandler(f'{logs_dir}/{name}_log.log', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Cria um handler para imprimir as mensagens do log no console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Cria o logger e adiciona os handlers apenas se não estiverem presentes
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
