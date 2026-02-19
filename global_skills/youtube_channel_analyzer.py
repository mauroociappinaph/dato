"""
Channel Analyzer - Resumir contenido de un canal de YouTube
"""

import os
import requests
from typing import Dict, List, Optional
from src.helpers import get_env_var

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "AIzaSyArrOoDFICLAQ3kW-vpjFyNoogRk-cNWOU")
BASE_URL = "https://www.googleapis.com/youtube/v3"


def search_channel(query: str) -> Optional[Dict]:
    """Busca un canal por nombre"""
    url = f"{BASE_URL}/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "channel",
        "maxResults": 5,
        "key": YOUTUBE_API_KEY
    }
    resp = requests.get(url, params=params, timeout=10).json()
    items = resp.get("items", [])
    if items:
        return items[0]
    return None


def get_channel_details(channel_id: str) -> Dict:
    """Obtiene detalles del canal"""
    url = f"{BASE_URL}/channels"
    params = {"part": "snippet,statistics,contentDetails", "id": channel_id, "key": YOUTUBE_API_KEY}
    resp = requests.get(url, params=params, timeout=10).json()
    return resp.get("items", [{}])[0]


def get_latest_videos(channel_id: str, max_videos: int = 20) -> List[Dict]:
    """Obtiene últimos vídeos del canal"""
    channel = get_channel_details(channel_id)
    uploads_id = channel.get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")

    url = f"{BASE_URL}/playlistItems"
    params = {
        "part": "snippet,contentDetails",
        "playlistId": uploads_id,
        "maxResults": max_videos,
        "key": YOUTUBE_API_KEY
    }
    resp = requests.get(url, params=params, timeout=10).json()
    return resp.get("items", [])


def get_video_details(video_ids: List[str]) -> List[Dict]:
    """Obtiene estadísticas de vídeos"""
    url = f"{BASE_URL}/videos"
    params = {
        "part": "snippet,statistics",
        "id": ",".join(video_ids),
        "key": YOUTUBE_API_KEY
    }
    resp = requests.get(url, params=params, timeout=10).json()
    return resp.get("items", [])


def analyze_channel(query: str):
    """Analiza y resume un canal"""
    print(f"\n{'='*60}")
    print(f"📺 ANALIZANDO CANAL: {query}")
    print(f"{'='*60}\n")

    channel = search_channel(query)
    if not channel:
        print(f"❌ No se encontró el canal: {query}")
        return

    channel_id = channel["id"]["channelId"]
    snippet = channel["snippet"]

    details = get_channel_details(channel_id)
    stats = details.get("statistics", {})

    print(f"📛 Canal: {snippet['title']}")
    print(f"🔗 Link: https://youtube.com/channel/{channel_id}")
    print(f"📝 Descripción:\n{snippet.get('description', 'N/A')[:400]}...")
    print(f"\n📊 Estadísticas:")
    print(f"   Suscriptores: {int(stats.get('subscriberCount', 0)):,}")
    print(f"   Vídeos: {int(stats.get('videoCount', 0)):,}")
    print(f"   Vistas totales: {int(stats.get('viewCount', 0)):,}")

    videos = get_latest_videos(channel_id, max_videos=20)

    titles = [v["snippet"]["title"] for v in videos]
    video_ids = [v["contentDetails"]["videoId"] for v in videos]

    print(f"\n🎥 ÚLTIMOS VÍDEOS ({len(titles)}):")
    for i, title in enumerate(titles[:10], 1):
        print(f"   {i}. {title[:65]}")

    video_stats = get_video_details(video_ids[:10])
    total_views = sum(int(v["statistics"].get("viewCount", 0)) for v in video_stats)
    total_likes = sum(int(v["statistics"].get("likeCount", 0)) for v in video_stats)

    print(f"\n📈 Engagement (últimos 10 vídeos):")
    print(f"   Vistas totales: {total_views:,}")
    print(f"   Likes totales: {total_likes:,}")

    print(f"\n🔍 ANÁLISIS DE CONTENIDO:")
    analyze_content(titles)


def analyze_content(titles: List[str]):
    """Analiza qué enseña el canal basándose en los títulos"""
    keywords = {
        "Python": ["python", "django", "flask", "fastapi", "pandas"],
        "JavaScript/Node": ["javascript", "js", "node", "react", "vue", "express", "typescript"],
        "Desarrollo Web": ["html", "css", "web", "frontend", "backend", "api", "rest", "http"],
        "Bases de Datos": ["sql", "mysql", "postgres", "mongodb", "database", "sqlite", "firebase"],
        "DevOps": ["docker", "git", "github", "deploy", "cloud", "aws", "linux", "ubuntu", "terminal"],
        "Mobile": ["android", "ios", "flutter", "react native", "kotlin", "swift", "app"],
        "Machine Learning/AI": ["machine learning", "ml", "ia", "ai", "inteligencia", "tensorflow", "pytorch", "chatgpt"],
        "C#/.NET": ["c#", "csharp", ".net", "asp.net", "visual studio"],
        "Java": ["java", "spring", "maven", "jdbc"],
        "C/C++": ["c++", "cpp", "arduino"],
        "Ruby": ["ruby", "rails"],
        "PHP": ["php", "laravel", "wordpress"],
        "General": ["tutorial", "curso", "aprende", "learn", "desde cero", "principiantes", "programación"]
    }

    results = {}
    text = " ".join(titles).lower()

    for category, terms in keywords.items():
        count = sum(1 for term in terms if term in text)
        if count > 0:
            results[category] = count

    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    print("   Categorías detectadas:")
    for cat, count in sorted_results:
        bar = "█" * min(count, 10)
        print(f"   {cat}: {bar} ({count})")

    print("\n📋 RESUMEN FINAL:")
    if sorted_results:
        top_3 = sorted_results[:3]
        cats = ", ".join([c[0] for c in top_3])
        print(f"   🎯 Especialidades: {cats}")
        print(f"   👥 Dirigido a: Principiantes y desarrolladores que buscan")


if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "CodigoEspinoza"
    analyze_channel(query)
