"""Exact B155 original progressive consumers andfive static actors."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['6fade983a1bf916805b28521d3113bcc7036ae587a60239c43f1614e69b6693c', '824bb4e25d253056374e4b4d267de43f68d95a4b241c3538450cb040462e67c0'])
SELECTORS=frozenset({2,6,9,15,20})
DEPENDENCIES={'work\\analysis\\lil_B155_source_v3658\\all50_clean_current_complete_context.json': 'cd7ff354417b0995ce8a545943382c6bffd1a0d9c9e67f4d625557be9cb78953', 'work\\analysis\\lil_B155_source_v3658\\subset100_dispatches_and21_source_exact_control_leaves.json': '17ecaf62336ff586def37545cb2c4246707917a8eea6ab6c16b46a556c76aa3d', 'work\\analysis\\lil_B155_B160_source_v3656\\voices_and_entry_evidence_rebind.json': '32790c9364d9db18debe0a7f59b193e0757960701c575b5d47dea1e24ca7a05f', 'work\\analysis\\lil_B155_branches_v3659\\original_relative_skip_operand_proof.json': '8fcb7618d278d63269c6fe13996019919b093d436408d99513aa2cb69ccd13c1', 'work\\analysis\\lil_B155_source_v3658\\five_names_and_original_entry_binding.json': '8ca5e49f3801328baf4539b3631075b39028900a4da6771d92190eeed595907a', 'work\\analysis\\lil_B155_controls_v3660\\seven_predicates_six_resource_sites_forty_boundaries_and21_leaves.json': '259db6478f4045f88d35c059df7ea070f7a63ea7a432c0be077168659a1d97cd'}
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B155 clean/current source and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    if consumer!='progressive':raise ValueError('B155 has no FE or dynamic text consumer')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B155-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';50 original54020 speeches/five static actors includingAngelo0F;sourceFI5/FA1,sevenpredicates,29relative sites,sixresource sites andtwoendwords bound. No natural event eligibility claim.')
