"""Exact Hodram B52 clean/current records, original progressive/FE consumers and measured runtime."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path("translations/hodram_B52_native_contract_v1.json")
CONTRACT_SHA="212a3c64e97465090d6483e50cd1ebec77115b3612562c18e95d9fffeb377e0b"
ARM9_SHA="12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b"
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError("Frozen Hodram-B52 contract changed")
    d=json.loads(raw)
    for p,h in d["dependencies"].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError("Native dependency changed:"+p)
    if len(d["record_bindings"])!=3 or len(d["choice_bindings"])!=2 or d["physical_native_rows_per_page"]!=4 or d["complete_native_pages"]!=3:
        raise ValueError("Complete3-speech/3-page/two-choice contract required")
    if d["measured_macro_ascii_lengths"]!={"FI":6,"FA":9,"FO":15} or d["source_macro_counts"]!={"FI":0,"FA":0,"FO":0}:
        raise ValueError("Exact measured Hodram macros required")
    return d
def expected_profile(ident,consumer=None):
    d=contract()
    if ident not in d["record_bindings"]:raise ValueError("Unreviewed Hodram-B52 paragraph")
    r=d["record_bindings"][ident];wanted="FE-paper" if r["source_selector"]==254 else "progressive"
    if consumer is not None and consumer!=wanted:raise ValueError("Original Hodram-B52 consumer required")
    base=get_dialogue_profile("hodram-story-live")
    if base.window_width_px!=216 or base.max_lines!=4 or base.macro_ascii_lengths!={"FI":6,"FA":9,"FO":15} or base.literal_prefix_policy!="forbid":
        raise ValueError("Original global Hodram profile required")
    return replace(base,name="Hodram-B52-source-bound-v1:"+ident,max_lines=r["maximum_total_rows"],
        macro_widths={"FI":36,"FA":54,"FO":90,"I":12},macro_ascii_lengths={"FI":6,"FA":9,"FO":15},
        leading_speaker_bytes=frozenset({254} if wanted=="FE-paper" else {r["source_selector"]}),
        literal_prefix_policy="native-guard-v255",
        metrics_source="Exact registeredV8609/captain1 runtime, original actor113 six-byte preambles and FI6/FA9/FO15 with zero source macros. Full216px width, three complete progressive/stored singlepages, one original line-count info, zero warnings/waivers; no authored ordinary breaks. Fourteen commands/four relatives/zero queries/four opaque controls, two typed choices and distinct preserving/clearing ends are bound. Six initialized cold boots50406frames/138complete body-name holds/12page occurrences cover all3speeches and both ordinary choices/end kinds. Twelve actual menus/24captions prove visible glyphs/centering/highlights; backing bounds remain offline, no new live owner/RAM/VRAM/palette/backing identity. Long withdrawal differs in components/actors/calendar/PRNG and46of93RGBpairs; long opposition matches components/actors but differs inPRNG/13of93RGBpairs. Focused withdrawal exact input prefix ends after4484: sampled components/actors/seed/calendar and13RGBpairs match, with no following commands. Preserve all command/menu timing and later differences; no causal explanation, future simulation equivalence, natural event activation/location/earned progress, actual cancel availability, fullroute orhardware claim.")
def profile_for(arm,block,ident,file_path,consumer=None):
    d=contract()
    if ident not in d["record_bindings"]:raise ValueError("Unreviewed Hodram-B52 paragraph")
    r=d["record_bindings"][ident]
    if sha(arm)!=ARM9_SHA or file_path!=r["file_path"] or sha(block) not in r["source_block_hashes"]:
        raise ValueError("Exact file-qualified Hodram-B52 source/current block and12eb runtime required")
    return expected_profile(ident,consumer)
def validate_runtime(image):
    d=contract()
    for path,digest in d["runtime_component_hashes"].items():
        if sha(image.read_file(path))!=digest:raise ValueError("Exact Hodram-B52 runtime component required:"+path)
    return d


def validate_approved_batch(doc):
    from dk4tool.dialogue.review import validate_natural_dialogue_batch
    d=contract()
    for key,value in d["batch_binding"].items():
        if doc.get(key)!=value:raise ValueError("Exact Hodram-B52 approved batch metadata required:"+key)
    validate_natural_dialogue_batch(doc)
    choice_doc={**doc,"records":doc.get("typed_choice_records")}
    validate_natural_dialogue_batch(choice_doc)
    for field,bindings in [("records",d["record_bindings"]),("typed_choice_records",d["choice_bindings"])]:
        rows=doc.get(field)
        if not isinstance(rows,list) or [r.get("id") for r in rows if isinstance(r,dict)]!=list(bindings):
            raise ValueError("Exact complete ordered Hodram-B52 approved records required:"+field)
        for row in rows:
            b=bindings[row["id"]]
            if any(row.get(k)!=v for k,v in b["approved_fields"].items()):
                raise ValueError("Exact Hodram-B52 approved prose/source/context required:"+row["id"])
            if not isinstance(row.get("review"),dict) or not all(row["review"].get(g) is True for g in d["review_gates"]):
                raise ValueError("All five individual Hodram-B52 gates required:"+row["id"])
    return d
