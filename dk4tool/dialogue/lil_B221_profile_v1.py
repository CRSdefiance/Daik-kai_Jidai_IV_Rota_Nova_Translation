"""Exact B221 source/paragraph/native geometry contract; typed menus remain distinct."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path('translations/lil_B221_native_contract_v1.json')
CONTRACT_SHA='fadc29885f24235a94c473e3e0ffbfb3eff1af4a30dbfb848248c5af6355e08d'
ARM9_SHA='aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05'
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError('B221 frozen native contract changed')
    d=json.loads(raw)
    for p,h in d['dependencies'].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError('B221 native dependency changed:'+p)
    if len(d['record_bindings'])!=14 or len(d['choice_bindings'])!=2 or d['physical_native_rows_per_page']!=4 or d['complete_native_pages']!=16:raise ValueError('Complete B221 fourteen-paragraph/two-choice/two-continuation contract required')
    return d
def expected_profile(ident):
    d=contract()
    if ident not in d['record_bindings']:raise ValueError('Unreviewed B221 paragraph')
    r=d['record_bindings'][ident];base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B221-source-bound-v1:'+ident,max_lines=r['maximum_total_rows'],leading_speaker_bytes=frozenset({2,17,85}),metrics_source=base.metrics_source+'; B221 exact paragraph '+ident+'. Original216x64/four-row page,6px ASCII,16px pitch,original pair phase and guards; original actors2/17/85,voices3/4/0,no source or invented macros;only R46/R60 retain six reviewed generated rows across two original four-row pages. Other twelve paragraphs remain one page. Two original response labels use their separate typed consumer.')
def profile_for(arm,block,ident):
    d=contract()
    if sha(arm)!=ARM9_SHA or sha(block) not in d['source_block_hashes']:raise ValueError('Exact B221 source/current block and AA5 runtime required')
    return expected_profile(ident)
