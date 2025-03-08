from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI  
import os
import json
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize the FastAPI application
app = FastAPI()

# Serve static files (HTML, CSS, JS, images)
app.mount("/static", StaticFiles(directory="/home/luis-barbara/AI-Powered-Visual-Novel-Game/dev_test/src/dev_test/static"), name="static")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Function to load JSON data with scenes and characters
def load_game_data():
    try:
        with open("keywords.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading game data: {str(e)}")

# Load game data from JSON
game_data = load_game_data()
scenes_data = game_data["scenes"]
characters_data = game_data["characters"]

# Store game session history
game_sessions = {}

def generate_text(session_id: str, player_input: str, max_characters: int = 500):
    """Generate story text using GPT-4 based on player input, ensuring a complete narrative with a start, middle, and end."""
    history = game_sessions.get(session_id, [])
    
    # If no history exists, create an engaging introduction
    if not history:
        prompt = f"""
        Write a quick and straightforward story with a clear beginning, middle, and end. Avoid long descriptions and keep it simple. Ensure:
        - A **start** that introduces the setting and main character.
        - A **middle** that provides conflict or action.
        - An **end** that concludes the story in a satisfying way, ensuring it doesn't leave any loose ends.
        - The narrative must **finish**. Even if there is space for more, you should complete the story within the given length. 

        Player input: {player_input}
        Write a very short story:
        """
    else:
        # Continue the story based on recent history
        recent_history = "\n".join(history[-5:])
        prompt = f"""
        Continue the story based on the player's input while keeping the setting and characters consistent.
        The continuation must include:
        - A **start** that sets up the scene or conflict.
        - A **middle** that moves the story forward.
        - A **conclusion** that wraps up the story in a complete and satisfying way, ensuring there are no loose ends.
        - The narrative should **finish** by the end of the response. Even if the story could go further, ensure it concludes well.

        STORY SO FAR:
        {recent_history}

        Player input: {player_input}
        Continue the story in a full, complete paragraph, ensuring there is a clear start, middle, and end, and finish it within the character limit:
        """
    
    try:
        # Generate story text using GPT-4
        response = client.chat.completions.create(
            model="gpt-4",  
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,  # A higher token limit as we're focusing on characters.
            temperature=0.7,
        )
        
        # Extract the story text from the response
        story_output = response.choices[0].message.content.strip()
        
        # Ensure we are within the character limit
        if len(story_output) > max_characters:
            story_output = story_output[:max_characters]
        
        # Add to session history
        history.append(f"Player: {player_input}\nStory: {story_output}")
        game_sessions[session_id] = history
        
        return story_output
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating story: {str(e)}")

def generate_dynamic_images(player_input: str):
    """Generate background and character images using DALL·E."""
    background_url = None
    character_url = None

    # Default prompts for background and character
    background_prompt = (
    f"A detailed environment of {player_input}. "
    "The scene is immersive and atmospheric, with possible NPCs, creatures, or secondary characters, "
    "but the main protagonist is NOT present in this scene."
)
    character_prompt = (
    f"A highly detailed portrait of a {player_input} character. "
    "The character is centered, standing in a neutral background (plain white or transparent). "
    "Only the character should be visible—no background details, no environment, just the character."
)

    # Try to extract scene and character from player input
    for scene in scenes_data:
        if scene["name"].lower() in player_input.lower():
            background_prompt = f"A {scene['name']} environment, fitting the ongoing story, without any characters."
            break

    for character in characters_data:
        if character["name"].lower() in player_input.lower():
            character_prompt = f"A {character['name']} character, depicted as a key character in the story, without any background."
            break

    # Generate background image
    try:
        background_url = generate_image(background_prompt)
    except Exception as e:
        print(f"Error generating background image: {e}")

    # Generate character image
    try:
        character_url = generate_image(character_prompt)
    except Exception as e:
        print(f"Error generating character image: {e}")

    return background_url, character_url

def generate_image(prompt: str):
    """Generate an image using DALL·E."""
    try:
        response = client.images.generate(
            model="dall-e-3", 
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return response.data[0].url
    except Exception as e:
        # Log errors if the prompt is rejected
        with open("image_errors.log", "a") as log:
            log.write(f"Prompt rejected: {prompt}\nError: {e}\n\n")
        return None

# Route to start a new session
@app.get("/initial_scene")
async def initial_scene():
    """Initialize a new game session."""
    session_id = os.urandom(8).hex()
    game_sessions[session_id] = []
    return {
        "session_id": session_id,
        "story": (
            "Welcome to the AI Visual Novel Game!\n\n"
            "To start your adventure, choose a character and a setting, or create your own!\n\n"
            "Here are some examples to inspire you:\n"
            "1. A brave knight exploring a magical forest.\n"
            "2. A space explorer discovering an alien planet.\n"
            "The AI will take your input and create an exciting story for you. Let your imagination run wild!"
        ),
        "background_url": "",
        "character_url": "",
    }

# Route to generate the next scene
@app.post("/next_scene")
async def next_scene(request: Request):
    """Generate the next scene based on player input."""
    data = await request.json()
    session_id = data.get("session_id", "default")
    user_prompt = data.get("input", "")

    if not user_prompt:
        raise HTTPException(status_code=400, detail="Player input is required")

    # Generate the story
    story = generate_text(session_id, user_prompt)
    
    # Generate dynamic images based on input
    background_url, character_url = generate_dynamic_images(user_prompt)
    
    return {
        "story": story,
        "background_url": background_url if background_url else "No change",
        "character_url": character_url if character_url else "No change",
        "session_id": session_id
    }

# Route to serve the main HTML file
@app.get("/")
async def home():
    return FileResponse("/home/luis-barbara/AI-Powered-Visual-Novel-Game/dev_test/src/dev_test/static/index.html")