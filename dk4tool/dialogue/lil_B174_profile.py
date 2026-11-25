"""Exact B174 source/current progressive consumer and four static actors."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['2cda89471cb7609824efb1b98e87b94bedfdc435bb0b1dfab60dfb196c5edf7c', '88eec719ab6bbe47ce604d5281e4059c3a37303dff8ce297a064cf7ddaeb36e0'])
SELECTORS=frozenset({2,14,26,201})
DEPENDENCIES={'work\\analysis\\lil_B174_source_v4453\\all33_clean_current_complete_context.json': 'be4eae1b2b137cd464fb53285beb8265611b52d08a04280a4e052c4227b4c8f0', 'work\\analysis\\lil_B174_dispatches_v4455\\all33_source_current_dispatches_no_macros_and8_control_leaves.json': '81ad094dd6886fae799fd0515fe3f3d240ddcf27280563ceb5d5cfcede73f1dd', 'work/analysis/lil_B174_voices_v4454/current4_static_names_voices_and207_catalog_rebind.json': '082a7a3a54e45415d9fe63414d5e2914f05e6ce8ff6942cbc80a7b9325871b87', 'work/analysis/lil_B174_branches_v4456/original_relative_skip_operand_proof.json': '1a9e21a03807435cdd6257bfe02b057ad8bcb1748818ed0bef2301158ffc565d', 'work/analysis/lil_B174_entry_v4457/source_EV2_B174_action_dependency_and_native_getter_binding.json': 'ba330a75ff226251a83d193018b03c1d17c493fc179ca78b3091607c20ce6fce', 'work/analysis/lil_B174_controls_v4459/one_resource_conditional_Emilio_four_spans_two_A000s_C200_and_single_end.json': '1a99053633cb2a489f6782ec260c0812bdfb89c0d032a4fd0a5e354c45f73df0', 'work\\analysis\\lil_B174_terms_v4460\\current_four_names_crown_tomb_Seoul_and_conditional_date_reconciliation.json': '4c20732fcfa4344b29940d09f8cce427ced86022cc153221332f30d7b4d3db1b', 'work/analysis/lil_B174_names_v4458/eight_original_name_consumers_and_owned_scratch_paths.json': '6589f50d3cc899d9f11d6fabf532e5ea007490eeda7e0a0a8b8ef5606f21eaa9'}

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B174 clean/current source and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    if consumer!='progressive':raise ValueError('B174 has no FE or typed/dynamic text consumer')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B174-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
        metrics_source=base.metrics_source+';33 original54020 speeches,Lil2/Emilio14/Julian26/Mihwa201,no FI/FA/FO,45 structural commands,eight nonrelative leaves,one resource,two presentations,two A000s,one predicate,four relative sites,C200 andsingle end. Emilio food aside remains conditional. Packed FE0E operand is not a system panel. Six owned scratch-name paths andtwo Mihwa readonly paths preserved. No natural event eligibility claim.')
