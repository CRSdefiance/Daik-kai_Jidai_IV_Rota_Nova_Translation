"""Exact B233 source/paragraph/native geometry contract; typed menus remain distinct."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path('translations/lil_B233_native_contract_v1.json')
CONTRACT_SHA='132a1340081724f8d78193b5399bab3f1f2a5618ad40f6fd4b5740f9966239ea'
ARM9_SHA='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError('B233 frozen native contract changed')
    d=json.loads(raw)
    for p,h in d['dependencies'].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError('B233 native dependency changed:'+p)
    if len(d['record_bindings'])!=11 or len(d['choice_bindings'])!=0 or d['physical_native_rows_per_page']!=4 or d['complete_native_pages']!=11:raise ValueError('Complete B233 eleven-paragraph/no-menu contract required')
    return d
def expected_profile(ident):
    d=contract()
    if ident not in d['record_bindings']:raise ValueError('Unreviewed B233 paragraph')
    r=d['record_bindings'][ident];base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B233-source-bound-v1:'+ident,max_lines=r['maximum_total_rows'],leading_speaker_bytes=frozenset({2,23}),metrics_source=base.metrics_source+'; B233 exact paragraph '+ident+'. Original216x64/four-row page,6px ASCII,16px pitch,original pair phase and guards; original static actors2/23,voices3/7,zero source or invented macros. All eleven complete paragraphs retain one original four-row page. Three informational row reasons andzero warning waivers preserve every base diagnostic. Personal library discovery,reported chisel legend,Balkan clue,kings/tools humor andopportunity-conditioned request remain. Two personal names andnull middles match both original getters;catalogue UI remains unvisited. All ASCII metrics,canaries,viewport,pair phase andguards remain unchanged.')
def profile_for(arm,block,ident):
    d=contract()
    if sha(arm)!=ARM9_SHA or sha(block) not in d['source_block_hashes']:raise ValueError('Exact B233 source/current block and exact2b6 runtime required')
    return expected_profile(ident)
