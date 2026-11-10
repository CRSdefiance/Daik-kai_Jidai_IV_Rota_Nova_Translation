"""Exact SC0B246/SC1B237 source, route, prose and guarded geometry contract."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path('translations/papal_trade_native_contract_v1.json')
CONTRACT_SHA='984790ce6b2a675f9068285f8fd9311277c1dcc91e893c9aaa3468e889ede201'
ARM9_SHA='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError('Frozen papal-trade contract changed')
    d=json.loads(raw)
    for p,h in d['dependencies'].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError('Native dependency changed:'+p)
    if len(d['record_bindings'])!=36 or d['choice_bindings'] or d['physical_native_rows_per_page']!=4 or d['complete_native_pages']!=36:raise ValueError('Complete36-paragraph/no-menu contract required')
    return d
def expected_profile(ident):
    d=contract()
    if ident not in d['record_bindings']:raise ValueError('Unreviewed papal-trade paragraph')
    r=d['record_bindings'][ident];base=get_dialogue_profile(r['route_aware_base_profile'])
    return replace(base,name='papal-trade-source-bound-v1:'+ident,max_lines=r['maximum_total_rows'],leading_speaker_bytes=frozenset({19,104}),literal_prefix_policy='native-guard-v255',metrics_source=base.metrics_source+'; exact route-bound '+ident+'. Original216x64/four-row page,6px ASCII,16px pitch,original pair phase andguards. Actual captain0/1 route dispatch/getters andlogical/compiled processor bytes bound;zero source/English FI/FA/FO. Only source-bound R5 original three CP932 ellipses are non-ASCII prose. One exact R33 article continuation perfile keeps Papal States whole. Every base QA issue androw reason preserved. No global font,width,literal I/F,macro orweak-ending change. Stored,actual andrelease approval remains separate.')
def profile_for(arm,block,ident,file_path):
    d=contract()
    if ident not in d['record_bindings']:raise ValueError('Unreviewed papal-trade paragraph')
    r=d['record_bindings'][ident]
    if sha(arm)!=ARM9_SHA or file_path!=r['file_path'] or sha(block) not in r['source_block_hashes']:raise ValueError('Exact file-qualified source/current block and2b6 runtime required')
    return expected_profile(ident)
