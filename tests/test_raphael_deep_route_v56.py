from __future__ import annotations

import json
from pathlib import Path

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.rom.nds import NdsImage
from dk4tool.script.translation_batch import materialize_translation_batch


BASE = Path("out/raphael_natural_v2_accepted_base.nds")
BATCH = Path("translations/raphael_deep_route_v56.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_raphael_v56_inventory_and_layout() -> None:
    source = NdsImage.open(BASE).read_file("/data/SC0.DK4")
    batch = _load(BATCH)
    assert len(batch["records"]) == 85
    assert batch["inventory"]["identified_records"] == 85
    assert batch["inventory"]["blocks"] == {
        "189": 10,
        "190": 13,
        "191": 8,
        "192": 11,
        "193": 10,
        "194": 8,
        "195": 25,
    }
    profile = get_dialogue_profile(str(batch["dialogue_profile"]))
    for row in materialize_translation_batch(batch, source):
        audit = audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]), row["english"], profile)
        assert not [issue for issue in audit["issues"] if issue["severity"] == "error"], row["id"]


def test_raphael_v56_release_stack_and_boom_coverage() -> None:
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["raphael-deep-route-v56"]["batches"][:-1] == profiles["raphael-deep-route-v55"]["batches"]
    assert profiles["raphael-deep-route-v56"]["batches"][-1] == BATCH.as_posix()
    text = "\n".join(record["english"] for record in _load(BATCH)["records"])
    for term in ("Tomatoes", "Wheat", "Wine", "Spices", "Rubies", "Gems", "Paintings"):
        assert f"{term} may boom".lower() in text.lower()
