"""Exact B139/B140 progressive consumers and source-owned UI control."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['127a704f98b30bed0ccffc55095ca2b953389b1f4a50f2095466d31581d4ca97', '43185fbc6f1e67b8b2f153c5bd2936a6e6aceb3723782c9b083c07c5028cdca0', '5581f0dd770ea527677d3fe93d750eab6dc861b8fb089ed0f055c7fe23c06a37', 'ff6dd768363c339b3bd5d1d7150c101d52865ed7686a3dd0e0d5f714545c66df'])
SELECTORS=frozenset({2,4,9,16,20,21,171})
DEPENDENCIES={'work\\analysis\\lil_remaining_B139_B140_source_v3456\\next67_B139_B140_clean_current_context.json': '4055d6a6c7f8423546b86959c2edad8655fa65e424a6185b9ea644cb95915c33', 'work\\analysis\\lil_B139_B140_controls_v3464\\all67_dispatches12_predicates1_query_and_C200_contract.json': '00f4977727b4bd7ee3d94f5536ee334fdb92a0a60c74323aab6fa131421f189d', 'work\\analysis\\lil_B139_B140_voices_v3460\\current_seven_static_names_voices_and207_catalog_rebind.json': '23327a44b0b337dc10f9bd7748ec8a89380bcc39b7c7b36c36d98ee5826b8b25', 'work\\analysis\\lil_B139_B140_terms_v3466\\clean_current_items_polder_names_entries_and_copy_census.json': 'ae05c5b72cb41c2e8c458340e044883aea018c07fdf7cc3fb791b713536bfa31', 'work\\analysis\\lil_B139_B140_branches_v3463b\\original_relative_skip_operand_proof.json': '1377f379ac9d75b5b2c7a2c3ab238f12fc4419025c5604815959f3abbb1e7f81', 'work\\analysis\\lil_B139_B140_dispatches_v3462\\current_registered_name_catalog_binding.json': 'e29ace380a12dfaf3973af0bfc5c40cdba38eb90246b5c2a06d0ac49560d2488', 'work\\analysis\\lil_B139_B140_conditionals_v3461c\\source13_conditionals_contract.json': '1fe63e2e459d5b0d07afdd35c751f26c7f23834fb0c61014baf7253a36df7c6f', 'work\\analysis\\lil_B139_C200_v3461e\\source_C200_UI_request_contract.json': 'dce660c7adb2e6b5af585df11731f10cf9ac99d2bf99aebba06307b467276ef8'}
CONTROL=Path('work\\analysis\\lil_B139_B140_controls_v3464\\all67_dispatches12_predicates1_query_and_C200_contract.json')
VOICE=Path('work\\analysis\\lil_B139_B140_voices_v3460\\current_seven_static_names_voices_and207_catalog_rebind.json')
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B139/B140 clean/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    c=json.loads(CONTROL.read_text(encoding='utf-8'));v=json.loads(VOICE.read_text(encoding='utf-8'))
    if consumer!='progressive' or len(c['speech_dispatch_cases'])!=134 or len(c['current_original_predicate_cases'])!=13 or len(c['original_event_queries'])!=1 or c['original_event_queries'][0]['event']!=129 or c['source_macro_counts']!={'FI':7,'FA':0,'FO':0} or len(c['source_C200_cases'])!=1 or len(v['fresh_seven_actor_names']['rows'])!=7:raise ValueError('Complete seven actor, twelve predicate, query129, FI7 and C200 contracts required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B139-B140-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';67 progressive speeches, seven static actors, Lil captain2 and FI7. Original query129, twelve predicates and source-owned C200 UI writes bound. Resource bodies and selected scene not executed by this profile.')
