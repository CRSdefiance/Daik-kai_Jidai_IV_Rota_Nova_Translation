"""Exact Rafael B46 clean/current records, original progressive/FE consumers and measured runtime."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path("translations/rafael_B46_native_contract_v1.json")
CONTRACT_SHA="395643ff65ddc88453c40432e75043ab5883ecc51ef68f56524450adb16a745d"
ARM9_SHA="2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a"
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError("Frozen Rafael-B46 contract changed")
    d=json.loads(raw)
    for p,h in d["dependencies"].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError("Native dependency changed:"+p)
    if len(d["record_bindings"])!=24 or len(d["choice_bindings"])!=2 or d["physical_native_rows_per_page"]!=4 or d["complete_native_pages"]!=24:
        raise ValueError("Complete24-speech/two-choice contract required")
    if d["measured_macro_ascii_lengths"]!={"FI":6,"FA":6,"FO":10} or d["source_macro_counts"]!={"FI":0,"FA":0,"FO":0}:
        raise ValueError("Exact measured Rafael macros required")
    return d
def expected_profile(ident,consumer=None):
    d=contract()
    if ident not in d["record_bindings"]:raise ValueError("Unreviewed Rafael-B46 paragraph")
    r=d["record_bindings"][ident];wanted="FE-paper" if r["source_selector"]==254 else "progressive"
    if consumer is not None and consumer!=wanted:raise ValueError("Original Rafael-B46 consumer required")
    base=get_dialogue_profile("raphael-story-live")
    if base.window_width_px!=216 or base.max_lines!=4 or base.macro_ascii_lengths["FI"]!=7 or base.literal_prefix_policy!="forbid":
        raise ValueError("Original global Rafael profile required")
    return replace(base,name="Rafael-B46-source-bound-v1:"+ident,max_lines=4,
        macro_widths={"FI":36,"FA":36,"FO":60,"I":12},macro_ascii_lengths={"FI":6,"FA":6,"FO":10},
        leading_speaker_bytes=frozenset({254} if wanted=="FE-paper" else {0,5,6}),
        literal_prefix_policy="native-guard-v255",
        metrics_source="Exact B46/current2b6:216px usable text/four physical rows;original progressive216x64 or FE228x48 logical/228x64 physical. Source00 actor stays in complete native preamble;body NUL guard unchanged. Native FI6/FA6/FO10,complete compiled/stored planes andpaired actual masks verified. No global font,profile,guard orweak-rule change. Menu highlight-off phase and later measured simulation/calendar/RGB/RNG differences retained;no full causal orfuture-state equivalence claim.")
def profile_for(arm,block,ident,file_path,consumer=None):
    d=contract()
    if ident not in d["record_bindings"]:raise ValueError("Unreviewed Rafael-B46 paragraph")
    r=d["record_bindings"][ident]
    if sha(arm)!=ARM9_SHA or file_path!=r["file_path"] or sha(block) not in r["source_block_hashes"]:
        raise ValueError("Exact file-qualified B46 source/current block and2b6 runtime required")
    return expected_profile(ident,consumer)
def validate_runtime(image):
    d=contract()
    for path,digest in d["runtime_component_hashes"].items():
        if sha(image.read_file(path))!=digest:raise ValueError("Exact Rafael-B46 runtime component required:"+path)
    return d


def validate_approved_batch(doc):
    from dk4tool.dialogue.review import validate_natural_dialogue_batch
    d=contract()
    for key,value in d["batch_binding"].items():
        if doc.get(key)!=value:raise ValueError("Exact B46 approved batch metadata required:"+key)
    validate_natural_dialogue_batch(doc)
    choice_doc={**doc,"records":doc.get("typed_choice_records")}
    validate_natural_dialogue_batch(choice_doc)
    for field,bindings in [("records",d["record_bindings"]),("typed_choice_records",d["choice_bindings"])]:
        rows=doc.get(field)
        if not isinstance(rows,list) or [r.get("id") for r in rows if isinstance(r,dict)]!=list(bindings):
            raise ValueError("Exact complete ordered B46 approved records required:"+field)
        for row in rows:
            b=bindings[row["id"]]
            if any(row.get(k)!=v for k,v in b["approved_fields"].items()):
                raise ValueError("Exact B46 approved prose/source/context required:"+row["id"])
            if not isinstance(row.get("review"),dict) or not all(row["review"].get(g) is True for g in d["review_gates"]):
                raise ValueError("All five individual B46 gates required:"+row["id"])
    return d
