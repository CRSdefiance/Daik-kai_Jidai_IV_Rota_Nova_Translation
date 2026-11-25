"""Exact B201 complete rigging negotiation,three actors/twoFI/threeFE and both source paths."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='bceb685cd92f2ecf26746999fc7fc5e3c0a82b681f269d4e8a00044bb234360e'
BLOCKS={'f33dbaacc405653ceeaf83a0a2795ced98e6370f740b7a71aa9ab984b9145f3b', '90066ab0908e3bd2ec1891238e3a583b049f2b8f1aa3f167dde9de1b0ca5b396'}
SELECTORS=frozenset({2,19,105})
DEPENDENCIES={'work\\analysis\\lil_B201_source_v5902\\all26_clean_current_complete_context_with_two_choice_labels.json': '91fe1455e4c3f82d8446ed0cc887e8bb79482aa23e0432afd611a9b3ce0009f9', 'work/analysis/lil_B201_voices_v5903/current207_catalog_eight_voices_and_three_source_selectors.json': '8f8a92e8999e29da5d7c9c3d354497ecc0a783b952a4b9cb864c56a6262cd1a6', 'work/analysis/lil_B201_dispatches_v5904/all24_source_current_dispatches_two_FI_and15_control_leaves.json': 'd78be2bc8b79d402b080ed0e4283bef9d63ba313dfa114f61e183a3dde7dba91', 'work/analysis/lil_B201_branches_v5906/original_relative_skip_operand_proof.json': 'c5b51f8adb475b3105855dc3d25a1bb31dda8195e8206cc03123bb70a768a5be', 'work/analysis/lil_B201_entry_v5905/source_EV2_B201_action_dependency_and_native_getter_binding.json': '6420a3ae7874216273f8a6d1ba0d8a387e742549c954dc7beb50002428d80e04', 'work/analysis/lil_B201_controls_v5908/fifteen_exact_leaves_three_resources_two6003_picture_eight_structural_pairs_and_complete_end.json': '279d943cb286b8ecccafd67921f429418349592228e113c29ab36db0e2b6d35d', 'work/analysis/lil_B201_names_v5907/six_original_progressive_and_catalogue_name_consumers.json': '07504fcb2266d27544c8052b954b69935943788b9fe4e87c91387c138e91a789', 'work/analysis/lil_B201_funds_v5912/one_exact100000_source_price_one_unforced_and_five_offline_payment_boundaries.json': '1ee06ef02661978e831cde2f27bb5ae0f2d5cde1ecc86230cf2b5612b44a96f3', 'work\\analysis\\lil_B201_comparison_v5915\\complete_clean_context_source_paths_three_names_prices_stat_terms_and_item_scope.json': 'b9ba753759b90a921f3f6c7284bf4700b12c855af5ffe7a9d7a047ac04d76660', 'work/analysis/lil_B201_source_paths_v5914/two_actual_source_choice_paths_all24_speeches_all53_commands_and_returns.json': 'cd6696d9cd916803bf1979254e5c38485390e0e7dc9b75de2972b8c1b7b61a71'}
CONTROL='work/analysis/lil_B201_dispatches_v5904/all24_source_current_dispatches_two_FI_and15_control_leaves.json'
TERMS='work\\analysis\\lil_B201_comparison_v5915\\complete_clean_context_source_paths_three_names_prices_stat_terms_and_item_scope.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B201 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B201 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=48 or sum(r['source_selector']==254 for r in cases)!=6:raise ValueError('All24 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE must remain null actor')
    if control['source_macro_counts']!={'FI':2,'FA':0,'FO':0}:raise ValueError('B201 has exactly two original FI macros')
    terms=json.loads(Path(TERMS).read_bytes())
    if terms['source_actual_speeches']!=24 or terms['offline_only_speeches']:raise ValueError('Complete24-source-panel evidence required')
    if not terms['source_menu_Buy_decline_order_0_1_both_observed_no_delegation'] or terms['final_native_payment']!=100000:raise ValueError('Original two choice paths and final price required')
    if terms['native_source_voices']!={'2':3,'19':7,'105':0}:raise ValueError('All three source actors/voices required')
    if [r['stat'] for r in terms['source_FE_notices']]!=['Charm','Wits','Spirit']:raise ValueError('Three distinct original system notices required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B201-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';21 original54020 speeches,Lil2 voice3/Carlo19 voice7/Trader105 voice0,six original name consumers.44 source commands,one2100,four relative sites,no predicates,one complete end/no tailzeros. V5891 only name-data differs from prior font/runtime;native width,guard,pair phase and four rows unchanged.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B201-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';three original24310 null-actor then5473C notices:FI Charm+1,Carlo Wits+1,FI Spirit+1. Current defaultFI expandsLil3.228x48logical/228x64physical,conservative216px planning. Complete source paths observed;English scene and full effect semantics remain separate.')
    raise ValueError('Unknown B201 consumer')
