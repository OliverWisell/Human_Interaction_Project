from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room


# Flask app with SocketIO for real-time communication
app = Flask(__name__)
socketio = SocketIO(app)

clients = {}  
choices = {}
vote_counter = {
    "Yes": 0,
    "No": 0
}
clients = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

num_players = 0
@socketio.on('join')
def handle_join(data):
    name = data.get('name')
    clients[request.sid] = name
    print(f"{name } joined with session ID {request.sid}")
    global num_players
    num_players += 1
    emit('player_joined', {'name': name }, broadcast=True)
    emit("num_players", {"count": num_players}, to=request.sid)


@socketio.on('start')
def handle_start():
    print("Game started")
    vote_counter["Yes"] = 0
    vote_counter["No"] = 0
    # Broadcasta nollad status till admin
    emit("vote_update", vote_counter, broadcast=True)
    # Skicka startmeddelande till alla spelare
    emit('start_question', broadcast=True)

@socketio.on('answer')
def handle_answer(data):
    choice = data.get('choice')
    sid = request.sid
    name = clients.get(sid, 'Unknown')
    print(f"{name} answered: {choice}")
    
    if sid in choices:
        return

    if choice in vote_counter:
        vote_counter[choice] += 1
        choices[sid] = choice
        emit('vote_update', vote_counter, broadcast=True)
    emit('vote_update', vote_counter, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    name = clients.pop(request.sid, 'Okänd')
    print(f"{name} disconnected")

@socketio.on('show_results')
def handle_show_results():
    total_votes = vote_counter["Yes"] + vote_counter["No"]
    if total_votes == 0:
        return

    yes_percent = vote_counter["Yes"] / total_votes

    for sid, choice in choices.items():
        if yes_percent >= 0.6 and choice == "Yes":
            socketio.emit("result", {"outcome": "win"}, to=sid)
        elif yes_percent < 0.6 and choice == "No":
            socketio.emit("result", {"outcome": "win"}, to=sid)
        else:
            socketio.emit("result", {"outcome": "lose"}, to=sid)

    print("Resultat skickat!")

if __name__ == '__main__':
    #socketio.run(app, host='0.0.0.0', port=50001, debug=True)
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
