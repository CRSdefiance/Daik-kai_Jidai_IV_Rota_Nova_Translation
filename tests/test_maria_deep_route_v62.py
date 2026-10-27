from __future__ import annotations
import json
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import changed_segments
BASE=Path("out/raphael_natural_v2_accepted_base.nds");BATCH=Path("translations/maria_deep_route_v62.json")
def _load(path):return json.loads(Path(path).read_text(encoding="utf-8"))
def test_maria_v62_inventory_and_allocations():
 b=_load(BATCH);assert b["inventory"]["identified_records"]==55;assert b["inventory"]["translated_records"]==55;source=NdsImage.open(BASE).read_file("/data/SC3.DK4");profile=get_dialogue_profile(b["dialogue_profile"]);rows=materialize_translation_batch(b,source);fail=[]
 for row in rows:
  errors=[i for i in audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]),row["english"],profile)["issues"] if i["severity"]=="error"]
  if errors:fail.append((row["id"],errors))
 assert not fail,fail;rebuilt=rebuild_mesfile(source,rows);expected={(int(r["id"].split("_B",1)[1].split("_",1)[0]),int(r["id"].rsplit("R",1)[1])) for r in rows};assert changed_segments(source,rebuilt)==expected
def test_maria_v62_content_and_release():
 b=_load(BATCH);by={r["id"]:r for r in b["records"]};assert "Mivor Gentz" in by["DK4_MES_B57_R0079"]["english"];assert "{MACRO:FI} {MACRO:FA}" in by["DK4_MES_B57_R0129"]["english"];assert "sailing sounds fun" in by["DK4_MES_B57_R0194"]["english"];release=_load("translations/release_stack.json");assert release["profiles"]["maria-deep-route-v62"]["batches"][-2:]==["translations/maria_deep_route_v61.json",BATCH.as_posix()]
