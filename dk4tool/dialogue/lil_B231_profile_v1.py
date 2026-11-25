"""Exact B231 source/paragraph/native geometry contract; typed menus remain distinct."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path('translations/lil_B231_native_contract_v1.json')
CONTRACT_SHA='da9f313da4dc3bbd004cb8040d7e818a9f6a912ac793780d9916fb0a11676f84'
ARM9_SHA='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError('B231 frozen native contract changed')
    d=json.loads(raw)
    for p,h in d['dependencies'].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError('B231 native dependency changed:'+p)
    if len(d['record_bindings'])!=16 or len(d['choice_bindings'])!=0 or d['physical_native_rows_per_page']!=4 or d['complete_native_pages']!=16:raise ValueError('Complete B231 sixteen-paragraph/no-menu contract required')
    return d
def expected_profile(ident):
    d=contract()
    if ident not in d['record_bindings']:raise ValueError('Unreviewed B231 paragraph')
    r=d['record_bindings'][ident];base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B231-source-bound-v1:'+ident,max_lines=r['maximum_total_rows'],leading_speaker_bytes=frozenset({2,19}),metrics_source=base.metrics_source+'; B231 exact paragraph '+ident+'. Original216x64/four-row page,6px ASCII,16px pitch,original pair phase and guards; original static actors2/19,voices3/7,zero source or invented macros. All sixteen complete paragraphs retain one original four-row page. Four informational row reasons andone exact R35 line2 article continuation classification preserve every base diagnostic. All ASCII metrics,canaries,viewport,pair phase andguards remain unchanged.')
def profile_for(arm,block,ident):
    d=contract()
    if sha(arm)!=ARM9_SHA or sha(block) not in d['source_block_hashes']:raise ValueError('Exact B231 source/current block and exact2b6 runtime required')
    return expected_profile(ident)
