"""Exact Gerhard surname clean/current records, original progressive/FE consumers and measured runtime."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path("translations/gerhard_surname_native_contract_v1.json")
CONTRACT_SHA="dad0ce0c4b6016cd29163caf8d36ed922123a6b920a20370b35b96db3d8798a7"
ARM9_SHA="2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a"
TARGET_ARM9_SHA="12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b"
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError("Frozen Gerhard-surname contract changed")
    d=json.loads(raw)
    for p,h in d["dependencies"].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError("Native dependency changed:"+p)
    if len(d["record_bindings"])!=5 or d["choice_bindings"] or d["physical_native_rows_per_page"]!=4 or d["complete_native_pages"]!=5:
        raise ValueError("Complete five-sparse-paragraph/five-page/no-new-menu contract required")
    if d["measured_macro_ascii_lengths"]!={"FI":3,"FA":5,"FO":9} or d["source_macro_counts"]!={"FI":1,"FA":0,"FO":0}:
        raise ValueError("Exact measured Rafael macros required")
    return d
def expected_profile(ident,consumer=None):
    d=contract()
    if ident not in d["record_bindings"]:raise ValueError("Unreviewed Gerhard-surname paragraph")
    r=d["record_bindings"][ident];wanted="FE-paper" if r["source_selector"]==254 else "progressive"
    if consumer is not None and consumer!=wanted:raise ValueError("Original Gerhard-surname consumer required")
    base=get_dialogue_profile("lil-story-deep-route-live")
    if base.window_width_px!=216 or base.max_lines!=4 or base.macro_ascii_lengths["FI"]!=3 or base.literal_prefix_policy!="forbid":
        raise ValueError("Original global Rafael profile required")
    return replace(base,name="Gerhard-surname-source-bound-v1:"+ident,max_lines=r["maximum_total_rows"],
        macro_widths={"FI":18,"FA":30,"FO":54,"I":12},macro_ascii_lengths={"FI":3,"FA":5,"FO":9},
        leading_speaker_bytes=frozenset({254} if wanted=="FE-paper" else {1,9,16}),
        literal_prefix_policy="native-guard-v255",
        metrics_source="Exact sparse Gerhard surname correction:five SC2B27/B74 progressive speeches,oneowned12-byte ARM9 name,Blades8 protected. Lil3/Argot5/ArgotCo9,FI1/noFAFO,216px/6pxASCII/12pxCP932/fourrows,complete native/stored/actual glyphs andnames. WholeB27 actual35of51 andcaptain0laterSC0B44 fixturelimit;wholeB74 actual75of79/defaultchoice0;introdisplay8 bypassesoutercondition explicitly. Thirty bodyholds/262nameholds/117sceneRGBpairs;alltiming,RNG,component,byte,calendar,RGB andfixturelimits retained. Fullsourcecontrols/207names/fullgoal remainseparate;no globalfont/profile/guard change.")
def profile_for(arm,block,ident,file_path,consumer=None):
    d=contract()
    if ident not in d["record_bindings"]:raise ValueError("Unreviewed Gerhard-surname paragraph")
    r=d["record_bindings"][ident]
    if sha(arm) not in [ARM9_SHA,TARGET_ARM9_SHA] or file_path!=r["file_path"] or sha(block) not in r["source_block_hashes"]:
        raise ValueError("Exact file-qualified B50 source/current block and2b6 runtime required")
    return expected_profile(ident,consumer)
def validate_runtime(image,phase="parent"):
    d=contract()
    if phase not in ["parent","target"]:raise ValueError("Exact parent ortarget runtime phase required")
    for path,digest in d["runtime_component_hashes" if phase=="parent" else "target_runtime_component_hashes"].items():
        if sha(image.read_file(path))!=digest:raise ValueError("Exact Gerhard-surname runtime component required:"+path)
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
        raise ValueError("No new surname-revisit typed menu records authorized")
    validate_name_records(doc)
    return d

def validate_name_records(doc):
    d=contract();rows=doc.get("name_records")
    if not isinstance(rows,list) or len(rows)!=1 or not isinstance(rows[0],dict):
        raise ValueError("Exactly one owned Gerhard surname record required")
    row=rows[0];binding=d["name_bindings"][0]
    if not isinstance(row.get("review"),dict) or not all(row["review"].get(g) is True for g in d["review_gates"]):
        raise ValueError("All five individual Gerhard name gates required")
    if any(row.get(k)!=v for k,v in binding["approved_fields"].items()):
        raise ValueError("Exact approved surname source/context/owned12-byte span required")
    return d

def validate_name_transition(source,target):
    d=contract();span=d["owned_name_span"];at=span["offset"];old=bytes.fromhex(span["current_hex"]);new=bytes.fromhex(span["target_hex"])
    if not isinstance(source,bytes) or not isinstance(target,bytes) or len(source)!=len(target):
        raise ValueError("Complete equal-size ARM9 byte strings required")
    if span["bytes"]!=12 or len(old)!=12 or len(new)!=12 or source[at:at+12]!=old or target[at:at+12]!=new:
        raise ValueError("Exact terminated owned12-byte surname replacement required")
    if source[:at]!=target[:at] or source[at+12:]!=target[at+12:]:
        raise ValueError("Unowned ARM9 bytes or protected Blades changed")
    neighbor=d["protected_neighbor"];begin=neighbor["offset"];raw=bytes.fromhex(neighbor["current_hex"])
    if neighbor["bytes"]!=8 or source[begin:begin+8]!=raw or target[begin:begin+8]!=raw or raw!=b"Blades\0\0":
        raise ValueError("Exact independently referenced Blades neighbor required")
    for ref in d["name_andneighbor_pointer_references"]:
        field=ref["pointer_field_offset"];value=bytes.fromhex(ref["field_bytes"])
        if source[field:field+4]!=value or target[field:field+4]!=value:
            raise ValueError("Protected name/item pointer field changed")
    for relative in range(1,12):
        pointer=(d["owned_name_address"]+relative).to_bytes(4,"little")
        if pointer in source or pointer in target:raise ValueError("Interior surname literal pointer alias")
    if sha(source)!=d["runtime_component_hashes"]["/__arm9__.bin"] or sha(target)!=d["target_runtime_component_hashes"]["/__arm9__.bin"]:
        raise ValueError("Exact source andtarget surname ARM9 hashes required")
    return dict(bytes=12,protected_Blades_exact=True,all_other_ARM9_bytes_andpointer_fields_exact=True,
        whole_ARM9_inverse_exact=True,literal_pointer_census_not_arbitrary_dynamic_alias_proof=True)
