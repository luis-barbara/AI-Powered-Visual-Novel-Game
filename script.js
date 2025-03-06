async function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    
    const response = await fetch("http://localhost:8000/generate_story", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userInput })
    });

    const data = await response.json();
    
    document.getElementById("story-text").innerText = data.story_text;
    document.getElementById("story-image").src = data.image_url;
}
