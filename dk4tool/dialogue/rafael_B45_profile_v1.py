"""Exact Rafael B45 clean/current records, original progressive/FE consumers and measured runtime."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path("translations/rafael_B45_native_contract_v1.json")
CONTRACT_SHA="cf94193d0da8accec4542c4306c4d060af5152b0e803c660890cbef889881c8b"
ARM9_SHA="2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a"
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError("Frozen Rafael-B45 contract changed")
    d=json.loads(raw)
    for p,h in d["dependencies"].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError("Native dependency changed:"+p)
    if len(d["record_bindings"])!=12 or d["choice_bindings"] or d["physical_native_rows_per_page"]!=4 or d["complete_native_pages"]!=12:
        raise ValueError("Complete twelve-paragraph/no-menu contract required")
    if d["measured_macro_ascii_lengths"]!={"FI":6,"FA":6,"FO":10} or d["source_macro_counts"]!={"FI":0,"FA":0,"FO":1}:
        raise ValueError("Exact measured Rafael macros required")
    return d
def expected_profile(ident,consumer=None):
    d=contract()
    if ident not in d["record_bindings"]:raise ValueError("Unreviewed Rafael-B45 paragraph")
    r=d["record_bindings"][ident];wanted="FE-paper" if r["source_selector"]==254 else "progressive"
    if consumer is not None and consumer!=wanted:raise ValueError("Original Rafael-B45 consumer required")
    base=get_dialogue_profile("raphael-story-live")
    if base.window_width_px!=216 or base.max_lines!=4 or base.macro_ascii_lengths["FI"]!=7 or base.literal_prefix_policy!="forbid":
        raise ValueError("Original global Rafael profile required")
    return replace(base,name="Rafael-B45-source-bound-v1:"+ident,max_lines=4,
        macro_widths={"FI":36,"FA":36,"FO":60,"I":12},macro_ascii_lengths={"FI":6,"FA":6,"FO":10},
        leading_speaker_bytes=frozenset({254} if wanted=="FE-paper" else {0,6}),
        literal_prefix_policy="native-guard-v255",
        metrics_source="Exact B45/current2b6:216px usable text/four physical rows;original progressive216x64 or FE228x48 logical/228x64 physical. Source00 actor stays in complete native preamble;body NUL guard unchanged. Native FI6/FA6/FO10,complete compiled/stored planes andpaired actual masks verified. No global font,profile,guard orweak-rule change. One-step RNG timing difference retained;future random outcomes not proved equal.")
def profile_for(arm,block,ident,file_path,consumer=None):
    d=contract()
    if ident not in d["record_bindings"]:raise ValueError("Unreviewed Rafael-B45 paragraph")
    r=d["record_bindings"][ident]
    if sha(arm)!=ARM9_SHA or file_path!=r["file_path"] or sha(block) not in r["source_block_hashes"]:
        raise ValueError("Exact file-qualified B45 source/current block and2b6 runtime required")
    return expected_profile(ident,consumer)
def validate_runtime(image):
    d=contract()
    for path,digest in d["runtime_component_hashes"].items():
        if sha(image.read_file(path))!=digest:raise ValueError("Exact Rafael-B45 runtime component required:"+path)
    return d
