"""Exact seven-block Mediterranean/Africa progressive and FE planning profiles."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
PROOF=Path('work/analysis/lil_Mediterranean_Africa_controls_v2761/source_bound146_preambles_FE_and_original_conditional_predicates.json')
PROOF_SHA='d607df7508955a1d276f6eb3299f2896af7229e5e8a749d6f9bd6d2b63f14174'
FE_RULE=Path('work/analysis/lil_Seville_FE_v2713/current_FE_macro_font_and_typed_paper_proof.json')
FE_RULE_SHA='eec677a7a5558d2dfddba929389c30a45c8eff94a158121ecae30d6a9870a677'
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['0bde3fb41d29752d941ec155a481305889767d696b49520165f42b1b0fca7bc7', '188b5dc99f739429d878bb4d5aabbb99a06d92cda04f023e8653e259ec3a25c6', '1bdfae670f0114108dc6fdb88423ec1174b3faaee6dec2699699c15b9694c8ba', '27ee6519e3a038b3df893bacf0920f2949f8c96af2ea31e3708faa59c0fc63fc', '7166d5644088e23e3613a7b34d4621f931ab48eba05fc644ff33344c014fe6d2', '8b9cb6c6a91f16d931f637363947d2e393537f0b1444d7111a50308f7a7ccc0d', '8fffb72f5e7f3391defef167ae11898fe0c2e0ed8a0a49f1d84fb1b48438e3a8', 'a575084dd4444205855df77269ad6c5f617ff1dcdbb4144094ac0c756a4081ef', 'bb23df35e348b5a4fa4053dd38a39750f154eefeb86d1133ec4bc65ab8eaabaf', 'de61fc4b210c71f3fca2add9078ab7f2fe3a386f95dae5072aa7983b14590ba5', 'e45f0aa7c272bec096316fd2bd5fa87171ff1486918fbecd497f7b0f5e293a84', 'e7bca3b1fc3c09cfa24591dbd92ad5d1649f4811131977b83eac681e717c851e', 'f417ec682d7f9823cb00806076ee4cc9fcc1eb907154ff11c422c81263ff25bb', 'f565a8418e3f304587fc41f1a7d911eab098aae8e8701ee551edd2bb57d25fe9'])


def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:
        raise ValueError('Mediterranean/Africa requires exact reviewed seven-block source/runtime')
    if sha(PROOF.read_bytes())!=PROOF_SHA or sha(FE_RULE.read_bytes())!=FE_RULE_SHA:
        raise ValueError('Mediterranean/Africa source-control or FE rule changed')
    proof=json.loads(PROOF.read_text(encoding='utf-8'));fe=json.loads(FE_RULE.read_text(encoding='utf-8'))
    expected={str(k):k for k in [2,4,9,11,14,16,20,21,23,34,35,36,84,113,114,151]}
    if (proof['ARM9_sha256']!=ARM9_SHA or not proof['all146_complete_preambles_and292_historical_dispatch_contexts_pass']
        or len(proof['dispatch_cases'])!=292 or proof['ordinary_native_actor_selectors']!=expected
        or fe['ARM9_sha256']!=ARM9_SHA or not fe['one_native_page_consumes_complete_target']
        or not fe['complete_native_independent_plane_and_all_glyphs_and_canaries_equal']):
        raise ValueError('Complete ordinary and inherited FE contracts required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-mediterranean-africa-progressive-runtime-bound-v1',leading_speaker_bytes=frozenset(expected.values()),
            metrics_source=base.metrics_source+'; exactB20/32/33/34/35/36/134complete preambles andordinary54020selectors. No individual new nameplate/activation claim;current fonts/reference/representative/release gates required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-mediterranean-africa-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+'; exactsource FEbeforefallback208and5473C,withsame-ARM inherited null-actor/228x48mode1paper rule. Conservative216pxplanning;fresh completeFEfont/pagination required.')
    raise ValueError('Unknown Mediterranean/Africa presentation consumer')
