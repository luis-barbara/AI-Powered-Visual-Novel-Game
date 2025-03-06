import openai
import os
from dotenv import load_dotenv

# Carregar chave da API
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def generate_image(prompt):
    """Gera uma imagem baseada em um prompt usando a API mais recente do DALL·E."""
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']

# Teste
if __name__ == "__main__":
    user_prompt = input("Digite um prompt para gerar a imagem: ")
    image_url = generate_image(user_prompt)
    print("\n Imagem gerada:", image_url)


    

