async function sendQuestion() {

    const input = document.getElementById("questionInput");
    const question = input.value.trim();

    if (!question) {
        return;
    }

    addMessage("Tú", question, "user");

    input.value = "";

    addMessage(
        "Agente",
        "Pensando...",
        "agent",
        true
    );

    try {

        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        removeLoading();

        if (!response.ok) {
            addMessage(
                "Agente",
                `Error: ${data.detail}`,
                "agent"
            );
            return;
        }

        addMessage(
            "Agente",
            data.answer,
            "agent"
        );

    } catch (error) {

        removeLoading();

        addMessage(
            "Agente",
            `Error de conexión: ${error.message}`,
            "agent"
        );
    }
}


function askExample(question) {

    document.getElementById("questionInput").value = question;

    sendQuestion();
}


function addMessage(sender, text, className, loading = false) {

    const chatBox = document.getElementById("chatBox");

    const div = document.createElement("div");

    div.classList.add("message");

    if (loading) {
        div.id = "loadingMessage";
    }

    div.innerHTML = `
        <div class="${className}">
            ${sender}
        </div>
        <div class="agent">
            ${text}
        </div>
    `;

    chatBox.appendChild(div);

    chatBox.scrollTop = chatBox.scrollHeight;
}


function removeLoading() {

    const loading = document.getElementById("loadingMessage");

    if (loading) {
        loading.remove();
    }
}