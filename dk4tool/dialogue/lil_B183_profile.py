"""Exact B183 source/current commands,five roles and progressive/FE consumers."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'
BLOCKS=frozenset(['031bdd0db6ebd3234322c1b91ab5940749e754046202d2433cf12a09779125f4', '1a5520c1987dec6eb27d8172ad93c84475a29ecd8fdd474411f79bebc01f3eba'])
SELECTORS=frozenset({85,110,132,148,153})
DEPENDENCIES={'work\\analysis\\lil_B183_source_v4925\\all25_clean_current_complete_context.json': '4e9a8e3a643a30470d90fc64b719a9c9c6f11c58f33efbcd9279a498e0343ae8', 'work/analysis/lil_B183_dispatches_v4927/all25_source_current_dispatches_no_macros_and3_control_leaves.json': '3e5e32cd42c47a10ceefdff156a8f9335ffa5bd760b373fb0a633c8a36206247', 'work/analysis/lil_B183_voices_v4926/current207_catalog_eight_voices_and_five_source_selectors.json': 'eaf9e2733667ce86d5873d5743b701ec9021c086a6b229dabeaab79a0d3bd328', 'work/analysis/lil_B183_controls_v4929/A000_C200_single_end_and_no_relative_or_predicate_contract.json': '46c6a2d444ccbc7524afde8be3eca2479300ad3d7007c4cd363a8d441d41198c', 'work/analysis/lil_B183_entry_v4928/source_EV2_B183_action_dependency_and_native_getter_binding.json': '5aad15d1b9465d5a09e47fb619ff19e23bf8d0405b95f3108e5bfbc39da34c52', 'work\\analysis\\lil_B183_terms_v4931\\five_roles_Basra_Artwork_and_complete_shop_exchange_reconciliation.json': '9d74bfbe36d41eb1393dbdcb8845d217cdd8b8286242aebf852e17ac8c8e11ae', 'work/analysis/lil_B183_names_v4930/ten_original_progressive_and_catalogue_name_consumers.json': 'ebf8cd6f20d40d63c5f70611cdcdc8399d5bf7f716feb2e2418b5e787288748d'}
CONTROL='work/analysis/lil_B183_dispatches_v4927/all25_source_current_dispatches_no_macros_and3_control_leaves.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B183 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B183 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=50 or sum(r['source_selector']==254 for r in cases)!=4:raise ValueError('All25 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('Both FE objects must remain null-actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B183 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B183-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';23 original54020 speeches,five static actors and ten read-only names.153 is progressive Sailor,separate catalogue Retainer,voice4;other four source voices0.28 linear commands,A0008 raw00a0ffff013926a1,C200950,end952. No inferred player identity or relationship. Current V4914 font/guards;native planes need fresh approval.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B183-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';two original24310null actor then5473C objects:closing impact sound and prospective Artwork/Basra notice.228x48logical/228x64physical,conservative216px planning. No earlier scene location or earned boom inference. Current native planes need fresh approval.')
    raise ValueError('Unknown B183 consumer')
