"""Exact Rafael B50 clean/current records, original progressive/FE consumers and measured runtime."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path("translations/rafael_B50_native_contract_v1.json")
CONTRACT_SHA="1a8751c931336a73ddea449bd671eaafb1291e2d4b75d4be9a46d0b912e44872"
ARM9_SHA="2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a"
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError("Frozen Rafael-B50 contract changed")
    d=json.loads(raw)
    for p,h in d["dependencies"].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError("Native dependency changed:"+p)
    if len(d["record_bindings"])!=28 or d["choice_bindings"] or d["physical_native_rows_per_page"]!=4 or d["complete_native_pages"]!=28:
        raise ValueError("Complete twenty-eight-paragraph/twenty-eight-page/no-menu contract required")
    if d["measured_macro_ascii_lengths"]!={"FI":6,"FA":6,"FO":10} or d["source_macro_counts"]!={"FI":1,"FA":2,"FO":0}:
        raise ValueError("Exact measured Rafael macros required")
    return d
def expected_profile(ident,consumer=None):
    d=contract()
    if ident not in d["record_bindings"]:raise ValueError("Unreviewed Rafael-B50 paragraph")
    r=d["record_bindings"][ident];wanted="FE-paper" if r["source_selector"]==254 else "progressive"
    if consumer is not None and consumer!=wanted:raise ValueError("Original Rafael-B50 consumer required")
    base=get_dialogue_profile("raphael-story-live")
    if base.window_width_px!=216 or base.max_lines!=4 or base.macro_ascii_lengths["FI"]!=7 or base.literal_prefix_policy!="forbid":
        raise ValueError("Original global Rafael profile required")
    return replace(base,name="Rafael-B50-source-bound-v1:"+ident,max_lines=r["maximum_total_rows"],
        macro_widths={"FI":36,"FA":36,"FO":60,"I":12},macro_ascii_lengths={"FI":6,"FA":6,"FO":10},
        leading_speaker_bytes=frozenset({254} if wanted=="FE-paper" else {0,2,9}),
        literal_prefix_policy="native-guard-v255",
        metrics_source="Exact B50/current2b6:216px usable text/four physical rows;all28 progressive paragraphs use one216x64 page. Source00/02/09 ten source00 objects/three selectors preserve complete preambles andbody NUL guard. Native FI6/FA6/FO10 withsourceFI1/FA2/noFO,full compiled/stored andpaired actual glyph/name masks. All28 speeches,three names and37 original commands actually observed;Red Dye picture,4821/A000/4720/4681 andnormalreturn pass. Two exact weak-boundary exceptions retain all original diagnostics and18infos. First seven focused sampled model/object/actor states match through postreturn/tutorial/departure;later underway models/actors/towns and17of87RGB samples differ. Every timing/RNG/component/byte/calendar/RGB limit retained for later re-audit;no future simulation equivalence orglobal font/profile/guard/weak-rule change.")
def profile_for(arm,block,ident,file_path,consumer=None):
    d=contract()
    if ident not in d["record_bindings"]:raise ValueError("Unreviewed Rafael-B50 paragraph")
    r=d["record_bindings"][ident]
    if sha(arm)!=ARM9_SHA or file_path!=r["file_path"] or sha(block) not in r["source_block_hashes"]:
        raise ValueError("Exact file-qualified B50 source/current block and2b6 runtime required")
    return expected_profile(ident,consumer)
def validate_runtime(image):
    d=contract()
    for path,digest in d["runtime_component_hashes"].items():
        if sha(image.read_file(path))!=digest:raise ValueError("Exact Rafael-B50 runtime component required:"+path)
    return d


def validate_approved_batch(doc):
    from dk4tool.dialogue.review import validate_natural_dialogue_batch
    d=contract()
    for key,value in d["batch_binding"].items():
        if doc.get(key)!=value:raise ValueError("Exact B50 approved batch metadata required:"+key)
    validate_natural_dialogue_batch(doc)
    rows=doc.get("records")
    if not isinstance(rows,list) or [r.get("id") for r in rows if isinstance(r,dict)]!=list(d["record_bindings"]):
        raise ValueError("Exact complete ordered B50 approved records required")
    for row in rows:
        b=d["record_bindings"][row["id"]]
        if any(row.get(k)!=v for k,v in b["approved_fields"].items()):
            raise ValueError("Exact B50 approved prose/source/context/waiver required:"+row["id"])
        if not isinstance(row.get("review"),dict) or not all(row["review"].get(g) is True for g in d["review_gates"]):
            raise ValueError("All five individual B50 gates required:"+row["id"])
    if doc.get("typed_choice_records"):
        raise ValueError("No B50 typed menu records authorized")
    return d
