import os
import subprocess
import shutil
from typing import List, Dict, Any
from src.utils.logger_config import logger
from datetime import datetime

def check_ffmpeg():
    """Verifica se o FFmpeg está instalado e acessível."""
    if not shutil.which("ffmpeg"):
        logger.error("FFMPEG não encontrado. Por favor, instale o FFmpeg e garanta que ele esteja no PATH do sistema.")
        raise FileNotFoundError("FFmpeg não encontrado.")
    logger.info("FFmpeg encontrado.")

def assemble_video(
    script_data: Dict[str, Any],
    image_paths: List[str],
    audio_path: str,
    output_dir: str,
    video_settings: Dict[str, Any],
    assets_path: str
) -> str:
    """
    Monta o vídeo final a partir de imagens, áudio e configurações, usando FFmpeg.
    """
    check_ffmpeg()

    # --- 1. Definição de caminhos e configurações ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_dir = os.path.join(output_dir, f"temp_{timestamp}")
    os.makedirs(temp_dir, exist_ok=True)

    resolution = video_settings.get("resolution", "1920x1080")
    image_duration = video_settings.get("image_duration_seconds", 5)
    video_format = video_settings.get("format", "mp4")
    final_video_path = os.path.join(output_dir, f"{script_data.get('titulo', 'video')}_{timestamp}.{video_format}")

    # --- 2. Criar clipes de vídeo a partir de cada imagem ---
    clip_paths = []
    logger.info("Criando clipes de vídeo a partir das imagens...")
    for i, img_path in enumerate(image_paths):
        clip_output_path = os.path.join(temp_dir, f"clip_{i}.mp4")
        command = [
            'ffmpeg', '-y', '-loop', '1', '-i', img_path,
            '-vf', f"scale={resolution}:force_original_aspect_ratio=decrease,pad={resolution}:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p",
            '-c:v', 'libx264', '-t', str(image_duration), '-r', '25',
            clip_output_path
        ]
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            clip_paths.append(clip_output_path)
        except subprocess.CalledProcessError as e:
            logger.error(f"Erro ao criar clipe para {img_path}: {e.stderr}")
            raise

    # --- 3. Concatenar os clipes em um slideshow ---
    logger.info("Concatenando clipes para formar o slideshow...")
    concat_list_path = os.path.join(temp_dir, "concat_list.txt")
    with open(concat_list_path, 'w') as f:
        for path in clip_paths:
            f.write(f"file '{os.path.abspath(path)}'\n")

    slideshow_path = os.path.join(temp_dir, "slideshow_silent.mp4")
    command = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', concat_list_path,
        '-c', 'copy', slideshow_path
    ]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao concatenar clipes: {e.stderr}")
        raise

    # --- 4. Montagem final: Adicionar áudio e marca d'água ---
    logger.info("Adicionando narração, música de fundo e marca d'água...")

    inputs = [
        '-i', slideshow_path,
        '-i', audio_path
    ]

    # Mapeamentos de stream e filtros complexos
    map_video = "[0:v]"
    map_audio = "[1:a]"
    complex_filter = []

    # Verificar música de fundo
    music_path = os.path.join(assets_path, "audio", "background_music.mp3")
    if os.path.exists(music_path):
        inputs.extend(['-i', music_path])
        # Mixa narração (map_audio) com música ([2:a]), baixando o volume da música
        complex_filter.append("[2:a]volume=0.15[bg_music];[1:a][bg_music]amix=inputs=2:duration=longest[audio_out]")
        map_audio = "[audio_out]"

    # Verificar marca d'água
    watermark_path = os.path.join(assets_path, "images", "watermark.png")
    if os.path.exists(watermark_path):
        inputs.extend(['-i', watermark_path])
        # Sobrepõe a marca d'água no canto inferior direito do vídeo
        video_input_stream = map_video.replace('[', '').replace(']', '')
        watermark_input_index = len(inputs) // 2 -1
        complex_filter.append(f"[{video_input_stream}][{watermark_input_index}:v]overlay=W-w-10:H-h-10[video_out]")
        map_video = "[video_out]"

    command = ['ffmpeg', '-y'] + inputs
    if complex_filter:
        command.extend(['-filter_complex', ";".join(complex_filter)])

    command.extend([
        '-map', map_video, '-map', map_audio,
        '-c:v', 'libx264', '-c:a', 'aac', '-shortest',
        final_video_path
    ])

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        logger.info(f"Vídeo final montado com sucesso em: {final_video_path}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro na montagem final do vídeo: {e.stderr}")
        raise

    # --- 5. Limpeza ---
    logger.info("Limpando arquivos temporários...")
    shutil.rmtree(temp_dir)

    return final_video_path
