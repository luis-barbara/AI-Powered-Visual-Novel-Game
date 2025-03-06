from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = FastAPI()

# URLs for APIs
OLLAMA_API_URL = "http://localhost:11434/api/generate"
STABILITY_API_URL = "https://api.stability.ai/v2beta/stable-image/generate/sd3"

# Load Stability AI API key from .env
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the API key
api_key = os.getenv('STABILITY_API_KEY')

# Define the URL for the API
url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"

# Prepare the headers with Authorization
headers = {
    'Authorization': f'Bearer {api_key}',
    'Accept': 'application/json',  # Specify that we want JSON response
}

# Define the parameters for the image generation
payload = {
    'prompt': 'A futuristic city skyline at sunset',
    'aspect_ratio': '16:9',
}

# Path to your image file (if you're using image-to-image mode)
image_path = 'path_to_your_image.jpg'

# Open the image file to send as part of the form
with open(image_path, 'rb') as img_file:
    files = {
        'image': img_file,
    }

    # Send POST request with multipart/form-data
    response = requests.post(url, headers=headers, data=payload, files=files)

# Check the response
if response.status_code == 200:
    print("Image generated successfully!")
    print(response.json())
else:
    print(f"Error {response.status_code}: {response.text}")


# Define the request models
class TextRequest(BaseModel):
    user_input: str

class ImageRequest(BaseModel):
    prompt: str

@app.post("/generate_text")
async def generate_text(data: TextRequest):
    """Generates text with Ollama"""
    payload = {"model": "mistral", "prompt": data.user_input}
    response = requests.post(OLLAMA_API_URL, json=payload)
    return response.json()

@app.post("/generate_image")
async def generate_image(data: ImageRequest):
    """Generates an image with Stability AI"""
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "application/json"
    }
    
    payload = {
        "prompt": data.prompt,
        "output_format": "png"
    }

    response = requests.post(STABILITY_API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.json()}

@app.post("/generate_story")
async def generate_story(data: TextRequest):
    """Generates story text and image together"""
    # Generate the narrative with Ollama
    text_response = requests.post(OLLAMA_API_URL, json={"model": "mistral", "prompt": data.user_input})
    text_data = text_response.json()
    story_text = text_data.get("response", "Error generating text.")

    # Generate the background image with Stability AI based on the story
    image_response = requests.post(STABILITY_API_URL, headers={"Authorization": f"Bearer {STABILITY_API_KEY}"}, json={"prompt": story_text, "output_format": "png"})
    image_data = image_response.json()

    return {
        "story_text": story_text,
        "image_url": image_data.get("image", "Error generating image.")  # This depends on the API response format
    }

@app.post("/game_action")
async def game_action(data: TextRequest):
    """Handles player input to generate text and image"""
    # Use player input to generate the next part of the story
    story_response = await generate_story(data)
    
    # Generate the next character image if needed
    # Example of adding a character image prompt based on the current scene
    character_prompt = f"A character appears in a {data.user_input} scene"
    character_image = await generate_image(ImageRequest(prompt=character_prompt))
    
    return {
        "story_text": story_response["story_text"],
        "background_image": story_response["image_url"],
        "character_image": character_image.get("image", "Error generating character image.")
    }

