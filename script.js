async function sendMessage() {
    const userInput = document.getElementById("user-input").value;

    const response = await fetch("http://127.0.0.1:8000/generate_story", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ prompt: userInput, max_tokens: 100 })
    });

    const data = await response.json();
    
    // Atualiza o texto da história na página
    document.getElementById("story-text").innerText = data.story;

    // Verifica se a URL da imagem foi fornecida e a exibe
    if (data.image_url) {
        document.getElementById("story-image").src = data.image_url;
    }
}
