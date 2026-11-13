"""Exact six-block Clifford/north/NewWorld ordinary andFE planning profiles."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
PROOF=Path('work/analysis/lil_Clifford_North_New_World_controls_v2968/source_bound143_preambles_FE_and_original_conditional_predicates.json')
PROOF_SHA='80106a6f46c674cbd71fc705242f6f0c10e712357d457c2e67328268875810f4'
FE_RULE=Path('work/analysis/lil_Seville_FE_v2713/current_FE_macro_font_and_typed_paper_proof.json')
FE_RULE_SHA='eec677a7a5558d2dfddba929389c30a45c8eff94a158121ecae30d6a9870a677'
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['1710c1db2a0c680c104c0fd381540535719f86400e01daa4709cc64e672af4b5', '210c9f6cb903d5752707367549b186765ab136bd0773fd2f72795cc447558f73', '61fede7c5da19d2470407354cfe30d71d359b882848b0c683bd273e63a4a90df', '66140adae97e6ed1600920f44e915938b32049b3bbe8d48ef9269c3aa39b4700', '9dd66abdff23bef3e691cc69eea5d5eba80d575bc015b201967b83b8bbeb7b2c', 'a94a40f772de9d0cacad899903b8a4f48e458eaf2c0d8948a9fb46f8805a32b1', 'af88cdad7f81e79bbafbcee8ce6ddb90159b1616f022a14887d3b14366b8a72d', 'b42353f71fcaad1089395e1f59f66fc3d42a4adfb1d2f1813b32a080b7f6b50a', 'b77e2f2c2f5559a4a0e1859d5e0abfad95dd38046a598a6be3bddfb6ac9fa1a1', 'cd98fd666a033bc35841be97de7d0e2bd8c4a8e4dcbb14ab499c261ee085202c', 'd6c67d8d5ab32bf5a29acea67c76e5fe35e6080491baa78825bb25a6a6c458bb', 'd88104bc2ba46a8e28c34a2fc2a5848b382114c8cb867208b84a1bf4e780ed8f'])

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:
        raise ValueError('Clifford/north/NewWorld requires exact reviewed six-block source/runtime')
    if sha(PROOF.read_bytes())!=PROOF_SHA or sha(FE_RULE.read_bytes())!=FE_RULE_SHA:
        raise ValueError('Clifford/north/NewWorld source-control or FE rule changed')
    proof=json.loads(PROOF.read_text(encoding='utf-8'));fe=json.loads(FE_RULE.read_text(encoding='utf-8'))
    expected={str(k):k for k in [2,9,11,12,13,14,16,17,18,20,21,22,27,28,42,92,151]}
    if (proof['ARM9_sha256']!=ARM9_SHA or not proof['all143_complete_preambles_and286_historical_dispatch_contexts_pass']
        or len(proof['dispatch_cases'])!=286 or proof['ordinary_native_actor_selectors']!=expected
        or len(proof['current_original_predicate_cases'])!=45
        or not proof['all3_FE_before_fallback208_use5473C_and_original24310_null_macro_actor']
        or not proof['all3_FE_source_bodies_have_no_name_macros']
        or fe['ARM9_sha256']!=ARM9_SHA or not fe['one_native_page_consumes_complete_target']
        or not fe['complete_native_independent_plane_and_all_glyphs_and_canaries_equal']):
        raise ValueError('Complete ordinary and inherited FE contracts required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-clifford-north-new-world-progressive-runtime-bound-v1',leading_speaker_bytes=frozenset(expected.values()),
            metrics_source=base.metrics_source+'; exactB67/68/69/149/150/151complete preambles andordinary54020selectors. No individual new nameplate/activation claim;current fonts/reference/representative/release gates required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-clifford-north-new-world-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+'; exactsource FEbeforefallback208and5473C,withsame-ARM inherited null-actor/228x48mode1paper rule. Conservative216pxplanning;fresh completeFEfont/pagination required.')
    raise ValueError('Unknown Clifford/north/NewWorld presentation consumer')
