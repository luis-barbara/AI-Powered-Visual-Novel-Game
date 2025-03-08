// Função para iniciar o jogo
async function startGame() {
    const response = await fetch('http://localhost:8000/initial_scene');
    const data = await response.json();
    console.log("Initial Scene Response:", data); // Verifica a resposta inicial

    localStorage.setItem("session_id", data.session_id); // Armazena o session_id
    document.getElementById("story").innerText = data.story; // Exibe a história inicial

    // Exibe o background e o character
    if (data.background_url !== "No change") {
        document.getElementById("background").src = data.background_url;
    }
    if (data.character_url !== "No change") {
        document.getElementById("character").src = data.character_url;
    }
}

// Função para enviar a entrada do jogador e gerar a próxima cena
async function nextScene() {
    const input = document.getElementById("player_input").value; // Obtém o input do jogador
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
    console.log("Next Scene Response:", data); // Verifica a resposta da próxima cena

    document.getElementById("story").innerText = data.story; // Atualiza a história

    // Verifica e atualiza as URLs das imagens
    console.log("Background URL:", data.background_url); // Verifica a URL do background
    console.log("Character URL:", data.character_url); // Verifica a URL do character

    if (data.background_url !== "No change") {
        document.getElementById("background").src = data.background_url;
    }

    if (data.character_url !== "No change") {
        document.getElementById("character").src = data.character_url;
    }

    // Limpa o input do jogador
    document.getElementById("player_input").value = "";
}

// Função para configurar o evento de submissão
document.getElementById("submit_button").addEventListener("click", nextScene);

// Inicia o jogo assim que a página carregar
window.onload = function() {
    startGame();
};
