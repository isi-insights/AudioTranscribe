import os
import tempfile
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import openai
from werkzeug.utils import secure_filename
from flask_dropzone import Dropzone

app = Flask(__name__)

# Configure Dropzone for audio uploads
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'audio'
app.config['DROPZONE_MAX_FILE_SIZE'] = 50  # in MB
app.config['DROPZONE_TIMEOUT'] = 120000    # in milliseconds

dropzone = Dropzone(app)

# Load secret key and OpenAI API key from environment
app.secret_key = os.getenv("SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("SECRET_KEY is not set in environment")

openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY is not set in environment")

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
