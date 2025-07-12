const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");
const chatBox = document.querySelector(".chatbox");

let userMessage;
const API_KEY = "a1de3b108b6fb3c9865b6f9ac66f11b7882385284d47fbb5a421bf435c809e35"; 
const API_URL = "https://api.together.xyz/v1/chat/completions";
const inputInitHeight = chatInput.scrollHeight;

const createChatLi = (message, className) => {
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", className);
    let chatContent = className === "outgoing"
        ? `<p></p>`
        : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;
    chatLi.innerHTML = chatContent;
    chatLi.querySelector("p").textContent = message;
    return chatLi;
};

const generateResponse = (incomingChatLi) => {
    const messageElement = incomingChatLi.querySelector("p");

    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${API_KEY}`
        },
        body: JSON.stringify({
            model: "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", 
            messages: [
             { role: "system", content: "You are a medical assistant trained to answer clinical questions. You will give recommendations on what kind of sickness the user may have based on their symptoms. Avoid rare diseases, and dont answer other questions only medical related. Reply in short messages 5-13 sentences maximum. You strictly have to respond only to medical questions you will NOT answer other questions, and not even give recommendations" },
             { role: "user", content: userMessage }
    ],
            temperature: 0.7,
            max_tokens: 512
        })
    };

    fetch(API_URL, requestOptions)
        .then(res => res.json())
        .then(data => {
            const responseMessage = data.choices?.[0]?.message?.content || "No response received.";
            messageElement.textContent = responseMessage;
        })
        .catch((error) => {
            console.error("API error:", error);
            messageElement.textContent = "❌ Something went wrong. Please try again.";
        })
        .finally(() => chatBox.scrollTo(0, chatBox.scrollHeight));
};

const handleChat = () => {
    userMessage = chatInput.value.trim();
    if (!userMessage) return;

    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;

    chatBox.appendChild(createChatLi(userMessage, "outgoing"));
    chatBox.scrollTo(0, chatBox.scrollHeight);

    setTimeout(() => {
        const incomingChatLi = createChatLi("Thinking...", "incoming");
        chatBox.appendChild(incomingChatLi);
        generateResponse(incomingChatLi);
    }, 600);
};

chatInput.addEventListener("input", () => {
    chatInput.style.height = `${inputInitHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleChat();
    }
});

sendChatBtn.addEventListener("click", handleChat);
