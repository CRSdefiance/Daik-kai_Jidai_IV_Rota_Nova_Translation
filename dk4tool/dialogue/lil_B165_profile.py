"""Exact B165 source binding:24 progressive speeches,three static actors,FI3."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['61ee9554cab518d51b7a5be118d91527778434d7da3ad8eaf45cbeeef71b67fe', 'a124678ec1f316d837205bb66602e59bec783465fb6f797c1612579b38c7546f'])
SELECTORS=frozenset({2,6,9})
DEPENDENCIES={'work\\analysis\\lil_B165_source_v4008\\all24_clean_current_complete_context.json': 'd92c7b796bcd994a6ea9b866608bc200c9ed384f86a9082a412de9c6637f780f', 'work\\analysis\\lil_B165_dispatches_v4012\\all24_source_current_dispatches_FI3_and12_control_leaves.json': '9fe4e16e0befd8a1d4494f92aa19e3b46d481cb898aba0a3c2d130043c539c5d', 'work/analysis/lil_B165_voices_v4011/current3_static_names_voices_and207_catalog_rebind.json': '2a2ee845dd05e5829c2f5718827df453e977bec14427fff2800822c88bbe18d6', 'work/analysis/lil_B165_branches_v4013/original_relative_skip_operand_proof.json': 'e64cbe460e63651a09eb8913bf774f55a3fb371c4c71a076734f7b8fd0a9df37', 'work/analysis/lil_B165_entry_v4014/source_EV2_B165_action_dependency_and_native_getter_binding.json': 'a2703057e3944e5ff11227041fc13295757e9b0261f43ab282654a0db92808e7', 'work/analysis/lil_B165_controls_v4015/five_Camille_queries_solo_present_alternatives_resource_and12_leaves.json': '0ef7df481371b87b489d0d3340d8627312b41cae92ecc8974c257046cbdb8532', 'work\\analysis\\lil_B165_comparison_v4017\\three_names_FI3_source_alternatives_and_active_navigator_joke_binding.json': '738ec0b9119b3245d9ccb8caccd72d20ef230d93b0678a7959054ff9d42805a1', 'work\\analysis\\lil_B165_names_v4016\\source_Julio_Erneco_progressive_and_full_name.json': '18a74c287e20bcc0a02a82ea7f0251f2d36cbbad4c248a5379fb3b9a56485047'}
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B165 clean/current source and runtime required')
    if consumer!='progressive':raise ValueError('Only original B165 progressive consumer is source-bound')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B165-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';24 original54020 speeches,three static actors including Julio06,FI3,20spans,five Camille membership sites,12opaque leaves,resource6329,oneA000 andone end. Firstsolo remark differs fromoptional three-line Camille exchange. No natural eligibility ornewrelationship claim.')
