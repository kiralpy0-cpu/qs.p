from flask import Flask, send_file, request, jsonify
from PIL import Image
from datetime import datetime
import requests

app = Flask(__name__)

# stockage simple en mémoire
logs = []

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

    logs.append(log)
    print(log)

    return send_file("tracker.png", mimetype="image/png")


# 📡 API pour dashboard (polling)
@app.route('/logs')
def get_logs():
    return jsonify(logs)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
