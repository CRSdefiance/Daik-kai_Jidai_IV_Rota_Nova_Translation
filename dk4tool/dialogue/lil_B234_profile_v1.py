"""Exact B234 source/paragraph/native geometry contract; typed menus remain distinct."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path('translations/lil_B234_native_contract_v1.json')
CONTRACT_SHA='7e0d46547986450d364e1983071536b4a37f8b01449e81615cafc6c988023047'
ARM9_SHA='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError('B234 frozen native contract changed')
    d=json.loads(raw)
    for p,h in d['dependencies'].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError('B234 native dependency changed:'+p)
    if len(d['record_bindings'])!=18 or len(d['choice_bindings'])!=0 or d['physical_native_rows_per_page']!=4 or d['complete_native_pages']!=18:raise ValueError('Complete B234 eighteen-paragraph/no-menu contract required')
    return d
def expected_profile(ident):
    d=contract()
    if ident not in d['record_bindings']:raise ValueError('Unreviewed B234 paragraph')
    r=d['record_bindings'][ident];base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B234-source-bound-v1:'+ident,max_lines=r['maximum_total_rows'],leading_speaker_bytes=frozenset({19,104}),metrics_source=base.metrics_source+'; B234 exact paragraph '+ident+'. Original216x64/four-row page,6px ASCII,16px pitch,original pair phase and guards; original static actors19/104,voices7/0,zero source or invented macros. All eighteen complete paragraphs retain one original four-row page. Eight informational row reasons andone exact R33 line1 article continuation classification preserve every base diagnostic. The sole non-ASCII prose is the exact original three CP932 ellipses at R5;its actual light-gray palette is checked separately. Carlo Sinat andshared Trader are contextually retained;Filippo is a source-bound spoken address only. Regional European is excluded from both returned names andsupplies no surname orapproved nationality. All ASCII metrics,canaries,viewport,pair phase andguards remain unchanged.')
def profile_for(arm,block,ident):
    d=contract()
    if sha(arm)!=ARM9_SHA or sha(block) not in d['source_block_hashes']:raise ValueError('Exact B234 source/current block and exact2b6 runtime required')
    return expected_profile(ident)
