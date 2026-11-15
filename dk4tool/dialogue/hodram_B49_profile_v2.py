"""Exact Hodram B49 clean/current records, original progressive/FE consumers and measured runtime."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path("translations/hodram_B49_native_contract_v2.json")
CONTRACT_SHA="320692ec559ec574dcefd755acdfa918d4ec811809e9159f461dccadec34d422"
ARM9_SHA="12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b"
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError("Frozen Hodram-B49 contract changed")
    d=json.loads(raw)
    for p,h in d["dependencies"].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError("Native dependency changed:"+p)
    if len(d["record_bindings"])!=14 or len(d["choice_bindings"])!=2 or d["physical_native_rows_per_page"]!=4 or d["complete_native_pages"]!=14:
        raise ValueError("Complete14-speech/14-page/two-choice contract required")
    if d["measured_macro_ascii_lengths"]!={"FI":6,"FA":9,"FO":15} or d["source_macro_counts"]!={"FI":0,"FA":0,"FO":0}:
        raise ValueError("Exact measured Hodram macros required")
    return d
def expected_profile(ident,consumer=None):
    d=contract()
    if ident not in d["record_bindings"]:raise ValueError("Unreviewed Hodram-B49 paragraph")
    r=d["record_bindings"][ident];wanted="FE-paper" if r["source_selector"]==254 else "progressive"
    if consumer is not None and consumer!=wanted:raise ValueError("Original Hodram-B49 consumer required")
    base=get_dialogue_profile("hodram-story-live")
    if base.window_width_px!=216 or base.max_lines!=4 or base.macro_ascii_lengths!={"FI":6,"FA":9,"FO":15} or base.literal_prefix_policy!="forbid":
        raise ValueError("Original global Hodram profile required")
    return replace(base,name="Hodram-B49-source-bound-v1:"+ident,max_lines=r["maximum_total_rows"],
        macro_widths={"FI":36,"FA":54,"FO":90,"I":12},macro_ascii_lengths={"FI":6,"FA":9,"FO":15},
        leading_speaker_bytes=frozenset({254} if wanted=="FE-paper" else {r["source_selector"]}),
        literal_prefix_policy="native-guard-v255",
        metrics_source="Exact complete registeredV8377/captain1 runtime andsource1/2/FE preambles. Full216usablewidth,13progressive pages plusoriginalFE228x48/288stride/6x12/16pitch;FI6FA9FO15,zero source macros. Fourteen complete native/stored pages,seven line-count infos,zero warnings/waivers. Two exact source-bound ellipses andone source-qualified New/World ordinaryboundary;no global exceptions. Actual69868frames includes20002whole-script initialized fixtures,40004bounded-tail choices and9862focusedFE frames. All14unique speech displays/bothmenus passcompleteglyphs,owned surfaces,headers/absentFEheader andnormalreturns. Measured timing,boundary/final PRNG andlaterRGB differences remain;five sampled components/actors match. Not natural activation,earned inventory/trade eligibility,original location,customnames,fullroute,hardware,everyframe causality orfuture-outcome equivalence.")
def profile_for(arm,block,ident,file_path,consumer=None):
    d=contract()
    if ident not in d["record_bindings"]:raise ValueError("Unreviewed Hodram-B49 paragraph")
    r=d["record_bindings"][ident]
    if sha(arm)!=ARM9_SHA or file_path!=r["file_path"] or sha(block) not in r["source_block_hashes"]:
        raise ValueError("Exact file-qualified Hodram-B49 source/current block and12eb runtime required")
    return expected_profile(ident,consumer)
def validate_runtime(image):
    d=contract()
    for path,digest in d["runtime_component_hashes"].items():
        if sha(image.read_file(path))!=digest:raise ValueError("Exact Hodram-B49 runtime component required:"+path)
    return d


def validate_approved_batch(doc):
    from dk4tool.dialogue.review import validate_natural_dialogue_batch
    d=contract()
    for key,value in d["batch_binding"].items():
        if doc.get(key)!=value:raise ValueError("Exact Hodram-B49 approved batch metadata required:"+key)
    validate_natural_dialogue_batch(doc)
    choice_doc={**doc,"records":doc.get("typed_choice_records")}
    validate_natural_dialogue_batch(choice_doc)
    for field,bindings in [("records",d["record_bindings"]),("typed_choice_records",d["choice_bindings"])]:
        rows=doc.get(field)
        if not isinstance(rows,list) or [r.get("id") for r in rows if isinstance(r,dict)]!=list(bindings):
            raise ValueError("Exact complete ordered Hodram-B49 approved records required:"+field)
        for row in rows:
            b=bindings[row["id"]]
            if any(row.get(k)!=v for k,v in b["approved_fields"].items()):
                raise ValueError("Exact Hodram-B49 approved prose/source/context required:"+row["id"])
            if not isinstance(row.get("review"),dict) or not all(row["review"].get(g) is True for g in d["review_gates"]):
                raise ValueError("All five individual Hodram-B49 gates required:"+row["id"])
    return d
