from __future__ import annotations
import json
from pathlib import Path
import pytest
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import changed_segments
B=Path("out/raphael_natural_v2_accepted_base.nds")
def load(p):return json.loads(Path(p).read_text(encoding="utf-8"))
@pytest.mark.parametrize("v,block,count",[(74,74,20),(75,75,15),(76,76,15)])
def test_allocations(v,block,count):
 t=Path(f"translations/maria_deep_route_v{v}.json");b=load(t);assert b["inventory"]["identified_records"]==count;s=NdsImage.open(B).read_file("/data/SC3.DK4");p=get_dialogue_profile(b["dialogue_profile"]);rows=materialize_translation_batch(b,s);fail=[]
 for r in rows:
  e=[i for i in audit_fixed_dialogue_record(bytes.fromhex(r["source_hex"]),r["english"],p)["issues"] if i["severity"]=="error"]
  if e:fail.append((r["id"],e))
 assert not fail,fail;assert changed_segments(s,rebuild_mesfile(s,rows))=={(block,int(r["id"].rsplit("R",1)[1])) for r in rows}
def test_content_and_stack():
 assert "Shield of Minerva" in load("translations/maria_deep_route_v74.json")["records"][13]["english"]
 assert any("Cape of Good Hope" in r["english"] for r in load("translations/maria_deep_route_v75.json")["records"])
 assert any("Jaguar God" in r["english"] for r in load("translations/maria_deep_route_v76.json")["records"])
 assert load("translations/release_stack.json")["profiles"]["maria-deep-route-v76"]["batches"][-1]=="translations/maria_deep_route_v76.json"
