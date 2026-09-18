from __future__ import annotations

import json
from pathlib import Path

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.rom.nds import NdsImage
from dk4tool.script.translation_batch import materialize_translation_batch


BASE = Path("out/raphael_natural_v2_accepted_base.nds")
BATCH = Path("translations/raphael_deep_route_v68.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_raphael_v68_inventory_and_layout() -> None:
    source = NdsImage.open(BASE).read_file("/data/SC0.DK4")
    batch = _load(BATCH)
    assert len(batch["records"]) == 30
    assert batch["inventory"]["identified_records"] == 30
    assert batch["inventory"]["blocks"] == {
        "286": 5, "287": 9, "288": 2, "289": 4,
        "290": 7, "291": 2, "292": 1,
    }
    profile = get_dialogue_profile(str(batch["dialogue_profile"]))
    for row in materialize_translation_batch(batch, source):
        audit = audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]), row["english"], profile)
        assert not [issue for issue in audit["issues"] if issue["severity"] == "error"], row["id"]


def test_raphael_v68_release_stack_and_scene_coverage() -> None:
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["raphael-deep-route-v68"]["batches"][:-1] == profiles["raphael-deep-route-v67"]["batches"]
    assert profiles["raphael-deep-route-v68"]["batches"][-1] == BATCH.as_posix()
    text = "\n".join(record["english"] for record in _load(BATCH)["records"])
    for term in ("William Clive", "Zaganos Bey", "100,000 coins", "Roman ruins"):
        assert term.lower() in text.lower()
