# YouTube-Live-Chat-Summarizer
Real-time AI-powered browser extension for YouTube live chat summarization using fine-tuned Google Gemini 2.0 Flash

## Features
- Captures live chat messages from YouTube streams
- Sends messages to a FastAPI backend over WebSocket
- Uses Gemini 2.0 Flash model API for AI-generated summarization in real-time
- Displays summaries in a popup UI at regular intervals
- Compatible with Firefox browser add-ons

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Requirements include:
- `fastapi`
- `uvicorn`
- `httpx`
- `google-generativeai`
- `python-dotenv`
- `pytchat`

### 2. Configure Gemini API Key

In `config.py`, add your [API key](https://aistudio.google.com/apikey):

```python
gemini_api_key  = "enter-key"
```

## Running the Backend

Start the FastAPI server:

```bash
uvicorn app:app --reload --port 5000
```

This opens a WebSocket server at: `ws://localhost:5000/ws?video_id=YOUR_VIDEO_ID`

## Installing the Firefox Extension

1. Open Firefox and go to `about:debugging#/runtime/this-firefox`
2. Click **“Load Temporary Add-on”**
3. Select `manifest.json` from this project

## How It Works

1. `content.js` captures live chat from YouTube.
2. It sends chat messages to the backend via WebSocket.
3. Messages are grouped and stored using `chat_handler.py`.
4. `summarizer.py` periodically sends collected messages to Gemini API.
5. Summary is displayed in the extension popup (`popup.html`).

## Contributing
If you'd like to add new features, improve the extension, or fix bugs then feel free to fork the repo, create a branch, and open a pull request.
