"""Exact B141 progressive consumers,source monetary contracts and relative controls."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['92466a5cd13a5d982d98b8972b0f1b47e30985ba4843f3caa6a02f644a135702', 'dda11e2966e3b99da392561bd57d20684e1dfb62d882f03d86fec771fcb37673'])
SELECTORS=frozenset({2,9,20,171})
DEPENDENCIES={'work\\analysis\\lil_B141_source_v3532b\\all14_clean_current_complete_context.json': '6948048dafc924ffeed1908bee07543a08c0b13cbb3004e2b8f30c2ca656667f', 'work\\analysis\\lil_B141_controls_v3538b\\all14_source_current_dispatches_FI_C200_and630A_contract.json': '53ea11909b8307ebf531bf2d88e2ebe7e3cb8b01716f7dee11359e569a958adf', 'work\\analysis\\lil_B141_voices_v3533\\current_four_static_names_voices_and207_catalog_rebind.json': '7fe94a82ae3f7b72f8a04c33307407e7730b24dee6ca8df9ff78d1c20e127134', 'work\\analysis\\lil_B141_funds_v3537b\\source_million_threshold_and900000_payment_seven_boundary_cases.json': '97382e53bf47333fa3a01d36289fca25aff44b4306feff1aebcc2d955d6f1f4e', 'work\\analysis\\lil_B141_branches_v3539\\original_relative_skip_operand_proof.json': '2a8d1cb10dd6b3cd935f2b7c068606e448034f3d480f36cba0be730a7270cf21', 'work\\analysis\\lil_B141_entry_v3536\\source_EV2_B141_action_dependency_and_native_getter_binding.json': '8162582e0cb5e131a3415bf9bb279ab3406a0a6312cdcd48128817eaaf6dd88e', 'work\\analysis\\lil_B141_terms_v3541\\source_current_polder_and_distinct_monetary_amounts.json': '36ee07db886cbb88bd3e3c9b8d3e0db5c6cad252e698cd75152d768d212582bc'}
CONTROL=Path('work\\analysis\\lil_B141_controls_v3538b\\all14_source_current_dispatches_FI_C200_and630A_contract.json')
VOICE=Path('work\\analysis\\lil_B141_voices_v3533\\current_four_static_names_voices_and207_catalog_rebind.json')
FUNDS=Path('work\\analysis\\lil_B141_funds_v3537b\\source_million_threshold_and900000_payment_seven_boundary_cases.json')
BRANCH=Path('work\\analysis\\lil_B141_branches_v3539\\original_relative_skip_operand_proof.json')
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B141 clean/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    c,v,f,b=[json.loads(p.read_text(encoding='utf-8')) for p in [CONTROL,VOICE,FUNDS,BRANCH]]
    if consumer!='progressive' or len(c['speech_dispatch_cases'])!=28 or c['source_macro_counts']!={'FI':1,'FA':0,'FO':0} or len(c['source_C200_cases'])!=2 or len(c['source_630A_cases'])!=10 or len(v['fresh_four_actor_names']['rows'])!=4 or len(f['cases'])!=7 or f['source_threshold_gold']!=1000000 or f['source_payment_gold']!=900000 or len(b['cases'])!=130:raise ValueError('Complete four-actor,FI1,source monetary,C200/630A and relative contracts required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B141-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';14 B141 progressive speeches,four static actors,Lil captain2 and FI1. One-million threshold and900000 payment are source-bound. Opaque630A/resource bodies and selected scene are not executed by this profile.')
