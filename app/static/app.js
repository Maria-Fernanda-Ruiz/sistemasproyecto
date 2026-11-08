const userForm = document.querySelector("#user-form");
const usernameInput = document.querySelector("#username");
const currentUserPanel = document.querySelector("#current-user");
const identityLabel = document.querySelector("#identity-label");
const statusMessage = document.querySelector("#status-message");
const messagesPanel = document.querySelector("#messages");
const messageForm = document.querySelector("#message-form");
const messageInput = document.querySelector("#message-body");
const sendButton = messageForm.querySelector("button");

const USER_KEY = "distributed-chat-user";
let currentUser = null;
let currentIdentity = null;
let lastMessageSignature = null;

function showStatus(message, kind = "info") {
  statusMessage.textContent = message;
  statusMessage.dataset.kind = kind;
}

function setCurrentUser(username, identity) {
  currentUser = username;
  currentIdentity = identity;
  localStorage.setItem(USER_KEY, JSON.stringify({ username, identity }));
  userForm.hidden = true;
  currentUserPanel.hidden = false;
  identityLabel.textContent = identity;
  messageInput.disabled = false;
  sendButton.disabled = false;
  messageInput.focus();
  showStatus("Ya puedes enviar mensajes a #general.");
}

function createEmptyState() {
  const empty = document.createElement("div");
  empty.className = "empty-state";

  const title = document.createElement("strong");
  title.textContent = "El lobby está tranquilo";

  const hint = document.createElement("span");
  hint.textContent = "Sé la primera persona en escribir.";

  empty.append(title, hint);
  return empty;
}

function renderMessages(messages) {
  const isNearBottom =
    messagesPanel.scrollHeight - messagesPanel.scrollTop - messagesPanel.clientHeight < 60;
  messagesPanel.replaceChildren();

  if (messages.length === 0) {
    messagesPanel.append(createEmptyState());
    return;
  }

  for (const message of messages) {
    const item = document.createElement("article");
    item.className = "message";
    if (message.from === currentIdentity) {
      item.classList.add("is-own");
    }

    const meta = document.createElement("div");
    meta.className = "message-meta";
    const sender = document.createElement("strong");
    sender.textContent = message.from;
    const time = document.createElement("time");
    time.dateTime = message.sent_at;
    const date = new Date(message.sent_at);
    time.textContent = Number.isNaN(date.getTime())
      ? ""
      : date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    meta.append(sender, time);

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";
    bubble.textContent = message.body;

    item.append(meta, bubble);
    messagesPanel.append(item);
  }

  if (isNearBottom) {
    messagesPanel.scrollTop = messagesPanel.scrollHeight;
  }
}

async function loadMessages() {
  try {
    const response = await fetch("/messages");
    if (!response.ok) {
      throw new Error(`El servidor respondió ${response.status}.`);
    }

    const messages = await response.json();
    const signature = messages.map((message) => message.id).join("|");
    if (signature !== lastMessageSignature) {
      renderMessages(messages);
      lastMessageSignature = signature;
    }
  } catch (error) {
    showStatus(`No se pudieron cargar los mensajes: ${error.message}`, "error");
  }
}

userForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const username = usernameInput.value.trim();

  try {
    const response = await fetch("/users", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username }),
    });
    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.detail ?? `El servidor respondió ${response.status}.`);
    }

    setCurrentUser(result.username, result.identity);
    await loadMessages();
  } catch (error) {
    showStatus(error.message, "error");
  }
});

messageForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!currentUser) {
    showStatus("Primero elige un nombre de usuario.", "error");
    return;
  }

  const body = messageInput.value.trim();
  if (!body) {
    return;
  }

  sendButton.disabled = true;
  try {
    const response = await fetch("/messages", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: currentUser, body }),
    });
    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.detail ?? `El servidor respondió ${response.status}.`);
    }

    messageInput.value = "";
    await loadMessages();
    messageInput.focus();
    showStatus("Mensaje enviado.");
  } catch (error) {
    showStatus(error.message, "error");
  } finally {
    sendButton.disabled = false;
  }
});

const savedUser = localStorage.getItem(USER_KEY);
if (savedUser) {
  try {
    const parsedUser = JSON.parse(savedUser);
    if (parsedUser.username && parsedUser.identity) {
      setCurrentUser(parsedUser.username, parsedUser.identity);
    }
  } catch {
    localStorage.removeItem(USER_KEY);
  }
}

void loadMessages();
window.setInterval(loadMessages, 2000);
