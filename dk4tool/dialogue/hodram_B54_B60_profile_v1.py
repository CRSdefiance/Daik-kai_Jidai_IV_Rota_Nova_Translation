"""Exact Hodram B54-B60 clean/current records, original progressive/FE consumers and measured runtime."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path("translations/hodram_B54_B60_native_contract_v1.json")
CONTRACT_SHA="da458715d0f6962e46e53cc7f32e234c58ca125b558cdcaae22a0014d6850395"
ARM9_SHA="12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b"
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError("Frozen Hodram-B54-B60 contract changed")
    d=json.loads(raw)
    for p,h in d["dependencies"].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError("Native dependency changed:"+p)
    if len(d["record_bindings"])!=82 or d["choice_bindings"] or d["physical_native_rows_per_page"]!=4 or d["complete_native_pages"]!=85:
        raise ValueError("Complete 82-paragraph/85-page/no-menu contract required")
    if d["measured_macro_ascii_lengths"]!={"FI":6,"FA":9,"FO":15} or d["source_macro_counts"]!={"FI":3,"FA":4,"FO":0}:
        raise ValueError("Exact measured Hodram macros required")
    return d
def expected_profile(ident,consumer=None):
    d=contract()
    if ident not in d["record_bindings"]:raise ValueError("Unreviewed Hodram-B54-B60 paragraph")
    r=d["record_bindings"][ident];wanted="FE-paper" if r["source_selector"]==254 else "progressive"
    if consumer is not None and consumer!=wanted:raise ValueError("Original Hodram-B54-B60 consumer required")
    base=get_dialogue_profile("hodram-story-live")
    if base.window_width_px!=216 or base.max_lines!=4 or base.macro_ascii_lengths!={"FI":6,"FA":9,"FO":15} or base.literal_prefix_policy!="forbid":
        raise ValueError("Original global Hodram profile required")
    return replace(base,name="Hodram-B54-B60-source-bound-v1:"+ident,max_lines=r["maximum_total_rows"],
        macro_widths={"FI":36,"FA":54,"FO":90,"I":12},macro_ascii_lengths={"FI":6,"FA":9,"FO":15},
        leading_speaker_bytes=frozenset({r["source_selector"]}),
        literal_prefix_policy="native-guard-v255",
        metrics_source="Exact registeredV8778/captain1;82original preambles/152commands/seven blocks/24relatives/sixqueries/33nonprosecontrols/seven distinct fullnormalends andtails. Full216px usable width,84progressive pages plusoneFE228x48/288stride/6x12/16pitch. Three English records use two pages. FI6/FA9/FO15 withsourceFI3/FA4/FO0;source-captain virtual slots prove given/surname semantics. Six exact source-bound ellipsis/question reactions.24original QAinfos,zero errors/warnings/waivers. Forty compiler-owned parity tails preserve the85viewed fullnative planes. Independent block/archive/wholeNDS inverses;325fresh loads,14fresh plus636exactreused parentmodes;source/current/finalrefs andunchanged caller units bound. Twelve initialized whole-script coldboots116012frames/580holds/129pageoccurrences observe63unique utterances;19remainoffline including18B58conditionals andB55. B56 actual FE contexts/palette/bitmap/VRAM/RGB andabsentheader pass. B59 originalresource show-hide sequence andall7corresponding upperpanels match. B60 focused14002frames shares theoriginal prefix throughA6400;81callbacks beforeA6640 matchtheir ownlongrun fullmemory/CPU/TCM. At7001 all5sampled components/wholeactors/captain/calendar match. All long/focused duration,RNG,RGB,followingcommand andB60lateactor differences remain;no immediate-return mainRAM snapshot,causal diagnosis orfuture equivalence claim. Ten progressive labels retain source/contextual names;8actual,20and113offline here. Geronimo/Alonso sharedde/fullcatalogue/all207/customnames/widercontexts remainopen. No natural eventactivation,original location,earned chronology,forced predicates/roster/flags/results,fullroute orhardware claim.")
def profile_for(arm,block,ident,file_path,consumer=None):
    d=contract()
    if ident not in d["record_bindings"]:raise ValueError("Unreviewed Hodram-B54-B60 paragraph")
    r=d["record_bindings"][ident]
    if sha(arm)!=ARM9_SHA or file_path!=r["file_path"] or sha(block) not in r["source_block_hashes"]:
        raise ValueError("Exact file-qualified Hodram-B54-B60 source/current block and12eb runtime required")
    return expected_profile(ident,consumer)
def validate_runtime(image):
    d=contract()
    for path,digest in d["runtime_component_hashes"].items():
        if sha(image.read_file(path))!=digest:raise ValueError("Exact Hodram-B54-B60 runtime component required:"+path)
    return d


def validate_approved_batch(doc):
    from dk4tool.dialogue.review import validate_natural_dialogue_batch
    d=contract()
    if set(doc)!=set(d["batch_binding"])|{"records"}:raise ValueError("Exact complete approved batch keys required")
    for key,value in d["batch_binding"].items():
        if doc.get(key)!=value:raise ValueError("Exact Hodram-B54-B60 approved batch metadata required:"+key)
    validate_natural_dialogue_batch(doc)
    rows=doc.get("records")
    if not isinstance(rows,list) or [r.get("id") for r in rows if isinstance(r,dict)]!=list(d["record_bindings"]):
        raise ValueError("Exact complete ordered Hodram-B54-B60 approved records required")
    for row in rows:
        b=d["record_bindings"][row["id"]]
        if row!=b["approved_fields"]:
            raise ValueError("Exact Hodram-B54-B60 approved prose/source/context/waiver required:"+row["id"])
        if not isinstance(row.get("review"),dict) or not all(row["review"].get(g) is True for g in d["review_gates"]):
            raise ValueError("All five individual Hodram-B54-B60 gates required:"+row["id"])
    if doc.get("typed_choice_records"):
        raise ValueError("No Hodram-B54-B60 typed menu records authorized")
    return d
