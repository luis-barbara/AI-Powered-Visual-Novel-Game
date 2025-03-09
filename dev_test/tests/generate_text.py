import os
from dotenv import load_dotenv
from openai import OpenAI
import json

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Function to generate text based on the player's input
def generate_text(player_input: str, session_id: str = "test_session", max_characters: int = 500):
    """Generate a complete story with a clear and satisfying end."""
    
    prompt = f"""
    Write a short, complete story with a clear structure:
    - **Beginning**: Introduce the main character, setting, and their goal.
    - **Middle**: The character faces a challenge or conflict.
    - **End**: Provide a conclusion where the conflict is resolved, and the story ends definitively.

    The story should:
    - Be **one paragraph**.
    - **End with a period** and not be cut off.
    - Be concise and clear, with no loose ends.

    Player input: {player_input}
    Write the story following these guidelines and ensure it finishes properly with a complete ending.
    """
    
    try:
        # Generate the story using GPT-4
        response = client.chat.completions.create(
            model="gpt-4",  
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,  # Token limit for brevity
            temperature=0.7,
        )
        
        # Extract the generated story from the response
        story_output = response.choices[0].message.content.strip()
        
        # Ensure the story ends with a period
        if not story_output.endswith('.'):
            story_output += '.'
        
        return story_output
    except Exception as e:
        print(f"Error generating text: {str(e)}")
        return None

if __name__ == "__main__":
    # Take input directly from the terminal
    player_input = input("Enter what you want for the story (e.g., 'A brave knight exploring a magical forest'): ")
    
    # Generate the story
    story = generate_text(player_input)
    
    # Display the generated story
    if story:
        print("\nGenerated story:\n")
        print(story)
    else:
        print("Error generating the story.")
