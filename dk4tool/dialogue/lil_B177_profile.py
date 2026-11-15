"""B177 exact source/current controls:nine progressive and one impersonal null-actor FE notice."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['18093df13c90047c9327909844b14d19ae264f343ba1a51bf7fb5478c420d736', '42bb6680bf654047f411c22c3a5e7fbcab2cc7cc23327a5297797aa85fb77935'])
SELECTORS=frozenset({174,175})
DEPENDENCIES={'work\\analysis\\lil_B177_source_v4602\\all10_clean_current_complete_context.json': 'b638f8c4d1bee1305bc706f5c9630a2c91161e797dadaf857386cb0e6af287aa', 'work\\analysis\\lil_B177_dispatches_v4604\\all10_source_current_dispatches_no_macros_and3_control_leaves.json': '48e1978861957f3bd6a3021419e2023e061a5cc45d5393cb9bdddf8e44b39936', 'work/analysis/lil_B177_voices_v4603/current2_static_names_voices_and207_catalog_rebind.json': '979023b067b0dd424658224f9d2360881748ba2e6198aacc71f4b878914cae08', 'work/analysis/lil_B177_branches_v4605/original_relative_skip_operand_proof.json': '42b941b404ec8a1fb020b54f43082ab1c4d3aa5b1618a180031bea1753a2d039', 'work/analysis/lil_B177_entry_v4606/source_EV2_B177_action_dependency_and_native_getter_binding.json': '2023f86c1b58d0a7bba8b1f422573be0344a0fe48c17a2a1fd3eaccdf33093db', 'work/analysis/lil_B177_controls_v4608/one_A000_C200_single_end_and3_source_leaves.json': '074ceefbbf5301e517865d49320cf8bfff09d30048d30a444a793880b23ce436', 'work\\analysis\\lil_B177_terms_v4609\\Owner_Cook_Genoa_and_prospective_tomato_fashion_reconciliation.json': 'd1e90991dc739095cf7d8099246b90ee1f068d1570df0d0703bc0ae35673b1e6', 'work/analysis/lil_B177_names_v4607/four_original_Owner_Cook_name_consumers_readonly_paths.json': '7f254e6a486763a275ef5a926c4c860f65c9abad383fca61af43fa1290ff35ed'}
CONTROL='work\\analysis\\lil_B177_dispatches_v4604\\all10_source_current_dispatches_no_macros_and3_control_leaves.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B177 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B177 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=20 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All ten source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE notice must remain null-actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B177 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B177-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';nine original54020 speeches,Owner174/Cook175,no source FI/FA/FO. Exact13 commands,opaque leading A0008,C200480,end482. Four read-only name paths;no resource,presentation,predicate,relative or typed objects. No natural eligibility or earned fashion-state claim.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B177-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one impersonal prospective Genoa tomato-fashion notice,original24310null actor then5473C before fallback.228x48logical/228x64physical paper;conservative216px planning. No invented speaker or name label;native complete-page approval remains separate.')
    raise ValueError('Unknown B177 consumer')
