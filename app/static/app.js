let conversations = JSON.parse(localStorage.getItem("conversations")) || [];
let currentConversationId = null;

function saveConversations() {
    localStorage.setItem("conversations", JSON.stringify(conversations));
}

function newConversation() {
    const conversation = {
        id: Date.now(),
        title: "Nueva conversación",
        messages: []
    };

    conversations.unshift(conversation);
    currentConversationId = conversation.id;

    saveConversations();
    renderConversationList();
    renderChat();
}

function getCurrentConversation() {
    return conversations.find(c => c.id === currentConversationId);
}

function renderConversationList() {
    const list = document.getElementById("conversationList");
    list.innerHTML = "";

    conversations.forEach(conversation => {
        const div = document.createElement("div");
        div.className = "conversation-item";
        div.textContent = conversation.title;

        div.onclick = () => {
            currentConversationId = conversation.id;
            renderChat();
            renderConversationList();
        };

        list.appendChild(div);
    });
}

function renderChat() {
    const chatBox = document.getElementById("chatBox");
    chatBox.innerHTML = "";

    const conversation = getCurrentConversation();

    if (!conversation) return;

    conversation.messages.forEach(message => {
        addMessageToDOM(message.sender, message.text, message.type);
    });
}

async function sendQuestion() {
    const input = document.getElementById("questionInput");
    const question = input.value.trim();

    if (!question) return;

    if (!currentConversationId) {
        newConversation();
    }

    const conversation = getCurrentConversation();

    if (conversation.messages.length === 0) {
        conversation.title = question.slice(0, 35);
    }

    conversation.messages.push({
        sender: "Tú",
        text: question,
        type: "user"
    });

    saveConversations();
    renderConversationList();
    renderChat();

    input.value = "";

    addMessageToDOM("Agente", "Pensando...", "agent", true);

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question,
                history: conversation.messages.map(message => ({
                    role: message.type === "user" ? "user" : "assistant",
                    content: message.text
                }))
            })
        });

        const data = await response.json();

        removeLoading();

        if (!response.ok) {
            conversation.messages.push({
                sender: "Agente",
                text: `Error: ${data.detail}`,
                type: "agent"
            });
        } else {
            conversation.messages.push({
                sender: "Agente",
                text: data.answer,
                type: "agent"
            });
        }

        saveConversations();
        renderChat();

    } catch (error) {
        removeLoading();

        conversation.messages.push({
            sender: "Agente",
            text: `Error de conexión: ${error.message}`,
            type: "agent"
        });

        saveConversations();
        renderChat();
    }
}

function askExample(question) {
    document.getElementById("questionInput").value = question;
    sendQuestion();
}

function addMessageToDOM(sender, text, type, loading = false) {
    const chatBox = document.getElementById("chatBox");

    const div = document.createElement("div");
    div.classList.add("message");

    if (loading) {
        div.id = "loadingMessage";
    }

    if (type === "user") {
        div.innerHTML = `
            <div class="user">${sender}</div>
            <div>${text}</div>
        `;
    } else {
        div.innerHTML = `
            <div class="agent-label">${sender}</div>
            <div class="agent">${marked.parse(text)}</div>
        `;
    }

    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function removeLoading() {
    const loading = document.getElementById("loadingMessage");
    if (loading) loading.remove();
}

if (conversations.length === 0) {
    newConversation();
} else {
    currentConversationId = conversations[0].id;
    renderConversationList();
    renderChat();
}