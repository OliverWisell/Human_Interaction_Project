from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
from classes import Stats, Agent  # Assuming classes.py contains the Agent and Stats classes


# Flask app with SocketIO for real-time communication
app = Flask(__name__)
socketio = SocketIO(app)

clients = {}  
agent_register = Stats()  # Dictionary to keep track of agents and their names
#choices = {}
#vote_counter = {
#    "Yes": 0,
#    "No": 0
#}
#clients = {}
question_text = "Kommer du gå till baren denna vecka?"

@app.route('/')
def index():
    return render_template('el_farol.html')

@app.route('/admin')
def admin():
    agents_data = [{'name': agent.name, 'results': agent.result} for agent in agent_register.agents]
    group_data = agent_register.previous_results
    return render_template('admin.html', agents=agents_data, group_data=group_data)


@socketio.on('join')
def handle_join(data):
    print("🔥 Fick join på servern!", data)
    global num_players
    name = data.get('name')
    sid = request.sid
    clients[sid] = name

    agent = Agent(name, user=sid)
    agent_register.add_agent(agent)
    
    print(f"{name} joined with sid {sid}")

    # Notify client to enter waiting view
    socketio.emit("joined_waiting", to=sid)
    socketio.emit("num_players", {"count": agent_register.total})
    # Optionally notify admin or other clients
    socketio.emit("player_joined", {"name": name})



@socketio.on('start')
def handle_start():
    #global vote_counter, choices
    #choices = {}
    #vote_counter["Yes"] = 0
    #vote_counter["No"] = 0
    # Broadcasta nollad status till admin
    # Skicka startmeddelande till alla spelare
    socketio.emit('start_question', {"question": question_text})
    #socketio.emit("vote_update", vote_counter)
    
@socketio.on('answer')
def handle_answer(data):
    choice = data.get('choice')
    sid = request.sid
    name = clients.get(sid, 'Unknown')
    print(f"{name} answered: {choice}")
    
    agent = agent_register.search_agent(name)
    if agent:
        agent.add_result(1 if choice == "Yes" else 0)

    # 🧮 Uppdatera räkning
    yes_count = sum(1 for a in agent_register.agents if a.past_result() == 1)
    no_count = sum(1 for a in agent_register.agents if a.past_result() == 0)

    socketio.emit("vote_update", {"Yes": yes_count, "No": no_count})


    #if sid in choices:
    #    return

    #if choice in vote_counter:
    #    vote_counter[choice] += 1
    #    choices[sid] = choice
    #    socketio.emit('vote_update', vote_counter)
    #socketio.emit('vote_update', vote_counter)

@socketio.on('disconnect')
def handle_disconnect():
    #name = clients.pop(request.sid, 'Okänd')
    #print(f"{name} disconnected")
    sid = request.sid
    name = clients.pop(sid, None)
    if name:
        agent_register.delete_agent(name)
        print(f"{name} disconnected")

@socketio.on('show_results')
def handle_show_results():
    
    crowd_ratio = agent_register.new_result()  # 0–1

    for agent in agent_register.agents:
        last = agent.past_result()
        if last is None:
            continue
        if crowd_ratio > 0.6:
            # För trångt
            outcome = "lose" if last == 1 else "win"
        else:
            # OK att gå
            outcome = "win" if last == 1 else "lose"
        socketio.emit("result", {"outcome": outcome}, to=agent.user)
    print("Resultat skickat!")
    agents_data = [{'name': a.name, 'results': a.result} for a in agent_register.agents]
    group_data = agent_register.previous_results
    socketio.emit("update_stats", {
        "agents": agents_data,
        "group_data": group_data})

if __name__ == '__main__':
    #socketio.run(app, host='0.0.0.0', port=50001, debug=True)
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
