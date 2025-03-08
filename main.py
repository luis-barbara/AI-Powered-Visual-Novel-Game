from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
import json
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Inicializar a aplicação FastAPI
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Função para carregar o JSON com os cenários e personagens
def load_game_data():
    with open("keywords.json", "r", encoding="utf-8") as file:
        return json.load(file)

# Carregar os dados do JSON
game_data = load_game_data()
scenes_data = game_data["scenes"]
characters_data = game_data["characters"]

# Armazenar o histórico de sessões
game_sessions = {}

def generate_text(session_id: str, player_input: str, max_tokens: int = 100):
    history = game_sessions.get(session_id, [])
    
    if not history:
        prompt = f"""
        You are an AI storyteller. Create an engaging introduction based on the player's initial input.
        Include a description of the setting and the character based on the input if mentioned.

        Player input: {player_input}
        Begin the story:
        """
    else:
        recent_history = "\n".join(history[-5:])
        prompt = f"""
        Continue the story based on the player's input while keeping the setting and characters consistent.

        STORY SO FAR:
        {recent_history}

        Player input: {player_input}
        Continue the story in 2-3 sentences:
        """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        
        story_output = response['choices'][0]['message']['content'].strip()
        
        # Adicionar ao histórico
        history.append(f"Player: {player_input}\nStory: {story_output}")
        game_sessions[session_id] = history
        
        return story_output
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating story: {str(e)}")

# Função para gerar imagens dinamicamente com base no nome das cenas e personagens
def generate_dynamic_images(player_input: str):
    background_url = None
    character_url = None

    # Encontrar um cenário correspondente
    selected_scene = None
    for scene in scenes_data:
        if scene["name"].lower() in player_input.lower():  # Verificar se o nome da cena está no input
            selected_scene = scene["name"]
            break

    # Gerar imagem de fundo caso um cenário tenha sido encontrado
    if selected_scene:
        background_url = generate_image(f"A {selected_scene} environment, fitting the ongoing story")
    
    # Encontrar um personagem correspondente
    selected_character = None
    for character in characters_data:
        if character["name"].lower() in player_input.lower():  # Verificar se o nome do personagem está no input
            selected_character = character["name"]
            break

    # Gerar imagem do personagem caso tenha sido encontrado
    if selected_character:
        character_url = generate_image(f"A {selected_character} character, depicted as a key character in the story")
    
    # Caso nenhum cenário ou personagem seja mencionado, criar uma imagem genérica
    if not background_url and not character_url:
        background_url = generate_image("A fantasy environment, setting the stage for an adventure")
        character_url = generate_image("A fantasy character, leading the story")
    
    return background_url, character_url

# Função para gerar imagens com tratamento de erros
def generate_image(prompt: str):
    try:
        response = openai.Image.create(
            model="dall-e-3", 
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return response["data"][0]["url"]
    except openai.error.InvalidRequestError as e:
        with open("image_errors.log", "a") as log:
            log.write(f"Prompt rejected: {prompt}\nError: {e}\n\n")
        return None

# Rota para iniciar uma nova sessão
@app.get("/initial_scene")
async def initial_scene():
    session_id = os.urandom(8).hex()
    game_sessions[session_id] = []
    return {
        "session_id": session_id,
        "story": "Type the beginning of your story and let the AI take over!",
        "background_url": "",
        "character_url": "",
    }

# Rota para gerar a próxima cena
@app.post("/next_scene")
async def next_scene(request: Request):
    data = await request.json()
    session_id = data.get("session_id", "default")
    user_prompt = data.get("input", "")

    if not user_prompt:
        raise HTTPException(status_code=400, detail="Player input is required")

    # Gerar a história
    story = generate_text(session_id, user_prompt)
    
    # Gerar imagens dinamicamente com base no nome
    background_url, character_url = generate_dynamic_images(user_prompt)
    
    return {
        "story": story,
        "background_url": background_url if background_url else "No change",
        "character_url": character_url if character_url else "No change",
        "session_id": session_id
}

# Rota para verificar se a API está online
@app.get("/")
async def home():
    return {"message": "AI Visual Novel Game API is running"}
