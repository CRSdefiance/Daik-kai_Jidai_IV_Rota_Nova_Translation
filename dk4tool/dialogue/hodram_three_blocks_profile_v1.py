"""Exact Hodram B137/B45/B46 clean/current records, original progressive/FE consumers and measured runtime."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path("translations/hodram_three_blocks_native_contract_v1.json")
CONTRACT_SHA="15f677bd433171fc5b8feac2dd198547a693b948638433c474789dd72aa49462"
ARM9_SHA="12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b"
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError("Frozen Hodram-three-blocks contract changed")
    d=json.loads(raw)
    for p,h in d["dependencies"].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError("Native dependency changed:"+p)
    if len(d["record_bindings"])!=28 or d["choice_bindings"] or d["physical_native_rows_per_page"]!=4 or d["complete_native_pages"]!=28:
        raise ValueError("Complete twenty-eight-paragraph/twenty-eight-page/no-menu contract required")
    if d["measured_macro_ascii_lengths"]!={"FI":6,"FA":9,"FO":15} or d["source_macro_counts"]!={"FI":0,"FA":0,"FO":0}:
        raise ValueError("Exact measured Hodram macros required")
    return d
def expected_profile(ident,consumer=None):
    d=contract()
    if ident not in d["record_bindings"]:raise ValueError("Unreviewed Hodram-three-blocks paragraph")
    r=d["record_bindings"][ident];wanted="FE-paper" if r["source_selector"]==254 else "progressive"
    if consumer is not None and consumer!=wanted:raise ValueError("Original Hodram-three-blocks consumer required")
    base=get_dialogue_profile("hodram-story-live")
    if base.window_width_px!=216 or base.max_lines!=4 or base.macro_ascii_lengths!={"FI":6,"FA":9,"FO":15} or base.literal_prefix_policy!="forbid":
        raise ValueError("Original global Hodram profile required")
    return replace(base,name="Hodram-three-blocks-source-bound-v1:"+ident,max_lines=r["maximum_total_rows"],
        macro_widths={"FI":36,"FA":54,"FO":90,"I":12},macro_ascii_lengths={"FI":6,"FA":9,"FO":15},
        leading_speaker_bytes=frozenset({254} if wanted=="FE-paper" else {1,2,9,16,18,113}),
        literal_prefix_policy="native-guard-v255",
        metrics_source="Exact registered V8259 Hodram captain1:216px/four rows,28single native pages;source01/02/09/10/12/71 with complete sixbyte preambles. Default FI6/FA9/FO15,zero source macros. Three source ellipsis records retained. Full compiled/stored andactual body/name masks,all28source/revised passages andsix names in disclosed whole-script fixtures,original4800/layout0/4700 andnormalvaluecarry verified. Two exact weak-boundary exceptions andfive infos retained. B137 laterfixture captain0/SC0B44 isnot normal Hodram continuity;all measured timing/RNG/UI/component/calendar/RGB limits remain. No global font/profile/guard changes,allattainable effect-path,fullroute orhardware claim.")
def profile_for(arm,block,ident,file_path,consumer=None):
    d=contract()
    if ident not in d["record_bindings"]:raise ValueError("Unreviewed Hodram-three-blocks paragraph")
    r=d["record_bindings"][ident]
    if sha(arm)!=ARM9_SHA or file_path!=r["file_path"] or sha(block) not in r["source_block_hashes"]:
        raise ValueError("Exact file-qualified Hodram-three-blocks source/current block and12eb runtime required")
    return expected_profile(ident,consumer)
def validate_runtime(image):
    d=contract()
    for path,digest in d["runtime_component_hashes"].items():
        if sha(image.read_file(path))!=digest:raise ValueError("Exact Hodram-three-blocks runtime component required:"+path)
    return d


def validate_approved_batch(doc):
    from dk4tool.dialogue.review import validate_natural_dialogue_batch
    d=contract()
    for key,value in d["batch_binding"].items():
        if doc.get(key)!=value:raise ValueError("Exact Hodram-three-blocks approved batch metadata required:"+key)
    validate_natural_dialogue_batch(doc)
    rows=doc.get("records")
    if not isinstance(rows,list) or [r.get("id") for r in rows if isinstance(r,dict)]!=list(d["record_bindings"]):
        raise ValueError("Exact complete ordered Hodram-three-blocks approved records required")
    for row in rows:
        b=d["record_bindings"][row["id"]]
        if any(row.get(k)!=v for k,v in b["approved_fields"].items()):
            raise ValueError("Exact Hodram-three-blocks approved prose/source/context/waiver required:"+row["id"])
        if not isinstance(row.get("review"),dict) or not all(row["review"].get(g) is True for g in d["review_gates"]):
            raise ValueError("All five individual Hodram-three-blocks gates required:"+row["id"])
    if doc.get("typed_choice_records"):
        raise ValueError("No Hodram-three-blocks typed menu records authorized")
    return d
