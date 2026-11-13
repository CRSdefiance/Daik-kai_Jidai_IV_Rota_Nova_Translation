"""B181 nine progressive speeches,one impersonal FE and three linear control leaves."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'
BLOCKS=frozenset(['5ed1d66d3e76e96936bb5750ed13dd9509190a49ab6c62589bf87bbbd65a5185', 'd02227ab2806ab4e61d30fa10415e57eeb4a58e9fdd76eef7150901bbd971fe9'])
SELECTORS=frozenset({166,167,168})
DEPENDENCIES={'work\\analysis\\lil_B181_source_v4832\\all10_clean_current_complete_context.json': '3e3b55675c715489c4b1edfe117a0e2e1a9f59d3861e344c8a72b350f3df35f9', 'work/analysis/lil_B181_dispatches_v4834/all10_source_current_dispatches_no_macros_and3_control_leaves.json': 'a236077ad5cbe42abf0f1ebea8f932c5b04807b347124cbcfd8a58d41677de01', 'work/analysis/lil_B181_voices_v4833/current207_catalog_eight_voices_and_three_source_selectors.json': 'f65a9f5293044fa2733ca1c0393790ba0f1348ab166b08f13275f6457697ebcd', 'work/analysis/lil_B181_controls_v4836/A000_C200_single_end_and_no_relative_or_predicate_contract.json': '4f1144b139461ebe6f7f448fff96b56db74d0fe26d3c6eb6584eb2c55dd4415c', 'work/analysis/lil_B181_entry_v4835/source_EV2_B181_action_dependency_and_native_getter_binding.json': '9b2f5a5e951c53758a2eff38db2d1237866ed2b04bdd6e1d9fe12e438731b139', 'work\\analysis\\lil_B181_terms_v4838b\\three_Ladies_Athens_Rubies_and_wistful_source_context.json': 'ee4c05a1803a10b6d365529429d523e0f73c838ee67c477fa111df1f3fcd5e43', 'work/analysis/lil_B181_names_v4837/six_original_Lady_name_consumers.json': '1cfbdcf39f9bd9336fe150f46dca728ea77b516c5eaa1db37bdfc74b3ff382ca'}
CONTROL='work/analysis/lil_B181_dispatches_v4834/all10_source_current_dispatches_no_macros_and3_control_leaves.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B181 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B181 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=20 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All ten source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE notice must remain null-actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B181 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B181-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';nine original54020 speeches,Lady166/Lady167/Lady168,six read-only name paths. No inferred rank,marriage,giver identity or necklace gift provenance.13 commands,A0008,C200390,end392;no predicates or relative sites. Current V4821 font and guards;native planes still need approval.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B181-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one prospective Athens Rubies notice,original24310null actor then5473C.228x48logical/228x64physical,conservative216px planning. No earlier location,earned boom or demand/price inference. Current font native plane still needs approval.')
    raise ValueError('Unknown B181 consumer')
