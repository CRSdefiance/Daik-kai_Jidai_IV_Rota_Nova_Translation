"""B157's seven source static actors and two first-person FE null-actor panels."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['bd982a8c154fd40faf52200b41de0016a87e776be0473aed6c9f2d2814ef8613', 'e2ed6280f09c920f6ba64ddd4a7d45080dc59954f80aa79cfde685e8c11dea71'])
SELECTORS=frozenset({2,9,14,19,20,105,142})
DEPENDENCIES={'work\\analysis\\lil_B157_source_v3746\\all75_clean_current_complete_context.json': 'a6145162521d05ada8f6d5ed072b5087ffb245e99da53211dd4cb8c23ff375f1', 'work\\analysis\\lil_B157_source_v3746\\subset150_dispatches_and27_source_exact_control_leaves.json': 'dc1c2e33b89658550c4160989f8b35d2763975790c446ce73e6885701a088304', 'work\\analysis\\lil_B157_B160_source_v3744\\voices_and_entry_evidence_rebind.json': 'b3b6f93c0261c07104d30a3729d65a4318a5865d0513029a64c6ef171a3ad985', 'work\\analysis\\lil_B157_branches_v3747\\original_relative_skip_operand_proof.json': 'd1603fe43b53f4e59e6228821fced803932ba26803b14fe1fba65d6ba2224ec9', 'work\\analysis\\lil_B157_source_v3746\\seven_names_two_FE_and_original_entry_binding.json': '0ce41543b62af53325e22382f7ddd92ad6c54ad74ab22ee3bc6bbb5bdefdc769', 'work\\analysis\\lil_B157_controls_v3749\\two_predicates_two_C200_three_resource_sites_and27_source_leaves.json': '4e8a2b786b3fad8e0cd20136298e9d9aa6bfe6e70f1ded5136dfe86db5243473'}
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B157 clean/current source and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':return replace(base,name='lil-B157-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';73 original54020 speeches/seven static actors including Carlo13;FI2,8 relative sites and27 source leaves bound. No selected event eligibility claim.')
    if consumer=='FE-paper':return replace(base,name='lil-B157-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),metrics_source=base.metrics_source+';two original FE null-actor5473C first-person Carlo recollections;conservative216px planning with separate native228x48 logical/228x64 physical painter and complete-input/pagination proof required.')
    raise ValueError('Unknown B157 consumer')
