"""Emplacements utilises par l'agent.

Ce depot est PUBLIC : aucun secret n'y vit. Les identifiants Google et le
jeton d'autorisation restent dans un dossier local a part, hors de tout depot
Git, qu'on peut deplacer avec la variable MINITWIST_SECRETS_DIR.
"""

import os
from pathlib import Path

HOME = Path.home()
REPO_ROOT = Path(__file__).resolve().parents[2]

SECRETS_DIR = Path(os.environ.get("MINITWIST_SECRETS_DIR", HOME / "Documents" / "minitwist-secrets"))
CLIENT_SECRET_FILE = SECRETS_DIR / "client_secret.json"
TOKEN_FILE = SECRETS_DIR / "token.json"

VIDEOS_DIR = Path(os.environ.get(
    "MINITWIST_VIDEOS_DIR", HOME / "Documents" / "MoneyPrinterTurbo" / "minitwist-exports"
))
QUEUE_FILE = REPO_ROOT / "config" / "queue.json"

# Seul droit demande : envoyer des videos. Pas de lecture de la chaine, des
# commentaires ou des statistiques. C'est aussi ce qu'annonce la politique de
# confidentialite publiee, et ce que l'audit YouTube verifiera.
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

YOUTUBE_CATEGORY_ENTERTAINMENT = "24"
