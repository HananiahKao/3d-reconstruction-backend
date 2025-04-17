from flask import Flask, request, jsonify, send_from_directory, render_template
import os
from usdz_exporter import export_usdz

app = Flask(__name__, template_folder="templates", static_folder="static")
UPLOAD_DIR = "uploads"
EXPORT_DIR = "exports"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        return jsonify({"error": "No video uploaded"}), 400

    video = request.files["video"]
    video_path = os.path.join(UPLOAD_DIR, video.filename)
    video.save(video_path)

    try:
        usdz_path = export_usdz(video_path, EXPORT_DIR)
        download_url = f"/exports/{os.path.basename(usdz_path)}"
        return jsonify({"download_url": download_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/exports/<filename>")
def download_file(filename):
    return send_from_directory(EXPORT_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
    
