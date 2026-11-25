"""Exact B20017 progressive speeches and two distinct original null-actor FE objects."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'
BLOCKS={'5f691d261fd9a45c788065dfaaf470db7f70aa7df4b9d9cfcb3e37ee4704077e', 'b4d3cacef855713aa235cccd4970dcc5f184a8eef109845444fb8991f4af8a0b'}
SELECTORS=frozenset({19,172})
DEPENDENCIES={'work\\analysis\\lil_B200_source_v5826\\all19_clean_current_complete_context.json': '418c2b0b7bff5e6bbc052d958e714947eb2b4524c316c71f648cbf8f48e087b9', 'work/analysis/lil_B200_voices_v5827/current207_catalog_eight_voices_and_two_source_selectors.json': 'f6a27b78708a6af207a01053f54f2694973b4b4b4cbf12dc7756d1765c1247c1', 'work/analysis/lil_B200_dispatches_v5828/all19_source_current_dispatches_no_macros_and12_control_leaves.json': '50b846eb725e9173ed658c4a601b340982da977d3bab09f600a9e58d945b1089', 'work/analysis/lil_B200_branches_v5830/original_relative_skip_operand_proof.json': 'dac9760244bdcb0e5f399336ce124ad7bc26758b9ba80ad199aa58ba9eee4d96', 'work/analysis/lil_B200_entry_v5829/source_EV2_B200_action_dependency_and_native_getter_binding.json': 'f4f7fb94a75602b7217bb496ddcc1285700fae5f62d4dfef6cc5fe3cf5065029', 'work/analysis/lil_B200_controls_v5833/twelve_exact_leaves_two_resources6003_picture47xx_six_structural_pairs_and_end.json': 'e55397235e04dd71786f5d24f369a0118bba21f9e15b79559d7be1c3abd0a4bd', 'work/analysis/lil_B200_names_v5831/four_original_progressive_and_catalogue_name_consumers.json': 'd07c23bbbbc2c4b454463f49ea2f5c67014620bea9c51fd05c0aa01b9f65122a', 'work/analysis/collapsed_speaker_lead_v5832/all_route_literal_uses_exact_name_fields_and_localization_finding.json': '1cadce9b3084b07273bd76de0f9bc7ab4f196aefe979068e072ce7da71db8626', 'work\\analysis\\lil_B200_comparison_v5838\\complete_clean_context_source_scene_names_role_label_and_terms.json': 'b5b5e81484cb9cbe8c5a2f9dfb3470e5bf4514a5b970228a9d54280aaa55a3de', 'work\\analysis\\lil_B200_source_paths_v5837\\one_actual_source_path_and_complete_command_intervals.json': '8df1ab3aaf3d6a5ee749bbceb3736cbb5f5e14d281bcffec0d6b16acc85f84d5'}
CONTROL='work/analysis/lil_B200_dispatches_v5828/all19_source_current_dispatches_no_macros_and12_control_leaves.json'
TERMS='work\\analysis\\lil_B200_comparison_v5838\\complete_clean_context_source_scene_names_role_label_and_terms.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B200 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B200 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=38 or sum(r['source_selector']==254 for r in cases)!=4:raise ValueError('All19 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE must remain null actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B200 has no original runtime name macro')
    terms=json.loads(Path(TERMS).read_bytes())
    if not terms['explicit_not_a_doctor_denial_preserved']:raise ValueError('Complete rescue and profession-denial context required')
    if terms['source_FE_impact_index']!=5 or terms['source_FE_stat_notice_index']!=72:raise ValueError('Distinct collapse sound and stat FE objects required')
    if terms['source_actual_speeches']!=19 or terms['offline_only_speeches']:raise ValueError('Complete19-source-panel fixture evidence required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B200-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';17 original54020 speeches,Carlo19 voice7/anonymous172 voice0,four name consumers.31 source commands/no choices,relatives,predicates or macros.One original end with two tailzeros.V5816 unchanged font,width,guard and pair phase.Stranger label is a separate unimplemented target.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B200-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';two original24310 null-actor then5473C objects:collapse sound and Carlo Charm+1 notice.No FE macros.228x48logical/228x64physical,conservative216px planning.All19 source panels observed;English scene and complete effect-body semantics unapproved.')
    raise ValueError('Unknown B200 consumer')
