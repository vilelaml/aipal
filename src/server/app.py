from flask import Flask, request, jsonify

from src.server.command.command import Command
from src.server.config.config import Config
from src.server.memory import *

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
    config = Config()
    config.initialize()
    app.run(debug=True)
