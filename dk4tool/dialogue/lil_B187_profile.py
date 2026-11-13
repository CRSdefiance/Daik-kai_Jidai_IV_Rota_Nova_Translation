"""Exact B187 source/current blocks,Sailor155/Shopkeeper87 and progressive/FE consumers."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'
BLOCKS=frozenset(['70c18a9b1633c8a4979edde90427c5b8fa24ef90bfe2158e00e96f9d671301f1', '8c1b29bd2c75a308c29cb91a87150d1d8de3a88e4c0282744d1d15273519e285'])
SELECTORS=frozenset({87,155})
DEPENDENCIES={'work\\analysis\\lil_B187_source_v5188\\all16_clean_current_complete_context.json': 'abb09dbb6113e842fc7568ca3daf5221f196628740182a7ae05e4987cc7e9737', 'work/analysis/lil_B187_dispatches_v5190/all16_source_current_dispatches_no_macros_and3_control_leaves.json': 'f35956a68c9f13df391d159313661f12f2a3d5ba6d9e4abcd4e1f6edd4b65955', 'work/analysis/lil_B187_voices_v5189/current207_catalog_eight_voices_and_two_source_selectors.json': '41f319ca613424dec556a096f06fddb096587e9e2f067c892b346fcab8e2e8f2', 'work/analysis/lil_B187_controls_v5192/A000_C200_single_end_and_no_relative_or_predicate_contract.json': '920e9f22083834e81067e5ed1292972ce844f2f027680cd3c75eda34b0f71134', 'work/analysis/lil_B187_entry_v5191/source_EV2_B187_action_dependency_and_native_getter_binding.json': '724a052d537d0fe8fd018dbcafc96edb96d64e2ff8970a754fad1cba2c35d064', 'work\\analysis\\lil_B187_terms_v5194\\Sailor_Square_Shopkeeper_Malacca_Almond_and_reported_remedy_reconciliation.json': 'a4b5693b51b4062454193c023214f212a832aa226e8efed034dc7c4fed64b93b', 'work/analysis/lil_B187_names_v5193/four_original_progressive_and_catalogue_name_consumers.json': '1101bd7bb7b44a3b7a3f2b7a68d2d505248e64ab87748c901bb760b4a64acce8'}
CONTROL='work/analysis/lil_B187_dispatches_v5190/all16_source_current_dispatches_no_macros_and3_control_leaves.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B187 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B187 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=32 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All16 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('The FE object must remain null-actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B187 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B187-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';15 original54020 speeches,clean Square Shopkeeper87 voice0 and progressive Sailor155 voice4,separate full-catalogue Retainer155,four read-only name consumers.19 linear commands,A0008 raw00a0ffff014e2fa1,C200672,end674,two tailzeros,no predicates/relative sites. Current V5177 font/guards;fresh native approval required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B187-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310null actor then5473C object:tentative Almonds/Malacca notice.228x48logical/228x64physical,conservative216px planning. Almonds is dialogue inflection of approved Almond78. No earlier location,earned boom or verified remedy claim;fresh native approval required.')
    raise ValueError('Unknown B187 consumer')
