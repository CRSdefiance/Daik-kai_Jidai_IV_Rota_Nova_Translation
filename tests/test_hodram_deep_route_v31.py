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
NEW = [Path(f"translations/hodram_deep_route_v{i}.json") for i in (29, 30, 31)]
EXPECTED = [(50, 51), (49, 49), (80, 80)]


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


@pytest.mark.parametrize(("path", "expected"), list(zip(NEW, EXPECTED, strict=True)))
def test_hodram_v31_inventory_and_layout(path: Path, expected: tuple[int, int]) -> None:
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


def test_hodram_v31_preserves_controls_and_runtime_macros() -> None:
    v29 = _load(NEW[0])
    assert "DK4_MES_B00_R0004" in v29["excluded_records"]
    v31 = _load(NEW[2])
    by_id = {record["id"]: record["english"] for record in v31["records"]}
    assert "{MACRO:FO}" in by_id["DK4_MES_B17_R0049"]
    assert "{MACRO:FO}" in by_id["DK4_MES_B17_R0060"]
    assert "{MACRO:FI} {MACRO:FA}" in by_id["DK4_MES_B17_R0125"]


def test_hodram_v31_cumulative_changed_records_are_exact() -> None:
    release = _load(Path("translations/release_stack.json"))
    prior = [
        Path(path)
        for path in release["profiles"]["hodram-deep-route-v28"]["batches"]
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
    assert len(expected) == 4805
    assert changed_segments(source, rebuilt) == expected
    parsed_source = IlnkContainer.parse(source)
    parsed_rebuilt = IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(parsed_rebuilt.blocks[block].split(b"\0")[index]) == len(
            parsed_source.blocks[block].split(b"\0")[index]
        )


def test_hodram_v31_release_stack_extends_v28() -> None:
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["hodram-deep-route-v31"]["batches"][:-3] == profiles["hodram-deep-route-v28"]["batches"]
    assert profiles["hodram-deep-route-v31"]["batches"][-3:] == [path.as_posix() for path in NEW]
    profile = get_dialogue_profile("hodram-story-opening-battles-live")
    assert {0x10, 0x11, 0x12, 0x1B, 0x49, 0xB7, 0xB8, 0xB9} <= profile.leading_speaker_bytes
