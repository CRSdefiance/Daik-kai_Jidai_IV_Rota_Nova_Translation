from __future__ import annotations
import json
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.rom.nds import NdsImage
from dk4tool.script.translation_batch import materialize_translation_batch
BASE=Path("out/raphael_natural_v2_accepted_base.nds"); BATCH=Path("translations/raphael_deep_route_v74.json")
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def test_v74_layout():
 source=NdsImage.open(BASE).read_file("/data/SC0.DK4"); b=load(BATCH)
 assert len(b["records"])==41 and b["inventory"]["identified_records"]==43 and len(b["excluded_records"])==2
 p=get_dialogue_profile(b["dialogue_profile"])
 for r in materialize_translation_batch(b,source):
  a=audit_fixed_dialogue_record(bytes.fromhex(r["source_hex"]),r["english"],p)
  assert not [i for i in a["issues"] if i["severity"]=="error"],r["id"]
def test_v74_stack():
 p=load(Path("translations/release_stack.json"))["profiles"]
 assert p["raphael-deep-route-v74"]["batches"][:-1]==p["raphael-deep-route-v73"]["batches"]
 assert p["raphael-deep-route-v74"]["batches"][-1]==BATCH.as_posix()
