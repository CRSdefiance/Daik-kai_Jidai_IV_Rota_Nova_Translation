from __future__ import annotations

import json
from pathlib import Path

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.rom.nds import NdsImage
from dk4tool.script.translation_batch import materialize_translation_batch


BASE = Path("out/raphael_natural_v2_accepted_base.nds")
BATCH = Path("translations/raphael_deep_route_v82.json")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_v82_layout() -> None:
    source = NdsImage.open(BASE).read_file("/data/SC0.DK4")
    batch = load(BATCH)
    assert len(batch["records"]) == 78
    assert batch["inventory"]["identified_records"] == 80
    assert len(batch["excluded_records"]) == 2
    profile = get_dialogue_profile(batch["dialogue_profile"])
    for record in materialize_translation_batch(batch, source):
        audit = audit_fixed_dialogue_record(
            bytes.fromhex(record["source_hex"]), record["english"], profile
        )
        assert not [issue for issue in audit["issues"] if issue["severity"] == "error"], record["id"]


def test_v82_stack() -> None:
    profiles = load(Path("translations/release_stack.json"))["profiles"]
    previous = profiles["raphael-deep-route-v81"]["batches"]
    current = profiles["raphael-deep-route-v82"]["batches"]
    assert current[:-1] == previous
    assert current[-1] == BATCH.as_posix()
    assert sum(
        len(load(Path(path)).get("records", []))
        for path in current
        if path.startswith("translations/raphael_deep_route_")
    ) == 4853
