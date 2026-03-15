#!/usr/bin/env python3
"""
Mini servidor Flask local para lanzar VLC desde la web app.
Ejecutar: python vlc_server.py
"""
from flask import Flask, request, jsonify
import subprocess, shutil

app = Flask(__name__)

@app.after_request
def cors(r):
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r

@app.route("/play")
def play():
    url = request.args.get("url", "")
    if not url:
        return jsonify({"ok": False, "error": "No URL provided"})
    vlc = shutil.which("vlc") or "/usr/bin/vlc"
    try:
        subprocess.Popen([vlc, "--no-video-title-show", url])
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

if __name__ == "__main__":
    print("VLC server running on http://127.0.0.1:5566")
    app.run(host="127.0.0.1", port=5566)