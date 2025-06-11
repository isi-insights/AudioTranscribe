import os
import tempfile

from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import openai
import configparser
from werkzeug.utils import secure_filename

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "config.ini"))

app = Flask(__name__)

# Configure Dropzone for audio uploads
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'audio'
app.config['DROPZONE_MAX_FILE_SIZE'] = 50  # in MB
app.config['DROPZONE_TIMEOUT'] = 120000    # in milliseconds

from flask_dropzone import Dropzone
dropzone = Dropzone(app)
app.secret_key = os.getenv("SECRET_KEY", config["flask"]["secret_key"])

openai.api_key = os.getenv("OPENAI_API_KEY", config["openai"]["api_key"])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    audio_file = request.files.get("audio_file")
    if not audio_file:
        flash("No file uploaded")
        return redirect(url_for("index"))

    filename = secure_filename(audio_file.filename)
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp:
        audio_path = tmp.name
        audio_file.save(audio_path)

    try:
        with open(audio_path, "rb") as f:
            transcript = openai.audio.transcriptions.create(
                file=f,
                model="whisper-1"
            )
        text = transcript.text
    except Exception as exc:
        flash(f"Transcription failed: {exc}")
        os.remove(audio_path)
        return redirect(url_for("index"))

    os.remove(audio_path)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as tf:
        tf.write(text)
        tf.flush()
        transcript_path = tf.name

    return send_file(transcript_path, as_attachment=True,
                     download_name="transcript.txt", mimetype="text/plain")

if __name__ == "__main__":
    app.run(debug=True)
