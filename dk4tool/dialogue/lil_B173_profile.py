"""Exact B173 source/current progressive consumer and two static actors."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['87d542a15ca09af2e1c40c8bfc950020ed1f194be90aabb9fdcc64ef62e88ecb', 'b23e68a97a4111e0f579fdde85f58164818a342a3ae972c8c1b74631710291f4'])
SELECTORS=frozenset({2,202})
DEPENDENCIES={'work\\analysis\\lil_B173_source_v4411\\all11_clean_current_complete_context.json': 'c014a1c60aa103865c2ba1d7c1cd5fd7ba78d215e4582374fb637feb008b7878', 'work\\analysis\\lil_B173_dispatches_v4413\\all11_source_current_dispatches_no_macros_and8_control_leaves.json': 'b9107c4114c335a13414e8d456529ab8068f1187e3fc64d89c41059295ab8fda', 'work/analysis/lil_B173_voices_v4412/current2_static_names_voices_and207_catalog_rebind.json': 'ffea2fd1c1f2e8fece01be62aeed6235fe40b667af8dd71a98cddec1f91154b7', 'work/analysis/lil_B173_branches_v4414/original_relative_skip_operand_proof.json': '8d1ac3b9a468f669c286bb092b75dc3039618e345712aa9893c1397443a89001', 'work/analysis/lil_B173_entry_v4415/source_EV2_B173_action_dependency_and_native_getter_binding.json': '31ab0d5d402490a67af0bf9e29df220de0d866d340a8705ee9f4adc39e1ce1df', 'work/analysis/lil_B173_controls_v4417/two_resources_one_predicate_four_spans_two_A000s_and_single_end.json': 'b3ccc0297c80351b14b64ccf7c016250e721ff27a5e214d4f0fefd2a23813705', 'work\\analysis\\lil_B173_terms_v4418\\current_crown_tomb_Reika_and_uncertain_Julian_lead_reconciliation.json': '08c66169a0c263064580b1042b20532fe0217bb25c60437a9885f6aad00f74cc', 'work/analysis/lil_B173_names_v4416/four_original_name_consumers_and_owned_scratch_paths.json': 'f19ef1c9a985ee8c67ee26be68ab77cc624df3633d36a3d82d9e90b4fb277494'}

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B173 clean/current source and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    if consumer!='progressive':raise ValueError('B173 has no FE or typed/dynamic text consumer')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B173-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
        metrics_source=base.metrics_source+';11 original54020 speeches,Lil2/Reika202,no FI/FA/FO,23 structural commands,eight nonrelative leaves,two resources,two presentations,two A000s,one predicate,four relative sites andsingle tail end. All speech precedes the conditional suffix. CA is actor202,not literal prose. Reika original name pointer is readonly;Lil owned scratch paths remain intact. No natural event eligibility claim.')
