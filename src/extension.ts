import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  const disposable = vscode.commands.registerCommand('my-developer-darling.explainCode', () => {
    const selectedText = vscode.window.activeTextEditor?.document.getText(vscode.window.activeTextEditor.selection);
    const panel = vscode.window.createWebviewPanel(
      'myDeveloperDarlingChat',
      'My Developer Darling 💻💕',
      vscode.ViewColumn.Beside,
      {
        enableScripts: true,
      }
    );

    panel.webview.html = getWebviewContent(selectedText);

    panel.webview.onDidReceiveMessage(
      message => {
        if (message.command === 'chat') {
          const userInput = message.text;
          const reply = generateResponse(userInput);
          panel.webview.postMessage({ command: 'reply', text: reply });
        }
      },
      undefined,
      context.subscriptions
    );
  });

  context.subscriptions.push(disposable);
}

function generateResponse(input: string): string {
  if (/hello|hi/i.test(input)) return "Hewwo! I'm so excited to help you today~! 💕";
  if (/help/i.test(input)) return "Of course, darling! What do you need help with? ✨";
  return `You said: "${input}"? That's so interesting! Tell me more~ 💬`;
}

function getWebviewContent(selectedText: string | undefined): string {
  // If no text is selected, use a default message
  const initialText = selectedText
    ? `<p>Hi Daddy Raul-Senpai~! 💕 You selected this code:</p><pre>${selectedText}</pre><p>I’m still learning to explain it... but I’ll get better for you!! 🥺👉👈</p>`
    : `<p>Hi Daddy Raul-Senpai~! 💕 I’m ready to help you with your code!</p><p>What would you like me to do? 🧑‍💻</p>`;

  return `
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Developer Darling</title>
    <style>
      body { font-family: sans-serif; padding: 1em; }
      #chat { max-height: 300px; overflow-y: auto; border: 1px solid #ccc; padding: 1em; margin-bottom: 1em; }
      .message { margin: 0.5em 0; }
      .user { color: #007acc; }
      .darling { color: hotpink; }
    </style>
  </head>
  <body>
    <div id="chat">
      <!-- Display initial selected text -->
      <div class="message darling">${initialText}</div>
    </div>
    <input type="text" id="input" placeholder="Talk to your darling~ 💕" style="width: 100%; padding: 0.5em;" />
    <script>
      const chat = document.getElementById('chat');
      const input = document.getElementById('input');

      window.addEventListener('message', event => {
        const message = event.data;
        if (message.command === 'reply') {
          const div = document.createElement('div');
          div.className = 'message darling';
          div.textContent = "Darling: " + message.text;
          chat.appendChild(div);
          chat.scrollTop = chat.scrollHeight;
        }
      });

      input.addEventListener('keydown', e => {
        if (e.key === 'Enter') {
          const text = input.value;
          if (text.trim()) {
            // Display user's message
            const div = document.createElement('div');
            div.className = 'message user';
            div.textContent = "You: " + text;
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;

            // Send the user message to the extension
            window.vscode.postMessage({ command: 'chat', text });

            // Clear input field after sending the message
            input.value = '';
          }
        }
      });

      window.vscode = acquireVsCodeApi();
    </script>
  </body>
  </html>
  `;
}

export function deactivate() {}
