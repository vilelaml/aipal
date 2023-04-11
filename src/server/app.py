from flask import Flask, request, jsonify

from src.server.command.command import Command
from src.server.config.load_commands import load_core_commands
from src.server.language_model.gpt_client import GptClient
from src.server.memory.local import LocalMemory

app = Flask(__name__)


@app.route('/command', methods=['GET'])
def list_commands():
    return jsonify({'commands': ['show_memories']})


@app.route('/command', methods=['POST'])
def process_command():
    command = Command(request.form['command'], request.form.get('args', '{}'))
    return jsonify({'response': command.execute()})


if __name__ == '__main__':
    memory = LocalMemory()
    memory.load()
    load_core_commands()
    app.run(debug=True)
