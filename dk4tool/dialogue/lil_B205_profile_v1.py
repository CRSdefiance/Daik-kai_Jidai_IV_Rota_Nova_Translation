"""Exact B205 two actors,10 progressive speeches and seven actorless sound/echo objects."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='03a905a9e4a4df117b8a4b5280ec3c669a4db00547972397413bc8bebc4afbbd'
BLOCKS={'ce980e705501b8435021d6b734d4c178dc52073cfe43504923dd71ec308f59d4', 'cea80eb2883e16a9fe589c0cf1e89345e703f16a002bdc5b12322f4fc0e44159'}
DEPENDENCIES={'work\\analysis\\lil_B205_source_v6172\\all17_clean_current_complete_context.json': '0102a31e63a64f2f93d606c0088b6d581f70b0233be428a515df7bc1da3f00b9', 'work\\analysis\\lil_B205_contextual_findings_v6185\\seventeen_source_current_findings_nine_retentions_eight_revisions.json': 'ce7e660a143e9884b8726b56b34fcd3c47d50bed70456a4dd05f2abc2ff4f5fc', 'work\\analysis\\lil_B205_dispatches_v6176\\all17_source_current_dispatches_seven_FE_sounds_echoes_no_macros_and8_control_leaves.json': 'aca2cd8ffc28455d84de743cc80ec4383a4ff47fe5372f10a67093bb8bd9dc59', 'work\\analysis\\lil_B205_source_names_v6175\\two_exact_source_name_fields_voices_and_distinct_name_consumers.json': 'dba2d114cca316ff47c72a6d3db2d9d13216d967ca0d2829b0ebf412ac4f9871', 'work\\analysis\\lil_B205_source_view_v6184\\complete_source_scenes_and_return_visual_review.json': '5c629ae016fbe934dad33687c26a9d72c516943c96f9b3a3fc6807762ffdb2b5', 'scripts\\lil_B205_prose_v6186.py': 'c7631699de2f09f5d282fcd33ea12d96e063cd1621cf7501032ff08d6b9540e6', 'translations/lil_B205_editorial_manuscript_v1.json': '62b7aab0f2e94095040e855553d2f94b21cb1013e438d59d3cfbeab27c45900e', 'work/analysis/lil_FE_row_capacity_v6125/original228px_descriptor_native36_ASCII_row_capacity.json': 'f2c989ecd772beded8d75cfa45005d88988c5226ea3003b0220023d302b46dbc'}
CONTROL='work\\analysis\\lil_B205_dispatches_v6176\\all17_source_current_dispatches_seven_FE_sounds_echoes_no_macros_and8_control_leaves.json'
SOURCE='work\\analysis\\lil_B205_source_v6172\\all17_clean_current_complete_context.json'
SELECTORS=frozenset({2,15})
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B205 source/current block and current V6160 runtime required')
    for p,h in DEPENDENCIES.items():
        if sha(Path(p).read_bytes())!=h:raise ValueError('Frozen B205 contract changed:'+p)
    control=json.loads(Path(CONTROL).read_bytes());source=json.loads(Path(SOURCE).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=34 or sum(r['source_selector']==254 for r in cases)!=14:raise ValueError('All17 clean/current speech pairs and seven FE sound/echo objects required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE sound/echo objects remain null actor')
    if any(r['source_selector'] not in SELECTORS or r['resolved_actor_ID']!=r['source_selector'] for r in cases if r['source_selector']!=254):raise ValueError('Both original static actors required')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0} or len(control['source_current_opaque_nonrelative_control_leaves'])!=8:raise ValueError('B205 has eight leaves and no speech macros')
    if source['ordinary_source_speeches']!=10 or source['system_FE_panels']!=7:raise ValueError('Source10 progressive/seven FE consumer split required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':return replace(base,name='lil-B205-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';10 source-bound progressive54020 speeches,two static actors. Original216x64 consumer,6px ASCII,four rows,guard and pair phase preserved. No macros,choices,predicates,relative sites or2000 pauses.')
    if consumer=='FE-paper':return replace(base,name='lil-B205-FE-runtime-bound-v1',window_width_px=216,leading_speaker_bytes=frozenset({254}),metrics_source=base.metrics_source+';seven original24310 null-actor then5473C sound/echo objects. Source-owned typed descriptor proves228x48logical/228x64physical,6x12logical glyph placement. Eight original native capacity probes establish36 printable ASCII glyphs per row despite the228px bitmap descriptor. Host planning uses measured216px text capacity;no native viewport,font,clip,guard,pair-phase or four-row change. Each new plane must prove complete glyphs and one-page return before approval. No macros.')
    raise ValueError('Unknown B205 consumer')
