import argparse

def get_user_input():
    """
    Configura e processa os argumentos da linha de comando para obter o tema do vídeo.

    Returns:
        argparse.Namespace: Um objeto contendo os argumentos processados.
                            Ex: args.tema
    """
    parser = argparse.ArgumentParser(description="Automatiza a criação de vídeos para o YouTube.")
    parser.add_argument(
        "--tema",
        type=str,
        required=True,
        help="O tema central do vídeo a ser criado."
    )

    args = parser.parse_args()
    return args
