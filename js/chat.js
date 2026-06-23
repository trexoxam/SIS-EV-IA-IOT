const nombreGuardado = localStorage.getItem('nombreUsuario');
if (nombreGuardado) {
    console.log("Bienvenido de vuelta, " + nombreGuardado);
document.getElementById('chatForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Evita que la página se recargue
    const inputField = document.getElementById('userInput');
    const messageText = inputField.value.trim();
    if (messageText === '') return;
    appendMessage(messageText, 'user-message');
    inputField.value = ''; // Limpiar el input
    const chatBox = document.getElementById('chatBox');
    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'message bot-message';
    typingIndicator.innerHTML = '<p><em>Buscando apoyos...</em></p>';
    chatBox.appendChild(typingIndicator);
    chatBox.scrollTop = chatBox.scrollHeight;
    fetch('/api/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        pregunta: messageText
    })
})
.then(response => response.json())
.then(data => {

    chatBox.removeChild(typingIndicator);

    appendMessage(
        data.respuesta,
        'bot-message'
    );

})
.catch(error => {

    chatBox.removeChild(typingIndicator);

    appendMessage(
        'Ocurrió un error al consultar la información.',
        'bot-message'
    );

    console.error(error);
});
});

function appendMessage(text, className) {
    const chatBox = document.getElementById('chatBox');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${className}`;
messageDiv.innerHTML =
    `<p>${text.replace(/\n/g, '<br>')}</p>`;    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
function loginExitoso() {
    localStorage.setItem('usuarioLogueado', 'true');
    localStorage.setItem('rolUsuario', 'admin'); 
    window.location.href = 'index.html';
}
}