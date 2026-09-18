"""Point d'entree : python -m minitwist_publisher <commande>

  authorize     autorisation Google, une seule fois (le proprietaire clique)
  status        etat de la file d'attente
  upload-next   envoie la prochaine video en attente
"""

import argparse
from datetime import datetime, timezone

from . import auth, config, upload, video_queue


def cmd_authorize(_args) -> None:
    auth.authorize_interactively()
    print(f"Autorisation enregistree dans {config.TOKEN_FILE}")


def cmd_status(_args) -> None:
    for e in video_queue.load(config.QUEUE_FILE):
        extra = f" -> https://youtu.be/{e['video_id']}" if e.get("video_id") else ""
        print(f"[{e['status']:<9}] {e['id']:<26} {e.get('privacy', 'private'):<8}{extra}")


def cmd_upload_next(args) -> None:
    entries = video_queue.load(config.QUEUE_FILE)
    entry = video_queue.next_pending(entries)
    if entry is None:
        print("Rien a envoyer : aucune video en attente.")
        return

    print(f"Video : {entry['id']} ({entry['file']}) | {entry.get('privacy', 'private')}")
    if args.dry_run:
        print("Simulation : rien n'est envoye.")
        return

    video_id = upload.upload(auth.load(), entry, config.VIDEOS_DIR)
    entry.update(status="uploaded", video_id=video_id,
                 uploaded_at=datetime.now(timezone.utc).isoformat(timespec="seconds"))
    # Sauvegarde immediate : si la suite plante, on ne renverra pas la meme video.
    video_queue.save(config.QUEUE_FILE, entries)
    print(f"Envoyee : https://youtu.be/{video_id}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="minitwist_publisher")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("authorize").set_defaults(func=cmd_authorize)
    sub.add_parser("status").set_defaults(func=cmd_status)
    up = sub.add_parser("upload-next")
    up.add_argument("--dry-run", action="store_true", help="montre la video choisie sans l'envoyer")
    up.set_defaults(func=cmd_upload_next)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
