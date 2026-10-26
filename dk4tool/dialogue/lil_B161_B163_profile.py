"""Exact B161-B163 source binding:45 progressive speeches/six original static actors."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['22f6d5b8fa6eea5f77560c63e32ebc874ff0289e277137469eaa508a55308bb7', '8ede078eb3dd5a58d203b5b44e2b570a2a82661b39ac9da1cdbba6814cf559a9', '9d84e231dd5d423800f53bcde72d579749ac119f2c5861b5402f92c077ad84c3', 'ae6a1eaed437ef980b112c94ef9965ab3205481f180d40cb519c0fe57aa25841'])
SELECTORS=frozenset({2,9,11,15,20,116})
DEPENDENCIES={'work\\analysis\\lil_B161_B163_source_v3912\\all45_clean_current_complete_context.json': 'ecafc0f891d32701eed9e2cd9f97d15e66f702e842e434685bbb787ca52161e1', 'work\\analysis\\lil_B161_B163_dispatches_v3915\\all45_source_current_dispatches_FI1_and29_control_leaves.json': '3038de1ba483affa7ac35949b5806741c7f560ce97cc91d15f4254554401de98', 'work\\analysis\\lil_B161_B163_voices_v3914\\current6_static_names_voices_and207_catalog_rebind.json': 'd1f1c5d079baee847d459a80c8e0c69e7b2eacfe908f76a68c1d8d70423882a4', 'work\\analysis\\lil_B161_B163_branches_v3916\\original_relative_skip_operand_proof.json': '9b4b27051ca668b2203e39ed82812d3c1c86b9305619033db908ecb3a49dbaa7', 'work\\analysis\\lil_B161_B163_entry_v3917\\source_EV2_B161_B163_action_dependency_and_native_getter_binding.json': 'ecc8adc34d2192eee11f1b6f6c26b620a6006d0249a5e0d0fc96960ca84265fa', 'work\\analysis\\lil_B161_B163_controls_v3918\\eight_predicates_two_C200_two_resource_values_one_pause_and29_source_leaves.json': '96b33ed22ff5bb46c6bb9fdbc7db7aff8cc0fe9df4bb0d522076eb47b4cee83f', 'work\\analysis\\lil_B161_B163_scope_v3920b\\six_names_source_entry_and_Jam_full_intro_binding.json': '8d63bb322f28597aded99740786166002d171756c9e9106832ca4cc96e9ec285', 'work\\analysis\\lil_B161_B163_names_v3919\\source_Jam_Ludwyan_progressive_and_Jam_Jack_Ludwyan_full_name.json': 'd9ad64c169b7fecfae885da85590bc01d0a7d0787097b1bdc6dd4222997b80bf'}
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B161-B163 clean/current source and runtime required')
    if consumer!='progressive':raise ValueError('Only original B161-B163 progressive consumer is source-bound')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B161-B163-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';45 original54020 speeches/six static actors,FI1,32 spans,29 leaves,eight predicates,two C200,one A000,one two-byte pause andfour ends;Jam Ludwyan progressive/Jam Jack Ludwyan full-name consumers bound. No natural eligibility claim.')
