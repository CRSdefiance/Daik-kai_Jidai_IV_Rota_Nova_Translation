"""Exact B164 progressive consumer;typed advice choice remains separate."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['0856f0dfa8f6f2402e424a159a97ecca37f4a1d7e53f181c18a7b5ca1508b9dc', '96b6589f7ba663ab7e590cb9fc7fa528f2769ba138049e4f23119b833eed1f58'])
SELECTORS=frozenset({2,9,13})
DEPENDENCIES={'work\\analysis\\lil_B164_source_v3960\\all49_clean_current_complete_context_with_typed_choice.json': '0a52999e8f7520bb30eb54c75842c11765b821f01f41e9c4485e5c63411b3287', 'work\\analysis\\lil_B164_dispatches_v3964\\all47_source_current_dispatches_no_macros_and9_control_leaves.json': '7a9121b385375715de79d1f3a852269f75d2d04d5d0e2c03da55287f279b41d2', 'work/analysis/lil_B164_voices_v3963/current3_static_names_voices_and207_catalog_rebind.json': 'dde434bfef42253fe5c6f80afd623a644c1201da514c908cf34089850cab64cd', 'work/analysis/lil_B164_branches_v3965/original_relative_skip_operand_proof.json': '00082fc03e142819592419b6edf889f990896477b7a58e8420cb265d6bd6b1b8', 'work/analysis/lil_B164_entry_v3966/source_EV2_B164_action_dependency_and_native_getter_binding.json': '5d3f0c4ae4865be77c5bcad34ade58730eceb856e6dbda0cefe146377c7cb706', 'work/analysis/lil_B164_controls_v3968/four_branches_typed_advice_outcomes_resource_and9_leaves.json': 'bbccf57555b7883c3a1050793f8ea1227587189f893090c0396c28a24c2db24a', 'work\\analysis\\lil_B164_comparison_v3969\\three_names_advice_choice_and_ship_terms_binding.json': 'e050ed9e4673b533a1781c5e722373446507c4734a7522571da247c80382e4cc', 'work\\analysis\\lil_B164_names_v3967\\source_Cesare_Tony_progressive_and_full_name.json': '51ce0278c82ec394fbf4e13d4044ed4ae03bf9e1f539c3692b824cc87c833de8'}
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B164 clean/current source and runtime required')
    if consumer!='progressive':raise ValueError('Only original B164 progressive consumer is bound here;typed2100 separate')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B164-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';47 original54020 speeches,3 static actors including0D Cesare Tony,no macros,4 relative sites,9 opaque leaves,one typed advice choice after A000 andtwo separated ends. Current0D proof does not close older audit.')
