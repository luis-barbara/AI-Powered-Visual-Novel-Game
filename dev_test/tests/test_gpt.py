from openai import OpenAI  
import os
from dotenv import load_dotenv


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configure the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_text(prompt):
    """Generate a narrative using ChatGPT."""
    response = client.chat.completions.create(
        model="gpt-4",  
        messages=[{"role": "user", "content": prompt}]  # Input messages
    )
    return response.choices[0].message.content  # Access the response content

# Test the function
if __name__ == "__main__":
    user_prompt = input("Enter a prompt to generate a story: ")
    story_text = generate_text(user_prompt)
    print("\nGenerated story:\n", story_text)