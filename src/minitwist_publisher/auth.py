"""Autorisation Google (OAuth).

La premiere autorisation est faite une seule fois, par le proprietaire de la
chaine, dans son navigateur : il clique lui-meme sur "Autoriser". L'agent ne
voit jamais son mot de passe. Google renvoie un jeton de rafraichissement,
stocke dans le dossier des secrets, que l'agent reutilise ensuite seul.
"""

import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from . import config


def authorize_interactively() -> Credentials:
    """Ouvre le navigateur pour que le proprietaire autorise l'agent."""
    if not config.CLIENT_SECRET_FILE.is_file():
        raise SystemExit(f"Identifiant Google introuvable : {config.CLIENT_SECRET_FILE}")

    flow = InstalledAppFlow.from_client_secrets_file(str(config.CLIENT_SECRET_FILE), config.SCOPES)
    # access_type=offline + prompt=consent : garantit un jeton de
    # rafraichissement, meme si une autorisation a deja ete donnee avant.
    creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")
    save(creds)
    return creds


def save(creds: Credentials) -> None:
    config.SECRETS_DIR.mkdir(parents=True, exist_ok=True)
    config.TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")


def load() -> Credentials:
    """Recharge le jeton enregistre et le renouvelle s'il a expire."""
    if not config.TOKEN_FILE.is_file():
        raise SystemExit("Agent pas encore autorise : lance d'abord la commande 'authorize'.")

    creds = Credentials.from_authorized_user_info(
        json.loads(config.TOKEN_FILE.read_text(encoding="utf-8")), config.SCOPES
    )
    if not creds.valid:
        if not creds.refresh_token:
            raise SystemExit("Jeton sans rafraichissement : relance la commande 'authorize'.")
        creds.refresh(Request())
        save(creds)
    return creds
