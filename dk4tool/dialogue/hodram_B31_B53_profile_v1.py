"""Exact Hodram B31/B53 clean/current records, original progressive/FE consumers and measured runtime."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path("translations/hodram_B31_B53_native_contract_v1.json")
CONTRACT_SHA="5279862c16ef0dd93d7dc8703f7a54c0500359003993caed1b32a06d16c20f0b"
ARM9_SHA="12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b"
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError("Frozen Hodram-B31-B53 contract changed")
    d=json.loads(raw)
    for p,h in d["dependencies"].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError("Native dependency changed:"+p)
    if len(d["record_bindings"])!=3 or d["choice_bindings"] or d["physical_native_rows_per_page"]!=4 or d["complete_native_pages"]!=3:
        raise ValueError("Complete three-paragraph/three-page/no-menu contract required")
    if d["measured_macro_ascii_lengths"]!={"FI":6,"FA":9,"FO":15} or d["source_macro_counts"]!={"FI":0,"FA":0,"FO":0}:
        raise ValueError("Exact measured Hodram macros required")
    return d
def expected_profile(ident,consumer=None):
    d=contract()
    if ident not in d["record_bindings"]:raise ValueError("Unreviewed Hodram-B31-B53 paragraph")
    r=d["record_bindings"][ident];wanted="FE-paper" if r["source_selector"]==254 else "progressive"
    if consumer is not None and consumer!=wanted:raise ValueError("Original Hodram-B31-B53 consumer required")
    base=get_dialogue_profile("hodram-story-live")
    if base.window_width_px!=216 or base.max_lines!=4 or base.macro_ascii_lengths!={"FI":6,"FA":9,"FO":15} or base.literal_prefix_policy!="forbid":
        raise ValueError("Original global Hodram profile required")
    return replace(base,name="Hodram-B31-B53-source-bound-v1:"+ident,max_lines=r["maximum_total_rows"],
        macro_widths={"FI":36,"FA":54,"FO":90,"I":12},macro_ascii_lengths={"FI":6,"FA":9,"FO":15},
        leading_speaker_bytes=frozenset({r["source_selector"]}),
        literal_prefix_policy="native-guard-v255",
        metrics_source="Exact registeredV8704/captain1 runtime andoriginal22/71 six-byte preambles. Full216px width, three native/stored singlepages, FI6/FA9/FO15 withzero source macros,zero QAissues/warnings/waivers. Two complete blocks18commands/four relatives/one rawquery/eight opaquecontrols/two normalends,independent block/archive/wholeNDS inverses,325loads650parentmodes andcomplete unchanged caller census arebound. Four initialized whole-block coldboots24004frames/76complete body-name holds/fourpageoccurrences verify long B31 andB53warning;shortB31 remains offline-only,never force selected. Actual normalreturns B31[0,1]at4016 andB53[0,0]at4013 matchbothlanguages. Normalend preserves the existing parserresult secondword independently ofinterpreter r3;50source seededends and50unchanged callerfragments bind separatechannels. Only three decodedlength differences remain;commandduration/UIrequest/boundaryRNG/followingcommands match. Allfive finalcomponents/wholeactors/captain1/rawcalendar/finalseed3325064553 and68laterRGBpairs matchthrough6001frames. Actor34 source getters include the actual Fazul middlefield;retain sourced components/order andexisting mixedwidth storage. Actual progressive34/113 headers areverified;fullcatalogueUI/all207/customnames remainopen. No natural eventactivation,original location,earnedchronology,opaque effectsemantic invention,everyframecausality,broad future simulation,fullroute orhardware claim.")
def profile_for(arm,block,ident,file_path,consumer=None):
    d=contract()
    if ident not in d["record_bindings"]:raise ValueError("Unreviewed Hodram-B31-B53 paragraph")
    r=d["record_bindings"][ident]
    if sha(arm)!=ARM9_SHA or file_path!=r["file_path"] or sha(block) not in r["source_block_hashes"]:
        raise ValueError("Exact file-qualified Hodram-B31-B53 source/current block and12eb runtime required")
    return expected_profile(ident,consumer)
def validate_runtime(image):
    d=contract()
    for path,digest in d["runtime_component_hashes"].items():
        if sha(image.read_file(path))!=digest:raise ValueError("Exact Hodram-B31-B53 runtime component required:"+path)
    return d


def validate_approved_batch(doc):
    from dk4tool.dialogue.review import validate_natural_dialogue_batch
    d=contract()
    if set(doc)!=set(d["batch_binding"])|{"records"}:raise ValueError("Exact complete approved batch keys required")
    for key,value in d["batch_binding"].items():
        if doc.get(key)!=value:raise ValueError("Exact Hodram-B31-B53 approved batch metadata required:"+key)
    validate_natural_dialogue_batch(doc)
    rows=doc.get("records")
    if not isinstance(rows,list) or [r.get("id") for r in rows if isinstance(r,dict)]!=list(d["record_bindings"]):
        raise ValueError("Exact complete ordered Hodram-B31-B53 approved records required")
    for row in rows:
        b=d["record_bindings"][row["id"]]
        if row!=b["approved_fields"]:
            raise ValueError("Exact Hodram-B31-B53 approved prose/source/context/waiver required:"+row["id"])
        if not isinstance(row.get("review"),dict) or not all(row["review"].get(g) is True for g in d["review_gates"]):
            raise ValueError("All five individual Hodram-B31-B53 gates required:"+row["id"])
    if doc.get("typed_choice_records"):
        raise ValueError("No Hodram-B31-B53 typed menu records authorized")
    return d
