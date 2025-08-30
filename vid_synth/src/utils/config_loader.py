import json
import os

def load_config(config_path="config.json"):
    """
    Carrega o arquivo de configuração JSON.

    Args:
        config_path (str): O caminho para o arquivo config.json.

    Returns:
        dict: Um dicionário contendo as configurações.

    Raises:
        FileNotFoundError: Se o arquivo de configuração não for encontrado.
        json.JSONDecodeError: Se o arquivo de configuração tiver um formato inválido.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Erro: Arquivo de configuração não encontrado em '{config_path}'")

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Erro: Formato JSON inválido em '{config_path}': {e.msg}", e.doc, e.pos)
