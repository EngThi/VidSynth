import json
import re
from typing import Dict, Any
import google.generativeai as genai
from src.utils.logger_config import logger

def clean_json_response(response_text: str) -> str:
    """
    Limpa a resposta da IA para extrair apenas o bloco de código JSON.
    Remove ```json ... ``` e outros textos.
    """
    # Usa uma expressão regular para encontrar o conteúdo dentro de ```json ... ```
    match = re.search(r"```json\s*([\s\S]*?)\s*```", response_text)
    if match:
        return match.group(1).strip()

    # Se não encontrar o bloco, assume que a resposta pode ser o JSON diretamente
    return response_text.strip()

def generate_script(theme: str, api_key: str) -> Dict[str, Any]:
    """
    Gera um roteiro de vídeo estruturado usando a API do Gemini.

    Args:
        theme (str): O tema para o roteiro do vídeo.
        api_key (str): A chave da API para autenticação no serviço do Gemini.

    Returns:
        Dict[str, Any]: Um dicionário estruturado contendo o roteiro.
                        Retorna None em caso de falha.
    """
    logger.info(f"Gerando roteiro via API do Gemini para o tema: '{theme}'")

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

        prompt = f"""
        Sua tarefa é atuar como um roteirista para vídeos curtos do YouTube.
        Crie um roteiro conciso para um vídeo sobre o tema: "{theme}".

        O roteiro deve ser dividido em 3 a 5 cenas.
        Para cada cena, você deve fornecer:
        1.  'cena': O número da cena (começando em 1).
        2.  'narracao': Um texto curto e envolvente para a narração da cena (máximo de 2 frases).
        3.  'prompt_imagem': Uma descrição detalhada para uma IA de geração de imagem (como Imagen ou Midjourney) criar um visual para a cena. Seja descritivo e visual.

        Além das cenas, forneça um 'titulo' geral para o vídeo.

        FORMATE SUA RESPOSTA ESTRITAMENTE COMO UM OBJETO JSON, sem nenhum texto ou formatação adicional fora do JSON.
        O JSON deve ter a seguinte estrutura:
        {{
          "titulo": "Seu Título Aqui",
          "cenas": [
            {{
              "cena": 1,
              "narracao": "Texto da narração da cena 1.",
              "prompt_imagem": "Descrição da imagem para a cena 1."
            }},
            ... (outras cenas)
          ]
        }}
        """

        response = model.generate_content(prompt)

        logger.info("Resposta recebida da API do Gemini. Processando...")

        cleaned_response = clean_json_response(response.text)

        script_data = json.loads(cleaned_response)

        # Validação da estrutura do JSON recebido
        if "titulo" not in script_data or "cenas" not in script_data:
            logger.error("O JSON recebido da API não possui a estrutura esperada.")
            return None

        logger.info("Roteiro gerado e validado com sucesso!")
        return script_data

    except Exception as e:
        logger.error(f"Falha ao gerar o roteiro com a API do Gemini: {e}", exc_info=True)
        # Retornar o mock script pode ser uma alternativa em caso de falha
        # return generate_mock_script(theme)
        return None

def generate_mock_script(theme: str) -> Dict[str, Any]:
    """Função de fallback que gera um roteiro de exemplo."""
    logger.warning("Usando roteiro de exemplo (mock) devido a uma falha na API.")
    return {
        "titulo": f"Um Olhar Sobre {theme}",
        "cenas": [
            {"cena": 1, "narracao": f"Explorando os conceitos de {theme}.", "prompt_imagem": f"abstração de {theme}"},
            {"cena": 2, "narracao": "O impacto do tema hoje.", "prompt_imagem": f"tecnologia de {theme}"},
            {"cena": 3, "narracao": "O futuro de {theme}.", "prompt_imagem": f"futuro com {theme}"}
        ]
    }
