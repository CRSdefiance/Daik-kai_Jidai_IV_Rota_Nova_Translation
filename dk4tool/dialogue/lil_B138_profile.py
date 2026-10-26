"""Exact B138 progressive profile with raw result2 and the source event137 query."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['baa641a2c11bfd0dc6dd2cbc859c0f291d1d6e1890e03686ed0addec115051f7', 'dac52550b132918191bdc0a83c078595c91ab9e9f6ed15e16ef56a8482a77711'])
SELECTORS=frozenset({2,14,20,21,22,23,92})
DEPENDENCIES={'work\\analysis\\lil_remaining_B138_B140_source_v3422\\next44_B138_clean_current_context.json': 'afbf625c13c3a5adb575a91d708ec89fa726c6ba1ecb29e56d89416dd36e96e2', 'work\\analysis\\lil_B138_controls_v3426e\\all44_source_current_dispatches10_predicates_and1_query.json': '5e8dfccb8352d8c8aff4b6fdfc0041faa86a4a5b46301a288d9f885670452095', 'work\\analysis\\lil_B138_voices_v3425\\current_seven_static_names_voices_and207_catalog_rebind.json': '643233434b187167825437fc3e8b8c913b1349dfe5d75a12c8a5a0cf31b24699', 'work\\analysis\\lil_B138_terms_v3429\\clean_current_names_leaf_price_macro_and_entry_reconciliation.json': '6b90d3642c51490f6f8a356fc2114720285aa87eb59ac1d33005b6a4bea13e60', 'work\\analysis\\lil_B138_branches_v3427b\\original_relative_skip_operand_proof.json': '740a68d90dbdd17fa4fb8189e734a4624463052ca5e136d7a993476613c1763b', 'work\\analysis\\lil_B138_controls_v3426e\\current_registered_name_catalog_binding.json': '5d907f7a5c9e57a08cf441ff03e4fe42c7fd4da26ab4b7dd322b0bc994644bfc', 'work\\analysis\\lil_B138_conditional_contract_v3426d\\native_result_contract.json': 'd965445aa44ce5b5754a20e6fc067b04231fda4e7076f64707dde7559b74f0de'}
CONTROL=Path('work\\analysis\\lil_B138_controls_v3426e\\all44_source_current_dispatches10_predicates_and1_query.json')
VOICE=Path('work\\analysis\\lil_B138_voices_v3425\\current_seven_static_names_voices_and207_catalog_rebind.json')
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('B138 exact clean/current block andruntime required')
    for p,digest in DEPENDENCIES.items():
        if sha(Path(p).read_bytes())!=digest:raise ValueError('B138 source contract changed:'+p)
    control=json.loads(CONTROL.read_text(encoding='utf-8'));voice=json.loads(VOICE.read_text(encoding='utf-8'))
    if consumer!='progressive' or len(control['speech_dispatch_cases'])!=88 or len(control['current_original_predicate_cases'])!=11 or len(control['original_event_queries'])!=1 or control['original_event_queries'][0]['event']!=137 or control['source_macro_counts']!={'FI':0,'FA':0,'FO':1} or len(voice['fresh_seven_actor_names']['rows'])!=7:raise ValueError('Complete B138 actors,predicates,event137 query andFO contracts required')
    result2=[c for c in control['current_original_predicate_cases'] if c['source_command_hex']=='0080ffff200301a1']
    if len(result2)!=1 or result2[0]['native_result']!=[2,2,0,0,0,0]:raise ValueError('B138 source raw-result2 contract required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B138-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';44 progressive speeches,seven static actors. FI3/FA5/FO9 use Lil captain2;FO1 in source. Ten predicates preserve raw result2 andone event137 query remains Boolean. No FE/source00/dynamic/4100/2000/2100.')
