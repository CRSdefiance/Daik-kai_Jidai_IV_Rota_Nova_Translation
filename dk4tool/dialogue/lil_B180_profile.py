"""B180 ten progressive speeches,one impersonal FE and conditional native controls."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'
BLOCKS=frozenset(['646ed89f19871fc3476128aa8a3e75e094ab7f55394d825cc9c3c6af70a6ef75', 'b3fed143e22eb0a7378a64d45cf59f76d749e91ddd11bb18c6589e5d6ed8cf35'])
SELECTORS=frozenset({166,167})
DEPENDENCIES={'work\\analysis\\lil_B180_source_v4773\\all11_clean_current_complete_context.json': '438ae464f053dbdbc5e7698e425d74895c08a761d0f949bcabdb8742e1dea6c6', 'work/analysis/lil_B180_dispatches_v4776/all11_source_current_dispatches_no_macros_and7_control_leaves.json': '88622bbd84681b3cad25c7838059ab213fd64d432b8a7dee8149e6db14696755', 'work/analysis/lil_B180_voices_v4775/current207_catalog_eight_voices_and_two_source_selectors.json': 'b6b44f89c131f06783441feec17a9d56377612cbb523e79a03ab740434516315', 'work/analysis/lil_B180_branches_v4777/original_relative_skip_operand_proof.json': '57fbf4a847ba3f6a5b0943d7445fd6afd187eb98c7e095fea6dea0e24f2d280c', 'work/analysis/lil_B180_entry_v4778/source_EV2_B180_action_dependency_and_native_getter_binding.json': '39a0836c565849632b012c510c8f8314da03092ea442731254d4d31315930e20', 'work/analysis/lil_B180_controls_v4780c/two_predicates_three_A000_C200_ten_relative_sites_and_single_end.json': 'dc756d99caa263c4f2c48002f6e7ffe92cbe3d635e09537093e19e83f3c4fff3', 'work\\analysis\\lil_B180_terms_v4785c\\Lady_Lisbon_Scents_and_prospective_fashion_reconciliation.json': '090a6a1eee86837e305078e768305438a9c299d93537cbf7b4b0b186367e2e11', 'work/analysis/lil_B180_names_v4779/four_original_Lady_name_consumers.json': '0417641dc6b520d1fb2c38d9b1c410df4621b06cae2d0d50796bed8323aa672b', 'work/analysis/lil_B180_predicate500_v4782/all16_original500_predicate_RNG_ownership_cases.json': '9b9270bbca5f646bab3dfdac02e0821ed90ef1eacac465b82bf3a32d2a32932d', 'work/analysis/lil_B180_C200_v4784/source_fleet_descriptor_two_C200_contracts.json': 'dc8f8c3e9d7c8ac6cea538005209eae75d01ebab294c3aac7d4b00ebbc6164dc'}
CONTROL='work/analysis/lil_B180_dispatches_v4776/all11_source_current_dispatches_no_macros_and7_control_leaves.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B180 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B180 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=22 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All eleven source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE notice must remain null-actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B180 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B180-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';ten original54020 speeches,Lady166/Lady167,four read-only name paths. No inferred noble rank,marriage or third-person gender.28 commands,ten relative sites,two original500 threshold/RNG predicates,three alternative opaque effects,C200570,end572. Current V4766 font and guards;native planes still need fresh approval.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B180-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one prospective Lisbon Scents-category notice,original24310null actor then5473C.228x48logical/228x64physical,conservative216px planning. No earlier location,earned boom or demand/price inference. Current font native plane still needs fresh approval.')
    raise ValueError('Unknown B180 consumer')
