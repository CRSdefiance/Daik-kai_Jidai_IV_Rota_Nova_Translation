"""Exact nine-block Kuhn/China progressive and FE planning profiles."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
PROOF=Path('work/analysis/lil_Kuhn_China_controls_v2894/source_bound218_preambles_FE_and_original_conditional_predicates.json')
PROOF_SHA='bfd01e8fd636ff3f60ba788d92de7130ca55c24d90708fb0e4e33ae67460d40c'
FE_RULE=Path('work/analysis/lil_Seville_FE_v2713/current_FE_macro_font_and_typed_paper_proof.json')
FE_RULE_SHA='eec677a7a5558d2dfddba929389c30a45c8eff94a158121ecae30d6a9870a677'
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['021481f3ad17f2786237d7de8d746a192be63cbe9fe4bbbd6151d8be9176ed25', '0e3f7f14eb20d64bf25efeea6f6a90cf18620da527ec772497de39a5ec74410d', '2196a091b9aad57233a564fcbcf2c27854327e017c67bd77ed600c17a8e046a7', '5fa7178787323a958e83f213ea92b750b7fd95c09577bec257f32ec84b7e2121', '620116cf5136a75497cc164852070eaf22b9f3cab3b119f7cd4defd297cdab54', '871dc90eefb50ab39225168d3d3ceb8d377f83f2d80f770607df769aa6556153', '8ba18ce9e747c7499d324dfb4d6e9e9476e336446d0eda4bfa40bb0945156dfa', '97d44d27fca3549be26cd0f91e7d38efa9d13614e29b36cb5aa9d9a1d04f57da', '9c08586846ca9f3230f21b6a17516ba88303af292b0b2d64f85ff9c07e338cac', '9ca288d67083be99fbd73714b9591d6425a1661d5334e3bd5bac2d02b694b9b1', 'a307447152f2a4f98ecfcb3ce93a8ba0e44d106bc1e04c2a69d53bd76f73c0ba', 'a774d4c53c823e1048e0f564d6fe920431245edfa228b4c3b036819d4f5f5afe', 'ada04ecf57706e9a0c27aed77e73a96eff34463864dac0e90ddb439df499bcd9', 'b2a93404be6724be4def94d8970eeda9696a382faa932cf4502bfb9b5505cb2f', 'c063634e8df8ec9353065884074ab172ae837e1620dcc6e66a227109bdc7c440', 'd1c3fba916dd92a9246555ddd449c6d7bcfc785549613fb7d4fc03f9a0689464', 'e7d718d0dc260e39025841df72b2bf05e7e2434e3eb3167706d2eca54c091407', 'fc1a9e674967ad7808a78e570e013301f7740974158c3d27ec96b72cf2984427'])

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:
        raise ValueError('Kuhn/China requires exact reviewed nine-block source/runtime')
    if sha(PROOF.read_bytes())!=PROOF_SHA or sha(FE_RULE.read_bytes())!=FE_RULE_SHA:
        raise ValueError('Kuhn/China source-control or FE rule changed')
    proof=json.loads(PROOF.read_text(encoding='utf-8'));fe=json.loads(FE_RULE.read_text(encoding='utf-8'))
    expected={str(k):k for k in [1,2,3,4,6,7,9,10,12,14,15,16,17,19,20,21,23,26,40,56,92,151]}
    if (proof['ARM9_sha256']!=ARM9_SHA or not proof['all218_complete_preambles_and436_historical_dispatch_contexts_pass']
        or len(proof['dispatch_cases'])!=436 or proof['ordinary_native_actor_selectors']!=expected
        or len(proof['current_original_predicate_cases'])!=40
        or not proof['all22_FE_before_fallback208_use5473C_and_original24310_null_macro_actor']
        or not proof['FE_FI_substitution_original_dispatcher_output_bound']
        or fe['ARM9_sha256']!=ARM9_SHA or not fe['one_native_page_consumes_complete_target']
        or not fe['complete_native_independent_plane_and_all_glyphs_and_canaries_equal']):
        raise ValueError('Complete ordinary and inherited FE contracts required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-kuhn-china-progressive-runtime-bound-v1',leading_speaker_bytes=frozenset(expected.values()),
            metrics_source=base.metrics_source+'; exactB51/52/53/54/55/56/146/147/148complete preambles andordinary54020selectors. No individual new nameplate/activation claim;current fonts/reference/representative/release gates required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-kuhn-china-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+'; exactsource FEbeforefallback208and5473C,withsame-ARM inherited null-actor/228x48mode1paper rule. Conservative216pxplanning;fresh completeFEfont/pagination required.')
    raise ValueError('Unknown Kuhn/China presentation consumer')
