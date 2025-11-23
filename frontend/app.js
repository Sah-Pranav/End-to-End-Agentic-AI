const form = document.getElementById('queryForm');
const input = document.getElementById('userInput');
const chatHistory = document.getElementById('chat-history');
const toolStatus = document.getElementById('tool-status');
const toolText = document.getElementById('tool-text');
const sendBtn = document.getElementById('sendBtn');

// Generate a random thread ID for the session
const threadId = crypto.randomUUID();
const BASE_URL = ""; // Use relative path to hit the proxy on the same server (port 3000)

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const query = input.value.trim();
  if (!query) return;

  // Add User Message
  appendMessage('user', query);
  input.value = '';
  input.disabled = true;
  sendBtn.disabled = true;

  // Create Assistant Message Placeholder
  const assistantMsgContent = appendMessage('assistant', '');
  let fullResponse = "";

  try {
    const response = await fetch(`${BASE_URL}/chat/stream`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: query, thread_id: threadId })
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const dataStr = line.slice(6).trim();
          if (dataStr === '[DONE]') break;
          if (!dataStr) continue;

          try {
            const eventData = JSON.parse(dataStr);
            console.log("Received event:", eventData); // Debug log

            // Handle Tool Calls (Agent "Thinking")
            if (eventData.agent && eventData.agent.messages && eventData.agent.messages[0].tool_calls) {
              const toolCall = eventData.agent.messages[0].tool_calls[0];
              showToolStatus(`Using tool: ${toolCall.name}`);
            }

            // Handle Tool Outputs (Agent "Done Thinking")
            if (eventData.tools) {
              showToolStatus("Processing data...");
            }

            // Handle Agent Content (Final Answer)
            if (eventData.agent && eventData.agent.messages) {
              const msg = eventData.agent.messages[0];
              if (msg.content) {
                // Remove <function=...> tags if present
                const cleanContent = msg.content.replace(/<function=.*?>.*?<\/function>/gs, '').trim();

                if (cleanContent) {
                  fullResponse = cleanContent;
                  // Render Markdown
                  assistantMsgContent.innerHTML = marked.parse(fullResponse);
                  hideToolStatus();
                }
              }
            }
          } catch (e) {
            console.error("Error parsing JSON:", e, "Raw data:", dataStr);
          }
        }
      }
      scrollToBottom();
    }
  } catch (err) {
    appendMessage('assistant', `Error: ${err.message}`);
  } finally {
    input.disabled = false;
    sendBtn.disabled = false;
    input.focus();
    hideToolStatus();
  }
});

function appendMessage(role, text) {
  const msgDiv = document.createElement('div');
  msgDiv.className = `message ${role}`;

  const avatarDiv = document.createElement('div');
  avatarDiv.className = 'avatar';
  avatarDiv.innerHTML = role === 'user' ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-robot"></i>';

  const contentDiv = document.createElement('div');
  contentDiv.className = 'content';
  contentDiv.innerHTML = role === 'user' ? text : marked.parse(text); // Render markdown immediately for user too if needed

  msgDiv.appendChild(avatarDiv);
  msgDiv.appendChild(contentDiv);

  chatHistory.appendChild(msgDiv);
  scrollToBottom();

  return contentDiv; // Return content div for streaming updates
}

function showToolStatus(text) {
  toolStatus.style.display = 'flex';
  toolText.textContent = text;
  scrollToBottom();
}

function hideToolStatus() {
  toolStatus.style.display = 'none';
}

function scrollToBottom() {
  chatHistory.scrollTop = chatHistory.scrollHeight;
}
