from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

yes_count = 0
no_count = 0
connected_users = 0
admin_sid = None  # Store the admin socket ID

@app.route('/')
@app.route('/start')
def start_screen():
    return render_template('start_screen.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/choice', methods=['POST'])
def choice():
    global yes_count, no_count
    data = request.get_json()
    if data['choice'] == 'yes':
        yes_count += 1
    elif data['choice'] == 'no':
        no_count += 1
    send_counts()
    return '', 204

@socketio.on('connect')
def on_connect():
    global connected_users
    connected_users += 1
    send_counts()

@socketio.on('disconnect')
def on_disconnect():
    global connected_users
    connected_users = max(0, connected_users - 1)
    send_counts()

@socketio.on('admin_view')
def register_admin():
    global admin_sid
    admin_sid = request.sid
    send_counts()

def send_counts():
    socketio.emit('counts', {
        'yes': yes_count,
        'no': no_count,
        'users': connected_users
    })

@socketio.on('join')
def handle_join(data):
    print(f"{data['name']} joined")
    emit('welcome', {'msg': f"Hej {data['name']}!"}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
