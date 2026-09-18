from __future__ import annotations

import json
from pathlib import Path

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.rom.nds import NdsImage
from dk4tool.script.translation_batch import materialize_translation_batch


BASE = Path("out/raphael_natural_v2_accepted_base.nds")
BATCH = Path("translations/raphael_deep_route_v49.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_raphael_v49_inventory_and_layout() -> None:
    batch = _load(BATCH)
    assert batch["inventory"] == {"identified_records": 79, "translated_records": 78, "blocks": {"171": 24, "172": 35, "173": 19}}
    source = NdsImage.open(BASE).read_file("/data/SC0.DK4")
    profile = get_dialogue_profile(str(batch["dialogue_profile"]))
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 78
    for row in rows:
        audit = audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]), row["english"], profile)
        assert not [issue for issue in audit["issues"] if issue["severity"] == "error"], row["id"]


def test_raphael_v49_release_stack_and_scene_coverage() -> None:
    batch = _load(BATCH)
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["raphael-deep-route-v49"]["batches"][:-1] == profiles["raphael-deep-route-v48"]["batches"]
    assert profiles["raphael-deep-route-v49"]["batches"][-1] == BATCH.as_posix()
    text = "\n".join(record["english"] for record in batch["records"])
    for term in ("flamenco", "Samuel da Khan", "cooking", "ship thief"):
        assert term.lower() in text.lower()
