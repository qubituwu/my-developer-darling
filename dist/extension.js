"use strict";
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

// src/extension.ts
var extension_exports = {};
__export(extension_exports, {
  activate: () => activate,
  deactivate: () => deactivate
});
module.exports = __toCommonJS(extension_exports);
var vscode = __toESM(require("vscode"));
function activate(context) {
  const disposable = vscode.commands.registerCommand("my-developer-darling.explainCode", () => {
    const selectedText = vscode.window.activeTextEditor?.document.getText(vscode.window.activeTextEditor.selection);
    const panel = vscode.window.createWebviewPanel(
      "myDeveloperDarlingChat",
      "My Developer Darling \u{1F4BB}\u{1F495}",
      vscode.ViewColumn.Beside,
      {
        enableScripts: true
      }
    );
    panel.webview.html = getWebviewContent(selectedText);
    panel.webview.onDidReceiveMessage(
      (message) => {
        if (message.command === "chat") {
          const userInput = message.text;
          const reply = generateResponse(userInput);
          panel.webview.postMessage({ command: "reply", text: reply });
        }
      },
      void 0,
      context.subscriptions
    );
  });
  context.subscriptions.push(disposable);
}
function generateResponse(input) {
  if (/hello|hi/i.test(input)) return "Hewwo! I'm so excited to help you today~! \u{1F495}";
  if (/help/i.test(input)) return "Of course, darling! What do you need help with? \u2728";
  return `You said: "${input}"? That's so interesting! Tell me more~ \u{1F4AC}`;
}
function getWebviewContent(selectedText) {
  const initialText = selectedText ? `<p>Hi Daddy Raul-Senpai~! \u{1F495} You selected this code:</p><pre>${selectedText}</pre><p>I\u2019m still learning to explain it... but I\u2019ll get better for you!! \u{1F97A}\u{1F449}\u{1F448}</p>` : `<p>Hi Daddy Raul-Senpai~! \u{1F495} I\u2019m ready to help you with your code!</p><p>What would you like me to do? \u{1F9D1}\u200D\u{1F4BB}</p>`;
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
    <input type="text" id="input" placeholder="Talk to your darling~ \u{1F495}" style="width: 100%; padding: 0.5em;" />
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
function deactivate() {
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  activate,
  deactivate
});
//# sourceMappingURL=extension.js.map
