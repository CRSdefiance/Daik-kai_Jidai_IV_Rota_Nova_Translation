"""Exact B172 source/current progressive consumer and three static actors."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['f6c2929a1937c65d5d51dee41fb5d8a84cfd46140e62654629bd685238eac0c6', 'feb4596dcc453b242d6e13aedb93aa1908699ea00f2d23750ff230be457ca59e'])
SELECTORS=frozenset({2,26,201})
DEPENDENCIES={'work\\analysis\\lil_B172_source_v4364\\all27_clean_current_complete_context.json': '42c973da2c2256a4951da2d6eb0922e93ff9c54addcb25320e41a73c448bbd5c', 'work\\analysis\\lil_B172_dispatches_v4366\\all27_source_current_dispatches_no_macros_and11_control_leaves.json': '5bfa0b55df53eb4872928a5cf9fd0192a1842a1eb67df9a1864be3846b93d3b4', 'work/analysis/lil_B172_voices_v4365/current3_static_names_voices_and207_catalog_rebind.json': '409052fbcc8923152ba7bba455aba4645b4622b51a22a78c7e540d73fad4ee31', 'work/analysis/lil_B172_branches_v4367/original_relative_skip_operand_proof.json': '678447e3ea741a8995799e83b131c75dc6df5e8ecdf26d2e7954d99b4a89b47f', 'work/analysis/lil_B172_entry_v4368/source_EV2_B172_action_dependency_and_native_getter_binding.json': '15f946a34f3809604f79bf0133183e1a273a9406cc3cb3d536b23701494ce4f2', 'work/analysis/lil_B172_controls_v4370/three_resources_C200_five_presentations_later_A000_one_end_and11_source_leaves.json': '546ae41595cd3c94ac3fdf5bf85d974bfcaff3c48bc66b1cb1f84a88b9a8fff7', 'work\\analysis\\lil_B172_terms_v4371\\current_crown_Seoul_names_and_qualified_date_reconciliation.json': '60b25832404e2a83fbab92476346fd978b3a4b0e9b33c2499fc68331d97f7ca4', 'work/analysis/lil_B172_names_v4369/six_original_name_consumers_and_owned_scratch_paths.json': '0a81be32ed6b9787d193754a2cb172988cfcf7ade3c7fd25da4b25e2d09c580e'}

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B172 clean/current source and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    if consumer!='progressive':raise ValueError('B172 has no FE or typed/dynamic text consumer')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B172-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';27 original54020 speeches,Lil2/Julian26/Mihwa201,no FI/FA/FO,38 commands,11 leaves,three resources,five presentations,C200 then later A000 and one tail end. Source1A/C9 are actor26/201,not literal prose. Mihwa original name pointer is readonly;Lil/Julian owned scratch paths are preserved. No natural event eligibility claim.')
