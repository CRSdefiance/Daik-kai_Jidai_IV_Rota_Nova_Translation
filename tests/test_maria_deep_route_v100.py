import json
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import changed_segments
B=Path("out/raphael_natural_v2_accepted_base.nds");T=Path("translations/maria_deep_route_v100.json")
def load(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def test_v100_allocations():
 b=load(T);assert b["inventory"]["identified_records"]==22;s=NdsImage.open(B).read_file("/data/SC3.DK4");p=get_dialogue_profile(b["dialogue_profile"]);rows=materialize_translation_batch(b,s);fail=[]
 for r in rows:
  e=[i for i in audit_fixed_dialogue_record(bytes.fromhex(r["source_hex"]),r["english"],p)["issues"] if i["severity"]=="error"]
  if e:fail.append((r["id"],e))
 assert not fail,fail;assert changed_segments(s,rebuild_mesfile(s,rows))=={(137,int(r["id"].rsplit("R",1)[1])) for r in rows}
def test_v100_content_and_stack():
 b=load(T);m={r["id"]:r["english"] for r in b["records"]};assert "Julio Erneco" in m["DK4_MES_B137_R0046"];assert "FI" in m["DK4_MES_B137_R0080"];assert load("translations/release_stack.json")["profiles"]["maria-deep-route-v100"]["batches"][-1]==T.as_posix()
