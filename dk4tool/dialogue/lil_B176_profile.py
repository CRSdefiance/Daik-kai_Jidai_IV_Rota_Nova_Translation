"""B176 exact source/current controls:nine progressive and one impersonal null-actor FE notice."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['04a6366f1e88a5d33d02031bbce7a7952ae789f47280f58fa9b53048d817dfe5', 'd63bb4676da7a28dd85c068f34d38b2f9ba85729141b800335e1ce6c0edb28f1'])
SELECTORS=frozenset({174,175})
DEPENDENCIES={'work\\analysis\\lil_B176_source_v4548\\all10_clean_current_complete_context.json': '14eb800776d1b2edf29647361d3aef980be9d3e476af3a479fdc693aa38a5ddc', 'work\\analysis\\lil_B176_dispatches_v4550\\all10_source_current_dispatches_no_macros_and3_control_leaves.json': '5f2c60ca35326dafc3ecdc640c7f0d399d4099244d9dd8cbdc40b4ef2165f2b4', 'work/analysis/lil_B176_voices_v4549/current2_static_names_voices_and207_catalog_rebind.json': '0fe6fb44a7db8d32a02a0c57025a954fe29ee9b8e4f2c04c407a37b97006b00d', 'work/analysis/lil_B176_branches_v4551/original_relative_skip_operand_proof.json': 'c2eca4ad46219b7eb5b4d87dca796cd6c9446c6f2745f0123537d7aeb155d451', 'work/analysis/lil_B176_entry_v4552/source_EV2_B176_action_dependency_and_native_getter_binding.json': '4d0e8ad574bc64af050cfa52b9472d46c02aa71f88379a98f19b4eb1b2b4c74c', 'work/analysis/lil_B176_controls_v4554/one_A000_C200_single_end_and3_source_leaves.json': '9528338ae035f045cbecbaf5cddd1176400317c43cc66cc52339fe80c7247fa5', 'work\\analysis\\lil_B176_terms_v4555\\Owner_Cook_Seville_and_prospective_banana_fashion_reconciliation.json': '10f06ffa3e41303b4ffe0a77e41e2058aa2e95323b99f8faf2a8265528af832a', 'work/analysis/lil_B176_names_v4553/four_original_Owner_Cook_name_consumers_readonly_paths.json': '7db8d282425b18c7666ed7034a7bbccc60eaa36ea717c1dc0547101c582be69a'}
CONTROL='work\\analysis\\lil_B176_dispatches_v4550\\all10_source_current_dispatches_no_macros_and3_control_leaves.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B176 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B176 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=20 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All ten source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE notice must remain null-actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B176 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B176-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';nine original54020 speeches,Owner174/Cook175,no source FI/FA/FO. Exact13 commands,opaque leading A0008,C200384,end386. Four read-only name paths;no resource,presentation,predicate,relative or typed objects. No natural eligibility or earned fashion-state claim.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B176-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one impersonal prospective Seville banana-fashion notice,original24310null actor then5473C before fallback.228x48logical/228x64physical paper;conservative216px planning. No invented speaker or name label;native complete-page approval remains separate.')
    raise ValueError('Unknown B176 consumer')
