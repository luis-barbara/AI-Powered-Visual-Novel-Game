async function sendPlayerInput() {
    const playerInput = document.getElementById("text-input").value;

    // Send input to the backend to generate story and images
    const response = await fetch('http://localhost:8000/game_action', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input: playerInput }),
    });

    const data = await response.json();

    // Update story text and images
    document.getElementById("story-text").textContent = data.story_text;
    document.getElementById("image").src = data.background_image;
    document.getElementById("character").src = data.character_image;
}
