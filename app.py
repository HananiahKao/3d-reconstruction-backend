from flask import Flask, request, jsonify, send_from_directory
import os
import uuid
from processor import process_video_to_mesh
from usdz_exporter import export_usdz

app = Flask(__name__)
UPLOAD_DIR = 'uploads'
OUTPUT_DIR = 'outputs'

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_video():
    video = request.files.get('video')
    if not video:
        return jsonify({"error": "No video uploaded"}), 400

    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(UPLOAD_DIR, filename)
    video.save(filepath)

    # Generate mesh
    mesh_path = process_video_to_mesh(filepath)

    # Convert to USDZ
    usdz_path = export_usdz(mesh_path, OUTPUT_DIR)

    return jsonify({"usdz_url": f"/download/{os.path.basename(usdz_path)}"})

@app.route('/download/<filename>', methods=['GET'])
def download_usdz(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
