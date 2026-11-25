"""Exact B171 source/current progressive consumer and three static actors."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['3eef66f9ac4a87991b9a95665470b95d831b5d9e657ef44d6ebf2942369c8fed', '7a2bc741e383516b09858d93b836176780e2905ec7f276c33adf7fb55f55ea12'])
SELECTORS=frozenset({2,25,81})
DEPENDENCIES={'work\\analysis\\lil_B171_source_v4311\\all37_clean_current_complete_context.json': '7390cbd9f0dd0ec0ddbaece8e8254678ff8b7656ea82cae70f83be26df8fb1b0', 'work\\analysis\\lil_B171_dispatches_v4313\\all37_source_current_dispatches_FI1_FO0_and8_control_leaves.json': '6a1c396c612ae13aabfbd1bae48c14b10e118f6d28e019efcd66b079041d8955', 'work/analysis/lil_B171_voices_v4312/current3_static_names_voices_and207_catalog_rebind.json': '445a2fde66692131d106a0e8f1afce565937f920defbd700db3d1818dd5c6548', 'work/analysis/lil_B171_branches_v4314/original_relative_skip_operand_proof.json': 'f9489154688b2a0eed72c145f2be30a61b324e3b400f55974140e1c8f368e3b3', 'work/analysis/lil_B171_entry_v4315/source_EV2_B171_action_dependency_and_native_getter_binding.json': 'a6f7de3681dccf410de8d39e76f970a01091999d173bb8700d3f29a25057d655', 'work/analysis/lil_B171_controls_v4317/one_resource_C200_four_presentations_two_ends_and8_source_leaves.json': '0d582e88109924b65384be6161ee9828061b36eb7ba45a62d7e782dda7e22bc5', 'work\\analysis\\lil_B171_terms_v4318b\\current_Taoist_arts_Sanghyeon_training_bond_and_new_facts_reconciliation.json': '487c3c8763a796d97514155bb93ded6bcc8e80fc2b995f23ca5d2853c2ad0b0d', 'work/analysis/lil_B171_names_v4316/six_original_name_consumers_and_owned_scratch_paths.json': 'c6fb96110b854d1d402b9ff86c0f6e4deed200c3da9807b1c80a9562a508f87e'}

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B171 clean/current source and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    if consumer!='progressive':raise ValueError('B171 has no FE or typed/dynamic text consumer')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B171-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';37 original54020 speeches,Lil2/Yifa25/Sanghyeon81,FI1,45 commands,eight leaves,four presentations,one resource,C200 andtwo endwords bound. Source51 is actor81,not literal Q. No natural event eligibility claim.')
