"""Exact B158 source binding:15 progressive and4 original null-actor FE panels."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['99e2dff3eae3e2ef843c4662139d1622add8818f9bfc10704da5c9c1d1b09feb', 'c0ac85a5cd02ad03418e4ccdeda499b5094df39d1aa7638e3061fd0ce5690eb8'])
SELECTORS=frozenset({2,7,9,14})
DEPENDENCIES={'work\\analysis\\lil_B158_source_v3788b\\all19_clean_current_complete_context.json': '3fcd6919a0e2325a58a250062d39fbda9d7c14bc95721637726a76270d299459', 'work\\analysis\\lil_B158_source_v3788b\\subset38_dispatches_and22_source_exact_control_leaves.json': 'f63a64e363ec4cd1f0977511eb4401aa59fd520a5bae4550cc69e5e770366a67', 'work\\analysis\\lil_B158_B160_source_v3786\\voices_and_entry_evidence_rebind.json': 'ccdd9523ef90bfdc2e88cc7e67dfc7de88a162cdd9698ef3f57ac46e35f4ac8c', 'work\\analysis\\lil_B158_branches_v3789\\original_relative_skip_operand_proof.json': '43817688907e8f9b03069107c3f629317526a7d55c384a257b854faf02e4b225', 'work\\analysis\\lil_B158_source_v3788b\\four_names_four_FE_and_original_entry_binding.json': '200601b88ee730587ea94d899e4f9feafb377661ec2b616b7aa671387c54b3d7', 'work\\analysis\\lil_B158_controls_v3790\\six_predicates_four_resource_sites_two_pauses_and22_source_leaves.json': '482dab72a7689fcbc328371d48d28efadfe37991ce54cb531902714c1105fa3e'}
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B158 clean/current source and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':return replace(base,name='lil-B158-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';15 original54020 speeches/four actors, approved Cristina07, FI1,24 spans and22 source leaves. No natural event eligibility claim.')
    if consumer=='FE-paper':return replace(base,name='lil-B158-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),metrics_source=base.metrics_source+';four original null-actor5473C FE patron/cheering/applause panels with embedded labels;216px conservative plan, separate228x48 logical/228x64 physical painter and complete input/pagination proof required.')
    raise ValueError('Unknown B158 consumer')
