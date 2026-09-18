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
NEW = [
    Path("translations/hodram_deep_route_v27a.json"),
    Path("translations/hodram_deep_route_v27b.json"),
    Path("translations/hodram_deep_route_v28.json"),
]
EXPECTED = [(70, 74), (102, 108), (50, 50)]
PRIOR = [Path(f"translations/hodram_deep_route_v{i}.json") for i in (1, 2, 3)] + [
    Path("translations/hodram_deep_route_v4a.json"), Path("translations/hodram_deep_route_v4b.json"),
    Path("translations/hodram_deep_route_v5.json"), Path("translations/hodram_deep_route_v6a.json"),
    Path("translations/hodram_deep_route_v6b.json"), *[Path(f"translations/hodram_deep_route_v{i}.json") for i in range(7, 20)],
    Path("translations/hodram_deep_route_v20a.json"), Path("translations/hodram_deep_route_v20b.json"),
    Path("translations/hodram_deep_route_v21.json"), Path("translations/hodram_deep_route_v22.json"),
    Path("translations/hodram_deep_route_v23.json"), Path("translations/hodram_deep_route_v24a.json"),
    Path("translations/hodram_deep_route_v24b.json"), Path("translations/hodram_deep_route_v24c.json"),
    *[Path(f"translations/hodram_deep_route_v25{suffix}.json") for suffix in "abcdef"],
    Path("translations/hodram_deep_route_v26a.json"), Path("translations/hodram_deep_route_v26b.json"),
]


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


@pytest.mark.parametrize(("path", "expected"), list(zip(NEW, EXPECTED, strict=True)))
def test_hodram_v28_inventory_and_layout(path: Path, expected: tuple[int, int]) -> None:
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


def test_hodram_v28_cumulative_changed_records_are_exact() -> None:
    source = NdsImage.open(BASE).read_file("/data/SC1.DK4")
    rows = []
    for path in [*PRIOR, *NEW]:
        rows.extend(materialize_translation_batch(_load(path), source))
    rebuilt = rebuild_mesfile(source, rows)
    expected = {(int(row["id"].split("_B", 1)[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 4626
    assert changed_segments(source, rebuilt) == expected
    parsed_source = IlnkContainer.parse(source)
    parsed_rebuilt = IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(parsed_rebuilt.blocks[block].split(b"\0")[index]) == len(parsed_source.blocks[block].split(b"\0")[index])


def test_hodram_v28_release_stack_extends_v26() -> None:
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["hodram-deep-route-v28"]["batches"][:-3] == profiles["hodram-deep-route-v26"]["batches"]
    assert profiles["hodram-deep-route-v28"]["batches"][-3:] == [path.as_posix() for path in NEW]
    profile = get_dialogue_profile("hodram-story-final-treasures-live")
    assert {0x16, 0x97, 0xA1, 0xB3, 0xCE, 0xCF} <= profile.leading_speaker_bytes
