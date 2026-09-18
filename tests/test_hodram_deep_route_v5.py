from __future__ import annotations

import json
from pathlib import Path

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import changed_segments
from scripts.materialize_hodram_deep_route_v5 import BLOCKS, TRANSLATIONS

BASE = Path("out/raphael_natural_v2_accepted_base.nds")
V5 = Path("translations/hodram_deep_route_v5.json")
PRIOR = [
    Path("translations/hodram_deep_route_v1.json"),
    Path("translations/hodram_deep_route_v2.json"),
    Path("translations/hodram_deep_route_v3.json"),
    Path("translations/hodram_deep_route_v4a.json"),
    Path("translations/hodram_deep_route_v4b.json"),
]


def _load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_hodram_v5_inventory_and_layout() -> None:
    batch = _load(V5)
    assert len(batch["records"]) == sum(map(len, TRANSLATIONS.values())) == 162
    assert set(batch["inventory"]["blocks"]) == {str(block) for block in BLOCKS}
    source = NdsImage.open(BASE).read_file("/data/SC1.DK4")
    rows = materialize_translation_batch(batch, source)
    profile = get_dialogue_profile("hodram-story-live")
    for row in rows:
        audit = audit_fixed_dialogue_record(
            bytes.fromhex(row["source_hex"]), row["english"], profile
        )
        assert not [issue for issue in audit["issues"] if issue["severity"] == "error"]


def test_hodram_v5_cumulative_changed_records_are_exact() -> None:
    source = NdsImage.open(BASE).read_file("/data/SC1.DK4")
    rows = []
    for path in [*PRIOR, V5]:
        rows.extend(materialize_translation_batch(_load(path), source))
    rebuilt = rebuild_mesfile(source, rows)
    expected = {
        (
            int(row["id"].split("_B", 1)[1].split("_", 1)[0]),
            int(row["id"].rsplit("R", 1)[1]),
        )
        for row in rows
    }
    assert len(expected) == 964
    assert changed_segments(source, rebuilt) == expected


def test_hodram_v5_release_stack_extends_v4() -> None:
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["hodram-deep-route-v5"]["batches"][:-1] == profiles["hodram-deep-route-v4"]["batches"]
    assert profiles["hodram-deep-route-v5"]["batches"][-1] == V5.as_posix()
