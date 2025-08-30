# Importações necessárias
import sys
import json # Adicionar para imprimir o dicionário de forma legível
from src.utils.config_loader import load_config
from src.modules.input_handler import get_user_input
from src.modules.script_generator import ScriptGenerator # <--- NOVA IMPORTAÇÃO

def main():
    print("🚀 Pipeline de Automação de Vídeo Iniciado...")

    # 1. Carregar configuração
    try:
        config = load_config()
        print("✅ Configuração carregada.")
    except Exception as e:
        print(f"❌ Erro crítico ao carregar configuração: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. Obter input do usuário
    try:
        args = get_user_input()
        tema_do_video = args.tema
        print(f"✅ Tema recebido: '{tema_do_video}'")
    except Exception as e:
        print(f"❌ Erro ao processar argumentos de entrada: {e}", file=sys.stderr)
        sys.exit(1)

    # 3. Gerar Roteiro  # <--- NOVO BLOCO
    try:
        print("🧠 Gerando roteiro com a IA...")
        gemini_api_key = config['api_keys']['GEMINI_API_KEY']
        script_gen = ScriptGenerator(api_key=gemini_api_key)
        roteiro = script_gen.generate_script(tema_do_video)

        if roteiro:
            print("✅ Roteiro gerado com sucesso!")
            # Imprime o roteiro de forma bonita para verificação
            print(json.dumps(roteiro, indent=2, ensure_ascii=False))
        else:
            raise Exception("Falha ao gerar o roteiro.")

    except Exception as e:
        print(f"❌ Erro na geração do roteiro: {e}", file=sys.stderr)
        sys.exit(1)

    print("-" * 30)
    print("🏁 Pipeline Concluído (por enquanto).")


if __name__ == "__main__":
    main()
