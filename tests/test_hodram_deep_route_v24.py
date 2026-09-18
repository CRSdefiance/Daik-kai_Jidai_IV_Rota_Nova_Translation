from __future__ import annotations

import json
from pathlib import Path

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import changed_segments
from scripts.materialize_hodram_deep_route_v24a import EXCLUDED as EXCLUDED_A, LINES as LINES_A
from scripts.materialize_hodram_deep_route_v24b import EXCLUDED as EXCLUDED_B, LINES as LINES_B
from scripts.materialize_hodram_deep_route_v24c import BLOCKS as BLOCKS_C, EXCLUDED as EXCLUDED_C, LINES as LINES_C


BASE = Path("out/raphael_natural_v2_accepted_base.nds")
V24A = Path("translations/hodram_deep_route_v24a.json")
V24B = Path("translations/hodram_deep_route_v24b.json")
V24C = Path("translations/hodram_deep_route_v24c.json")
PRIOR = [Path(f"translations/hodram_deep_route_v{i}.json") for i in (1, 2, 3)] + [
    Path("translations/hodram_deep_route_v4a.json"), Path("translations/hodram_deep_route_v4b.json"),
    Path("translations/hodram_deep_route_v5.json"), Path("translations/hodram_deep_route_v6a.json"),
    Path("translations/hodram_deep_route_v6b.json"), *[Path(f"translations/hodram_deep_route_v{i}.json") for i in range(7, 20)],
    Path("translations/hodram_deep_route_v20a.json"), Path("translations/hodram_deep_route_v20b.json"),
    Path("translations/hodram_deep_route_v21.json"), Path("translations/hodram_deep_route_v22.json"),
    Path("translations/hodram_deep_route_v23.json"),
]


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_hodram_v24a_inventory_and_layout() -> None:
    batch = _load(V24A)
    assert len(batch["records"]) == len(LINES_A) == 86
    assert batch["inventory"]["identified_records"] == 87
    assert batch["excluded_records"] == EXCLUDED_A
    source = NdsImage.open(BASE).read_file("/data/SC1.DK4")
    profile = get_dialogue_profile("hodram-story-jungle-live")
    failures = []
    for row in materialize_translation_batch(batch, source):
        audit = audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]), row["english"], profile)
        errors = [issue for issue in audit["issues"] if issue["severity"] == "error"]
        if errors:
            failures.append((row["id"], errors))
    assert not failures, "\n".join(f"{row_id}: {errors}" for row_id, errors in failures)
    assert 0x97 not in profile.leading_speaker_bytes


def test_hodram_v24b_inventory_and_layout() -> None:
    batch = _load(V24B)
    assert len(batch["records"]) == len(LINES_B) == 60
    assert batch["inventory"]["identified_records"] == 60
    assert batch["excluded_records"] == EXCLUDED_B == {}
    source = NdsImage.open(BASE).read_file("/data/SC1.DK4")
    profile = get_dialogue_profile("hodram-story-cave-live")
    failures = []
    for row in materialize_translation_batch(batch, source):
        audit = audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]), row["english"], profile)
        errors = [issue for issue in audit["issues"] if issue["severity"] == "error"]
        if errors:
            failures.append((row["id"], errors))
    assert not failures, "\n".join(f"{row_id}: {errors}" for row_id, errors in failures)
    assert 0x97 in profile.leading_speaker_bytes
    assert not ({0x89, 0x8B, 0x8D, 0x93} & profile.leading_speaker_bytes)


def test_hodram_v24c_inventory_and_layout() -> None:
    batch = _load(V24C)
    assert len(batch["records"]) == len(LINES_C) == 98
    assert batch["inventory"]["identified_records"] == 98
    assert batch["excluded_records"] == EXCLUDED_C == {}
    assert set(batch["inventory"]["blocks"]) == {str(block) for block in BLOCKS_C}
    source = NdsImage.open(BASE).read_file("/data/SC1.DK4")
    profile = get_dialogue_profile("hodram-story-ruins-live")
    failures = []
    for row in materialize_translation_batch(batch, source):
        audit = audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]), row["english"], profile)
        errors = [issue for issue in audit["issues"] if issue["severity"] == "error"]
        if errors:
            failures.append((row["id"], errors))
    assert not failures, "\n".join(f"{row_id}: {errors}" for row_id, errors in failures)
    assert {0xC2, 0xD3} <= profile.leading_speaker_bytes


def test_hodram_v24_cumulative_changed_records_are_exact() -> None:
    source = NdsImage.open(BASE).read_file("/data/SC1.DK4")
    rows = []
    for path in [*PRIOR, V24A, V24B, V24C]:
        rows.extend(materialize_translation_batch(_load(path), source))
    rebuilt = rebuild_mesfile(source, rows)
    expected = {(int(row["id"].split("_B", 1)[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 3958
    assert changed_segments(source, rebuilt) == expected
    parsed_source = IlnkContainer.parse(source)
    parsed_rebuilt = IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(parsed_rebuilt.blocks[block].split(b"\0")[index]) == len(parsed_source.blocks[block].split(b"\0")[index])


def test_hodram_v24_release_stack_extends_v23() -> None:
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["hodram-deep-route-v24"]["batches"][:-3] == profiles["hodram-deep-route-v23"]["batches"]
    assert profiles["hodram-deep-route-v24"]["batches"][-3:] == [V24A.as_posix(), V24B.as_posix(), V24C.as_posix()]
