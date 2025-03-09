from openai import OpenAI  
import os
from dotenv import load_dotenv


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configure the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_image(prompt):
    """Generate an image based on a prompt using the DALL·E API."""
    response = client.images.generate(
        model="dall-e-3",  
        prompt=prompt,
        n=1,  # Number of images to generate
        size="1024x1024"  # Image size
    )
    return response.data[0].url  # Access the URL of the generated image

# Test the function
if __name__ == "__main__":
    user_prompt = input("Enter a prompt to generate an image: ")
    image_url = generate_image(user_prompt)
    print("\nGenerated image URL:", image_url)