"""Exact B167 source/runtime binding:27 speeches,five actors,no macros,two ends."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['977043570dd446efe5e650ca1579194cacc30a2b24c9599a40c873746119bec9', 'a7983da5c74b59b21f20c14595376ba7b62ee305ce5b3f6c4c13621fe6af0430'])
SELECTORS=frozenset({2,4,13,23,109})
DEPENDENCIES={'work\\analysis\\lil_B167_source_v4118\\all29_clean_current_complete_context_with_typed_choice.json': 'ce115dee184d0e44d27940d7e56c96d8d0a1e16c286bcecf3b57cf7c2873e9c6', 'work\\analysis\\lil_B167_dispatches_v4121\\all27_source_current_dispatches_no_macros_and6_control_leaves.json': '7a310c2dc34c9c3ddb7b475372b371ebadbb8dbe76f09141417616aaecf374d3', 'work/analysis/lil_B167_voices_v4120/current5_static_names_voices_and207_catalog_rebind.json': 'a8a2f2297a9dc9a8ae613787229e00002214d8e461f5cd71497b20734f8a03f1', 'work/analysis/lil_B167_branches_v4122/original_relative_skip_operand_proof.json': '375049a0ba5b764e35880aa63cfd6f7d15f947a8b1998ab02138957ef8f19f36', 'work/analysis/lil_B167_entry_v4123/source_EV2_B167_action_dependency_and_native_getter_binding.json': 'bd0505a8e631c25dbfebdc224afd7b4c33e75e069dfac1c30bfd2ec7301bb03e', 'work/analysis/lil_B167_controls_v4125/two_Cesare_queries_two_resources_four_paths_and6_leaves.json': '0c4a1bfdd8f2a787cc94b7892a73a02044376a730c81386b99c5963553a5d0d7', 'work\\analysis\\lil_B167_terms_v4126\\six_sail_terms_current_Refit_bodies_and_Spritsail_Jigger_labels.json': '41156f5d350777799592b6ad979d3b2e623da1ef0b0c5d395d0426bbe6fa0696', 'work/analysis/lil_B167_names_v4124b/ten_original_names_owned_scratch_and_readonly_paths.json': '304c17f6f64560500b8e247f99283483544fe05bc7bf7e0fa92e8caaf673239c'}
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B167 clean/current source and runtime required')
    if consumer!='progressive':raise ValueError('Only original B167 progressive consumer is source-bound')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B167-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';27 original54020 speeches,five static actors including printable6D Shipwright andsource0D Cesare,no macros,twelve spans,two optionalCesare predicates,six exact leaves,two resources,one typed lecture choice andtwo separated ends. No A000. Typed2100 has a separate consumer. Older0D audit remains open.')
