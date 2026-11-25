"""Exact B212 source/paragraph/native geometry contract; typed menus remain distinct."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path('translations/lil_B212_native_contract_v1.json')
CONTRACT_SHA='3d222faa81e99dd8719b5d7cb6ffc6a353781f9e6e774c40f60de8041a017cbd'
ARM9_SHA='aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05'
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError('B212 frozen native contract changed')
    d=json.loads(raw)
    for p,h in d['dependencies'].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError('B212 native dependency changed:'+p)
    if len(d['record_bindings'])!=9 or len(d['choice_bindings'])!=2 or d['physical_native_rows_per_page']!=4 or d['complete_native_pages']!=9:raise ValueError('Complete B212 nine-paragraph/two-menu contract required')
    return d
def expected_profile(ident):
    d=contract()
    if ident not in d['record_bindings']:raise ValueError('Unreviewed B212 paragraph')
    r=d['record_bindings'][ident];base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B212-source-bound-v1:'+ident,max_lines=4,leading_speaker_bytes=frozenset({149}),metrics_source=base.metrics_source+'; B212 exact paragraph '+ident+'. Original216x64/four-row page,6px ASCII,16px pitch,original pair phase and guards; actor149 voice0, no FE/macro/role reinterpretation.')
def profile_for(arm,block,ident):
    d=contract()
    if sha(arm)!=ARM9_SHA or sha(block) not in d['source_block_hashes']:raise ValueError('Exact B212 source/current block and AA5 runtime required')
    return expected_profile(ident)
