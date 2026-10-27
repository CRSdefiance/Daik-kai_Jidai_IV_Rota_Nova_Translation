"""Prepare B172 whole-source binding and fresh three-actor native contracts."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B172_source_tools_v4364')
if __name__=='__main__':
    assert not ROOT.exists()
    old='lil_B171_source_v4311/all37_clean_current_complete_context'
    new='lil_B172_source_v4364/all27_clean_current_complete_context'
    tools=[derive('scripts/map_lil_B171_source_v4311.py','scripts/map_lil_B172_source_v4364.py',{
        'Bind37 clean/current complete preambles and45 commands':'Bind27 clean/current complete preambles and38 commands',
        'lil_B171_source_v4311':'lil_B172_source_v4364',
        'editorial_handoff_verification_v4308b':'editorial_handoff_verification_v4363',
        'lil_B170_source_v4260/all33_clean_current_complete_context':'lil_B171_source_v4311/all37_clean_current_complete_context',
        'lil_B171_clean_context_v4309/all37_complete_B171_exchange':'lil_B172_clean_context_v4361/all27_complete_B172_exchange',
        'len(known) == 5725':'len(known) == 5762','blocks[171]':'blocks[172]',
        'len(old) == 45 and len(spoken) == 37':'len(old) == 38 and len(spoken) == 27',
        'selectors = [], [2,25,81]':'selectors = [], [2,26,201]',
        'DK4_MES_B171_R':'DK4_MES_B172_R',"{'FI':1,'FA':0,'FO':0}":"{'FI':0,'FA':0,'FO':0}",
        'block=171':'block=172','physical_speeches=37':'physical_speeches=27',
        'all37_clean_current_complete_context':'all27_clean_current_complete_context',
        'historical_snapshot_is_Lil_London_not_selected_B171':'historical_snapshot_is_Lil_London_not_selected_B172',
        'total_editorial_objects=37, speech_objects=37, ordinary_source_speeches=37':'total_editorial_objects=27, speech_objects=27, ordinary_source_speeches=27',
        'all37_clean_first_glosses':'all27_clean_first_glosses','source_native_commands=45':'source_native_commands=38',
        'B171 mapped:37 complete preambles/45 commands/no relative sites,FI1/FO0':'B172 mapped:27 complete preambles/38 commands/no relative sites,no macros',
        "        assert row['source_hex'] == raw.hex()":"        assert row['source_hex'] == raw.hex()\n        if index == 11:\n            row['historical_clean_first_gloss'] = row['fresh_source_gloss']\n            row['fresh_source_gloss'] = '美華 responds to ユリアン with familiar, gently chiding or fond address and a trailing pause. Preserve that tone without adding a literal again, a new arrival, a laugh, a blush or an established romantic relationship.'\n            row['clean_gloss_precision_note'] = 'Clarify the original you-again-style tonal shorthand before predecessor English comparison:ったら supplies familiar affect, not a literal repeated-arrival fact. Original clean gloss and source bytes remain preserved.'",
    })]
    tools.append(derive('scripts/reconcile_lil_B171_voices_v4312.py','scripts/reconcile_lil_B172_voices_v4365.py',{
        'lil_B171_voices_v4312':'lil_B172_voices_v4365',old:new,
        'all37_dispatches_still_require_separate_proof':'all27_dispatches_still_require_separate_proof',
    }))
    tools.append(derive('scripts/prove_lil_B171_dispatches_v4313.py','scripts/prove_lil_B172_dispatches_v4366.py',{
        'Bind74 source/current speech calls and8 exact non-relative control leaves.':'Bind54 source/current speech calls and11 exact non-relative control leaves.',
        'lil_B171_dispatches_v4313':'lil_B172_dispatches_v4366',old:new,
        'lil_B171_voices_v4312':'lil_B172_voices_v4365',
        'len(cases)==74 and len(leaves)==8':'len(cases)==54 and len(leaves)==11',
        'all37_source_current_dispatches_FI1_FO0_and8_control_leaves':'all27_source_current_dispatches_no_macros_and11_control_leaves',
        'all8_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact':'all11_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact',
        'actual_selected_B171_IDs':'actual_selected_B172_IDs',
        '74 source/current dispatches pass:three static actors,FI1/FO0,noFE. All8 nonrelative nontext leaves exact.':'54 source/current dispatches pass:three static actors,no macros/noFE. All11 nonrelative nontext leaves exact.',
    }))
    tools.append(derive('scripts/prove_lil_B171_branches_v4314.py','scripts/prove_lil_B172_branches_v4367.py',{
        'lil_B171_branches_v4314':'lil_B172_branches_v4367',old:new,
    }))
    tools.append(derive('scripts/prove_lil_B171_entry_v4315.py','scripts/prove_lil_B172_entry_v4368.py',{
        'lil_B171_entry_v4315':'lil_B172_entry_v4368',old:new,
        'lil_B171_voices_v4312':'lil_B172_voices_v4365','B171':'B172','in [171]':'in [172]',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,source_scope=dict(block=172,speeches=27,commands=38,
        selectors=[2,26,201],FI=0,FA=0,FO=0,relative_sites=0,predicates=0,nonrelative_leaves=11,
        C200_offset=1868,A000_offset=1870,A000_hex='00a0ffff010cc960',last6240_offset=1878,end_offsets=[1880],pause=0),
        clean_gloss11_tonal_shorthand_clarified_before_English_comparison=True,
        no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
    print('Prepared B172 source/current,three voices,54 dispatches,zero-relative and entry producers;27 clean glosses precede English.')
