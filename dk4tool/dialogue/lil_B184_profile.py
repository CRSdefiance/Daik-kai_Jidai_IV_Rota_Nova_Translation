"""Exact B184 source/current commands,two couple roles and progressive/FE consumers."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'
BLOCKS=frozenset(['8c4c043e1e864e98349a5614723e8caa2352c68fe3f3cf363ce51c28a24d3c35', 'a3a97b2bbffc55cfd815947f00d47f398c8b789852583558ba3f81c2956ac585'])
SELECTORS=frozenset({164,165})
DEPENDENCIES={'work\\analysis\\lil_B184_source_v5039\\all9_clean_current_complete_context.json': '791e55fad6920cddbe3deb7d24e415fad8d09287e94e71ab56432ed1abc5c8aa', 'work/analysis/lil_B184_dispatches_v5041/all9_source_current_dispatches_no_macros_and3_control_leaves.json': '38af78193a306938f43ee7cad784034a28382e682fd9035a454dbd9a840de7ca', 'work/analysis/lil_B184_voices_v5040/current207_catalog_eight_voices_and_two_source_selectors.json': 'a3c7fd8b98b266e30b578e7a9a248971b76a4865184496b19505afeebce2d12e', 'work/analysis/lil_B184_controls_v5043/A000_C200_single_end_and_no_relative_or_predicate_contract.json': '26fa43097cee312092ec041998594762396ba9f8ddbd773f5729337d3601b756', 'work/analysis/lil_B184_entry_v5042/source_EV2_B184_action_dependency_and_native_getter_binding.json': 'a06d8bec496694ed6233ae494390699e6ce61a219e6b071afcd2ff0f0c8d9a79', 'work\\analysis\\lil_B184_terms_v5045\\two_couple_roles_Sofala_Tea_and_household_request_reconciliation.json': 'f6a889d3ee2439985179d32d8b27f48da13892b656582460d9247337426e8a15', 'work/analysis/lil_B184_names_v5044/four_original_progressive_and_catalogue_name_consumers.json': 'ce35d2800d729fea2bf49aaac0daee5aa5be9c81aba593e3a1420b0a28ee72b4'}
CONTROL='work/analysis/lil_B184_dispatches_v5041/all9_source_current_dispatches_no_macros_and3_control_leaves.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B184 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B184 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=18 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All9 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('The FE object must remain null-actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B184 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B184-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';8 original54020 speeches,two static couple roles164/165,four read-only name consumers and source voice0.12 linear commands,A0008 raw00a0ffff011f22a1,C200426,end428. No inferred marriage,age or kinship. Current V5030 font/guards;native planes need fresh approval.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B184-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310null actor then5473C object:prospective Tea/Sofala notice.228x48logical/228x64physical,conservative216px planning. No earlier scene location or earned boom inference. Current native planes need fresh approval.')
    raise ValueError('Unknown B184 consumer')
