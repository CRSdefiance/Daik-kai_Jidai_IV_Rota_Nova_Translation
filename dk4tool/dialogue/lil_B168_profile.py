"""Exact B168 source consumers:51 progressive speeches and three null-actor FE notices."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['32cd98a61f4800d10259270f63887f2dfdac40d1d9d17984f97e049783da8822', '53de30dc8018fb309688a4bf34e3d7f35f2650f747c6c1a294ce04e69ec8e335'])
SELECTORS=frozenset({2,6,9,20,76,87,165,166})
DEPENDENCIES={'work\\analysis\\lil_B168_source_v4168\\all54_clean_current_complete_context.json': '8f25d8f5c4d5094a2710cfcc0cd744ed8d9519e7f6fddc7561eea2d456429796', 'work\\analysis\\lil_B168_dispatches_v4171\\all54_source_current_dispatches_macros_FE_and16_control_leaves.json': '0ce3ed88ca7ea5ca520ca80aaebb3e0c8b26a5edea358b43592517e93817a5ff', 'work/analysis/lil_B168_voices_v4170/current8_static_names_voices_and207_catalog_rebind.json': 'fb40fd6639a521204aff982b67c637665b9bee9c9fd811be324a15f75f2a68a1', 'work/analysis/lil_B168_branches_v4172/original_relative_skip_operand_proof.json': '3b1d8a1a9d37e05d3173732a32524278e2df86a5c0601817842ae1756fe1b362', 'work/analysis/lil_B168_entry_v4173/source_EV2_B168_action_dependency_and_native_getter_binding.json': 'd3937013b0f33cef7aa4a4de29483700a7d1115aa994b2e85553c2f08a4ef0b8', 'work/analysis/lil_B168_controls_v4175/three_predicates_four_resources_six_presentations_and16_leaves.json': '0e54c5fa067c310efefb09012814d78a53b8c640b6103500dba9fee4b0443146', 'work\\analysis\\lil_B168_terms_v4176b\\current_Deck_officers_items_X_Brunei_and_naturalist_wording.json': 'bd8c5517ec0ad43d7f388eaf6642e8e758f5daeecb761db1a2c69f001dfc87b6', 'work/analysis/lil_B168_names_v4174/sixteen_original_name_consumers_and_owned_or_readonly_paths.json': '57e763ad0221f37f49358ce69fa0bec75c5cbb9b4d7b9e8b9f76e15a14133e69'}
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B168 clean/current source and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':return replace(base,name='lil-B168-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';51 original54020 speeches/eight static actors,FI7/FA1/FO1,twelve relative sites,three predicates and sixteen source leaves;printable57/4C/A5/A6 are mapped actors. No natural eligibility claim.')
    if consumer=='FE-paper':return replace(base,name='lil-B168-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),metrics_source=base.metrics_source+';three original null-actor5473C naturalist/nonofficer/Deck/item-information/X notices;216px conservative plan,separate228x48 logical/228x64 physical painter and complete input/pagination proof required.')
    raise ValueError('Unknown B168 consumer')
