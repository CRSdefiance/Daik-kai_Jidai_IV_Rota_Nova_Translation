from __future__ import annotations

import json
from pathlib import Path

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.rom.nds import NdsImage
from dk4tool.script.translation_batch import materialize_translation_batch


BASE = Path("out/raphael_natural_v2_accepted_base.nds")
BATCH = Path("translations/raphael_deep_route_v67.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_raphael_v67_inventory_and_layout() -> None:
    source = NdsImage.open(BASE).read_file("/data/SC0.DK4")
    batch = _load(BATCH)
    assert len(batch["records"]) == 61
    assert batch["inventory"]["identified_records"] == 61
    assert batch["inventory"]["blocks"] == {
        "271": 5, "272": 2, "273": 4, "274": 1, "275": 2,
        "276": 7, "277": 2, "278": 6, "279": 2, "280": 3,
        "281": 9, "282": 2, "283": 4, "284": 10, "285": 2,
    }
    profile = get_dialogue_profile(str(batch["dialogue_profile"]))
    for row in materialize_translation_batch(batch, source):
        audit = audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]), row["english"], profile)
        assert not [issue for issue in audit["issues"] if issue["severity"] == "error"], row["id"]


def test_raphael_v67_release_stack_and_scene_coverage() -> None:
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["raphael-deep-route-v67"]["batches"][:-1] == profiles["raphael-deep-route-v66"]["batches"]
    assert profiles["raphael-deep-route-v67"]["batches"][-1] == BATCH.as_posix()
    text = "\n".join(record["english"] for record in _load(BATCH)["records"])
    for term in ("Jacks Bloom", "Julian Vermeer", "Prett Perot", "Peralonso Aguirre"):
        assert term.lower() in text.lower()
