"""Exact B208 two actors,23 progressive objects incl private thought and one actorless named attribute notice."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='4f4e41d26a0b24610a38a9da03dc549e4afec82121a1c72f35665104bb7ea351'
BLOCKS={'7e2e61e5a4abc139a9f45842490e76955bd1132b9536d01ca8121f02ebd5fa39', 'eb5f12e8e5ff374f2150d4c47ff0493da9bcbbaf720c1f3dd36c327a5ec05d30'}
DEPENDENCIES={'work\\analysis\\lil_B208_source_v6390\\all24_clean_current_complete_context.json': '15ea4614e38c08c7a534640c76cb8fb32f9d95904a9c351db7be69cbfdf407e1', 'work\\analysis\\lil_B208_effective_v6401\\all24_effective_current_paragraphs_related_item40_and_exact_Charm_UI_label.json': '56aab8b82b773ee57c19249f27d458a8ada4b407076b42fb74f67bccfa080533', 'work\\analysis\\lil_B208_dispatches_v6394\\all24_source_current_dispatches_two_actors_one_FE_no_macros_and5_control_leaves.json': '3893886245c81a611ae39e4790d16f1506a0bb0eb1e22b512aa1704238e15f05', 'work\\analysis\\lil_B208_source_names_v6393\\two_exact_source_name_fields_voices_and_distinct_name_consumers.json': '9c9d7470df876411a4a06ac75fb734e7c22a9c90a54cacd8587d875cc8221904', 'work\\analysis\\lil_B208_source_view_v6400\\all24_source_panels_names_thought_FE_notice_and_return_viewed.json': 'f66cb95cc154d9e66c349448b4df750452999c0117dd961f68b0875941042c35', 'scripts\\lil_B208_prose_v6402.py': 'a7c439d5680ae4f01368281e59ecc20b37da1b01f92d655003d35e81ca2bd01f', 'translations\\lil_B208_speaker_names_review_v1.json': '0d7aeb2ce8f431447f49da6fc8e06f3d10247171daa1be0f14a89d9795d43b0e', 'work\\analysis\\lil_B207_name_planes_v6405\\two_complete_native_names32_literal_macro_alignments_and_actual_headers.json': '12cdca890a7fda0952f393cf57ff601bc7ce4beedd7c24735ec616abc5313dbc', 'translations\\lil_B208_editorial_manuscript_v2.json': 'f639443006e8146504b48ac5dbd3f62eb578c37595445256739d30302dc4e972', 'work/analysis/lil_FE_row_capacity_v6125/original228px_descriptor_native36_ASCII_row_capacity.json': 'f2c989ecd772beded8d75cfa45005d88988c5226ea3003b0220023d302b46dbc', 'scripts/shady_man_font_oracles_v6263.py': '9d205656f30078f6d6777a3b4f6c03cba07f07cd48a5b5243c9c1e2c43ec65f9', 'work/analysis/lil_B208_name_approval_v6406/two_name_retentions91_headers_no_asset_change.json': '2707c8c11044b896239143abeb2c1ebe828ee225eeb57dada3483521438b0ea6'}
CONTROL='work\\analysis\\lil_B208_dispatches_v6394\\all24_source_current_dispatches_two_actors_one_FE_no_macros_and5_control_leaves.json'
SOURCE='work\\analysis\\lil_B208_source_v6390\\all24_clean_current_complete_context.json'
SELECTORS=frozenset({7,170})
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B208 source/current block and current V6380 runtime required')
    for p,h in DEPENDENCIES.items():
        if sha(Path(p).read_bytes())!=h:raise ValueError('Frozen B208 contract changed:'+p)
    control=json.loads(Path(CONTROL).read_bytes());source=json.loads(Path(SOURCE).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=48 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All24 clean/current pairs and one FE named notice required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE named notice remains null actor')
    if any(r['source_selector'] not in SELECTORS or r['resolved_actor_ID']!=r['source_selector'] for r in cases if r['source_selector']!=254):raise ValueError('Both original static actors required')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0} or len(control['source_current_opaque_nonrelative_control_leaves'])!=5:raise ValueError('B208 has five leaves and no speech macros')
    if source['ordinary_source_speeches']!=23 or source['system_FE_panels']!=1:raise ValueError('Source23 progressive/one FE consumer split required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':return replace(base,name='lil-B208-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';23 source-bound progressive54020 objects including a parenthesized private thought,two static actors with voices3/0. Original216x64 consumer,6px ASCII,four rows,guard and pair phase preserved. No macros,choices,predicates,relative sites or2000 pauses.')
    if consumer=='FE-paper':return replace(base,name='lil-B208-FE-runtime-bound-v1',window_width_px=216,leading_speaker_bytes=frozenset({254}),metrics_source=base.metrics_source+';one original24310 null-actor then5473C named attribute notice. Source-owned typed descriptor proves228x48logical/228x64physical,6x12logical glyph placement. Eight original native capacity probes establish36 printable ASCII glyphs per row despite the228px bitmap descriptor. Host planning uses measured216px text capacity;no native viewport,font,clip,guard,pair-phase or four-row change. Each new plane must prove complete glyphs and one-page return before approval. No macros.')
    raise ValueError('Unknown B208 consumer')
