import requests
import json
from backend.app.utils.src.config import API_TOKEN

def fetch_transcript(video_id: str):
    headers = {
        "Authorization": f"Basic {API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(
        "https://www.youtube-transcript.io/api/transcripts",
        headers=headers,
        json={"ids": [video_id]}
    )
    if response.status_code != 200:
        raise Exception(f"Failed to fetch transcript: {response.text}")
    return response.json()
