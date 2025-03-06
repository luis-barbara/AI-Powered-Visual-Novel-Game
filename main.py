import openai
import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

# Carregar a chave da API da OpenAI do arquivo .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

app = FastAPI()

# Modelo de dados para receber input do usuário
class UserInput(BaseModel):
    message: str

@app.post("/generate_story")
async def generate_story(user_input: UserInput):
    """Gera texto e imagem com base na entrada do jogador."""

    # Chamada para o ChatGPT para criar a história
    text_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_input.message}]
    )
    story_text = text_response["choices"][0]["message"]["content"]

    # Chamada para o DALL·E para gerar imagem baseada no contexto da história
    image_response = openai.Image.create(
        prompt=story_text,  # Gerar a imagem baseada na narrativa
        n=1,
        size="1024x1024"
    )
    image_url = image_response["data"][0]["url"]

    return {"story_text": story_text, "image_url": image_url}

# Para rodar o servidor: `uvicorn backend:app --reload`
