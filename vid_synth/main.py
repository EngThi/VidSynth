# Importa as funções que precisamos
import sys
from src.utils.config_loader import load_config
from src.modules.input_handler import get_user_input # <--- NOVA IMPORTAÇÃO

def main():
    """
    Função principal que orquestra o pipeline de criação de vídeo.
    """
    print("🚀 Pipeline de Automação de Vídeo Iniciado...")

    # 1. Carregar configuração
    try:
        config = load_config()
        print("✅ Configuração carregada com sucesso.")
    except (FileNotFoundError, KeyError) as e:
        print(f"❌ Erro crítico ao carregar configuração: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. Obter input do usuário  # <--- NOVO BLOCO
    try:
        args = get_user_input()
        tema_do_video = args.tema
        print(f"✅ Tema recebido: '{tema_do_video}'")
    except Exception as e:
        print(f"❌ Erro ao processar argumentos de entrada: {e}", file=sys.stderr)
        sys.exit(1)

    print("-" * 30)

    # --- Próximos passos virão aqui ---

    print("🏁 Pipeline Concluído (por enquanto).")


if __name__ == "__main__":
    main()
