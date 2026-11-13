"""Exact B204 five actors,16 progressive speeches and four actorless letter objects."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='03a905a9e4a4df117b8a4b5280ec3c669a4db00547972397413bc8bebc4afbbd'
BLOCKS={'f1b7814a372d36b2b77dad57706674d706c3a28f5666576a933b0b2b7c261219', '68508958153ab9e923feb95e996dbf921aa582130eb0c64b210f98aa7f716a38'}
DEPENDENCIES={'work\\analysis\\lil_B204_current_v6118\\all20_clean_current_complete_context.json': 'bf37de0687e5b2d16f18d93adafb3fbeb44347776592954cfc1373c21cf36326', 'work\\analysis\\lil_B204_contextual_findings_v6088\\twenty_source_current_findings_eight_proposed_retentions_twelve_revisions.json': '6d84d59a76a94c33fa3bf6905e6bf36110737a2501759dcc1e80b6132af34729', 'work\\analysis\\lil_B204_dispatches_v6119b\\all20_source_current_dispatches_four_FE_letters_no_macros_and6_control_leaves.json': 'b8265786c463386e5531f46aae5eb5d8ad7cc17e8a26748d80988b6e9d5dbe29', 'work\\analysis\\lil_B204_source_names_v6065\\five_exact_source_name_fields_voices_and_distinct_name_consumers.json': '29a0188790ede7ca004e7b66d5c33563e9cccd707b31e5a760fd633a50a343a0', 'work\\analysis\\lil_B204_source_view_v6077\\complete_source_scenes_and_return_visual_review.json': '54b5e32413bbbffeffa971498532ba471c71650f93ad7887adcce07a8619d460', 'scripts\\lil_B204_prose_v6120.py': '95523baec005ae56029b07ba36d451e6ef8eea3b57c4a4ec6b3b6f9f5f37c432', 'translations/lil_B204_editorial_manuscript_v1.json': '6232dac2d67bbd85af018c01d79857e279f8d40beb50cb6bec8113389c12f682'}
CONTROL='work\\analysis\\lil_B204_dispatches_v6119b\\all20_source_current_dispatches_four_FE_letters_no_macros_and6_control_leaves.json'
SOURCE='work\\analysis\\lil_B204_current_v6118\\all20_clean_current_complete_context.json'
SELECTORS=frozenset({2,11,124,130,145})
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B204 source/current block and current V6110 runtime required')
    for p,h in DEPENDENCIES.items():
        if sha(Path(p).read_bytes())!=h:raise ValueError('Frozen B204 contract changed:'+p)
    control=json.loads(Path(CONTROL).read_bytes());source=json.loads(Path(SOURCE).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=40 or sum(r['source_selector']==254 for r in cases)!=8:raise ValueError('All20 clean/current speech pairs and four FE letters required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE letters remain null actor')
    if any(r['source_selector'] not in SELECTORS or r['resolved_actor_ID']!=r['source_selector'] for r in cases if r['source_selector']!=254):raise ValueError('All five original static actors required')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0} or len(control['source_current_opaque_nonrelative_control_leaves'])!=6:raise ValueError('B204 has six leaves and no speech macros')
    if source['ordinary_source_speeches']!=16 or source['system_FE_panels']!=4:raise ValueError('Source16 progressive/four FE consumer split required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':return replace(base,name='lil-B204-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';16 source-bound progressive54020 speeches,five static actors. Original216x64 consumer,6px ASCII,four rows,guard and pair phase preserved. No macros,choices,predicates,relative sites or2000 pauses.')
    if consumer=='FE-paper':return replace(base,name='lil-B204-FE-runtime-bound-v1',window_width_px=228,leading_speaker_bytes=frozenset({254}),metrics_source=base.metrics_source+';four original24310 null-actor then5473C letter objects. Source-owned typed descriptor proves228x48logical/228x64physical,6x12logical glyph placement. Host planning uses the actual228px width;no native viewport,font,clip,guard,pair-phase or four-row change. Each new plane must prove complete glyphs and one-page return before approval. No macros.')
    raise ValueError('Unknown B204 consumer')
