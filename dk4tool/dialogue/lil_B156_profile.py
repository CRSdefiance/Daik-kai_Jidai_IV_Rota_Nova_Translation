"""Exact B156 original progressive consumers and ten static actors."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['5e498e608c437ccf994ed788d70ca5667fd22000915cb12dfc5ae89b15b2adeb', '756ef617ab1545b6c2093569d16e78bdb31d9ef1ad19a19f2f9065a989a81728'])
SELECTORS=frozenset({2,9,14,20,21,92,96,152,164,165})
DEPENDENCIES={'work\\analysis\\lil_B156_source_v3700\\all76_clean_current_complete_context.json': '3285169adda5867ad955408a2a6f9fde27e6fff14008a3784717840a37ac0c8d', 'work\\analysis\\lil_B156_source_v3700\\subset152_dispatches_and43_source_exact_control_leaves.json': '562bf80ad993710f1707ec24571cc417258d103355e1edab7e50f6883e62442a', 'work\\analysis\\lil_B156_B160_source_v3698\\voices_and_entry_evidence_rebind.json': '6599e82b2f788e2b08f1b99224e7667a5573d7a1536191893ed3298c4d2dace9', 'work\\analysis\\lil_B156_branches_v3701\\original_relative_skip_operand_proof.json': '2f1fb6a598d94730e929a599614a1eb40e2a0f00b14e19614a0ac1e48fb1e474', 'work\\analysis\\lil_B156_source_v3700\\ten_names_and_original_entry_binding.json': '6636a1e260be1d6ebd35cc97ee7a452d6f6599f5c96cd6726eccd05456d68275', 'work\\analysis\\lil_B156_controls_v3702\\three_predicates_C200_fourteen_resource_sites_and43_source_leaves.json': '19009d2fef461c2c8c4629185e98b7ee6182b8a001f232c98e35e4b5eeb7d987'}
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B156 clean/current source and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    if consumer!='progressive':raise ValueError('B156 has no FE or dynamic text consumer')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B156-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';76 original54020 speeches/ten static actors including Ian15 and Retainer98;sourceFI2,three predicates,12 relative sites,14resource sites andtwo endwords bound. No natural event eligibility claim.')
