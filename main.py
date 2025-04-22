from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = Flask(__name__)
socketio = SocketIO(app)

class VoteHistory:
    def __init__(self, results=None):
        self.results = results if results is not None else []

    def add_vote(self, vote):
        if vote in [0, 1]:
            self.results.append(vote)

    def generate_plot_base64(self):
        x = list(range(1, len(self.results) + 1))
        y = self.results

        plt.figure(figsize=(8, 4))
        plt.plot(x, y, marker='o', color='black', linewidth=3)
        plt.ylim(-0.1, 1.1)
        plt.yticks([0, 1], ['No', 'Yes'])
        plt.xlabel("Vote #")
        plt.ylabel("Choice")
        plt.title("Vote History")

        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close()

        return img_base64

history = VoteHistory([])

@app.route('/')
def index():
    img_base64 = history.generate_plot_base64()
    return render_template('data.html', plot_data=img_base64)

@socketio.on('new_vote')
def handle_new_vote(vote):
    history.add_vote(int(vote))
    updated_plot = history.generate_plot_base64()
    emit('update_plot', {'plot': updated_plot, 'count': len(history.results)}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
