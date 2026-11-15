"""Exact Maria SC3B207 source, CS0101 header, prose and guarded geometry contract."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path('translations/maria_B207_native_contract_v1.json')
CONTRACT_SHA='00788351a083fead4d2513fd49c976847957fddb702fb3780ffc7ce9d114cd6d'
ARM9_SHA='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError('Frozen Maria-B207 contract changed')
    d=json.loads(raw)
    for p,h in d['dependencies'].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError('Native dependency changed:'+p)
    if len(d['record_bindings'])!=18 or d['choice_bindings'] or d['physical_native_rows_per_page']!=4 or d['complete_native_pages']!=18:raise ValueError('Complete18-paragraph/no-menu contract required')
    return d
def expected_profile(ident):
    d=contract()
    if ident not in d['record_bindings']:raise ValueError('Unreviewed Maria-B207 paragraph')
    r=d['record_bindings'][ident];base=get_dialogue_profile(r['route_aware_base_profile'])
    return replace(base,name='Maria-B207-source-bound-v1:'+ident,max_lines=r['maximum_total_rows'],leading_speaker_bytes=frozenset({19,104}),literal_prefix_policy='native-guard-v255',metrics_source=base.metrics_source+'; exact route-bound '+ident+'. Original216x64/four-row page,6px ASCII,16px pitch,original pair phase andguards. Actual Maria captain3/mask8 dispatch/getters andlogical/compiled bytes bound withthe exact disclosed system-only unlock,earned=false;zero source/English FI/FA/FO. Only source-bound R4 three CP932 ellipses are non-ASCII prose. Distinct CS0101 header preserved. Seven row-count infos andno warnings orwaivers. Every base QA issue androw reason preserved. No global font,width,literal I/F,macro orweak-ending change. Stored,actual andrelease approval remains separate.')
def profile_for(arm,block,ident,file_path):
    d=contract()
    if ident not in d['record_bindings']:raise ValueError('Unreviewed Maria-B207 paragraph')
    r=d['record_bindings'][ident]
    if sha(arm)!=ARM9_SHA or file_path!=r['file_path'] or sha(block) not in r['source_block_hashes']:raise ValueError('Exact file-qualified source/current block and2b6 runtime required')
    return expected_profile(ident)
