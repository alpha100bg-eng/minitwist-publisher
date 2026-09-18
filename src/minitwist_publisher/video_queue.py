"""File d'attente des videos a envoyer (config/queue.json).

Chaque entree decrit une video et son etat. La validation se fait ici, a la
frontiere du systeme : une entree invalide est refusee avant tout appel a
YouTube, plutot que de faire echouer un envoi a mi-chemin.
"""

import json
from datetime import datetime
from pathlib import Path

MAX_TITLE = 100          # limite imposee par YouTube
MAX_DESCRIPTION = 5000   # limite imposee par YouTube
MAX_TAGS_TOTAL = 500     # somme des caracteres des tags acceptee par YouTube
PRIVACY_VALUES = {"private", "unlisted", "public"}


class QueueError(ValueError):
    pass


def load(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise QueueError("queue.json doit contenir une liste de videos")
    for entry in data:
        validate(entry)
    return data


def save(path: Path, entries: list[dict]) -> None:
    path.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def validate(entry: dict) -> None:
    ident = entry.get("id", "?")
    for field in ("id", "file", "title", "description", "status"):
        if not isinstance(entry.get(field), str) or not entry[field].strip():
            raise QueueError(f"[{ident}] champ '{field}' manquant ou vide")

    if len(entry["title"]) > MAX_TITLE:
        raise QueueError(f"[{ident}] titre trop long ({len(entry['title'])} > {MAX_TITLE})")
    if len(entry["description"]) > MAX_DESCRIPTION:
        raise QueueError(f"[{ident}] description trop longue")
    # YouTube refuse les chevrons dans le titre et la description.
    for field in ("title", "description"):
        if "<" in entry[field] or ">" in entry[field]:
            raise QueueError(f"[{ident}] '<' ou '>' interdits dans '{field}'")

    tags = entry.get("tags", [])
    if not isinstance(tags, list) or not all(isinstance(t, str) for t in tags):
        raise QueueError(f"[{ident}] 'tags' doit etre une liste de textes")
    if sum(len(t) for t in tags) > MAX_TAGS_TOTAL:
        raise QueueError(f"[{ident}] tags trop longs au total")

    privacy = entry.get("privacy", "private")
    if privacy not in PRIVACY_VALUES:
        raise QueueError(f"[{ident}] 'privacy' doit valoir {sorted(PRIVACY_VALUES)}")

    publish_at = entry.get("publish_at")
    if publish_at is not None:
        try:
            parsed = datetime.fromisoformat(publish_at.replace("Z", "+00:00"))
        except (AttributeError, ValueError):
            raise QueueError(f"[{ident}] 'publish_at' doit etre une date ISO 8601") from None
        if parsed.tzinfo is None:
            raise QueueError(f"[{ident}] 'publish_at' doit preciser le fuseau (ex. +02:00)")
        # YouTube n'accepte une publication programmee que sur une video privee.
        if privacy != "private":
            raise QueueError(f"[{ident}] une video programmee doit etre 'private'")


def next_pending(entries: list[dict]) -> dict | None:
    return next((e for e in entries if e["status"] == "pending"), None)
