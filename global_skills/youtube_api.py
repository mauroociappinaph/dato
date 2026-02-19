"""
YouTube Data API v3 Utility
"""

import os
import requests
from typing import Dict, List, Optional
from dataclasses import dataclass
from src.helpers import get_env_var


YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "AIzaSyArrOoDFICLAQ3kW-vpjFyNoogRk-cNWOU")
BASE_URL = "https://www.googleapis.com/youtube/v3"


@dataclass
class Video:
    id: str
    title: str
    description: str
    channel_title: str
    published_at: str
    view_count: int
    like_count: int
    comment_count: int
    thumbnail_url: str


@dataclass
class Channel:
    id: str
    title: str
    description: str
    subscriber_count: int
    video_count: int
    thumbnail_url: str


class YouTubeAPI:
    def __init__(self, api_key: str = YOUTUBE_API_KEY):
        self.api_key = api_key
        self.session = requests.Session()

    def _request(self, endpoint: str, params: Dict) -> Optional[Dict]:
        params["key"] = self.api_key
        response = self.session.get(f"{BASE_URL}/{endpoint}", params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def search_videos(
        self,
        query: str,
        max_results: int = 10,
        order: str = "relevance"
    ) -> List[Video]:
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": max_results,
            "order": order
        }
        data = self._request("search", params)
        if not data:
            return []

        videos = []
        for item in data.get("items", []):
            vid = item["id"]["videoId"]
            snippet = item["snippet"]
            videos.append(Video(
                id=vid,
                title=snippet["title"],
                description=snippet["description"],
                channel_title=snippet["channelTitle"],
                published_at=snippet["publishedAt"],
                view_count=0,
                like_count=0,
                comment_count=0,
                thumbnail_url=snippet["thumbnails"]["medium"]["url"]
            ))
        return videos

    def get_video_details(self, video_id: str) -> Optional[Video]:
        params = {
            "part": "snippet,statistics",
            "id": video_id
        }
        data = self._request("videos", params)
        if not data or not data.get("items"):
            return None

        item = data["items"][0]
        stats = item.get("statistics", {})
        snippet = item["snippet"]

        return Video(
            id=video_id,
            title=snippet["title"],
            description=snippet["description"],
            channel_title=snippet["channelTitle"],
            published_at=snippet["publishedAt"],
            view_count=int(stats.get("viewCount", 0)),
            like_count=int(stats.get("likeCount", 0)),
            comment_count=int(stats.get("commentCount", 0)),
            thumbnail_url=snippet["thumbnails"]["medium"]["url"]
        )

    def get_channel(self, channel_id: str) -> Optional[Channel]:
        params = {
            "part": "snippet,statistics",
            "id": channel_id
        }
        data = self._request("channels", params)
        if not data or not data.get("items"):
            return None

        item = data["items"][0]
        stats = item.get("statistics", {})
        snippet = item["snippet"]

        return Channel(
            id=channel_id,
            title=snippet["title"],
            description=snippet["description"],
            subscriber_count=int(stats.get("subscriberCount", 0)),
            video_count=int(stats.get("videoCount", 0)),
            thumbnail_url=snippet["thumbnails"]["medium"]["url"]
        )

    def get_popular_videos(self, region_code: str = "US", max_results: int = 10) -> List[Video]:
        params = {
            "part": "snippet,statistics",
            "chart": "mostPopular",
            "regionCode": region_code,
            "maxResults": max_results
        }
        data = self._request("videos", params)
        if not data:
            return []

        videos = []
        for item in data.get("items", []):
            stats = item.get("statistics", {})
            snippet = item["snippet"]

            videos.append(Video(
                id=item["id"],
                title=snippet["title"],
                description=snippet["description"],
                channel_title=snippet["channelTitle"],
                published_at=snippet["publishedAt"],
                view_count=int(stats.get("viewCount", 0)),
                like_count=int(stats.get("likeCount", 0)),
                comment_count=int(stats.get("commentCount", 0)),
                thumbnail_url=snippet["thumbnails"]["medium"]["url"]
            ))
        return videos


if __name__ == "__main__":
    yt = YouTubeAPI()

    print("=== Vídeos Populares (US) ===")
    for video in yt.get_popular_videos(region_code="US", max_results=5):
        print(f"  {video.title[:50]}... ({video.view_count:,} vistas)")

    print("\n=== Búsqueda: 'Python tutorials' ===")
    for video in yt.search_videos("Python tutorials", max_results=3):
        print(f"  {video.title}")
