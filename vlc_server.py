#!/usr/bin/env python3
from flask import Flask, request, jsonify
import subprocess, shutil

app = Flask(__name__)

@app.after_request
def cors(r):
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r

# Rutas explícitas — /usr/bin/vlc tiene prioridad sobre snap
VLC_PATH = "/usr/bin/vlc"
ACE_PATH = "/snap/bin/acestreamplayer"

@app.route("/play")
def play():
    url = request.args.get("url", "")
    player = request.args.get("player", "vlc")
    if not url:
        return jsonify({"ok": False, "error": "No URL provided"})

    if player == "ace":
        if "ace/getstream?id=" in url:
            hash_id = url.split("ace/getstream?id=")[-1].split("&")[0]
            target_url = "acestream://" + hash_id
        else:
            target_url = url
        cmd = [ACE_PATH, target_url]
    else:
        cmd = [VLC_PATH, "--no-video-title-show", url]

    try:
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return jsonify({"ok": True, "player": cmd[0], "url": cmd[1]})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

if __name__ == "__main__":
    print(f"Server running on http://127.0.0.1:5566")
    print(f"  VLC:              {VLC_PATH}")
    print(f"  Acestream Player: {ACE_PATH}")
    app.run(host="127.0.0.1", port=5566)
