import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  const disposable = vscode.commands.registerCommand('my-developer-darling.explainCode', async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showInformationMessage("No active editor found.");
      return;
    }

    const selection = editor.selection;
    const text = editor.document.getText(selection);

    if (!text) {
      vscode.window.showInformationMessage("Please select some code.");
      return;
    }

    vscode.window.showInformationMessage(`Explaining: ${text}`);
  });

  context.subscriptions.push(disposable);
}

export function deactivate() {}
