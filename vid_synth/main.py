# Importa a função que acabamos de criar e outras bibliotecas
import sys
from src.utils.config_loader import load_config

def main():
    """
    Função principal que orquestra o pipeline de criação de vídeo.
    """
    print("🚀 Pipeline de Automação de Vídeo Iniciado...")

    # 1. Carregar configuração
    try:
        config = load_config()
        print("✅ Configuração carregada com sucesso.")
        # Opcional: imprimir uma parte da config para teste
        # print(f"   - Caminho de saída dos vídeos: {config['paths']['output_videos']}")
    except (FileNotFoundError, KeyError) as e:
        print(f"❌ Erro crítico ao carregar configuração: {e}", file=sys.stderr)
        sys.exit(1)

    print("-" * 30)

    # --- Próximos passos virão aqui ---

    print("🏁 Pipeline Concluído (por enquanto).")


if __name__ == "__main__":
    main()
