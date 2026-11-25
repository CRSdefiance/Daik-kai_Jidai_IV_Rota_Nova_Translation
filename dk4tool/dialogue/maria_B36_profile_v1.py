"""Exact Maria SC3B36 source, CS0101 header, prose and guarded geometry contract."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path('translations/maria_B36_native_contract_v1.json')
CONTRACT_SHA='84e2dc403317a38e1042d20dcc1709deafcf60dff748276853165fdb02774fc4'
ARM9_SHA='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError('Frozen Maria-B36 contract changed')
    d=json.loads(raw)
    for p,h in d['dependencies'].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError('Native dependency changed:'+p)
    if len(d['record_bindings'])!=16 or d['choice_bindings'] or d['physical_native_rows_per_page']!=4 or d['complete_native_pages']!=16:raise ValueError('Complete16-paragraph/no-menu contract required')
    return d
def expected_profile(ident):
    d=contract()
    if ident not in d['record_bindings']:raise ValueError('Unreviewed Maria-B36 paragraph')
    r=d['record_bindings'][ident];base=get_dialogue_profile(r['route_aware_base_profile'])
    return replace(base,name='Maria-B36-source-bound-v1:'+ident,max_lines=r['maximum_total_rows'],macro_widths={'FI':30,'FA':12,'FO':42,'I':12},macro_ascii_lengths={'FI':5,'FA':2,'FO':7},leading_speaker_bytes=frozenset({2,3,10}),literal_prefix_policy='native-guard-v255',metrics_source=base.metrics_source+'; exact route-bound '+ident+'. Original216x64/four-row page,6px ASCII,16px pitch,original pair phase andguards. Own Maria captain3/mask8 native macro/literal paths andfinal16 one-page paragraphs bound;scoped FI5/FA2/FO7 measurements replace no global defaults. Preserve three original selectors,all3 real substitutions,source-supported ellipses andCS0101. Nine individual row-count infos;no warnings orwaivers. Existing exact system-only unlock isdisclosed,earned=false. Shared155 label semantics andfull207 names remainopen. Every base QA issue androw reason preserved. No global font,width,literal I/F,macro orweak-ending change. Stored,actual andrelease approval remains separate.')
def profile_for(arm,block,ident,file_path):
    d=contract()
    if ident not in d['record_bindings']:raise ValueError('Unreviewed Maria-B36 paragraph')
    r=d['record_bindings'][ident]
    if sha(arm)!=ARM9_SHA or file_path!=r['file_path'] or sha(block) not in r['source_block_hashes']:raise ValueError('Exact file-qualified source/current block and2b6 runtime required')
    return expected_profile(ident)
