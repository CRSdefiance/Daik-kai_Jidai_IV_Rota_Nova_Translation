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

BASE=Path("out/raphael_natural_v2_accepted_base.nds"); BATCH=Path("translations/maria_deep_route_v36.json")
def _load(path:Path)->dict[str,object]:
    value=json.loads(path.read_text(encoding="utf-8")); assert isinstance(value,dict); return value
def test_maria_v36_inventory_layout_and_allocations()->None:
    batch=_load(BATCH); assert batch["inventory"]=={"identified_records":19,"translated_records":19,"excluded_records":0,"blocks":{"279":11,"280":8}}
    source=NdsImage.open(BASE).read_file("/data/SC3.DK4"); profile=get_dialogue_profile(str(batch["dialogue_profile"])); rows=materialize_translation_batch(batch,source); failures=[]
    for row in rows:
        audit=audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]),row["english"],profile); errors=[i for i in audit["issues"] if i["severity"]=="error"]
        if errors: failures.append((row["id"],errors))
    assert not failures,failures
    rebuilt=rebuild_mesfile(source,rows); expected={(int(r["id"].split("_B")[1].split("_")[0]),int(r["id"].rsplit("R",1)[1])) for r in rows}; assert changed_segments(source,rebuilt)==expected
    old,new=IlnkContainer.parse(source),IlnkContainer.parse(rebuilt)
    for block,index in expected: assert len(new.blocks[block].split(b"\0")[index])==len(old.blocks[block].split(b"\0")[index])
def test_maria_v36_states_text_leads_macro_and_release()->None:
    batch=_load(BATCH); by_id={r["id"]:r for r in batch["records"]}
    assert by_id["DK4_MES_B279_R0005"]["english"].startswith("{SPEAKER:CB}"); assert "{MACRO:FI}" in by_id["DK4_MES_B279_R0005"]["english"]
    assert by_id["DK4_MES_B280_R0008"]["english"].startswith("{SPEAKER:D0}")
    for row_id in ("DK4_MES_B280_R0010","DK4_MES_B280_R0016","DK4_MES_B280_R0017"): assert not by_id[row_id]["english"].startswith("{SPEAKER:")
    release=_load(Path("translations/release_stack.json")); assert release["profiles"]["maria-deep-route-v36"]["batches"][-1]==BATCH.as_posix()
