#!/usr/bin/env python3
from flask import Flask, request, jsonify
import subprocess, shutil

app = Flask(__name__)

@app.after_request
def cors(r):
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r

def find_bin(names, fallback):
    for name in names:
        path = shutil.which(name)
        if path:
            return path
    return fallback

@app.route("/play")
def play():
    url = request.args.get("url", "")
    player = request.args.get("player", "vlc")
    if not url:
        return jsonify({"ok": False, "error": "No URL provided"})

    if player == "ace":
        bin_path = find_bin(["acestreamplayer"], "/snap/bin/acestreamplayer")
        if "ace/getstream?id=" in url:
            hash_id = url.split("ace/getstream?id=")[-1].split("&")[0]
            ace_url = "acestream://" + hash_id
        elif url.startswith("acestream://"):
            ace_url = url
        else:
            ace_url = url
        cmd = [bin_path, ace_url]
    else:
        bin_path = find_bin(["vlc"], "/snap/bin/vlc")
        cmd = [bin_path, "--no-video-title-show", url]

    try:
        subprocess.Popen(cmd)
        return jsonify({"ok": True, "cmd": cmd[0], "url": cmd[1]})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

if __name__ == "__main__":
    vlc = find_bin(["vlc"], "/snap/bin/vlc")
    ace = find_bin(["acestreamplayer"], "/snap/bin/acestreamplayer")
    print(f"Server running on http://127.0.0.1:5566")
    print(f"  VLC:              {vlc}")
    print(f"  Acestream Player: {ace}")
    app.run(host="127.0.0.1", port=5566)
