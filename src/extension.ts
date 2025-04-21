import * as vscode from 'vscode';


const fetch = async (url: string, options?: any) => {
  const mod = await import('node-fetch');
  return mod.default(url, options);
};



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
      async message => {
        if (message.command === 'chat') {
          const userInput = message.text;
          const reply = await generateResponse(userInput, selectedText);
          panel.webview.postMessage({ command: 'reply', text: reply });
        }
      },
      undefined,
      context.subscriptions
    );
  });

  context.subscriptions.push(disposable);
}

async function generateResponse(userInput: string, selectedText?: string): Promise<string> {
  try {
    const persona = "silly"; // Default persona 💖
    const response = await fetch('http://localhost:8000/ai/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        code_snippet: selectedText || userInput,
        persona
      })
    });

    const data = await response.json();
    const parsed = data as { feedback: string };
    return parsed.feedback || "UwU~ Something went wrong, sowwy~ 💔";

  } catch (error) {
    return "Oopsies~ I couldn't reach my backend brain 😢 Make sure it's running!";
  }
}



function getWebviewContent(selectedText: string | undefined): string {
  const initialText = selectedText
    ? `<p>Hewwo pookie~! 💕 You selected this code:</p><pre>${selectedText}</pre><p>I’m ready to help you with your code! 🧠💞</p><p>What would you like help with? ^__< </p>`
    : `<p>Hi pookie~! 💕`;

  return `
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
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
      <div class="message darling">${initialText}</div>
    </div>
    <input type="text" id="input" placeholder="Talk to your darling~ 💕" style="width: 100%; padding: 0.5em;" />
    <script>
      const chat = document.getElementById('chat');
      const input = document.getElementById('input');
      window.vscode = acquireVsCodeApi();

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
            const div = document.createElement('div');
            div.className = 'message user';
            div.textContent = "You: " + text;
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
            window.vscode.postMessage({ command: 'chat', text });
            input.value = '';
          }
        }
      });
    </script>
  </body>
  </html>
  `;
}

export function deactivate() {}
