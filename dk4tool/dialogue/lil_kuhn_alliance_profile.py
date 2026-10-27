"""Exact four-block Kuhn-alliance source/current-runtime planning profile."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
PROOF=Path('work/analysis/lil_Kuhn_Alliance_controls_v2848/source_bound82_preambles_and_original_conditional_predicates.json')
PROOF_SHA='5594aafa42a394e85346c515415ef88c05bdb4a78c7def6f01fb93c80c224c99'
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['333e76dd708f420d5ae1967ee2f2207c0beb1a6f38a6046c127de8db7e38fd10', '4d2d426179156f46f0bd3cfb727a27e1406ce296c1d524da0a658b6146b32aca', '6dc563fb28211e992512b593e36e1563bf91327225a83bc5a18b029a839d9bfd', '975cd4504c52b03fb31ffd9e2f442beacb163cb8b1cc147d1d35edcf30d94aae', 'aac1756409b009d69ea8ddac47b0b91eb7fa5801e0a9cd1e5a72df9ee0de82c5', 'b26af413ea621368f66c54351f7677d16a8a39e941876a67ee5a7e618a97e38d', 'cd34ee165831b7547f14ff444569e7e8b632f388cc5462ccd8b0e75c0706fcbf', 'f958fd7f80a9bb53381c15f254ac7859882b4424c150ba6923e5fb669cb14d04'])

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:
        raise ValueError('Kuhn alliance requires exact reviewed four-block source/runtime')
    if sha(PROOF.read_bytes())!=PROOF_SHA:raise ValueError('Kuhn alliance source-control proof changed')
    proof=json.loads(PROOF.read_text(encoding='utf-8'));expected={str(k):k for k in [2,4,6,7,9,11,15,16,19,20,21,40,56]}
    if (proof['ARM9_sha256']!=ARM9_SHA or not proof['all82_complete_preambles_and164_historical_dispatch_contexts_pass']
        or len(proof['dispatch_cases'])!=164 or proof['ordinary_native_actor_selectors']!=expected
        or len(proof['current_original_predicate_cases'])!=15 or not proof['source_owned_unaligned_read_scratch_restored_all4MiB_exact']):
        raise ValueError('Complete source-bound preamble andpredicate contracts required')
    if consumer!='progressive':raise ValueError('Kuhn alliance source has only ordinary progressive speech')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-kuhn-alliance-progressive-runtime-bound-v1',leading_speaker_bytes=frozenset(expected.values()),metrics_source=base.metrics_source+'; exactB47/48/49/50 completepreambles andoriginal54020selectors,including56Georg and40AntonyKuhn. No newnameplate/activationclaim;currentfont/reference/representative/release gates required.')
