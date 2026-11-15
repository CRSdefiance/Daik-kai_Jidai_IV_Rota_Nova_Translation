"""Exact B186 source/current conditionals, Owner/Cook roles and two text consumers."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'
BLOCKS=frozenset(['119ae1c99ea180a72d17125006bb4d721da131d0f40065ce22dd125637843c7b', 'fa9a9b5ef5c68312672f5a1f6790d909a90f00f4118568e6cf469bf1e9c72eec'])
SELECTORS=frozenset({174,175})
DEPENDENCIES={'work\\analysis\\lil_B186_source_v5132\\all12_clean_current_complete_context.json': 'e79fb365072773897ab80276d32d56be649e6572d8c39f581690e07143b9bc0b', 'work/analysis/lil_B186_dispatches_v5135/all12_source_current_dispatches_no_macros_and3_control_leaves.json': 'dcf4dc1c61eed0bf09b6360e5ce731880b92e2a1a2cb7c95897a6d0af3362a2c', 'work/analysis/lil_B186_voices_v5133/current207_catalog_eight_voices_and_two_source_selectors.json': 'a4c454b060737434516fbb4ee52a1377a44458042069c2fc4d1ea4d42b8797a0', 'work/analysis/lil_B186_branches_v5134/original_relative_skip_operand_proof.json': '41d060ab35da2fb47e7f60b067d0eeea770c3e589285b08a970eddc9d60af64a', 'work/analysis/lil_B186_entry_v5136/source_EV2_B186_action_dependency_and_native_getter_binding.json': 'b718e575bd62f82a862fda01d621f363274961d5713c7e832a468bbb8167dae3', 'work/analysis/lil_B186_controls_v5138/one_predicate_three_A000_C200_six_relative_sites_and_single_end.json': 'ab7c5a2724c193d02e42f3fe9e36fb89f73ed462461929d9d152ef61832c2995', 'work\\analysis\\lil_B186_terms_v5139b\\Owner_Cook_Alexandria_and_sweet_things_context_reconciliation.json': 'c9367c122e4c175624a264b9637f4773a569ed40b9bde11c0797ded448946a40', 'work/analysis/lil_B186_names_v5137/four_original_progressive_and_catalogue_name_consumers.json': '80ace2cd85e0679e3ef74504b1a619ed3624f5e4bda77fb6283dbaeb1f6a9239', 'work/analysis/lil_B186_predicate700_v5138/all8_original700_predicate_RNG_ownership_cases.json': 'fd7c4ea18122e9df4687b4f3c387e7f83573f180de82dbf9b321b8fce3d7320f'}
CONTROL='work/analysis/lil_B186_dispatches_v5135/all12_source_current_dispatches_no_macros_and3_control_leaves.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B186 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B186 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=24 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All12 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('The FE object must remain null-actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B186 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B186-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';11 original54020 speeches,clean Owner174/Cook175 roles,four read-only name consumers,voice0. All24 commands:raw700 predicate540,six relative operands,three alternative A000s560/572/584,C200644,end646 and2 trailing zeros. Current V5122 font/guards;fresh native approval required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B186-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310null actor then5473C object:tentative Sweets/Alexandria notice.228x48logical/228x64physical,conservative216px planning. Sweets is source sweet things,not a single commodity or all Treats. Earlier scene location/earned state not inferred;fresh native approval required.')
    raise ValueError('Unknown B186 consumer')
