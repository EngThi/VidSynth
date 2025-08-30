import json
from typing import Dict, Any

def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    """
    Carrega, valida e fornece acesso ao arquivo de configuração JSON.

    Args:
        config_path (str): O caminho para o arquivo config.json.

    Returns:
        Dict[str, Any]: Um dicionário contendo as configurações.

    Raises:
        FileNotFoundError: Se o arquivo de configuração não for encontrado.
        json.JSONDecodeError: Se o arquivo de configuração tiver um formato JSON inválido.
        KeyError: Se uma chave essencial estiver faltando no arquivo de configuração.
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # Validação básica para garantir que as chaves principais existem
        required_keys = ["api_keys", "paths", "video_settings"]
        for key in required_keys:
            if key not in config:
                raise KeyError(f"A chave obrigatória '{key}' não foi encontrada no arquivo de configuração.")

        return config
    except FileNotFoundError:
        print(f"Erro: O arquivo de configuração '{config_path}' não foi encontrado.")
        print("Certifique-se de criar um arquivo 'config.json' na raiz do projeto.")
        raise
    except json.JSONDecodeError:
        print(f"Erro: O arquivo de configuração '{config_path}' contém JSON inválido.")
        raise
    except KeyError as e:
        print(f"Erro de configuração: {e}")
        raise
