"""Exact Hodram B47/B48 clean/current records, original progressive/FE consumers and measured runtime."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path("translations/hodram_outcomes_native_contract_v1.json")
CONTRACT_SHA="83b3770866e46df47dd0e5b6e6170da1454d3ccde77199abc9676941360774e3"
ARM9_SHA="12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b"
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError("Frozen Hodram-outcomes contract changed")
    d=json.loads(raw)
    for p,h in d["dependencies"].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError("Native dependency changed:"+p)
    if len(d["record_bindings"])!=6 or d["choice_bindings"] or d["physical_native_rows_per_page"]!=4 or d["complete_native_pages"]!=6:
        raise ValueError("Complete six-paragraph/six-page/no-menu contract required")
    if d["measured_macro_ascii_lengths"]!={"FI":6,"FA":9,"FO":15} or d["source_macro_counts"]!={"FI":1,"FA":0,"FO":0}:
        raise ValueError("Exact measured Hodram macros required")
    return d
def expected_profile(ident,consumer=None):
    d=contract()
    if ident not in d["record_bindings"]:raise ValueError("Unreviewed Hodram-outcomes paragraph")
    r=d["record_bindings"][ident];wanted="FE-paper" if r["source_selector"]==254 else "progressive"
    if consumer is not None and consumer!=wanted:raise ValueError("Original Hodram-outcomes consumer required")
    base=get_dialogue_profile("hodram-story-live")
    if base.window_width_px!=216 or base.max_lines!=4 or base.macro_ascii_lengths!={"FI":6,"FA":9,"FO":15} or base.literal_prefix_policy!="forbid":
        raise ValueError("Original global Hodram profile required")
    return replace(base,name="Hodram-outcomes-source-bound-v1:"+ident,max_lines=r["maximum_total_rows"],
        macro_widths={"FI":36,"FA":54,"FO":90,"I":12},macro_ascii_lengths={"FI":6,"FA":9,"FO":15},
        leading_speaker_bytes=frozenset({254} if wanted=="FE-paper" else {2}),
        literal_prefix_policy="native-guard-v255",
        metrics_source="Exact registered V8300 Hodram captain1:five progressive216px pages andone original FE228x48 bitmap with216px usablewidth,288stride/6x12/16physicalpitch;source02/FE sixbyte preambles. Default FI6/FA9/FO15,one sourceFI. Allsix complete native/stored pages and100 actual body/name orFE-absent-header holds;live FE descriptors/palette/bankD VRAM match independent nativeplanes. Six line-count infos,zero warnings orwaivers. Four whole-script initialized fixtures40004frames plus8002focusedFE frames are not naturaloptional activation. B48 source4495/English4494 returns[0,0];script-boundary seeds equal,butfinalB48 seeds differ and13of93laterRGB pairs differ. Allfive checked final components/actors/captain1 match. No everyframe causal,future-outcome,broad simulation,fullroute orhardware claim.")
def profile_for(arm,block,ident,file_path,consumer=None):
    d=contract()
    if ident not in d["record_bindings"]:raise ValueError("Unreviewed Hodram-outcomes paragraph")
    r=d["record_bindings"][ident]
    if sha(arm)!=ARM9_SHA or file_path!=r["file_path"] or sha(block) not in r["source_block_hashes"]:
        raise ValueError("Exact file-qualified Hodram-outcomes source/current block and12eb runtime required")
    return expected_profile(ident,consumer)
def validate_runtime(image):
    d=contract()
    for path,digest in d["runtime_component_hashes"].items():
        if sha(image.read_file(path))!=digest:raise ValueError("Exact Hodram-outcomes runtime component required:"+path)
    return d


def validate_approved_batch(doc):
    from dk4tool.dialogue.review import validate_natural_dialogue_batch
    d=contract()
    for key,value in d["batch_binding"].items():
        if doc.get(key)!=value:raise ValueError("Exact Hodram-outcomes approved batch metadata required:"+key)
    validate_natural_dialogue_batch(doc)
    rows=doc.get("records")
    if not isinstance(rows,list) or [r.get("id") for r in rows if isinstance(r,dict)]!=list(d["record_bindings"]):
        raise ValueError("Exact complete ordered Hodram-outcomes approved records required")
    for row in rows:
        b=d["record_bindings"][row["id"]]
        if any(row.get(k)!=v for k,v in b["approved_fields"].items()):
            raise ValueError("Exact Hodram-outcomes approved prose/source/context/waiver required:"+row["id"])
        if not isinstance(row.get("review"),dict) or not all(row["review"].get(g) is True for g in d["review_gates"]):
            raise ValueError("All five individual Hodram-outcomes gates required:"+row["id"])
    if doc.get("typed_choice_records"):
        raise ValueError("No Hodram-outcomes typed menu records authorized")
    return d
