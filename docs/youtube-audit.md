# Dossier d'audit YouTube API — MINI TWIST Publisher

Formulaire : **YouTube API Services – Audit and Quota Extension Form**
<https://support.google.com/youtube/contact/yt_api_form>

À remplir en **anglais**. Les réponses ci-dessous sont prêtes à copier-coller.
Les champs entre `[...]` sont les seuls que tu dois compléter toi-même.

---

## Informations du projet

| Champ du formulaire | Réponse |
|---|---|
| Google Cloud Project ID | `minitwist-publisher` |
| Google Cloud Project Number | `1043539991625` |
| API client name | `MINI TWIST Publisher` |
| Contact email | `alpha100bg@gmail.com` |
| Website / home page | `https://alpha100bg-eng.github.io/minitwist-publisher/` |
| Privacy policy URL | `https://alpha100bg-eng.github.io/minitwist-publisher/privacy.html` |
| Terms of service URL | `https://alpha100bg-eng.github.io/minitwist-publisher/terms.html` |
| YouTube channel URL | `[colle ici l'adresse de ta chaîne MINI TWIST]` |
| Quota requested | `Default quota is sufficient — this is a compliance audit request, not a quota increase.` |

---

## Description de l'application

> MINI TWIST Publisher is a private, single-user tool that uploads videos to one
> YouTube channel: the MINI TWIST channel, owned by the person who operates the
> tool. It is not offered to the public and has no other users.
>
> The channel publishes short original stories written by the channel owner.
> The owner writes each story, produces the video, and reviews it before it is
> queued. The tool does not create the content: it only automates the upload and
> scheduling step that the owner would otherwise do by hand in YouTube Studio,
> so that the channel can keep a regular publishing rhythm.

## Endpoints utilisés

> The client uses exactly one endpoint: `videos.insert`.
>
> It sets the video file, title, description, tags, category, language,
> privacy status, and, when the owner schedules a video, `status.publishAt`.
> Every upload declares `status.selfDeclaredMadeForKids = false` and
> `status.containsSyntheticMedia = true`, because the narration is generated
> with a text-to-speech voice.
>
> No other endpoint is called. The client never reads channel data, comments,
> subscribers, analytics, or any other user's content.

## Autorisation des utilisateurs

> The only authorized user is the channel owner. Authorization uses the standard
> OAuth 2.0 installed-application flow: the owner signs in with Google in their
> own browser and grants consent on Google's consent screen. The application
> never sees or handles the account password.
>
> A single scope is requested: `https://www.googleapis.com/auth/youtube.upload`.
> No other scope is requested.

## Stockage et suppression des données

> The application stores the OAuth refresh token returned by Google, kept on the
> owner's own machine outside any source repository, and the video files and
> their titles and descriptions that the owner prepared before upload.
>
> No personal data about viewers or any third party is collected, stored or
> processed. The application sets no cookies and uses no analytics.
>
> The refresh token is deleted when access is revoked or when the application is
> discontinued. The owner can revoke access at any time at
> <https://security.google.com/settings/security/permissions>; once revoked, the
> application can no longer upload anything.

## Volume attendu

> One video per day at most, on a single channel. Peak traffic is one
> `videos.insert` call per day, which is far below the default 10,000 unit
> daily quota. No quota increase is requested.

## Partage des données

> No data is sold, rented or shared with third parties. Video files and their
> metadata are sent only to YouTube, which is required to upload them.

---

## Vidéo de démonstration (environ 2 minutes)

Enregistre ton écran avec l'enregistreur de Windows (**Win + Alt + R**) ou tout
autre outil, sans commentaire audio obligatoire. Montre, dans cet ordre :

1. **La page d'accueil** : `https://alpha100bg-eng.github.io/minitwist-publisher/`
   avec les liens vers la confidentialité et les conditions — 10 secondes.
2. **Le lancement de l'autorisation** : la commande, puis la page Google qui
   s'ouvre, l'écran de consentement affichant **une seule permission**
   (« mettre en ligne des vidéos YouTube »), et ton clic sur *Continuer*.
3. **La file d'attente** : la commande `status`, qui montre la vidéo en attente
   avec son titre et sa visibilité.
4. **L'envoi** : la commande `upload-next`, puis le lien renvoyé.
5. **Le résultat dans YouTube Studio** : la vidéo apparue sur la chaîne, avec
   sa visibilité, « pas conçue pour les enfants » et « contenu synthétique ».
6. **La révocation** : la page <https://myaccount.google.com/permissions>
   montrant que l'accès peut être retiré en un clic.

Téléverse cette vidéo sur ta chaîne en **non répertoriée**, et colle son lien
dans le formulaire.

---

## Avant d'envoyer — vérifie

- [ ] L'adresse de ta chaîne est bien renseignée dans le tableau ci-dessus
- [ ] Les trois pages (accueil, confidentialité, conditions) s'ouvrent
- [ ] La vidéo de démonstration est en ligne et accessible en non répertoriée
- [ ] La vidéo de test `TEST - A Suitcase...` a été supprimée de la chaîne

## Après l'envoi

Google répond en général en **quelques semaines**, parfois plus, et peut poser
des questions complémentaires. Tant que la réponse n'est pas arrivée, les
vidéos envoyées par l'agent restent **privées** : continue à les programmer
depuis YouTube Studio.
