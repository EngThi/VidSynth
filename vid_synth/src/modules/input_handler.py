import argparse

def get_args():
    """
    Processa e retorna os argumentos da linha de comando.

    Returns:
        argparse.Namespace: Um objeto contendo os argumentos passados.
                            Atualmente, retorna o 'tema' do vídeo.
    """
    parser = argparse.ArgumentParser(
        description="VidSynth - Pipeline de Síntese de Vídeo Automatizado."
    )
    parser.add_argument(
        "--tema",
        type=str,
        required=True,
        help="O tema principal para a criação do vídeo."
    )
    # Futuramente, outros argumentos como --qualidade, --formato, etc. podem ser adicionados aqui.

    args = parser.parse_args()
    return args
