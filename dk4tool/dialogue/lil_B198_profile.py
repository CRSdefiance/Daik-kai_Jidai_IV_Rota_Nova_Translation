"""Exact B198 eleven progressive speeches and six unattributed FE voice panels."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'
BLOCKS={'0bf24691edab7de699865fa8c7ce6fc6bfe37c80c9cebd0e201ba7f12c813cf6', '86323b3f9b649888b924efe662c5d0f2499995d8eee36ebbf65cf960c97b86e5'}
SELECTORS=frozenset({12,15})
DEPENDENCIES={'work\\analysis\\lil_B198_source_v5702\\all17_clean_current_complete_context.json': '12eef863b97bdc01887b559ac59414ed6d4aa19cdaea11dc8d3909e8c5adc9f9', 'work/analysis/lil_B198_voices_v5703/current207_catalog_eight_voices_and_two_source_selectors.json': 'd130c0c231d8fe82711b21ae6b038b529ee0a1f67636ebf781b65c08fb6ceb39', 'work/analysis/lil_B198_dispatches_v5704/all17_source_current_dispatches_no_macros_and12_control_leaves.json': '356c863f24c560fb659c7ba5d63250c2b490fbb99117a83878d5c5fb6f87cb23', 'work/analysis/lil_B198_branches_v5706/original_relative_skip_operand_proof.json': '046eb0c80053d95dcc0ea8983511f22f6ce4c1e026828d32f87b553c01e72804', 'work/analysis/lil_B198_entry_v5705/source_EV2_B198_action_dependency_and_native_getter_binding.json': 'c12e6557e478ba2c94f78a1f7535f25fbc6d3d34cbae6de72073bacde763aa97', 'work/analysis/lil_B198_controls_v5710c/twelve_exact_leaves_two_predicates_resource_picture_seven_structural_pairs_and_end.json': 'f9d261fd8ea6f80ec735f6e720ae0f59c6930466fe6a00844eea77e14e1bcac0', 'work/analysis/lil_B198_names_v5707/four_original_progressive_and_catalogue_name_consumers.json': '5a50e01cbb4f77a6e4cd6753378c8f01616c6147e7b06e77ac42782e5b279b75', 'work/analysis/lil_B198_source_names_v5711/two_actors_all_clean_fields_and_current_consumers.json': '5ab0201e371a306666cad242cee24bf26aa8edc3d9961c0cac09bba83e67e388', 'work\\analysis\\lil_B198_context_v5715\\clean_first_context_Namahage_dream_and_original_unforced_path.json': '1ed3534b3571f239ebb2dfc53e3929dea4ba504e86d67ee2c282c744e9b3ec29', 'work\\analysis\\lil_B198_source_paths_v5714\\one_actual_source_path_and_complete_command_intervals.json': 'f17b0e8a8c4912e639294cd32e1cc8a8fab292e41630c74e2eeb303e8404d8db'}
CONTROL='work/analysis/lil_B198_dispatches_v5704/all17_source_current_dispatches_no_macros_and12_control_leaves.json'
TERMS='work\\analysis\\lil_B198_context_v5715\\clean_first_context_Namahage_dream_and_original_unforced_path.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B198 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B198 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=34 or sum(r['source_selector']==254 for r in cases)!=12:raise ValueError('All17 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE must remain null actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B198 has no source name macros')
    terms=json.loads(Path(TERMS).read_bytes())
    if not terms['source_FE_is_unattributed_speaking_voice_not_impersonal_notice']:raise ValueError('Complete encounter context required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B198-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';11 original54020 speeches,Yukihisa12 voice1/Angelo15 voice4,four name consumers.37 source commands/eight relative sites/two predicates/one end. No source macros. V5692 unchanged font,width,guard and pair phase.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B198-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';six original24310 null actor then5473C unattributed voice panels,no FI.228x48logical/228x64physical,conservative216px planning.15 source speeches observed,two conditional Angelo lines offline only;no English scene or full effect-body claim.')
    raise ValueError('Unknown B198 consumer')
