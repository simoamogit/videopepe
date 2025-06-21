from flask import Flask, render_template, request, jsonify
from auth import auth
import subprocess
import os
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'  # Cambia in produzione!

# Configurazione telecamere
CAMERAS = {
    "cucina": {
        "rtsp_url": "rtsp://username:password@<phone_ip>:8080/unicast",
        "hls_url": "/hls/cucina.m3u8"
    },
    "sala": {
        "rtsp_url": "rtsp://username:password@<phone_ip2>:8080/unicast",
        "hls_url": "/hls/sala.m3u8"
    }
}

@app.route('/auth', methods=['POST'])
def authenticate_stream():
    """Autenticazione per lo streaming RTMP"""
    name = request.form.get('name')
    password = request.form.get('password')
    
    # Verifica contro lista camere configurate
    if name in CAMERAS and password == "stream_key_segreta":  # Cambia questa chiave!
        return '', 200
    return 'Accesso negato', 401

@app.route('/start_stream/<camera_name>')
@auth.login_required
def start_stream(camera_name):
    """Avvia FFmpeg per conversione RTSP->RTMP"""
    if camera_name not in CAMERAS:
        return jsonify({"error": "Camera non trovata"}), 404
    
    cmd = [
        "ffmpeg",
        "-rtsp_transport", "tcp",
        "-i", CAMERAS[camera_name]["rtsp_url"],
        "-c:v", "copy",
        "-c:a", "aac",
        "-f", "flv",
        f"rtmp://localhost:1935/live/{camera_name}"
    ]
    
    # Avvia in background
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return jsonify({"status": "Stream avviato"})

@app.route('/')
@auth.login_required
def dashboard():
    return render_template('dashboard.html', cameras=list(CAMERAS.keys()))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
