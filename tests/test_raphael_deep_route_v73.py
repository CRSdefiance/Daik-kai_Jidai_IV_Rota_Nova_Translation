from __future__ import annotations
import json
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.rom.nds import NdsImage
from dk4tool.script.translation_batch import materialize_translation_batch
BASE=Path("out/raphael_natural_v2_accepted_base.nds"); BATCH=Path("translations/raphael_deep_route_v73.json")
def _load(p): return json.loads(p.read_text(encoding="utf-8"))
def test_raphael_v73_inventory_and_layout():
    source=NdsImage.open(BASE).read_file("/data/SC0.DK4"); batch=_load(BATCH)
    assert len(batch["records"])==20 and batch["inventory"]["identified_records"]==22
    assert len(batch["excluded_records"])==2 and batch["inventory"]["blocks"]=={"302":6,"303":5,"304":9}
    profile=get_dialogue_profile(batch["dialogue_profile"])
    for row in materialize_translation_batch(batch,source):
        audit=audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]),row["english"],profile)
        assert not [i for i in audit["issues"] if i["severity"]=="error"],row["id"]
def test_raphael_v73_release_stack_and_scene_coverage():
    profiles=_load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["raphael-deep-route-v73"]["batches"][:-1]==profiles["raphael-deep-route-v72"]["batches"]
    assert profiles["raphael-deep-route-v73"]["batches"][-1]==BATCH.as_posix()
    text="\n".join(r["english"] for r in _load(BATCH)["records"])
    for term in ("Veda","Proof of Hegemony","old coin"): assert term.lower() in text.lower()
