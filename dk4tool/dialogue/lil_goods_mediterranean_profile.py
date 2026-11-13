"""Exact five-block goods/Mediterranean source/current-runtime planning profile."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
PROOF=Path('work/analysis/lil_Goods_Mediterranean_controls_v2822/source_bound90_preambles_and_original_conditional_predicates.json')
PROOF_SHA='bd034cb77c66ee13d56373b27e6998489aaa79805191465594844f598c34b1d8'
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['0a1f12406332fa22439cd6a337fcc95da09cc64aa5bc450e8091c39f579bbb6a', '22372f4339b0999913baeb22ff5604e7c6e8d771855d98c4cb3a1a3824f7db87', '299c10a2b35e299cf96d37b87e13daa29fb47db322e62ee54e699fa125117d20', '3a061a767c24973ca6c1bbb3b2d91c979065981fdd4f1aca3e59ecbacf214a84', '5116904302665317636aedc8e713c97180546b13219cd370da6ca01d00321269', '5a459e7f44b0327ba2a31dcbee5b2db2825b944f61071208729108c85b3dccd2', '5d652e80f5e2abf115b5978cb5cadfae13bd267157668ef1a957ede56837e364', 'abc88d8c6a451a726da0c4de809aeab9ca5274b6c7fd462c09424bd6044dc46c', 'cc5d6e9bbf1e2e5cd0fb6bb66bf851ed769e650ab68f6c973b2271954a4509a5', 'd828d189de663f376f90495c4140dfa849dd9fe2a2aa63e8ae4837d051dc14f4'])

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:
        raise ValueError('Goods/Mediterranean requires exact reviewed five-block source/runtime')
    if sha(PROOF.read_bytes())!=PROOF_SHA:raise ValueError('Goods/Mediterranean source-control proof changed')
    proof=json.loads(PROOF.read_text(encoding='utf-8'));expected={str(k):k for k in [2,4,6,9,13,16,17,20,76,151,171]}
    if (proof['ARM9_sha256']!=ARM9_SHA or not proof['all90_complete_preambles_and180_historical_dispatch_contexts_pass']
        or len(proof['dispatch_cases'])!=180 or proof['ordinary_native_actor_selectors']!=expected
        or len(proof['current_original_predicate_cases'])!=32 or not proof['source_owned_unaligned_read_scratch_restored_all4MiB_exact']):
        raise ValueError('Complete source-bound preamble andpredicate contracts required')
    if consumer!='progressive':raise ValueError('Goods/Mediterranean source has only ordinary progressive speech')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-goods-mediterranean-progressive-runtime-bound-v1',leading_speaker_bytes=frozenset(expected.values()),metrics_source=base.metrics_source+'; exactB41/43/44/45/46 completepreambles andoriginal54020selectors,including76Mikhail and171ResearchStudent. No newnameplate/activationclaim;currentfont/reference/representative/release gates required.')
