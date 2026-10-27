"""B178 exact controls:twelve progressive speeches and one impersonal FE notice."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['37c78894ad7fd955b0012326cb78086dfb0f9c4bed8e139809cf46f5cee75b8c', 'c68bac87bf4491bebf574cd232792b3088c27739acb80e4d19cb68136819411e'])
SELECTORS=frozenset({166,167,168})
DEPENDENCIES={'work\\analysis\\lil_B178_source_v4662\\all13_clean_current_complete_context.json': '45148195d7ea0f6b779d45366192113ce3a31748153becdb1203d934a8aa9ad9', 'work\\analysis\\lil_B178_dispatches_v4664\\all13_source_current_dispatches_no_macros_and3_control_leaves.json': '487edfa7fd4a33aa9d2e2b2a097c84ed9e2b56c1d338798fc5662dd9e6411e61', 'work/analysis/lil_B178_voices_v4663/current3_static_names_voices_and207_catalog_rebind.json': '5a75254059242fd4923adb93140c075901e38bfdd8e41dacd5e1af92be6b398f', 'work/analysis/lil_B178_branches_v4665/original_relative_skip_operand_proof.json': '6fed8bd14d6cf05fba381d8429a4e60a371e2e8f5b7d646e87d35a7051675684', 'work/analysis/lil_B178_entry_v4666/source_EV2_B178_action_dependency_and_native_getter_binding.json': 'd857380e4b3b96aa3ffd2bc7e37f91326989dd3782ed0a818b2bef42c76b95e1', 'work/analysis/lil_B178_controls_v4668/one_A000_C200_single_end_and3_source_leaves.json': 'fd30835e5cffc40a259ca3cd7179e15f0a5272462a9cb3f419633b58a9479a2d', 'work\\analysis\\lil_B178_terms_v4669\\three_Ladies_Amsterdam_Wheat_and_prospective_home_baking_fashion_reconciliation.json': '85a75fb35c3e20c85cfa8da4f62cef5c158f45f64b980caa15f685f042c459ea', 'work/analysis/lil_B178_names_v4667b/six_original_Lady166_167_168_name_consumers_readonly_paths.json': '025f98e7232fd984c9e0c6b569421f086d68b39658340b0aea6d0d83b7d1d1f9'}
CONTROL='work\\analysis\\lil_B178_dispatches_v4664\\all13_source_current_dispatches_no_macros_and3_control_leaves.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B178 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B178 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=26 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All thirteen source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE notice must remain null-actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B178 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B178-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';twelve original54020 speeches,Lady166/167/168,no source FI/FA/FO. Exact16 commands,opaque A0008,C200488,end490. Six read-only name paths;no resource,presentation,predicate,relative or typed object. No natural eligibility or earned fashion-state claim.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B178-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one impersonal prospective Amsterdam wheat-fashion notice,original24310null actor then5473C before fallback.228x48logical/228x64physical paper;conservative216px planning. No invented speaker/name label;native complete-page approval remains separate.')
    raise ValueError('Unknown B178 consumer')
