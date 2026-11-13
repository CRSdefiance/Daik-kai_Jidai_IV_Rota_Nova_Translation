"""Exact B160 source binding:22 progressive speeches/six original static actors."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['09bb5e5667f22a3b61b069d158df99697188219581d0afdbab74aec0d1d4feeb', '8015b550753dccdf3c2f3bb63a7c0ffb5f8ea4469018e8eef57b4a9c1cc9e488'])
SELECTORS=frozenset({2,9,14,15,116,151})
DEPENDENCIES={'work\\analysis\\lil_B160_source_v3870\\all22_clean_current_complete_context.json': '947a3731162dee21ae0bc9f746e36e70b0d7ce0022ad5ff4875efde09f27122e', 'work\\analysis\\lil_B160_source_v3870\\subset44_dispatches_and12_source_exact_control_leaves.json': '3a8f805d14daf0df9e3b93737bf9426df19354eb2ce08dd616e92d2a6199ea27', 'work\\analysis\\lil_B160_source_v3868\\voices_and_entry_evidence_rebind.json': '8a917f54af8d3771b72a7d4f30d731fe6251e8111aa82082fef7ac22c5930d95', 'work\\analysis\\lil_B160_branches_v3871\\original_relative_skip_operand_proof.json': '6949812497373009aeb85bfa46b30dca8cb959bfcce5e89ce8968a6f1695760a', 'work\\analysis\\lil_B160_source_v3870\\six_names_original_Sailor151_alias_and_entry_binding.json': 'd37da5c6a3e3adf0b68d914f90bf2c908ebfe1768677f612556468ca6196db2a', 'work\\analysis\\lil_B160_controls_v3872\\five_predicates_C283_C200_three_resource_sites_and12_source_leaves.json': '92714d6b27195501c4326e0be9a90077865afbeb235058fb06d6480de7efe133', 'work\\analysis\\lil_B156_nameplate_v3737a\\source_native_catalogue_vs_progressive_Sailor_alias.json': '8481599e2fef9aeae52f8f2c3cb6f92d829ab6dc6a1a013d5b91efbb31aa2a9c'}
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B160 clean/current source and runtime required')
    if consumer!='progressive':raise ValueError('Only original B160 progressive consumer is source-bound')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B160-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';22 original54020 speeches/six static actors, FI1,20 spans,12 leaves,C283,C200 andtwo ends;Sailor151 original progressive alias separately bound. No natural eligibility claim.')
