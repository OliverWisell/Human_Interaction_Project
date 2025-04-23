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
question_text = "Kommer du gå till baren denna vecka?"

@app.route('/')
def index():
    return render_template('el_farol.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

num_players = 0
@socketio.on('join')
def handle_join(data):
    print("🔥 Fick join på servern!", data)
    global num_players
    name = data.get('name')
    sid = request.sid
    clients[sid] = name
    num_players += 1
    print(f"{name} joined with sid {sid}")

    # Notify client to enter waiting view
    socketio.emit("joined_waiting", to=sid)
    socketio.emit("num_players", {"count": num_players})
    # Optionally notify admin or other clients
    socketio.emit("player_joined", {"name": name})



@socketio.on('start')
def handle_start():
    global vote_counter, choices
    choices = {}
    vote_counter["Yes"] = 0
    vote_counter["No"] = 0
    # Broadcasta nollad status till admin
    # Skicka startmeddelande till alla spelare
    socketio.emit('start_question', {"question": question_text})
    socketio.emit("vote_update", vote_counter)
    
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
        socketio.emit('vote_update', vote_counter)
    socketio.emit('vote_update', vote_counter)

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
        if yes_percent > 0.6:
        # Baren var FÖR full (trångt)
            if choice == "Yes":
                outcome = "lose"   # Gick till baren → ångrade sig
            else:
                outcome = "win"    # Stannade hemma → nöjd
        else:
            # Baren var OK
            if choice == "Yes":
                outcome = "win"    # Gick till baren → hade kul
            else:
                outcome = "lose"   # Stannade hemma → FOMO
        socketio.emit("result", {"outcome": outcome}, to=sid)

    print("Resultat skickat!")

if __name__ == '__main__':
    #socketio.run(app, host='0.0.0.0', port=50001, debug=True)
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
