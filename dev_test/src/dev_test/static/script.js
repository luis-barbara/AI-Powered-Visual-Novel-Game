// Function to start the game
async function startGame() {
    const response = await fetch('http://localhost:8000/initial_scene');
    const data = await response.json();
    console.log("Initial Scene Response:", data); // Check the initial response

    localStorage.setItem("session_id", data.session_id); // Store the session_id
    document.getElementById("story").innerText = data.story; // Display the initial story

    // Display the background and character
    if (data.background_url !== "No change") {
        document.getElementById("background").src = data.background_url;
    }
    if (data.character_url !== "No change") {
        document.getElementById("character").src = data.character_url;
    }
}

// Function to send player input and generate the next scene
async function nextScene() {
    const input = document.getElementById("player_input").value; // Get player input
    if (!input) {
        alert("Please enter some text to continue.");
        return;
    }

    const session_id = localStorage.getItem("session_id");
    const response = await fetch('http://localhost:8000/next_scene', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            session_id: session_id,
            input: input
        })
    });

    const data = await response.json();
    console.log("Next Scene Response:", data); // Check the next scene response

    document.getElementById("story").innerText = data.story; // Update the story

    // Check and update image URLs
    console.log("Background URL:", data.background_url); // Check the background URL
    console.log("Character URL:", data.character_url); // Check the character URL

    if (data.background_url !== "No change") {
        document.getElementById("background").src = data.background_url;
    }

    if (data.character_url !== "No change") {
        document.getElementById("character").src = data.character_url;
    }

    // Clear player input
    document.getElementById("player_input").value = "";
}

// Function to set up the submit event
document.getElementById("submit_button").addEventListener("click", nextScene);

// Start the game when the page loads
window.onload = function() {
    startGame();
};