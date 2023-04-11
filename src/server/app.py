from flask import Flask, request, jsonify

from src.server.command.command import Command
from src.server.config.config import Config
from src.server.config.load_commands import load_core_commands
from src.server.memory.local import LocalMemory

app = Flask(__name__)


@app.route('/command', methods=['GET'])
def list_commands():
    commands = Config().command_names
    return jsonify({'commands': commands})


@app.route('/command', methods=['POST'])
def process_command():
    command = Command(request.form['command'], request.form.get('args', '{}'))
    return jsonify({'response': command.execute()})


if __name__ == '__main__':
    memory = LocalMemory()
    memory.load()
    load_core_commands()
    app.run(debug=True)
