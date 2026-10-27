"""Prepare six exact native Lady name consumers and complete B178 opaque controls."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B178_names_controls_tools_v4667')
assert not ROOT.exists()
OLD='lil_B177_source_v4602/all10_clean_current_complete_context'
NEW='lil_B178_source_v4662/all13_clean_current_complete_context'
tools=[derive('scripts/prove_lil_B177_names_v4607.py','scripts/prove_lil_B178_names_v4667.py',{
    OLD:NEW,'lil_B177_names_v4607':'lil_B178_names_v4667','lil_B177_voices_v4603':'lil_B178_voices_v4663',
    'current2_static_names':'current3_static_names','fresh2_actor_names':'fresh3_actor_names',
    'for ident in [174,175]:':'for ident in [166,167,168]:','::AE-AF-native-names':'::A6-A7-A8-native-names',
    'len(values)==4':'len(values)==6',"{174:'Owner',175:'Cook'}":"{166:'Lady',167:'Lady',168:'Lady'}",
    "{'174':'Owner','175':'Cook'}":"{'166':'Lady','167':'Lady','168':'Lady'}",
    'four_original_Owner_Cook_name_consumers_readonly_paths':'six_original_Lady166_167_168_name_consumers_readonly_paths',
    'native_four_consumer_cases':'native_six_consumer_cases',
    'source_AE_AF_are_static_Owner174_Cook175_not_literal_halfwidth_prose':'source_A6_A7_A8_are_static_Lady166_167_168_not_literal_halfwidth_prose',
    'not_actual_B177_nameplate_observation':'not_actual_B178_nameplate_observation',
})]
tools.append(derive('scripts/prove_lil_B177_controls_v4608.py','scripts/prove_lil_B178_controls_v4668.py',{
    OLD:NEW,'lil_B177_controls_v4608':'lil_B178_controls_v4668',
    'lil_B177_branches_v4605':'lil_B178_branches_v4665','lil_B177_voices_v4603':'lil_B178_voices_v4663',
    'B177':'B178','blocks[177]':'blocks[178]','block=177':'block=178',
    'len(commands)==13':'len(commands)==16',"for c in commands)==10":"for c in commands)==13",
    '00a0ffff01090fa1':'00a0ffff010002a1',
    "(480,'00c2'),(482,'00000000')":"(488,'00c2'),(490,'00000000')",
    'source_offset=480':'source_offset=488','source_declared_end_offsets=[482]':'source_declared_end_offsets=[490]',
    'all10_speeches':'all13_speeches','FE1_impersonal_notice_and_progressive9':'FE1_impersonal_notice_and_progressive12',
    'progressive=9':'progressive=12','end=482':'end=490',
}))
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tools=tools,three_static_Lady_labels_no_noble_rank_inferred=True,
    source_husband_reference_for167_only=True,all16_commands_and3_leaves_preserved=True,
    no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
print('Prepared six Lady-name consumers and B178 A000/C200/single-end proofs;no credit.')
