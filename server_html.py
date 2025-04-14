from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Global counters
yes_count = 0
no_count = 0

@app.route('/')
@app.route('/start')
def start_screen():
    return render_template('start_screen.html', yes=yes_count, no=no_count)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/choice', methods=['POST'])
def choice():
    global yes_count, no_count
    data = request.get_json()
    if data['choice'] == 'yes':
        yes_count += 1
    elif data['choice'] == 'no':
        no_count += 1
    return '', 204

@socketio.on('join')
def handle_join(data):
    print(f"{data['name']} joined")
    emit('welcome', {'msg': f"Hej {data['name']}!"}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
