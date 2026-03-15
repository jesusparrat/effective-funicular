#!/usr/bin/env python3
"""
Mini servidor Flask local para lanzar VLC / Acestream Player desde la web app.
Ejecutar: python vlc_server.py
"""
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
    player = request.args.get("player", "vlc")  # "vlc" o "ace"
    if not url:
        return jsonify({"ok": False, "error": "No URL provided"})

    if player == "ace":
        bin_path = find_bin(["acestreamplayer"], "/snap/bin/acestreamplayer")
        # Acestream Player acepta la URL http del engine directamente
        cmd = [bin_path, url]
    else:
        bin_path = find_bin(["vlc"], "/snap/bin/vlc")
        cmd = [bin_path, "--no-video-title-show", url]

    try:
        subprocess.Popen(cmd)
        return jsonify({"ok": True, "cmd": cmd[0]})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

if __name__ == "__main__":
    print("Server running on http://127.0.0.1:5566")
    print(f"  VLC:              {find_bin(['vlc'], '/snap/bin/vlc')}")
    print(f"  Acestream Player: {find_bin(['acestreamplayer'], '/snap/bin/acestreamplayer')}")
    app.run(host="127.0.0.1", port=5566)