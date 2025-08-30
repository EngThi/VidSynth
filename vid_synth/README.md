# Projeto VidSynth

Um pipeline modular para a síntese automatizada de conteúdo em vídeo.

## Sobre o Projeto

O VidSynth é um sistema de automação projetado para criar vídeos curtos a partir de um tema. Ele gera um roteiro, busca mídias relevantes, sintetiza a narração e monta o vídeo final de forma autônoma.

## Funcionalidades

- Geração de roteiro com base em um tema usando IA generativa.
- Busca de imagens e vídeos de APIs (Pexels) ou geração via AI Studio.
- Geração de narração em áudio a partir do roteiro (TTS).
- Montagem automática de vídeo com imagens, narração, música de fundo e marca d'água.
- Configuração centralizada e logging detalhado.

## Como Configurar

1. **Clone o repositório:**
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd vid_synth
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure as chaves e caminhos:**
   - Renomeie o arquivo `config.example.json` para `config.json`.
   - **NÃO** suba o arquivo `config.json` para o repositório se ele contiver chaves secretas. O `.gitignore` já está configurado para ignorá-lo.
   - Abra o `config.json` e preencha os valores necessários:
     - `api_keys`: Suas chaves para a API do Gemini, Pexels e qualquer serviço de TTS.
     - `paths`: Os caminhos para os diretórios de saída e assets (geralmente não precisam ser alterados).
     - `video_settings`: Configurações de resolução, formato e duração de cena.
     - `ai_studio_credentials`: Suas credenciais para o AI Studio, se for usar a geração de imagens por lá.

## Como Executar

Para gerar um vídeo, execute o `main.py` a partir da raiz do projeto, passando um tema como argumento.

**Exemplo:**
```bash
python main.py --tema "A história da exploração espacial"
```

O vídeo final será salvo no diretório `output/videos/`.

## Dependências

A lista completa de dependências está no arquivo `requirements.txt`.
