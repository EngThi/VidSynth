import sys
import os
from src.utils.logger_config import logger
from src.utils.config_loader import load_config
from src.modules.input_handler import get_args
from src.modules.script_generator import generate_script
from src.modules.media_retriever import get_media_from_api # Usando a API por padrão
from src.modules.audio_generator import generate_audio_from_api
from src.modules.video_assembler import assemble_video

def main():
    """
    Função principal que orquestra todo o pipeline de criação de vídeo.
    """
    try:
        # 1. Inicialização e Configuração
        logger.info("=============================================")
        logger.info(">>> INICIANDO O PIPELINE VIDSYNTH <<<")
        logger.info("=============================================")

        # Constrói o caminho para o config.json relativo à localização de main.py
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, "config.json")
        config = load_config(config_path)
        paths = config.get("paths", {})
        video_settings = config.get("video_settings", {})
        api_keys = config.get("api_keys", {})

        # Garantir que os diretórios de saída existam
        os.makedirs(paths.get("output_videos"), exist_ok=True)
        os.makedirs(paths.get("output_logs"), exist_ok=True)

        # 2. Obter Tema do Usuário
        args = get_args()
        theme = args.tema
        logger.info(f"Tema recebido da linha de comando: '{theme}'")

        # 3. Gerar Roteiro
        gemini_api_key = api_keys.get("GEMINI_API_KEY")
        if not gemini_api_key or gemini_api_key == "SUA_CHAVE_AQUI":
            logger.error("A chave da API do Gemini (GEMINI_API_KEY) não foi configurada em 'config.json'.")
            sys.exit(1)
        script_data = generate_script(theme, gemini_api_key)

        # 4. Extrair informações do roteiro
        narration_texts = [scene['narracao'] for scene in script_data['cenas']]
        image_prompts = [scene['prompt_imagem'] for scene in script_data['cenas']]
        logger.info("Narração e prompts de imagem extraídos do roteiro.")

        # 5. Obter Mídia Visual
        # A lógica para escolher entre API e AI Studio pode ser adicionada aqui.
        logger.info("Buscando mídias visuais via API Pexels...")
        pexels_api_key = api_keys.get("PEXELS_API_KEY")
        if not pexels_api_key or pexels_api_key == "SUA_CHAVE_AQUI":
            logger.error("A chave da API da Pexels (PEXELS_API_KEY) não foi configurada em 'config.json'.")
            sys.exit(1)

        # Criar um diretório para as imagens desta execução
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_dir = os.path.join(paths.get("assets"), "images", timestamp)
        os.makedirs(image_dir, exist_ok=True)

        image_paths = get_media_from_api(image_prompts, image_dir, pexels_api_key)

        # 6. Gerar Áudio da Narração
        logger.info("Gerando áudio da narração...")
        audio_dir = os.path.join(paths.get("assets"), "audio") # Diretório para salvar o áudio
        os.makedirs(audio_dir, exist_ok=True)
        audio_path = generate_audio_from_api(narration_texts, audio_dir)

        # 7. Montar o Vídeo Final
        logger.info("Iniciando a montagem do vídeo final...")
        final_video_path = assemble_video(
            script_data=script_data,
            image_paths=image_paths,
            audio_path=audio_path,
            output_dir=paths.get("output_videos"),
            video_settings=video_settings,
            assets_path=paths.get("assets")
        )

        logger.info("---------------------------------------------")
        logger.info(">>> PROCESSO CONCLUÍDO COM SUCESSO! <<<")
        logger.info(f"Vídeo final salvo em: {final_video_path}")
        logger.info("---------------------------------------------")

    except FileNotFoundError:
        logger.error("ERRO CRÍTICO: O arquivo 'config.json' não foi encontrado. Abortando.")
        sys.exit(1)
    except KeyError as e:
        logger.error(f"ERRO CRÍTICO: Chave de configuração ausente ou inválida: {e}. Verifique seu 'config.json'.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Ocorreu um erro inesperado no pipeline: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    # Para que os imports de 'src' funcionem ao executar 'python main.py'
    # da pasta 'vid_synth', o Python precisa encontrar o diretório 'src'.
    # A execução a partir da raiz do projeto já resolve isso naturalmente.
    main()
