# AudioTranscribe

Simple Flask application for transcribing audio files with OpenAI Whisper API.

## Setup

1. Create a `.env` file in the project root (this file is gitignored):
   ```ini
   OPENAI_API_KEY=your-openai-api-key
   SECRET_KEY=your-flask-secret-key
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open `http://localhost:5000` in your browser to upload an audio file and download the transcription.

## Environment Variables

- **OPENAI_API_KEY**: Your OpenAI API key for Whisper.
- **SECRET_KEY**: Flask secret key for session management.

The application uses `python-dotenv` to load these variables from `.env` at startup.
