import openai
import os
from dotenv import load_dotenv

# Carregar chave da API
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Definir chave da API do OpenAI
openai.api_key = OPENAI_API_KEY

def generate_text(prompt):
    """Gera uma narrativa usando ChatGPT."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# Teste
if __name__ == "__main__":
    user_prompt = input("Digite um prompt para gerar a história: ")
    story_text = generate_text(user_prompt)
    print("\nHistória gerada:\n", story_text)

