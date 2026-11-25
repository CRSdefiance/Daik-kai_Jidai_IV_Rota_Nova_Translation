"""Exact B190 two-actor conditional source/current progressive and FE profile."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'
BLOCKS=frozenset(['5e27896dc3163c02d66e9340d7c14e8dc13f4cc04cc444085dec4e5bad5352ce', 'bcf1d9ff7c3aca7376d5a9bc8c3488e145dac211a80a57d5e9f7bb8d362e8c85'])
SELECTORS=frozenset({119,159})
DEPENDENCIES={'work\\analysis\\lil_B190_source_v5314\\all17_clean_current_complete_context.json': 'd1eefa37c6b71a3fb1814de7c1bb8615bbefa245ecd7d3188e9d6d6b909ff7ca', 'work/analysis/lil_B190_dispatches_v5316/all17_source_current_dispatches_no_macros_and6_control_leaves.json': 'ee51c730159221188ff63b60887da459bd1b576be69529324c15946fa8aebdba', 'work/analysis/lil_B190_voices_v5315/current207_catalog_eight_voices_and_two_source_selectors.json': '4e15e136c0910c37bb091424bea87b76323f375abb913962684719af9f6f67da', 'work/analysis/lil_B190_branches_v5318/original_relative_skip_operand_proof.json': '19a16f766c7dc282cfae49e034f0d017cd9ab1b2232cfa715d903e5a4283a3d1', 'work/analysis/lil_B190_entry_v5317/source_EV2_B190_action_dependency_and_native_getter_binding.json': '73c7cb9f4dfd0ee6f645197f0866db3dc37c3cbedb9c3233aa87c8652d429543', 'work/analysis/lil_B190_controls_v5318/one_predicate_three_A000_C200_six_relative_sites_and_single_end.json': '07d4d0da90d606d062d6aa78104d767fc19bffe63c2a90ca7bee2ba5ddb61523', 'work\\analysis\\lil_B190_terms_v5320\\Sailor_Port_Worker_Havana_Medicine_and_reported_cure_reconciliation.json': '142b8a9f35d3b0526cd2471bbf1e3550c66432c6395377bad584e3c9decd9c23', 'work/analysis/lil_B190_names_v5319/four_original_progressive_and_catalogue_name_consumers.json': '2c466bd11cfe6b76ed21a3951d1ab0e65d358bef0b4389d709deba674957c5ce', 'work/analysis/lil_B190_predicate500_v5318/all8_original500_predicate_RNG_ownership_cases.json': '5df52d5a33d72be0ecf3f0da7ab5227b795ca70cc5015dd6541ca43e86cf6248'}
CONTROL='work/analysis/lil_B190_dispatches_v5316/all17_source_current_dispatches_no_macros_and6_control_leaves.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B190 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B190 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=34 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All17 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('The FE object must remain null-actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B190 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B190-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';16 original54020 speeches,clean PortWorker119 voice0/progressive Sailor159 voice4,distinct catalogue Retainer159,four read-only name consumers. Hex77/9F are decimal119/159.29 commands,one500 predicate at8,six relatives,three alternatives28/40/52,C200600,end602,two tailzeros. Current V5304 font/guards;fresh native approval required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B190-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310null actor then5473C object:tentative Medicine/Havana notice.228x48logical/228x64physical,conservative216px planning. Source category13 medicine,fullMedicine/compactMed labels unchanged;no single brand,verified cure,earned boom or earlier location claim;fresh native approval required.')
    raise ValueError('Unknown B190 consumer')
