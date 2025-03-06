from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import openai
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env (se existir)
load_dotenv()

# Inicializar cliente OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Criar aplicação FastAPI
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens (não recomendado para produção)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Definir estrutura da requisição
class StoryRequest(BaseModel):
    prompt: str
    max_tokens: int = 100

# Rota para gerar uma história
@app.post("/generate_story")
async def generate_story(request: StoryRequest):
    try:
        # Solicitação à OpenAI para gerar a história
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": request.prompt}],
            max_tokens=request.max_tokens
        )

        # Solicitação à OpenAI para gerar a imagem usando o DALL·E
        image_response = openai.Image.create(
            prompt=request.prompt,
            n=1,
            size="1024x1024"
        )

        # Obter a URL da imagem gerada
        image_url = image_response['data'][0]['url']

        # Retorna a história e a URL da imagem
        return {"story": response['choices'][0]['message']['content'], "image_url": image_url}
    
    except Exception as e:
        return {"error": str(e)}

# Rota padrão
@app.get("/")
async def home():
    return {"message": "API de geração de histórias com OpenAI"}
