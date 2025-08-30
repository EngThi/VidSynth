import os
from typing import List
from gtts import gTTS
from src.utils.logger_config import logger

def generate_audio_from_api(narration_texts: List[str], audio_dir: str) -> str:
    """
    Converte uma lista de textos de narração em um único arquivo de áudio usando gTTS.

    Args:
        narration_texts (List[str]): A lista de frases que compõem a narração.
        audio_dir (str): O diretório onde o arquivo de áudio final será salvo.

    Returns:
        str: O caminho completo para o arquivo de áudio gerado (.mp3).
             Retorna None em caso de falha.
    """
    if not narration_texts:
        logger.error("A lista de textos para narração está vazia. Não é possível gerar áudio.")
        return None

    full_narration = " ".join(narration_texts)
    logger.info("Iniciando a geração de áudio com gTTS.")
    logger.debug(f"Texto completo da narração: '{full_narration[:150]}...'")

    try:
        # Cria o objeto gTTS
        tts = gTTS(text=full_narration, lang='pt-br', slow=False)

        # Define o caminho do arquivo de saída
        output_path = os.path.join(audio_dir, "narration.mp3")

        # Salva o arquivo de áudio
        tts.save(output_path)

        logger.info(f"Áudio da narração gerado com sucesso e salvo em: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Falha ao gerar áudio com gTTS: {e}", exc_info=True)
        return None
