"""Exact six-block India/polder/gift source/current-runtime planning profile."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
PROOF=Path('work\\analysis\\lil_India_Polder_controls_v2794\\source_bound119_preambles_and_original_conditional_predicates.json')
PROOF_SHA='a4f411887b9b2ace70d60b6a2803c53733b15cdf093051a60899bb57325aef7f'
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['012051926e81bea4a967dee7ef1a484e8e6c372e8dc4f619e2495a1b3287483b', '0596209beef8252708ac1c78e9d9855c6a425fff8fb1ff8591893cd711f52cd3', '376faa767e0ba8151333db8cb81a67d43610eba2386cb5be6713e0bf5cce93e1', '54cb31df75fcb472c40c2ef7073538b2769d3a1499667aa229a761a14f08679b', '6bbf2b03a351840ecec0781d29b0636f88f845d7fbbfb8ae5bae218cf6f11334', '79c487a32d9f3e5d592fa0868f9fd03fce199ca78806946f152272b9f5712367', '7b04b14802c1efbd02f5ccd666d868a3888eeed836553a2dc67c793af8174f9f', '9c5250d302631ffeb30b2ac882a7d4b3295b6e1feaaf4ecedc5dfeb652ac8c3d', '9ec570b09d486bc320d9bdab9b7c3ca228af360c1bb0f9817075ce4c04b96673', 'a3f3fe1f1e361aee96dc113d547f4f6933cf03e8bb111f07a494acd151fe0397', 'b3ef2d1516d0c798985e2f31103429e7f369f260eddfc6f8adad7a1eb50c0cea', 'e533e665318a078a582c72d56ad2d8865dbaf6a74f3c2dd462fef5336eda4d80'])

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:
        raise ValueError('India/polder requires exact reviewed six-block source/runtime')
    if sha(PROOF.read_bytes())!=PROOF_SHA:raise ValueError('India/polder source-control proof changed')
    proof=json.loads(PROOF.read_text(encoding='utf-8'));expected={str(k):k for k in [2,9,16,21,92,151,171]}
    if (proof['ARM9_sha256']!=ARM9_SHA or not proof['all119_complete_preambles_and238_historical_dispatch_contexts_pass']
        or len(proof['dispatch_cases'])!=238 or proof['ordinary_native_actor_selectors']!=expected
        or len(proof['current_original_predicate_cases'])!=10 or not proof['source_owned_unaligned_read_scratch_restored_all4MiB_exact']):
        raise ValueError('Complete source-bound preamble andpredicate contracts required')
    if consumer!='progressive':raise ValueError('India/polder source has only ordinary progressive speech')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-india-polder-progressive-runtime-bound-v1',leading_speaker_bytes=frozenset(expected.values()),metrics_source=base.metrics_source+'; exactB37/38/39/40/129/130 completepreambles andoriginal54020selectors,including171ResearchStudent. No newnameplate/activationclaim;currentfont/reference/representative/release gates required.')
