"""Prepare clean/current B171 binding and fresh three-actor native contracts."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B171_source_tools_v4311')

if __name__ == '__main__':
    assert not ROOT.exists()
    old = 'lil_B170_source_v4260/all33_clean_current_complete_context'
    new = 'lil_B171_source_v4311/all37_clean_current_complete_context'
    tools = [derive('scripts/map_lil_B170_source_v4260.py', 'scripts/map_lil_B171_source_v4311.py', {
        'Bind33 clean/current complete preambles': 'Bind37 clean/current complete preambles',
        'lil_B170_source_v4260': 'lil_B171_source_v4311',
        'editorial_handoff_verification_v4259': 'editorial_handoff_verification_v4308b',
        'lil_B169_source_v4211/all36_clean_current_complete_context': 'lil_B170_source_v4260/all33_clean_current_complete_context',
        'lil_B170_clean_context_v4257/all33_complete_B170_exchange': 'lil_B171_clean_context_v4309/all37_complete_B171_exchange',
        'len(known) == 5692': 'len(known) == 5725', 'blocks[170]': 'blocks[171]',
        'len(old) == 45 and len(spoken) == 33': 'len(old) == 45 and len(spoken) == 37',
        'selectors = [], [2,25]': 'selectors = [], [2,25,81]',
        'DK4_MES_B170_R': 'DK4_MES_B171_R',
        "{'FI':1,'FA':0,'FO':1}": "{'FI':1,'FA':0,'FO':0}",
        'block=170': 'block=171', 'physical_speeches=33': 'physical_speeches=37',
        'all33_clean_current_complete_context': 'all37_clean_current_complete_context',
        'historical_snapshot_is_Lil_London_not_selected_B170': 'historical_snapshot_is_Lil_London_not_selected_B171',
        'total_editorial_objects=33, speech_objects=33, ordinary_source_speeches=33': 'total_editorial_objects=37, speech_objects=37, ordinary_source_speeches=37',
        'all33_clean_first_glosses': 'all37_clean_first_glosses',
        'B170 mapped:33 complete preambles/45 commands/no relative sites,FI1/FO1': 'B171 mapped:37 complete preambles/45 commands/no relative sites,FI1/FO0',
    })]
    tools.append(derive('scripts/reconcile_lil_B170_voices_v4262.py', 'scripts/reconcile_lil_B171_voices_v4312.py', {
        'two source-owned static names/voices': 'three source-owned static names/voices',
        'lil_B170_voices_v4262': 'lil_B171_voices_v4312', old: new,
        'len(chosen)==2': 'len(chosen)==3', '::2_source_names': '::3_source_names',
        'current2_static_names_voices': 'current3_static_names_voices', 'fresh2_actor_names': 'fresh3_actor_names',
        'all33_dispatches_still_require_separate_proof': 'all37_dispatches_still_require_separate_proof',
        '2 static names/voices pass': '3 static names/voices pass',
    }))
    tools.append(derive('scripts/prove_lil_B170_dispatches_v4263.py', 'scripts/prove_lil_B171_dispatches_v4313.py', {
        'Bind66 source/current speech calls and12 exact non-relative control leaves.': 'Bind74 source/current speech calls and8 exact non-relative control leaves.',
        'lil_B170_dispatches_v4263': 'lil_B171_dispatches_v4313', old: new,
        'lil_B170_voices_v4262': 'lil_B171_voices_v4312',
        'len(cases)==66 and len(leaves)==12': 'len(cases)==74 and len(leaves)==8',
        'all33_source_current_dispatches_FI1_FO1_and12_control_leaves': 'all37_source_current_dispatches_FI1_FO0_and8_control_leaves',
        'all12_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact': 'all8_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact',
        'all2_static_actors_without_role_or_roster_fixture': 'all3_static_actors_without_role_or_roster_fixture',
        'actual_selected_B170_IDs': 'actual_selected_B171_IDs',
        '66 source/current dispatches pass:two static actors,FI1/FO1,noFE. All12 nonrelative nontext leaves exact.': '74 source/current dispatches pass:three static actors,FI1/FO0,noFE. All8 nonrelative nontext leaves exact.',
    }))
    tools.append(derive('scripts/prove_lil_B170_branches_v4264.py', 'scripts/prove_lil_B171_branches_v4314.py', {
        'lil_B170_branches_v4264': 'lil_B171_branches_v4314', old: new,
    }))
    tools.append(derive('scripts/prove_lil_B170_entry_v4265.py', 'scripts/prove_lil_B171_entry_v4315.py', {
        'lil_B170_entry_v4265': 'lil_B171_entry_v4315', old: new,
        'lil_B170_voices_v4262': 'lil_B171_voices_v4312', 'B170': 'B171', 'in [170]': 'in [171]',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(tools=tools, source_scope=dict(block=171, speeches=37, commands=45,
        selectors=[2,25,81], FI=1, FA=0, FO=0, relative_sites=0, predicates=0, nonrelative_leaves=8,
        source_4500_offset=10, source_4621_offset=1252, source_61FF_offset=1256, source_6325_offset=1306,
        C200_offset=2110, end_offsets=[2112,2116], no2000_pause_or_A000=True),
        no_ROM_registry_ledger_orcredit_change=True, full_goal_complete=False))
    print('B171 source/current,three voices,74dispatches,zero-relative and entry producers prepared;no credit.')
