"""Exact two-block homecoming/wedding and optional Ian consumer profiles."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
PROOF=Path('work/analysis/lil_Christina_Mivor_controls_v3037/source_bound145_preambles_FE_and_original_conditional_predicates.json')
PROOF_SHA='57b69aa6d40f4b0971362b280103595646369e3fa5875091c222466f818250cb'
NAMES=Path('work/analysis/lil_Christina_Mivor_names_v3039c/current_registered_names_and_source_identity_contract.json')
NAMES_SHA='31d47b746898cc307b3fa8556059e6f932b7fbd19b4efee4b6983d550c65ebdf'
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['19b374a1bb58dc0e3dc4535b7c36950d5ee24b60aec982e1ce922558ebbd67df', '2342cbf9bdaf1cdaa8e910c09cfd7ff8d8e73d8f6964eb61a3bf0caa039e2cc7', '46ec686311c0de92f6af56271fb263895951303944396561ce850e06cc7e8ef3', 'ded04447b535cf1f39e6773451c111c1e8711539df929131ec09a3575dadf28a'])

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:
        raise ValueError('Christina/Mivor requires exact reviewed B72/B73 source/runtime')
    if sha(PROOF.read_bytes())!=PROOF_SHA or sha(NAMES.read_bytes())!=NAMES_SHA:
        raise ValueError('Christina/Mivor source-control or wedding rule changed')
    proof=json.loads(PROOF.read_text(encoding='utf-8'));names=json.loads(NAMES.read_text(encoding='utf-8'))
    expected={str(k):k for k in [2,6,7,9,20,79,162,167]}
    if (proof['ARM9_sha256']!=ARM9_SHA or not proof['all145_complete_preambles_and290_historical_dispatch_contexts_pass']
        or len(proof['dispatch_cases'])!=290 or proof['ordinary_native_actor_selectors']!=expected
        or len(proof['current_original_predicate_cases'])!=3
        or not proof['all3_FE_before_fallback208_use5473C_and_original24310_null_macro_actor']
        or not proof['all3_FE_source_visible_Boy_labels_preserved_by_original_dispatcher']
        or names['Mivor_full_name']!='Mivor Genz'
        or not names['original_name_ring_scratch_restored_recovers_all4MiB']):
        raise ValueError('Complete ordinary and actual wedding FE contracts required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-christina-mivor-progressive-runtime-bound-v1',leading_speaker_bytes=frozenset(expected.values()),
            metrics_source=base.metrics_source+'; exactB72/B73 complete preambles and8 ordinary54020 selectors. No individual new nameplate/activation claim;current fonts/reference/representative/release gates required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-christina-mivor-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+'; exact3 source FEbeforefallback208and5473C,original24310 null-actor source-labeled Boy panels andinherited228x48mode1paper. Conservative216pxplanning;fresh completeFEfont/pagination required.')
    raise ValueError('Unknown Christina/Mivor presentation consumer')
