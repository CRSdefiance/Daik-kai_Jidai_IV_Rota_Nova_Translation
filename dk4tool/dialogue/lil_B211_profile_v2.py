"""Exact B211 two-consumer/source/FI contract; no shared formatter or runtime mutation."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path('translations/lil_B211_native_contract_v2.json')
CONTRACT_SHA='0964a5e4a940b564e93604fdce9dfd14874474d1110a84dbd74a3f4926a93ffe'
ARM9_SHA='aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05'
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError('B211 frozen native contract changed')
    d=json.loads(raw)
    for p,h in d['dependencies'].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError('B211 native dependency changed:'+p)
    if len(d['record_bindings'])!=12 or d['physical_native_rows_per_page']!=4 or d['complete_native_pages']!=12 or d['FE_pages']!=3 or d['FI_objects']!=1:raise ValueError('Complete B211 twelve-object/two-consumer contract required')
    return d
def expected_profile(ident):
    d=contract()
    if ident not in d['record_bindings']:raise ValueError('Unreviewed B211 record')
    r=d['record_bindings'][ident];base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B211-source-bound-v2:'+ident,max_lines=4,leading_speaker_bytes=frozenset({r['source_selector']}),metrics_source=base.metrics_source+';exact B211 record '+ident+'. Nine original216x64 progressive objects,two static actors/voice3,three original null-actor FE228x48 logical/228x64 physical objects with measured216px text capacity,and one original FI expansion toLil. Every paragraph occupies one original four-row page. Fonts,guards,pair phase andnative metrics unchanged;full glyphs/pages/actual holds independently proved.')
def profile_for(arm,source_block,ident):
    d=contract()
    if sha(arm)!=ARM9_SHA or sha(source_block) not in d['source_block_hashes']:raise ValueError('Exact B211 clean/current block andV6541 runtime required')
    return expected_profile(ident)
