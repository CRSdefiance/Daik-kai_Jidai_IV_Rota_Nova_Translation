from __future__ import annotations

import json
from pathlib import Path

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.rom.nds import NdsImage
from dk4tool.script.translation_batch import materialize_translation_batch


BASE = Path("out/raphael_natural_v2_accepted_base.nds")
BATCHES = [Path(f"translations/raphael_deep_route_v{i}.json") for i in range(50, 53)]


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_raphael_v52_inventory_and_layout() -> None:
    source = NdsImage.open(BASE).read_file("/data/SC0.DK4")
    batches = [_load(path) for path in BATCHES]
    assert [len(batch["records"]) for batch in batches] == [36, 56, 63]
    assert sum(batch["inventory"]["identified_records"] for batch in batches) == 157
    assert sum(len(batch["excluded_records"]) for batch in batches) == 2
    for batch in batches:
        profile = get_dialogue_profile(str(batch["dialogue_profile"]))
        for row in materialize_translation_batch(batch, source):
            audit = audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]), row["english"], profile)
            assert not [issue for issue in audit["issues"] if issue["severity"] == "error"], row["id"]


def test_raphael_v52_release_stack_and_scene_coverage() -> None:
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["raphael-deep-route-v52"]["batches"][:-3] == profiles["raphael-deep-route-v49"]["batches"]
    assert profiles["raphael-deep-route-v52"]["batches"][-3:] == [path.as_posix() for path in BATCHES]
    text = "\n".join(record["english"] for path in BATCHES for record in _load(path)["records"])
    for term in ("Jam Jack Ludwyan", "Elysion", "extra armor", "one to five units", "Dias! Call me Dias", "multiple of four"):
        assert term.lower() in text.lower()
