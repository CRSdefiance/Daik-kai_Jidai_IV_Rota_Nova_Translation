"""Exact B170 source/current progressive consumer and two static actors."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['a6467dcc379b11c3a6b45563e994005864d872c23b8aa5726570ec6a15677260', 'e0926b0d4f96d701b614d3f236d2caf68fd79c774d0e7df6c696fea99818f3e3'])
SELECTORS=frozenset({2,25})
DEPENDENCIES={'work\\analysis\\lil_B170_source_v4260\\all33_clean_current_complete_context.json': '9a3594df24bf3c9b545473349bbeda1522a20f0ae1f848fd2d2b7464cef0ce92', 'work\\analysis\\lil_B170_dispatches_v4263\\all33_source_current_dispatches_FI1_FO1_and12_control_leaves.json': 'ada9460fa6c6e8f93e4dd24d53f8b609c71f62144816be96d63841269208a9fd', 'work/analysis/lil_B170_voices_v4262/current2_static_names_voices_and207_catalog_rebind.json': '2a5c7a36ba19b8f78f99100e772d4e374dbf9dd3bab39661bcaaaf12d3b722f6', 'work/analysis/lil_B170_branches_v4264/original_relative_skip_operand_proof.json': 'b7dde150273dfa9af4e844860ffea29633cc3837d5b3abd6908e4f430f19c509', 'work/analysis/lil_B170_entry_v4265/source_EV2_B170_action_dependency_and_native_getter_binding.json': 'cbe218632bb57b6b68804a12a4349fd6a8df80061cbecc2408e57a50c6f4419d', 'work/analysis/lil_B170_controls_v4267/two_resources_C200_pause_two_ends_and12_source_leaves.json': '4212405fe64ba0c0b73ea8cac9504441953258e8cf2abb4af386be02c56da500', 'work\\analysis\\lil_B170_terms_v4268\\current_Taoist_arts_Yifa_names_and_source_address_reconciliation.json': '1ea1a8c4694dc2f55f9be9a6da67c028e918cbc29eca5fce02da6100275d993b', 'work/analysis/lil_B170_names_v4266/four_original_name_consumers_and_owned_scratch_paths.json': '7768aedcf1245b246d86bb910eb6b3372490786b35929919b58948dcf9bf5949'}

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B170 clean/current source and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    if consumer!='progressive':raise ValueError('B170 has no FE or typed/dynamic text consumer')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B170-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';33 original54020 speeches,Lil2/Yifa25,FI1/FO1,45 commands,one pause,C200,two resources andtwo endwords bound. Source19 is Yifa25,not removable text. No natural event eligibility claim.')
