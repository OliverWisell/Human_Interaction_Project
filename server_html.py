from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room


# Flask app with SocketIO for real-time communication
app = Flask(__name__)
socketio = SocketIO(app)

clients = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@socketio.on('join')
def handle_join(data):
    name = data.get('name')
    clients[request.sid] = name
    print(f"{name } joined with session ID {request.sid}")
    emit('player_joined', {'name': name }, broadcast=True)


@socketio.on('start')
def handle_start():
    print("Game started")
    emit('start_question', broadcast=True)

@socketio.on('answer')
def handle_answer(data):
    name = clients.get(request.sid, 'Unknown')
    choice = data.get('choice')
    print(f"{name} answered: {choice}")
   

@socketio.on('disconnect')
def handle_disconnect():
    name = clients.pop(request.sid, 'Okänd')
    print(f"{name} disconnected")

if __name__ == '__main__':
    #socketio.run(app, host='0.0.0.0', port=50001, debug=True)
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
