"""Exact two-block homecoming/wedding and optional Ian consumer profiles."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
PROOF=Path('work/analysis/lil_Homecoming_Ian_controls_v3004/source_bound172_preambles_FE_and_original_conditional_predicates.json')
PROOF_SHA='6985085bb97a709c70a034fd4a0187bb6a477c499cc46b2243735e4f99834b18'
WEDDING=Path('work/analysis/lil_Homecoming_Ian_wedding_contract_v3006/historical_actual_wedding_FE_and_M26_source_contract.json')
WEDDING_SHA='655395a6b33a0d99700194b5e41cd45549be3cbe087ae125bc0807c0ed08805b'
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['0b6e0ae203913434a953220bb13592b340318a38b61aa9dc7ee014958a331f61', '42e6c4399d10b965bf3e82f9c2990ac84499f011352fc7c82d57309093c558e3', '865132bea803affde7dc85290bcbf4cd436a6af2355a17ca005d3a9aa4498a12', '9689ac3da7b47e63e0a9f53ff007aa70cd38798baa78f9c34060abc7f38f8a0c'])

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:
        raise ValueError('Homecoming/Ian requires exact reviewed B70/B71 source/runtime')
    if sha(PROOF.read_bytes())!=PROOF_SHA or sha(WEDDING.read_bytes())!=WEDDING_SHA:
        raise ValueError('Homecoming/Ian source-control or wedding rule changed')
    proof=json.loads(PROOF.read_text(encoding='utf-8'));wedding=json.loads(WEDDING.read_text(encoding='utf-8'))
    expected={str(k):k for k in [2,6,7,9,11,12,13,14,15,16,17,18,19,20,21,22,23,25,26,40,76,171]}
    if (proof['ARM9_sha256']!=ARM9_SHA or not proof['all172_complete_preambles_and344_historical_dispatch_contexts_pass']
        or len(proof['dispatch_cases'])!=344 or proof['ordinary_native_actor_selectors']!=expected
        or len(proof['current_original_predicate_cases'])!=31
        or not proof['all14_FE_before_fallback208_use5473C_and_original24310_null_macro_actor']
        or not proof['FE_FI_substitution_original_dispatcher_output_bound']
        or not wedding['current_native_paint_of_historical_first_wedding_body_complete_ink_and_blank_mask_equals_actual']
        or not wedding['current_complete_font_equals_historical_ROM_and_actual_resident_RAM']):
        raise ValueError('Complete ordinary and actual wedding FE contracts required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-homecoming-ian-progressive-runtime-bound-v1',leading_speaker_bytes=frozenset(expected.values()),
            metrics_source=base.metrics_source+'; exactB70/B71 complete preambles and22 ordinary54020 selectors. No individual new nameplate/activation claim;current fonts/reference/representative/release gates required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-homecoming-ian-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+'; exact14 source FEbeforefallback208and5473C,original24310 null-actor FI substitution andactual wedding228x48mode1paper. Conservative216pxplanning;fresh completeFEfont/pagination required.')
    raise ValueError('Unknown Homecoming/Ian presentation consumer')
