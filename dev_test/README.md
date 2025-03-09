# AI-Powered Visual Novel Game

A simple prototype of an endless visual novel game with AI-generated content.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Challenges Faced](#challenges-faced)
- [Testing](#testing)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)
- [Future Improvements](#future-improvements)

## Introduction

The AI-Powered Visual Novel Game is a prototype that generates endless visual novel content using OpenAI's GPT-4 and DALL·E models. Players can input prompts to generate dynamic stories and images, creating an immersive and interactive experience. The game provides an engaging and dynamic narrative where the player influences the story's direction through simple input. It also generates custom visuals using AI to enhance the storytelling.

## Features

- **AI-Generated Stories**: Generate engaging stories based on player input using GPT-4, with branching narratives and dynamic content.
- **Dynamic Images**: Create background and character images on the fly using DALL·E.
- **Interactive Gameplay**: Players can influence the story by providing input at each step of the narrative.
- **Web Interface**: A simple and intuitive web interface to play the game locally or deploy it on the web.
- **Customizable Content**: Players can create unique stories by interacting with the game.
- **FastAPI Backend**: A robust backend powered by FastAPI, allowing fast story generation and interaction.

## Installation

### Prerequisites

Before getting started, you need to have the following software installed:

- **Python 3.10+**
- **Poetry**: Dependency management and virtual environment tool for Python.
- **OpenAI API Key**: You need an OpenAI API key to interact with GPT-4 for story generation and DALL·E for image generation.

### 1. Clone the repository

Clone the repository to your local machine:

```bash
git clone https://github.com/luis-barbara/AI-Powered-Visual-Novel-Game
cd AI-Powered-Visual-Novel-Game/dev_test
```

### 2. Install dependencies

Ensure that Poetry is installed and use it to install the required dependencies:

```bash
poetry install
```

Poetry will automatically set up a virtual environment and install all the necessary dependencies listed in pyproject.toml.

### 3. Set up environment variables

Create a `.env` file in the `dev_test` directory with the following content:

```bash
OPENAI_API_KEY=your_openai_api_key
```

Make sure to replace `your_openai_api_key` with your actual OpenAI API key.

## Usage

### 1. Run the FastAPI server

Start the FastAPI server using Poetry:

```bash
poetry run uvicorn dev_test.src.dev_test.main:app --reload
```

This will start the server in development mode and allow you to test the application locally.

### 2. Open your browser

Open a browser and navigate to the following URL to start playing the game:

```bash
http://localhost:8000
```

### 3. Gameplay

Once you’ve navigated to the game in your browser, you will be prompted to describe a character and a setting. The AI will generate both the story and images based on your description. From there, you can continue generating new stories and images by repeating the process.

## Project Structure

Project structure:

```plaintext
dev_test/
├── .env                # Environment variables file
├── .gitignore          # Git ignore file
├── LICENSE             # Project license file
├── poetry.lock         # Poetry lock file
├── pyproject.toml      # Poetry project configuration file
├── README.md           # This file
├── src/
│   └── dev_test/
│       ├── __init__.py # Package initializer
│       ├── keywords.json # JSON file with scenes and characters data
│       ├── main.py      # Main FastAPI application file
│       ├── static/      # Directory containing static files
│       │   ├── index.html  # HTML file for the game interface
│       │   ├── script.js   # JavaScript file for interactivity
│       │   ├── styles.css  # CSS file for styling
│       │   └── images/     # Folder for static images (e.g., favicon)
│   └── tests/           # Directory containing test scripts
│       ├── __init__.py
│       ├── generate_text.py  # Test for the story generation function
│       ├── test_dalle.py     # Test for DALL·E image generation
│       └── test_gpt.py       # Test for GPT-4 story generation
└── LICENSE              # Project license file
```

- **`src/dev_test/main.py`**: Main FastAPI application file that handles requests and generates stories and images.
- **`src/dev_test/keywords.json`**: JSON file containing predefined scenes and characters used for story generation.
- **`src/dev_test/static/`**: Directory containing static files such as HTML, CSS, JS, and images.
- **`tests/`**: Directory containing unit tests for different components of the game, such as text generation and image generation.

## Challenges Faced

### Initial Approach: Running Models Locally

At first, I explored different approaches to running AI models locally. My initial attempts included:

- Running **Ollama** models in a **Docker container**.
- Running **Stable Diffusion** from **Hugging Face** in Docker.

#### Hardware Limitations

My biggest challenge was that my **hardware was not powerful enough** to run these models locally. My setup included:

- **4GB of available RAM**
- **NVIDIA GeForce GTX 950M (an older GPU)**

Due to these limitations, it was impossible to generate images, even though text generation worked for smaller models.

### Switching to OpenAI API

Since local inference was not feasible, I integrated **OpenAI's GPT-4 and DALL·E** APIs. This approach made it easier to run and test the project.

However, using an API has **its own limitations**:
- **Cost**: The API is **not free**, which could be a concern for large-scale or production use.
- **Dependence on OpenAI**: Since it is an external API, any **updates, failures, or downtime** could impact the project’s functionality.
- **Rate Limits**: API usage is subject to rate limits, which could restrict the number of requests per minute.

### Generating Character and Background Separately

Another challenge was **separating the character from the background** in image generation. By default, the model **did not distinguish between the two**, often merging them into a single image.

#### Solution:
- I created a **JSON file** containing **a list of characters** and **a list of backgrounds**.
- This helped the model **differentiate between the two**.
- If the requested character or background was not in the list, the model would **generate them dynamically**.

### Story Generation Challenges

Initially, I wanted to create a **branching narrative** where players **choose from multiple options** to continue the story. However, I encountered **several issues**:

- **Inconsistent Options**: The generated choices were sometimes unrelated to the story.
- **Input Interpretation**: When a user typed a response, the model sometimes failed to **match it to the available options**.

#### Solution:
- Instead of relying on free-text input for choices, I considered adding **buttons for selection**. However, this **limited player freedom**.
- I decided to **simplify the approach**, allowing the user to **describe a character and a setting**, and the AI would then **generate a story based on that input**.

## Future Improvements

While the current implementation provides a functional AI-powered visual novel, there are several ways to improve and expand the project:

### 1. **Character and Background Refinement**
- Improve **image generation consistency**, ensuring that characters and backgrounds align more naturally.
- Develop a **style-consistent character generation system** to prevent visual mismatches between different story elements.

### 2. **More Interactive Storytelling**
- Implement a **memory system** so that the AI can remember previous choices and generate a more **coherent** long-term story.
- Add **branching dialogue options** with structured responses to enhance user interaction.

### 3. **Game UI Enhancements**
- Improve the **web interface** by adding an **inventory system**, character stats, or RPG-like progression.
- Allow users to **customize their characters and settings** with sliders or dropdowns instead of free-text input.

### 4. **Multiplayer or Shared Stories**
- Implement a feature where multiple users can **collaborate on a story** in real-time.
- Allow users to **share and remix AI-generated stories**.

### 5. **Better Handling of AI Limitations**
- Implement **fail-safes** to handle **inconsistent or illogical AI outputs**.
- Provide **editable AI-generated content**, so players can tweak the story if they don’t like the output.

### 6. **Save System**
- Add a **save and load feature**, allowing players to continue their story later.
- Implement an **auto-save system** at key story points to prevent loss of progress.

### 7. **User Authentication (Login System)**
- Introduce a **user account system** so players can save their progress online.
- Store **custom characters, preferences, and achievements** linked to a user profile.

### 8. **Character Selection and Stats**
- Allow players to **choose a character** with different attributes like:
  - **Strength** (affects combat scenarios)
  - **Health** (determines survival in dangerous situations)
  - **Intelligence** (influences decision-making and AI-generated responses)
- Create **custom character leveling and progression** to enhance RPG elements.

By implementing these improvements, the project can evolve into a **fully-fledged interactive storytelling platform**, offering a richer and more immersive experience for users.

## Testing

To run the tests for different components of the game:

Run unit tests using pytest:

```bash
poetry run pytest
```

This will run all the tests in the tests/ directory.

Run specific tests (for example, test for GPT-4 story generation):

```bash
poetry run pytest tests/test_gpt.py
```

## Contributing
You're welcome contributions to this project. To contribute:

Fork the repository.
- Create a new branch (git checkout -b feature-name).
- Make your changes and commit them (git commit -am 'Add feature').
- Push to the branch (git push origin feature-name).
- Open a pull request.

## Acknowledgments
- OpenAI GPT-4: For generating stories and text-based content.
- OpenAI DALL·E: For generating dynamic images to complement the story.
- FastAPI: For building a fast and reliable backend server for the game.
- Poetry: For managing dependencies and virtual environments.
