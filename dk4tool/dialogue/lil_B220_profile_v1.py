"""Exact B220 source/paragraph/native geometry contract; typed menus remain distinct."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path('translations/lil_B220_native_contract_v1.json')
CONTRACT_SHA='c76ccb13fda4aa7912efec2f591b0aae4d8dae50784ee0414348eadea31a4be6'
ARM9_SHA='aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05'
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError('B220 frozen native contract changed')
    d=json.loads(raw)
    for p,h in d['dependencies'].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError('B220 native dependency changed:'+p)
    if len(d['record_bindings'])!=17 or len(d['choice_bindings'])!=0 or d['physical_native_rows_per_page']!=4 or d['complete_native_pages']!=17:raise ValueError('Complete B220 seventeen-paragraph/no-menu contract required')
    return d
def expected_profile(ident):
    d=contract()
    if ident not in d['record_bindings']:raise ValueError('Unreviewed B220 paragraph')
    r=d['record_bindings'][ident];base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B220-source-bound-v1:'+ident,max_lines=r['maximum_total_rows'],leading_speaker_bytes=frozenset({26,199}),metrics_source=base.metrics_source+'; B220 exact paragraph '+ident+'. Original216x64/four-row page,6px ASCII,16px pitch,original pair phase and guards; original actors26/199,voices2/0,no source or invented macros;all seventeen complete paragraphs retain one original four-row page.')
def profile_for(arm,block,ident):
    d=contract()
    if sha(arm)!=ARM9_SHA or sha(block) not in d['source_block_hashes']:raise ValueError('Exact B220 source/current block and AA5 runtime required')
    return expected_profile(ident)
