"""Exact B230 source/paragraph/native geometry contract; typed menus remain distinct."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path('translations/lil_B230_native_contract_v1.json')
CONTRACT_SHA='546d1f67a84722c4a718267402e98fb8d7b10300a0ca210f636c6f08d34944c4'
ARM9_SHA='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError('B230 frozen native contract changed')
    d=json.loads(raw)
    for p,h in d['dependencies'].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError('B230 native dependency changed:'+p)
    if len(d['record_bindings'])!=17 or len(d['choice_bindings'])!=0 or d['physical_native_rows_per_page']!=4 or d['complete_native_pages']!=17:raise ValueError('Complete B230 seventeen-paragraph/no-menu contract required')
    return d
def expected_profile(ident):
    d=contract()
    if ident not in d['record_bindings']:raise ValueError('Unreviewed B230 paragraph')
    r=d['record_bindings'][ident];base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B230-source-bound-v1:'+ident,max_lines=r['maximum_total_rows'],leading_speaker_bytes=frozenset({2,22}),metrics_source=base.metrics_source+'; B230 exact paragraph '+ident+'. Original216x64/four-row page,6px ASCII,16px pitch,original pair phase and guards; original static actors2/22,voices3/2,zero source or invented macros. All seventeen complete paragraphs retain one original four-row page. Seven informational row reasons andzero warning waivers preserve every base diagnostic. R21 full named-item complement,R17 complete question andR50 complete locative phrase change no words. Only the two progressive names are reviewed;Samwell catalogue middle remains explicitly unapproved. All ASCII metrics,canaries,viewport,pair phase andguards remain unchanged.')
def profile_for(arm,block,ident):
    d=contract()
    if sha(arm)!=ARM9_SHA or sha(block) not in d['source_block_hashes']:raise ValueError('Exact B230 source/current block and exact2b6 runtime required')
    return expected_profile(ident)
