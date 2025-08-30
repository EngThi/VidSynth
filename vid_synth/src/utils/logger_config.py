import logging
import os
from datetime import datetime

def setup_logger(log_dir: str = "output/logs"):
    """
    Configura um logger para registrar mensagens no console e em um arquivo.

    O arquivo de log será salvo no diretório especificado com um nome de arquivo
    baseado em timestamp (ex: 2023-10-27_15-30-00.log).

    Args:
        log_dir (str): O diretório onde os arquivos de log serão salvos.

    Returns:
        logging.Logger: O objeto logger configurado.
    """
    # Garante que o diretório de log exista
    os.makedirs(log_dir, exist_ok=True)

    # Cria um logger
    logger = logging.getLogger("VidSynth")
    logger.setLevel(logging.DEBUG)

    # Evita que handlers sejam adicionados múltiplas vezes
    if logger.hasHandlers():
        logger.handlers.clear()

    # Formato do log
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler para o console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler para o arquivo
    log_filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    file_handler = logging.FileHandler(os.path.join(log_dir, log_filename), encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# Instância global do logger para ser importada por outros módulos
logger = setup_logger()
