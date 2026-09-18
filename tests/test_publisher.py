import json

import pytest

from minitwist_publisher import config, upload, video_queue


def entry(**over):
    base = {
        "id": "x",
        "file": "x.mp4",
        "title": "A title",
        "description": "A description",
        "tags": ["a", "b"],
        "privacy": "private",
        "publish_at": None,
        "status": "pending",
    }
    base.update(over)
    return base


# --- file d'attente --------------------------------------------------------

def test_valid_entry_passes():
    video_queue.validate(entry())


@pytest.mark.parametrize("over, fragment", [
    ({"title": ""}, "title"),
    ({"title": "x" * 101}, "titre trop long"),
    ({"description": "a < b"}, "interdits"),
    ({"privacy": "secret"}, "privacy"),
    ({"tags": "pas une liste"}, "tags"),
    ({"publish_at": "2026-09-20T18:00:00"}, "fuseau"),
    ({"publish_at": "demain"}, "ISO 8601"),
    ({"publish_at": "2026-09-20T18:00:00+02:00", "privacy": "public"}, "programmee"),
])
def test_invalid_entries_are_rejected(over, fragment):
    with pytest.raises(video_queue.QueueError, match=fragment):
        video_queue.validate(entry(**over))


def test_next_pending_skips_uploaded():
    entries = [entry(id="a", status="uploaded"), entry(id="b"), entry(id="c")]
    assert video_queue.next_pending(entries)["id"] == "b"
    assert video_queue.next_pending([entry(status="uploaded")]) is None


def test_real_queue_file_is_valid():
    # Le fichier livre dans le depot doit toujours rester chargeable.
    assert video_queue.load(config.QUEUE_FILE)


def test_save_roundtrip(tmp_path):
    path = tmp_path / "q.json"
    video_queue.save(path, [entry()])
    assert json.loads(path.read_text(encoding="utf-8"))[0]["title"] == "A title"


# --- corps de la requete YouTube ------------------------------------------

def test_body_declares_not_for_kids_and_synthetic_media():
    status = upload.build_body(entry())["status"]
    assert status["selfDeclaredMadeForKids"] is False
    assert status["containsSyntheticMedia"] is True
    assert status["privacyStatus"] == "private"
    assert "publishAt" not in status


def test_body_schedules_when_publish_at_set():
    status = upload.build_body(entry(publish_at="2026-09-20T18:00:00+02:00"))["status"]
    assert status["publishAt"] == "2026-09-20T18:00:00+02:00"


def test_body_snippet_is_english_entertainment():
    snippet = upload.build_body(entry())["snippet"]
    assert snippet["categoryId"] == "24"
    assert snippet["defaultLanguage"] == snippet["defaultAudioLanguage"] == "en"


def test_only_upload_scope_is_requested():
    # La politique de confidentialite publiee et l'audit n'annoncent que ce droit.
    assert config.SCOPES == ["https://www.googleapis.com/auth/youtube.upload"]
