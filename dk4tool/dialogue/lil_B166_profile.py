"""Exact B166 source binding:42 progressive speeches,four static actors,FI3."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['140e8c8f20a7e524972e233b838a0ef2bade0ae5566af323550d9af48f18e922', '8746f17f1de82ecccbea9bd8dd89df1cce2034b89b5cd54f399969739d16cd4c'])
SELECTORS=frozenset({2,9,20,23})
DEPENDENCIES={'work\\analysis\\lil_B166_source_v4054\\all44_clean_current_complete_context_with_typed_choice.json': '10d8cc03f71bb852ef6aeac0262a9c0292ea1e1928b9cb5b84e4c22b9f113da1', 'work\\analysis\\lil_B166_dispatches_v4057\\all42_source_current_dispatches_FI3_and11_control_leaves.json': '241e4d2dcd0f079b6eb29d303551a6bdf9b30e45a69ce681fb96fde665651846', 'work/analysis/lil_B166_voices_v4056/current4_static_names_voices_and207_catalog_rebind.json': '4a6cd4a92629b38dc48dd99646e6494f1500827700e3b712873f551a84e88a61', 'work/analysis/lil_B166_branches_v4058/original_relative_skip_operand_proof.json': '3e26c70b10ddc74cc3b7c0c59e05d0f03a6e8fe2d412ab8f2575a35042585dfa', 'work/analysis/lil_B166_entry_v4059/source_EV2_B166_action_dependency_and_native_getter_binding.json': 'c5bac0a32bf5415b2d15c0fcf718f01c32baf89d27eb10616fbc394a78648dcb', 'work/analysis/lil_B166_controls_v4061/Fernando_predicate_two_resources_advice_paths_and11_leaves.json': '81e25de11c1f1a0ef2207c72bde558ac9ba6a9cf1c13038e0382b65db9693417', 'work\\analysis\\lil_B166_terms_v4062\\nine_rooms_active_Speech_Shipwright_Surgeon_and_source_distinctions.json': '34414c171306e20c4f96b0e3faa3c432c4040b7932781388717823f41e33f3f0', 'work/analysis/lil_B166_names_v4060/six_original_Manuel_Fernando_Camille_name_consumers.json': '00ca2d7cc9fd51d6947cd3c6b08108b34656d0b521a63a02981c354de18d4878'}
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B166 clean/current source and runtime required')
    if consumer!='progressive':raise ValueError('Only original B166 progressive consumer is source-bound')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B166-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';42 original54020 speeches,four static actors,FI3,eight spans,one optionalFernando20 predicate,11opaque leaves,two resources,one typed advice choice andone laterA000 after both paths rejoin. Typed2100 requires its separate consumer;older0D audit remains open.')
