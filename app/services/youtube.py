import requests
from app.core.config import settings

BASE_URL = "https://www.googleapis.com/youtube/v3"


def fetch_channel_by_search(query: str):
    url = f"{BASE_URL}/search"

    params = {
        "part": "snippet",
        "q": query,
        "type": "channel",
        "key": settings.YOUTUBE_API_KEY,
        "maxResults": 1
    }

    response = requests.get(url, params=params)
    data = response.json()

    if not data.get("items"):
        return None

    item = data["items"][0]

    return {
        "title": item["snippet"]["title"],
        "description": item["snippet"]["description"],
        "channel_id": item["snippet"]["channelId"]
    }


def fetch_videos_by_channel(channel_id: str):
    url = f"{BASE_URL}/search"

    params = {
        "part": "snippet",
        "channelId": channel_id,
        "type": "video",
        "order": "date",
        "maxResults": 5,
        "key": settings.YOUTUBE_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    videos = []

    for item in data.get("items", []):
        videos.append({
            "title": item["snippet"]["title"],
            "description": item["snippet"]["description"],
            "video_id": item["id"]["videoId"]
        })

    return videos