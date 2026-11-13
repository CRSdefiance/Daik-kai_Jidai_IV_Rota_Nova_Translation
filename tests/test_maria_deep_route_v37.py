from __future__ import annotations
import json
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import changed_segments
BASE=Path("out/raphael_natural_v2_accepted_base.nds"); BATCH=Path("translations/maria_deep_route_v37.json")
def _load(path:Path)->dict[str,object]:
    value=json.loads(path.read_text(encoding="utf-8")); assert isinstance(value,dict); return value
def test_maria_v37_inventory_layout_and_allocations()->None:
    batch=_load(BATCH); assert batch["inventory"]=={"identified_records":33,"translated_records":32,"excluded_records":1,"blocks":{"274":32}}
    source=NdsImage.open(BASE).read_file("/data/SC3.DK4"); profile=get_dialogue_profile(str(batch["dialogue_profile"])); rows=materialize_translation_batch(batch,source); failures=[]
    for row in rows:
        audit=audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]),row["english"],profile); errors=[i for i in audit["issues"] if i["severity"]=="error"]
        if errors: failures.append((row["id"],errors))
    assert not failures,failures
    rebuilt=rebuild_mesfile(source,rows); expected={(274,int(r["id"].rsplit("R",1)[1])) for r in rows}; assert changed_segments(source,rebuilt)==expected
    old,new=IlnkContainer.parse(source),IlnkContainer.parse(rebuilt)
    for block,index in expected: assert len(new.blocks[block].split(b"\0")[index])==len(old.blocks[block].split(b"\0")[index])
def test_maria_v37_choices_text_leads_exclusion_and_release()->None:
    batch=_load(BATCH); by_id={r["id"]:r for r in batch["records"]}
    assert by_id["DK4_MES_B274_R0086"]["english"]=="Compass{PAD}"; assert by_id["DK4_MES_B274_R0088"]["english"]=="Hunch{PAD}"
    for row_id in ("DK4_MES_B274_R0074","DK4_MES_B274_R0086","DK4_MES_B274_R0088"): assert not by_id[row_id]["english"].startswith("{SPEAKER:")
    assert batch["excluded"]==[{"id":"DK4_MES_B274_R0027","reason":"Opaque six-byte event payload 056060463E63; not dialogue."}]
    release=_load(Path("translations/release_stack.json")); assert release["profiles"]["maria-deep-route-v37"]["batches"][-1]==BATCH.as_posix()
