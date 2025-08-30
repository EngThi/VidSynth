import google.generativeai as genai
import json

class ScriptGenerator:
    """
    Usa a API do Google Gemini para gerar roteiros de vídeo estruturados.
    """
    def __init__(self, api_key):
        """
        Inicializa o cliente da API do Gemini.

        Args:
            api_key (str): A chave da API do Google.
        """
        if not api_key:
            raise ValueError("API Key do Gemini não pode ser vazia.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')

    def generate_script(self, theme):
        """
        Gera um roteiro de vídeo completo com base em um tema.

        Args:
            theme (str): O tema do vídeo.

        Returns:
            dict: Um dicionário Python contendo o roteiro estruturado.
        """
        # Prompt otimizado para pedir um JSON estruturado como resposta
        prompt = f"""
        Você é um roteirista especialista para vídeos do YouTube.
        Sua tarefa é criar um roteiro curto e cativante sobre o tema: "{theme}".

        Por favor, formate sua resposta EXCLUSIVAMENTE como um objeto JSON válido,
        seguindo esta estrutura:
        {{
          "video_title": "Um título criativo e chamativo para o vídeo",
          "scenes": [
            {{
              "scene_number": 1,
              "narration_text": "Texto da narração para a primeira cena. Comece com um gancho forte.",
              "image_prompt": "Uma descrição detalhada em inglês para uma IA de imagem (como Imagen ou Midjourney) criar um visual para esta cena."
            }},
            {{
              "scene_number": 2,
              "narration_text": "Desenvolvimento do tópico. Apresente um fato interessante.",
              "image_prompt": "Descrição da imagem para a segunda cena."
            }},
            {{
              "scene_number": 3,
              "narration_text": "Mais um fato ou aprofundamento do tema.",
              "image_prompt": "Descrição da imagem para a terceira cena."
            }},
            {{
              "scene_number": 4,
              "narration_text": "Conclusão e uma chamada para ação (call to action), como 'inscreva-se no canal'.",
              "image_prompt": "Uma imagem impactante para a conclusão do vídeo."
            }}
          ]
        }}

        Não adicione nenhum texto ou formatação antes ou depois do objeto JSON.
        """

        try:
            response = self.model.generate_content(prompt)
            # Limpa a resposta para garantir que seja um JSON válido
            cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
            script_data = json.loads(cleaned_response)
            return script_data
        except Exception as e:
            print(f"❌ Erro ao gerar roteiro ou decodificar JSON: {e}")
            return None
