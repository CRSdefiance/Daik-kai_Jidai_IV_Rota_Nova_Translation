"""Exact B222 source/paragraph/native geometry contract; typed menus remain distinct."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path('translations/lil_B222_native_contract_v1.json')
CONTRACT_SHA='d541e729bc83f6f6de8ae3294962d2dc8e084064b6583ddeb7a62a1a7f62ac8d'
ARM9_SHA='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError('B222 frozen native contract changed')
    d=json.loads(raw)
    for p,h in d['dependencies'].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError('B222 native dependency changed:'+p)
    if len(d['record_bindings'])!=16 or len(d['choice_bindings'])!=0 or d['physical_native_rows_per_page']!=4 or d['complete_native_pages']!=16:raise ValueError('Complete B222 sixteen-paragraph/no-menu contract required')
    return d
def expected_profile(ident):
    d=contract()
    if ident not in d['record_bindings']:raise ValueError('Unreviewed B222 paragraph')
    r=d['record_bindings'][ident];base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B222-source-bound-v1:'+ident,max_lines=r['maximum_total_rows'],leading_speaker_bytes=frozenset({2,16}),metrics_source=base.metrics_source+'; B222 exact paragraph '+ident+'. Original216x64/four-row page,6px ASCII,16px pitch,original pair phase and guards; original actors2/16,voices3/1,no source or invented macros;all sixteen complete paragraphs retain one original four-row page.')
def profile_for(arm,block,ident):
    d=contract()
    if sha(arm)!=ARM9_SHA or sha(block) not in d['source_block_hashes']:raise ValueError('Exact B222 source/current block and exact2b6 runtime required')
    return expected_profile(ident)
