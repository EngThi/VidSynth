import os
import requests
from typing import List
from src.utils.logger_config import logger

def get_media_from_api(prompts: List[str], image_dir: str, api_key: str) -> List[str]:
    """
    Busca e baixa imagens da API do Pexels com base em uma lista de prompts.

    Para cada prompt, busca uma imagem, baixa a versão 'large' e a salva
    localmente.

    Args:
        prompts (List[str]): Lista de prompts (palavras-chave) para a busca.
        image_dir (str): O diretório onde as imagens baixadas serão salvas.
        api_key (str): A chave da API do Pexels.

    Returns:
        List[str]: Uma lista de caminhos para os arquivos de imagem baixados.
                   Retorna uma lista vazia se nenhuma imagem for encontrada ou ocorrer um erro.
    """
    logger.info(f"Buscando {len(prompts)} mídias da Pexels API.")

    headers = {"Authorization": api_key}
    api_url = "https://api.pexels.com/v1/search"
    downloaded_image_paths = []

    for i, prompt in enumerate(prompts):
        params = {"query": prompt, "per_page": 1, "page": 1}

        try:
            response = requests.get(api_url, headers=headers, params=params, timeout=10)
            response.raise_for_status()  # Lança exceção para códigos de erro HTTP

            data = response.json()
            if not data["photos"]:
                logger.warning(f"Nenhuma foto encontrada para o prompt: '{prompt}'. Pulando.")
                continue

            photo = data["photos"][0]
            image_url = photo["src"]["large"]  # Baixando a versão grande da imagem

            # Baixa a imagem
            image_response = requests.get(image_url, timeout=15)
            image_response.raise_for_status()

            # Salva o arquivo
            file_extension = os.path.splitext(image_url)[1].split('?')[0] # Pega a extensão
            image_path = os.path.join(image_dir, f"scene_{i+1}{file_extension}")

            with open(image_path, "wb") as f:
                f.write(image_response.content)

            downloaded_image_paths.append(image_path)
            logger.info(f"Imagem para '{prompt}' baixada com sucesso e salva em: {image_path}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao fazer requisição à API Pexels para o prompt '{prompt}': {e}")
            continue # Continua para o próximo prompt
        except Exception as e:
            logger.error(f"Ocorreu um erro inesperado ao processar o prompt '{prompt}': {e}")
            continue

    if not downloaded_image_paths:
        logger.error("Nenhuma imagem pôde ser baixada. O processo de vídeo não pode continuar sem mídias.")
        # Poderia lançar uma exceção aqui para parar o pipeline
        raise RuntimeError("Falha ao baixar mídias visuais.")

    return downloaded_image_paths

def get_media_from_ai_studio(prompts: List[str], assets_dir: str) -> List[str]:
    """
    Gera e baixa imagens usando automação (Playwright) no AI Studio.
    (Esta função permanece como um placeholder por enquanto).
    """
    logger.info(f"Gerando mídias no AI Studio com os prompts: {prompts}")
    logger.warning("A função 'get_media_from_ai_studio' ainda não foi implementada.")

    # Simulação: Retorna caminhos de placeholder
    mock_paths = [
        f"{assets_dir}/images/placeholder_studio_1.jpg",
        f"{assets_dir}/images/placeholder_studio_2.jpg",
        f"{assets_dir}/images/placeholder_studio_3.jpg",
    ]

    logger.info(f"Mídias do AI Studio simuladas com sucesso. Caminhos: {mock_paths}")
    return mock_paths
