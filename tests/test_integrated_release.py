import hashlib
import json

import pytest

from dk4tool.formats.ilnk import IlnkContainer
from scripts.build_integrated_release import apply_arm9_fixed_batch, changed_segments


def container(*blocks: bytes) -> bytes:
    return IlnkContainer(list(blocks)).to_bytes()


def test_changed_segments_reports_only_modified_record():
    before = container(b"one\0two\0three", b"four\0five")
    after = container(b"one\0TWO\0three", b"four\0five")

    assert changed_segments(before, after) == {(0, 1)}


def test_changed_segments_accepts_byte_identical_container():
    data = container(b"one\0two", b"three")

    assert changed_segments(data, data) == set()


def test_changed_segments_rejects_record_count_change():
    before = container(b"one\0two")
    after = container(b"one\0two\0three")

    with pytest.raises(ValueError, match="segment count changed"):
        changed_segments(before, after)


def test_arm9_fixed_batch_replaces_only_verified_slot(tmp_path):
    source = b"before\0next"
    batch = tmp_path / "arm9.json"
    batch.write_text(
        json.dumps(
            {
                "format": "dk4-arm9-fixed-text-batch-v1",
                "source_file_sha256": hashlib.sha256(source).hexdigest(),
                "records": [
                    {
                        "id": "TEST_LABEL",
                        "offset": 0,
                        "source_hex": b"before".hex(),
                        "english": "after",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    rebuilt, record_ids = apply_arm9_fixed_batch(batch, source)

    assert rebuilt == b"after\0\0next"
    assert record_ids == ["TEST_LABEL"]
