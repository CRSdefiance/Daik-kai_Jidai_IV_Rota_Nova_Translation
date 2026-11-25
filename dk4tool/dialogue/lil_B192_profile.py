"""Exact B192 two-actor linear progressive/FE native profile."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'
BLOCKS=frozenset(['661c8dcf8586aef44be4a62de6c5e775075dc61a675acb1543daf568c4fe58e1', 'cc15b698d9f1a215fd402d31d590dd051e950407d720d92cac63014698ec2b77'])
SELECTORS=frozenset({115,153})
DEPENDENCIES={'work\\analysis\\lil_B192_source_v5406\\all8_clean_current_complete_context.json': 'aca5417308337d91c9cb11ba31839ceca05545065053d85fcc00b61ce516a417', 'work/analysis/lil_B192_dispatches_v5408/all8_source_current_dispatches_no_macros_and3_control_leaves.json': '7346e4010131bff0c0c3be077e397e101d5bcc3a683bb929331930530c75d5f4', 'work/analysis/lil_B192_voices_v5407/current207_catalog_eight_voices_and_two_source_selectors.json': '7ef0dd973faa79e763a1e2a113d633e5b1ba5649a156959514220f933ebc9874', 'work/analysis/lil_B192_controls_v5410/A000_C200_single_end_and_no_relative_or_predicate_contract.json': '79a52780e12dab287dba6fe8e6a8d4fa30f495015c7187c3e8a3f02eabc91566', 'work/analysis/lil_B192_entry_v5409/source_EV2_B192_action_dependency_and_native_getter_binding.json': 'c73de70abf6f3bf5ee0fb42d95ed106be6a1d481a05966035904632d086f7748', 'work\\analysis\\lil_B192_terms_v5412\\Sailor_Port_Worker_Istanbul_Tobacco_and_curiosity_reconciliation.json': '34f6fde87ccb8261aaa7ad36c35292cf9da8c6f4defab5456f98d4a388bc44e9', 'work/analysis/lil_B192_names_v5411/four_original_progressive_and_catalogue_name_consumers.json': 'af9d9f0b3cacc233ae44d97458f93863db45f2dc2c0dff03d7309dd4cd95a125'}
CONTROL='work/analysis/lil_B192_dispatches_v5408/all8_source_current_dispatches_no_macros_and3_control_leaves.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B192 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B192 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=16 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All8 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE must remain null actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B192 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B192-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';7 original54020 speeches,PortWorker115 voice0/Sailor153 voice4,distinct catalogue Retainer153,four original read-only names. Hex73/99 equal decimal115/153.11 linear commands,A0008,C200396,end398,two source tailzeros. Current V5396 font/guards;fresh native approval required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B192-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310null actor then5473C:prospective Tobacco/Istanbul notice.228x48logical/228x64physical,conservative216px planning. Commodity33 Tobacco/one Istanbul alias unchanged;no equipment,age,health,earned fashion or earlier location inference;fresh approval required.')
    raise ValueError('Unknown B192 consumer')
