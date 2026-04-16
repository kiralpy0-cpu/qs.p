from flask import Flask, send_file, request
from flask_socketio import SocketIO
from PIL import Image
from datetime import datetime
import requests
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
img.save('tracker.png')


def geo(ip):
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json")
        return r.json()
    except:
        return {}

@app.route('/tracker')
def tracker():
    ip = request.remote_addr
    ua = request.headers.get("User-Agent")
    time = datetime.now().strftime("%H:%M:%S")

    data = geo(ip)

    log = {
        "time": time,
        "ip": ip,
        "city": data.get("city"),
        "country": data.get("country"),
        "ua": ua
    }

    print(log)
    socketio.emit("new_log", log)

    return send_file("tracker.png", mimetype="image/png")


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)
