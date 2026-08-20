import hashlib

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.translation_batch import materialize_translation_batch


def source_data() -> bytes:
    return IlnkContainer(["港へ行く".encode("cp932") + b"\0ASCII"]).to_bytes()


def test_translation_batch_materializes_verified_rows():
    source = source_data()
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": hashlib.sha256(source).hexdigest(),
        "records": [
            {
                "id": "DK4_MES_B00_R0000",
                "english": "Go to port{PAD}",
                "speaker": "Guide",
            }
        ],
    }
    rows = materialize_translation_batch(batch, source)
    assert rows[0]["english"] == "Go to port{PAD}"
    assert rows[0]["speaker"] == "Guide"
    assert rows[0]["source_hex"] == "港へ行く".encode("cp932").hex().upper()


def test_translation_batch_rejects_wrong_source_hash():
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": "0" * 64,
        "records": [],
    }
    try:
        materialize_translation_batch(batch, source_data())
    except ValueError as error:
        assert "SHA-256 mismatch" in str(error)
    else:
        raise AssertionError("expected source hash rejection")


def test_translation_batch_can_replace_previously_english_record():
    source = IlnkContainer([b"see below"]).to_bytes()
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/COMMON/HELP.DK4",
        "source_file_sha256": hashlib.sha256(source).hexdigest(),
        "records": [{"id": "DK4_MES_B00_R0000", "english": "Useful help.{PAD}"}],
    }

    rows = materialize_translation_batch(batch, source)

    assert rows[0]["english"] == "Useful help.{PAD}"


def test_translation_batch_forwards_opt_in_dialogue_encoder_metadata():
    source = source_data()
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": hashlib.sha256(source).hexdigest(),
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "story",
        "records": [
            {"id": "DK4_MES_B00_R0000", "english": "Go now{PAD}"}
        ],
    }

    rows = materialize_translation_batch(batch, source)

    assert rows[0]["encoder"] == "dialogue-fixed-v1"
    assert rows[0]["dialogue_profile"] == "story"
