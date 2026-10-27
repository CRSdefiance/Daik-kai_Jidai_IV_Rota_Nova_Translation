"""Exact B152-B154 original progressive consumers and eight static selectors."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['022641ff57731444223fe527e979e4a4fa1425046a69c15e20a950d2c370524e', '70f6e838e9e14d130c5e16405574a7e66c5461ccb06b8b78da0d3a7a842eb2b5', '96870310053f6ecf42672b177b60701909c24260de8371cc0f1fec7bcd2dac12', 'ba938e624c1266e25755c113e2ed29948160af281cbb3b232a1eb2cc505e8860', 'e1159e0bd1716e934a2d59ca10a9be91b7223a760d22e58c15743a32beef49e4', 'e1bd01652546fcc6e8580e3050992ab0f480fcd7bb1da5bd8f6501d11aa4b140'])
SELECTORS=frozenset({2,9,14,17,20,92,115,148})
DEPENDENCIES={'work\\analysis\\lil_B152_B154_source_v3619\\all59_clean_current_complete_context.json': 'd14c86cfc488051008569d72117e9aeb046f24649b4375195167e9b1c6c16e38', 'work\\analysis\\lil_B152_B154_terms_v3621\\subset118_dispatches_and37_source_exact_control_leaves.json': 'bd7fd84c688aaab785224f894f8f6c51a963ad83e10f34ee210d4c614e4295bc', 'work\\analysis\\lil_B152_B160_voices_v3616\\current22_static_names_voices_and207_catalog_rebind.json': '090202f782fae3fbf7e0c967d4c7efb4dcb1ec2556bf0d9aea04204dce43e926', 'work\\analysis\\lil_B152_B154_branches_v3622\\original_relative_skip_operand_proof.json': 'fc305b2b7fb8c8738cdbade2f1da7922a5bf2a36d951c0d41fa40b1ba75d5760', 'work\\analysis\\lil_B152_B160_entries_v3620\\nine_original_entries_and_direct_dependency_getter_bindings.json': '5bc2227ae6888e39fdb04c9a905d02340b2e919c40827b7bd903a51b42ff3ed0', 'work\\analysis\\lil_B152_B154_controls_v3623\\two_predicates_three_C200_five_pictures_pause_and70_resource_cases.json': '3dc9ca094be37a6a3781add8cd50f1029de3f2eac80a5ffe3e5a3bafe1cf448c', 'work\\analysis\\lil_B152_B154_terms_v3621\\three_items_eight_names_and_59_source_context_terms.json': 'd526ceecbb43da511fa0fd7f6f6653fb696001070977b2b4a567a0b6de2a9a41'}
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B152-B154 clean/current source and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    if consumer!='progressive':raise ValueError('B152-B154 has no FE or dynamic text consumer')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B152-B154-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';59 ordinary54020 messages/eight static actors,including Barkeep92,PortWorker115,Guildmaster148 andAl17. Source FI3/FA1,2000pause/eightrelative sites andother source controls bound separately. No source scene eligibility claim.')
