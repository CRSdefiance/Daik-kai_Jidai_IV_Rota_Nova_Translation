from __future__ import annotations

import json
from pathlib import Path

import pytest

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import changed_segments


BASE = Path("out/raphael_natural_v2_accepted_base.nds")
NEW = [Path(f"translations/hodram_deep_route_v32{suffix}.json") for suffix in "abc"]
EXPECTED = [(59, 59), (67, 67), (73, 74)]


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


@pytest.mark.parametrize(("path", "expected"), list(zip(NEW, EXPECTED, strict=True)))
def test_hodram_v32_inventory_and_layout(path: Path, expected: tuple[int, int]) -> None:
    batch = _load(path)
    translated, identified = expected
    assert len(batch["records"]) == translated
    assert batch["inventory"]["identified_records"] == identified
    source = NdsImage.open(BASE).read_file("/data/SC1.DK4")
    profile = get_dialogue_profile(str(batch["dialogue_profile"]))
    failures = []
    for row in materialize_translation_batch(batch, source):
        audit = audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]), row["english"], profile)
        errors = [issue for issue in audit["issues"] if issue["severity"] == "error"]
        if errors:
            failures.append((row["id"], errors))
    assert not failures, "\n".join(f"{row_id}: {errors}" for row_id, errors in failures)


def test_hodram_v32_preserves_control_and_runtime_macros() -> None:
    v32c = _load(NEW[2])
    assert v32c["excluded_records"] == {
        "DK4_MES_B42_R0032": "Preserved four-byte nontext event payload; not dialogue."
    }
    by_id = {record["id"]: record["english"] for record in v32c["records"]}
    assert "{MACRO:FO}" in by_id["DK4_MES_B38_R0063"]
    assert "{MACRO:FA}" in by_id["DK4_MES_B40_R0019"]


def test_hodram_v32_cumulative_changed_records_are_exact() -> None:
    release = _load(Path("translations/release_stack.json"))
    prior = [
        Path(path)
        for path in release["profiles"]["hodram-deep-route-v31"]["batches"]
        if path.startswith("translations/hodram_deep_route_")
    ]
    source = NdsImage.open(BASE).read_file("/data/SC1.DK4")
    rows = []
    for path in [*prior, *NEW]:
        rows.extend(materialize_translation_batch(_load(path), source))
    rebuilt = rebuild_mesfile(source, rows)
    expected = {
        (int(row["id"].split("_B", 1)[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in rows
    }
    assert len(expected) == 5004
    assert changed_segments(source, rebuilt) == expected
    parsed_source = IlnkContainer.parse(source)
    parsed_rebuilt = IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(parsed_rebuilt.blocks[block].split(b"\0")[index]) == len(
            parsed_source.blocks[block].split(b"\0")[index]
        )


def test_hodram_v32_release_stack_extends_v31() -> None:
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["hodram-deep-route-v32"]["batches"][:-3] == profiles["hodram-deep-route-v31"]["batches"]
    assert profiles["hodram-deep-route-v32"]["batches"][-3:] == [path.as_posix() for path in NEW]
    profile = get_dialogue_profile("hodram-story-caribbean-battles-live")
    assert {0x1D, 0x21, 0x25, 0x28, 0x2A, 0x34, 0x35, 0x37, 0x38, 0x39, 0x3C, 0xD5} <= profile.leading_speaker_bytes
