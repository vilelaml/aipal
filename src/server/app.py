from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/command', methods=['GET'])
def list_commands():
    return jsonify({'commands': ['show_memories']})


@app.route('/command', methods=['POST'])
def process_command():
    command = request.form['command']
    args = request.form.get('args', '')
    return jsonify({'message': f'Hello, {command}!'})


if __name__ == '__main__':
    app.run(debug=True)
