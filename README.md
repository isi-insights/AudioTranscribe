# AudioTranscribe

Simple Flask application for transcribing audio files with OpenAI Whisper API.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Export your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=your-key-here
   ```
3. Run the application:
   ```bash
   python app.py
   ```

Open `http://localhost:5000` in your browser to upload an audio file and download the transcription.
