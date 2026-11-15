"""Exact B188 Daimyo/Guildmaster source/runtime progressive and FE profile."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'
BLOCKS=frozenset(['0293670e14045632185f95314c631afdbea888bbb743cf16dbdda64ad5b69a6c', '3217e8608245d4f4e03d0078a4823f19355c79059f72ea151727c12523b3f640'])
SELECTORS=frozenset({130,150})
DEPENDENCIES={'work\\analysis\\lil_B188_source_v5232\\all11_clean_current_complete_context.json': '5582aef129545d72a9b9b5fe688ce33cf0b6e5b21144025ff2fd89ae86ed25cb', 'work/analysis/lil_B188_dispatches_v5234/all11_source_current_dispatches_no_macros_and3_control_leaves.json': '12bc24558abae67e8b1af9fa617147297c47bd7377379e0f9a889cb9705bb93d', 'work/analysis/lil_B188_voices_v5233/current207_catalog_eight_voices_and_two_source_selectors.json': '13ab808c0cbfd5b3dfd98c6e94e723efeb8c4151feb9869e598868fdb5f2e2a1', 'work/analysis/lil_B188_controls_v5236/A000_C200_single_end_and_no_relative_or_predicate_contract.json': '731b39f801de48f92b22121dcb8693bb48f39fd360128f6dae90e4d25f3047d1', 'work/analysis/lil_B188_entry_v5235/source_EV2_B188_action_dependency_and_native_getter_binding.json': '5e9eeb9d109c6809d943f700ab579dbd3827eb594af8c7939f1f1f663454363a', 'work\\analysis\\lil_B188_terms_v5238\\Daimyo_Guildmaster_Osaka_Glass_and_giyaman_collection_reconciliation.json': '8bc1f003470263ff81baa6aa1170958ebe283d08194fcecdb6d0c10d56b67a19', 'work/analysis/lil_B188_names_v5237/four_original_progressive_and_catalogue_name_consumers.json': '7a799ad08d99deca77081ef40a72cdb39b46dfeb3eb3faca3906f77269ae23bd'}
CONTROL='work/analysis/lil_B188_dispatches_v5234/all11_source_current_dispatches_no_macros_and3_control_leaves.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B188 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B188 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=22 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All11 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('The FE object must remain null-actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B188 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B188-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';10 original54020 speeches,clean Daimyo130/Guildmaster150,both voice0,four read-only name consumers.14 linear commands,A0008 raw00a0ffff01293ba1,C200476,end478,two tailzeros,no predicates/relative sites. Current V5219 font/guards;fresh native approval required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B188-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310null actor then5473C object:tentative Glass/Osaka notice.228x48logical/228x64physical,conservative216px planning. Source giyaman is glossed glass,commodity41. No earlier location or earned boom claim;fresh native approval required.')
    raise ValueError('Unknown B188 consumer')
