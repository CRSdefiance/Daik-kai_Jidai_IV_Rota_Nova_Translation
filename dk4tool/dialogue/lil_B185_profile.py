"""Exact B185 source/current commands,two couple roles and progressive/FE consumers."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'
BLOCKS=frozenset(['37e0447b1c130ac58aaeee7adf18dccc9d54d96cdc31c49b8298f612668d038a', 'be1c1b65a71c72def0f351c3038c076a53e6993f42f4c1858f246224587cfb3a'])
SELECTORS=frozenset({164,165})
DEPENDENCIES={'work\\analysis\\lil_B185_source_v5087\\all8_clean_current_complete_context.json': '8f47e63cb66a460ced115419298bc76cd595bbe30a3ff33af5c0f9cb361eac3b', 'work/analysis/lil_B185_dispatches_v5089/all8_source_current_dispatches_no_macros_and3_control_leaves.json': 'cf34eaadc4efc0080c970298120290f1088c3a38ffd794ec25525e7e449cc1fc', 'work/analysis/lil_B185_voices_v5088/current207_catalog_eight_voices_and_two_source_selectors.json': '5fceac4bea646ea4406301e3caad1fe0a0f9b6758483aaf81ac5cbb9ee4dc935', 'work/analysis/lil_B185_controls_v5091/A000_C200_single_end_and_no_relative_or_predicate_contract.json': '7bde51509c2661b4a580c6bf6f897018c36da983d8b540b3f6cb1f993b317794', 'work/analysis/lil_B185_entry_v5090/source_EV2_B185_action_dependency_and_native_getter_binding.json': '9ffedfb20e2155c22367d705ed7ef416eb65f68191ae46c9c74b421e5b810dd9', 'work\\analysis\\lil_B185_terms_v5093\\two_couple_roles_Stockholm_Furs_and_reported_sales_prices_reconciliation.json': '7ba2b0017d486eff6958afebe5ca967fee24c9f0bf304f53f51d4855377d6dcf', 'work/analysis/lil_B185_names_v5092/four_original_progressive_and_catalogue_name_consumers.json': '6624cb12331a4d86e5739db127db0a5918a18c484600c3260de9cac9720b137e'}
CONTROL='work/analysis/lil_B185_dispatches_v5089/all8_source_current_dispatches_no_macros_and3_control_leaves.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B185 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B185 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=16 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All8 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('The FE object must remain null-actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B185 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B185-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';7 original54020 speeches,two static couple roles164/165,four read-only name consumers and source voice0.11 linear commands,A0008 raw00a0ffff013807a1,C200382,end384. No inferred marriage,age or kinship. Current V5076 font/guards;native planes need fresh approval.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B185-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310null actor then5473C object:prospective Furs/Stockholm notice.228x48logical/228x64physical,conservative216px planning. No earlier scene location or earned boom inference. Current native planes need fresh approval.')
    raise ValueError('Unknown B185 consumer')
