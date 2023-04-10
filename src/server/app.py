from flask import Flask, request, jsonify

from src.server.language_model.gpt_client import GptClient
from src.server.memory.local import LocalMemory

app = Flask(__name__)


@app.route('/chat', methods=['POST'])
def chat():
    message = request.form['message']
    gpt_client = GptClient()
    response = gpt_client.chat(message)
    return jsonify({'response': response})


@app.route('/command', methods=['GET'])
def list_commands():
    return jsonify({'commands': ['show_memories']})


@app.route('/command', methods=['POST'])
def process_command():
    command = request.form['command']
    args = request.form.get('args', '')
    return jsonify({'message': f'Hello, {command}!'})


if __name__ == '__main__':
    memory = LocalMemory()
    memory.load()
    app.run(debug=True)
