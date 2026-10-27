"""Exact B75-B79 recruitment/Julian speech and unlabeled FE consumers."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
PROOF=Path('work/analysis/lil_Recruits_Julian_controls_v3074/source_bound197_preambles_FE_and_original_conditional_predicates.json')
PROOF_SHA='099157e0ff0e834509053a34d37a85759e98503c370d2720f18fb969848ba494'
TERMS=Path('work/analysis/lil_Recruits_Julian_terms_v3076/clean_current_crown_Mihwa_alias_and_shipyard_UI_terms.json')
TERMS_SHA='d3e1ad936423f80248bf4e57f373787e2f9b5f6643da399c56c52b506c5c84ab'
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['1ae23d895b774aa7d30e162618bba30e2d4cee010fef842ee9c0cfc8c1000018', '732a376d3ca5f2ccaab51f1c9e36a0242224e60a0aaea0dd9d06376e5cc17691', '84ee915c1f12ca2949cd5534d333d8b88973eeb3a4f775613af36f2aaed8d90e', '920d02d0b6a0046b00c98f936ecd97868d91fb98a5d15e4b4f47cde3db90e8ed', 'ab8ba437b7a23dc0bc4ed5bbebf26768b990f7f7e765b50354eb0db6e2699458', 'bdf2bec6bf86c7253e8661a8e2c160f4667c311dda8fcf7567b5dff7e6c5fbe5', 'be55d75e0d3a204e4d06513b79d1a799b675105e46131dbfd5f187a7a99b0c38', 'd87aa6d96305e65791e512e14f1fadbcc94dbf68cee2c9320684f80f1ee8b3a0', 'e289599e962dd514e2d44168d21abbe941f5b2394d574fca97a779132d2e27fc', 'ebc95cb295c9db9357e15b0f7982140e667fd8f5d3be0bd983e3a1dd725e5d46'])
SELECTORS=frozenset([2, 4, 9, 12, 14, 18, 20, 22, 26, 41, 109, 158])

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:
        raise ValueError('Recruits/Julian requires exact reviewed B75-B79 source/runtime')
    if sha(PROOF.read_bytes())!=PROOF_SHA or sha(TERMS.read_bytes())!=TERMS_SHA:
        raise ValueError('Recruits/Julian source-control or approved terminology changed')
    proof=json.loads(PROOF.read_text(encoding='utf-8'));terms=json.loads(TERMS.read_text(encoding='utf-8'))
    if (proof['ARM9_sha256']!=ARM9_SHA or not proof['all197_complete_preambles_and394_historical_dispatch_contexts_pass']
        or len(proof['dispatch_cases'])!=394 or proof['ordinary_native_actor_selectors']!={str(k):k for k in SELECTORS}
        or len(proof['current_original_predicate_cases'])!=16 or proof['original_event_queries']
        or not proof['all1_FE_before_fallback208_use5473C_and_original24310_null_macro_actor']
        or not proof['all1_FE_source_unlabeled_ship_rename_guide_preserved_by_original_dispatcher']
        or terms['approved_item_name']!='Silla Gold Crown'
        or terms['versions'][1]['Mihwa_catalog201']['text']!='Mihwa'):
        raise ValueError('Complete ordinary, unlabeled FE and approved terminology contracts required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-recruits-julian-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+'; exactB75-B79 complete preambles and12 original ordinary54020 selectors. No new individual nameplate or earned recruitment claim; current font/reference/representative/release gates required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-recruits-julian-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+'; exact source FEbeforefallback208and5473C,original24310 null-actor unlabeled ship guide and inherited228x48mode1paper. Conservative216pxplanning; complete currentFEfont/pagination required.')
    raise ValueError('Unknown Recruits/Julian presentation consumer')
