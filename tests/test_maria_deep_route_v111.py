import json
import csv
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import changed_segments
B=Path("out/raphael_natural_v2_accepted_base.nds");T=Path("translations/maria_deep_route_v111.json")
def load(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def test_v111():
 b=load(T);s=NdsImage.open(B).read_file("/data/SC3.DK4");p=get_dialogue_profile(b["dialogue_profile"]);rows=materialize_translation_batch(b,s);fail=[]
 for r in rows:
  e=[i for i in audit_fixed_dialogue_record(bytes.fromhex(r["source_hex"]),r["english"],p)["issues"] if i["severity"]=="error"]
  if e:fail.append((r["id"],e))
 assert len(rows)==87 and not fail,fail;assert changed_segments(s,rebuild_mesfile(s,rows))=={(int(r["id"].split("_B",1)[1].split("_R",1)[0]),int(r["id"].rsplit("R",1)[1])) for r in rows};assert load("translations/release_stack.json")["profiles"]["maria-deep-route-v111"]["batches"][-1]==T.as_posix();assert {0x41,0x45,0xBE}<=p.leading_speaker_bytes

def test_v111_covers_every_sc3_record():
 stack=load("translations/release_stack.json");translated=set();excluded=set()
 for name in stack["profiles"]["maria-deep-route-v111"]["batches"]:
  batch=load(name)
  if batch.get("file_path")!="/data/SC3.DK4":continue
  translated.update(r["id"] for r in batch.get("records",[]))
  skipped=batch.get("excluded_records",batch.get("excluded",{}))
  excluded.update(skipped if isinstance(skipped,dict) else (r["id"] for r in skipped))
 with Path("work/sc3/script.csv").open(encoding="utf-8-sig",newline="") as handle:
  source={r["id"] for r in csv.DictReader(handle)}
 assert translated|excluded==source
 assert len(translated)==4953
 assert len(excluded-translated)==57
 assert translated&excluded=={"DK4_MES_B118_R0005"}
