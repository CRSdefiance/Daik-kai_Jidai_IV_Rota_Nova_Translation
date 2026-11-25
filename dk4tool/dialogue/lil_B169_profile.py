"""Exact B169 source consumers:36 progressive speeches,six static actors,FI5/FO2."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['02bd3e65cbc585df1f6598e5a2f8cbf7423ea085118124eba5cd77686a511537', '99e01d2fd2b90b0d4cfa8531859f304818f8cf06f3213ed7bc5f07f3f2e45990'])
SELECTORS=frozenset({2,6,9,20,21,76})
DEPENDENCIES={'work\\analysis\\lil_B169_source_v4211\\all36_clean_current_complete_context.json': '22fa983890fbd43fc5d95642f61f6badf0f7492d037f9f280bde0094671584b7', 'work\\analysis\\lil_B169_dispatches_v4214\\all36_source_current_dispatches_FI5_FO2_and5_control_leaves.json': '83f086b7d9147a3e8072c68a7238c65fe3b0b4f350a1cae2a81de1d9654eb8e9', 'work/analysis/lil_B169_voices_v4213/current6_static_names_voices_and207_catalog_rebind.json': '50b44600bb306cabc4c860178d22589a741e07a1a1c58819bd6981ffdb201feb', 'work/analysis/lil_B169_branches_v4215/original_relative_skip_operand_proof.json': 'a5b0ca9ea6770e13e91d07f67d958f2db1046859cb7531a1d10e22ee6567c594', 'work/analysis/lil_B169_entry_v4216/source_EV2_B169_action_dependency_and_native_getter_binding.json': 'c80b76eaf73a438be64329ab66fc167f358d1629c741e4562759f20ad2e9470b', 'work/analysis/lil_B169_controls_v4218/three_predicates_five_leaves_and_eight_source_paths.json': '19aed3f283b01196435ec55fb467015225c33ce8b28e0f41a92e4b96fbdfd571', 'work\\analysis\\lil_B169_terms_v4219\\current_Proof_title_Tavern_ruins_names_and_older_variant_refs.json': '855a0a4e83068381d7e491982d81ba4b7fe6ec3834764ff53bd11bbd3bcf7a05', 'work/analysis/lil_B169_names_v4217/twelve_original_name_consumers_and_owned_scratch_paths.json': 'bc847ce397d596341fc1a12b5a4351499b1d13bf294c0a7bf212e695c9cf7b7f'}

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B169 clean/current source and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    if consumer!='progressive':raise ValueError('B169 has no FE or other speech consumer')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B169-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';36 original54020 speeches/six source static actors,FI5/FO2,twelve relative sites,three predicates,five opaque leaves and one tail end;15 is Ian21 and4C is Mikhail76. No natural eligibility claim.')
