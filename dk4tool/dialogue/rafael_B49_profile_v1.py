"""Exact Rafael B49 clean/current records, original progressive/FE consumers and measured runtime."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path("translations/rafael_B49_native_contract_v1.json")
CONTRACT_SHA="6955020915e2cfbd1ceabedd14c7089c698d93abe9f77426a1664da5e79eeb50"
ARM9_SHA="2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a"
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError("Frozen Rafael-B49 contract changed")
    d=json.loads(raw)
    for p,h in d["dependencies"].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError("Native dependency changed:"+p)
    if len(d["record_bindings"])!=61 or d["choice_bindings"] or d["physical_native_rows_per_page"]!=4 or d["complete_native_pages"]!=61:
        raise ValueError("Complete sixty-one-paragraph/sixty-one-page/no-menu contract required")
    if d["measured_macro_ascii_lengths"]!={"FI":6,"FA":6,"FO":10} or d["source_macro_counts"]!={"FI":2,"FA":0,"FO":0}:
        raise ValueError("Exact measured Rafael macros required")
    return d
def expected_profile(ident,consumer=None):
    d=contract()
    if ident not in d["record_bindings"]:raise ValueError("Unreviewed Rafael-B49 paragraph")
    r=d["record_bindings"][ident];wanted="FE-paper" if r["source_selector"]==254 else "progressive"
    if consumer is not None and consumer!=wanted:raise ValueError("Original Rafael-B49 consumer required")
    base=get_dialogue_profile("raphael-story-live")
    if base.window_width_px!=216 or base.max_lines!=4 or base.macro_ascii_lengths["FI"]!=7 or base.literal_prefix_policy!="forbid":
        raise ValueError("Original global Rafael profile required")
    return replace(base,name="Rafael-B49-source-bound-v1:"+ident,max_lines=r["maximum_total_rows"],
        macro_widths={"FI":36,"FA":36,"FO":60,"I":12},macro_ascii_lengths={"FI":6,"FA":6,"FO":10},
        leading_speaker_bytes=frozenset({254} if wanted=="FE-paper" else {0,2,4,5,6,8,9}),
        literal_prefix_policy="native-guard-v255",
        metrics_source="Exact B49/current2b6:216px usable text/four physical rows; all61 progressive paragraphs use one216x64 page. Source00/02/09 and all seven selectors remain original preambles; body NUL guard unchanged. Native FI6/FA6/FO10,twoFI,complete compiled/stored planes andpaired actual masks verified. Coherent phrase preferences preserve all words androw counts. Three exact source/text/compiled/line-bound weak endings retain all original warnings and22infos. Four actual complete names,three native-only headers,50actual speeches per language and11native-only conditionals remain scoped. Timing,RNG andlater RGB differences retained despite equal sampled final components/actor. No full simulation equivalence or global font/profile/guard/weak-rule change.")
def profile_for(arm,block,ident,file_path,consumer=None):
    d=contract()
    if ident not in d["record_bindings"]:raise ValueError("Unreviewed Rafael-B49 paragraph")
    r=d["record_bindings"][ident]
    if sha(arm)!=ARM9_SHA or file_path!=r["file_path"] or sha(block) not in r["source_block_hashes"]:
        raise ValueError("Exact file-qualified B49 source/current block and2b6 runtime required")
    return expected_profile(ident,consumer)
def validate_runtime(image):
    d=contract()
    for path,digest in d["runtime_component_hashes"].items():
        if sha(image.read_file(path))!=digest:raise ValueError("Exact Rafael-B49 runtime component required:"+path)
    return d


def validate_approved_batch(doc):
    from dk4tool.dialogue.review import validate_natural_dialogue_batch
    d=contract()
    for key,value in d["batch_binding"].items():
        if doc.get(key)!=value:raise ValueError("Exact B49 approved batch metadata required:"+key)
    validate_natural_dialogue_batch(doc)
    rows=doc.get("records")
    if not isinstance(rows,list) or [r.get("id") for r in rows if isinstance(r,dict)]!=list(d["record_bindings"]):
        raise ValueError("Exact complete ordered B49 approved records required")
    for row in rows:
        b=d["record_bindings"][row["id"]]
        if any(row.get(k)!=v for k,v in b["approved_fields"].items()):
            raise ValueError("Exact B49 approved prose/source/context/waiver required:"+row["id"])
        if not isinstance(row.get("review"),dict) or not all(row["review"].get(g) is True for g in d["review_gates"]):
            raise ValueError("All five individual B49 gates required:"+row["id"])
    if doc.get("typed_choice_records"):
        raise ValueError("No B49 typed menu records authorized")
    return d
