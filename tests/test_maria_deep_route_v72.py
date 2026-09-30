from __future__ import annotations
import json
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import changed_segments
B=Path("out/raphael_natural_v2_accepted_base.nds");T=Path("translations/maria_deep_route_v72.json")
def load(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def test_v72_allocations():
 b=load(T);assert b["inventory"]["identified_records"]==28;s=NdsImage.open(B).read_file("/data/SC3.DK4");p=get_dialogue_profile(b["dialogue_profile"]);rows=materialize_translation_batch(b,s);fail=[]
 for r in rows:
  e=[i for i in audit_fixed_dialogue_record(bytes.fromhex(r["source_hex"]),r["english"],p)["issues"] if i["severity"]=="error"]
  if e:fail.append((r["id"],e))
 assert not fail,fail;assert changed_segments(s,rebuild_mesfile(s,rows))=={(70,int(r["id"].rsplit("R",1)[1])) for r in rows}
def test_v72_content():
 b=load(T);by={r["id"]:r for r in b["records"]};assert "Rogue Ninja's Garb" in by["DK4_MES_B70_R0045"]["english"];assert by["DK4_MES_B70_R0004"]["speaker"]=="Angelo Puccini";assert load("translations/release_stack.json")["profiles"]["maria-deep-route-v72"]["batches"][-1]==T.as_posix()
