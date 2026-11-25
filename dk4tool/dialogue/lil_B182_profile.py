"""B182 seven progressive speeches,one impersonal FE and conditional native controls."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'
BLOCKS=frozenset(['7c3d348f37b43671866005d2654cb2b9c332c7ef42896e0408fcb0b36ebf93d4', '8e9c466f0452f870854a2a63195d0f614c52d5d8afc40a34bed67d8f5eab159c'])
SELECTORS=frozenset({166,167})
DEPENDENCIES={'work\\analysis\\lil_B182_source_v4878\\all8_clean_current_complete_context.json': '315956cc027b0fd11c964a0ca2b7d1271c290c8530471dfe23ec4f8d24e55a63', 'work/analysis/lil_B182_dispatches_v4880/all8_source_current_dispatches_no_macros_and7_control_leaves.json': 'f05798f6d4ca5bbe2ead313ff6dc09033f56eca0fb2375bfff5d3f86ed695d4d', 'work/analysis/lil_B182_voices_v4879/current207_catalog_eight_voices_and_two_source_selectors.json': '2f7476d135705f5aedae8cc0981d1903a10c80271574849a1ef48f23d580e82b', 'work/analysis/lil_B182_branches_v4881/original_relative_skip_operand_proof.json': '3994213b2346e99ff48a0437a1b354103d5e85e92e17e654194b62be3c3eb542', 'work/analysis/lil_B182_entry_v4882/source_EV2_B182_action_dependency_and_native_getter_binding.json': '8e54f465a3cb9ebea79dd7b2f7977197d1e9add709ce38bb6485f71a6d594c4b', 'work/analysis/lil_B182_controls_v4883/two_predicates_three_A000_C200_ten_relative_sites_and_single_end.json': '9b578a14db9659f74b6e63e50aa98d14f99476bcf0c1d83b43f13950c7b56f04', 'work\\analysis\\lil_B182_terms_v4885\\Lady_London_Gems_reported_engagement_and_unknown_stone.json': 'e4f2805bb12c36d2e3276863a4d80a1985e3007fb286e0b06a6818541626ef5f', 'work/analysis/lil_B182_names_v4884/four_original_Lady_name_consumers.json': 'e3883bbbacfbb1a12d8b9a64827149761dad60123f8c0a927a27059428c94aa5', 'work\\analysis\\lil_B182_predicate500_v4883\\all16_original500_predicate_RNG_ownership_cases.json': '63473793fd150bfa6adeb76c9e538cac051802da9911f333c97285b59afcbf02', 'work\\analysis\\lil_B182_C200_v4883\\source_fleet_descriptor_two_C200_contracts.json': '4afbc8a99af008b74c85b337d6afa241fc7584065662f8aef1661b80ff196668'}
CONTROL='work/analysis/lil_B182_dispatches_v4880/all8_source_current_dispatches_no_macros_and7_control_leaves.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B182 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B182 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=16 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All eight source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE notice must remain null-actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B182 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B182-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';seven original54020 speeches,Lady166/Lady167,four read-only name paths. Source-explicit princess,duke and his son;no guessed personal names,marriage date or gemstone identity.25 commands,ten relative sites,two original500 threshold/RNG predicates,three alternative opaque effects,C200630,end632. Current V4867 font and guards;native planes still need fresh approval.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B182-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one prospective London Gems-category notice,original24310null actor then5473C.228x48logical/228x64physical,conservative216px planning. No earlier location,earned boom or demand/price inference. Current font native plane still needs fresh approval.')
    raise ValueError('Unknown B182 consumer')
