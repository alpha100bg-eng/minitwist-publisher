"""Envoi d'une video sur YouTube (API Data v3, videos.insert)."""

from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from . import config


def build_body(entry: dict) -> dict:
    """Traduit une entree de la file en corps de requete videos.insert.

    Fonction pure, sans appel reseau : c'est elle que les tests verifient.
    """
    status = {
        "privacyStatus": entry.get("privacy", "private"),
        # "Non, elle n'est pas concue pour les enfants" : un contenu declare
        # pour enfants perd les commentaires et la publicite personnalisee.
        "selfDeclaredMadeForKids": False,
        # Voix generee par IA : on le declare, comme le demande YouTube.
        "containsSyntheticMedia": True,
    }
    if entry.get("publish_at"):
        status["publishAt"] = entry["publish_at"]

    return {
        "snippet": {
            "title": entry["title"],
            "description": entry["description"],
            "tags": entry.get("tags", []),
            "categoryId": config.YOUTUBE_CATEGORY_ENTERTAINMENT,
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en",
        },
        "status": status,
    }


def upload(creds, entry: dict, videos_dir: Path) -> str:
    """Envoie la video et renvoie son identifiant YouTube."""
    video_path = videos_dir / entry["file"]
    if not video_path.is_file():
        raise FileNotFoundError(f"Video introuvable : {video_path}")

    youtube = build("youtube", "v3", credentials=creds, cache_discovery=False)
    media = MediaFileUpload(str(video_path), mimetype="video/mp4", chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=build_body(entry), media_body=media)

    response = None
    while response is None:
        progress, response = request.next_chunk()
        if progress:
            print(f"  envoi : {int(progress.progress() * 100)} %")
    return response["id"]
