from flask import Flask
from flask_socketio import SocketIO, send, emit

from datetime import datetime 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(data):
    role = data.get('role')  # 'user' или 'admin'
    message = data.get('message')
    send({
        'role': role,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, port=5000)