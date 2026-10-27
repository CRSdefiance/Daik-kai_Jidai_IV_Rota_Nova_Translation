"""Prepare B177 source/current binding and distinct voice,dispatch,entry/name/control checks."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B177_source_tools_v4602')
OLD='lil_B176_source_v4548/all10_clean_current_complete_context'
NEW='lil_B177_source_v4602/all10_clean_current_complete_context'
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/map_lil_B176_source_v4548.py','scripts/map_lil_B177_source_v4602.py',{
        'lil_B176_source_v4548':'lil_B177_source_v4602',
        'editorial_handoff_verification_v4546':'editorial_handoff_verification_v4600',
        'lil_B175_source_v4503/all32_clean_current_complete_context':'lil_B176_source_v4548/all10_clean_current_complete_context',
        'lil_B176_clean_context_v4547/all10_complete_B176_exchange':'lil_B177_clean_context_v4601/all10_complete_B177_exchange',
        'len(known)==5865':'len(known)==5875','blocks[176]':'blocks[177]',
        'DK4_MES_B176_R':'DK4_MES_B177_R','block=176':'block=177',
        'not_selected_B176':'not_selected_B177','B176 mapped':'B177 mapped',
    })]
    tools.append(derive('scripts/reconcile_lil_B176_voices_v4549.py','scripts/reconcile_lil_B177_voices_v4603.py',{
        OLD:NEW,'lil_B176_voices_v4549':'lil_B177_voices_v4603',
    }))
    tools.append(derive('scripts/prove_lil_B176_dispatches_v4550.py','scripts/prove_lil_B177_dispatches_v4604.py',{
        OLD:NEW,'lil_B176_dispatches_v4550':'lil_B177_dispatches_v4604',
        'lil_B176_voices_v4549':'lil_B177_voices_v4603','actual_selected_B176_IDs':'actual_selected_B177_IDs',
    }))
    tools.append(derive('scripts/prove_lil_B176_branches_v4551.py','scripts/prove_lil_B177_branches_v4605.py',{
        OLD:NEW,'lil_B176_branches_v4551':'lil_B177_branches_v4605',
    }))
    tools.append(derive('scripts/prove_lil_B176_entry_v4552.py','scripts/prove_lil_B177_entry_v4606.py',{
        OLD:NEW,'lil_B176_entry_v4552':'lil_B177_entry_v4606','lil_B176_voices_v4549':'lil_B177_voices_v4603',
        'B176':'B177','in [176]':'in [177]',
    }))
    tools.append(derive('scripts/prove_lil_B176_names_v4553.py','scripts/prove_lil_B177_names_v4607.py',{
        OLD:NEW,'lil_B176_names_v4553':'lil_B177_names_v4607','lil_B176_voices_v4549':'lil_B177_voices_v4603',
        'not_actual_B176_nameplate_observation':'not_actual_B177_nameplate_observation',
    }))
    tools.append(derive('scripts/prove_lil_B176_controls_v4554.py','scripts/prove_lil_B177_controls_v4608.py',{
        OLD:NEW,'lil_B176_controls_v4554':'lil_B177_controls_v4608',
        'lil_B176_branches_v4551':'lil_B177_branches_v4605','lil_B176_voices_v4549':'lil_B177_voices_v4603',
        'B176':'B177','blocks[176]':'blocks[177]','block=176':'block=177',
        '00a0ffff010a0da1':'00a0ffff01090fa1',
        "(384,'00c2'),(386,'00000000')":"(480,'00c2'),(482,'00000000')",
        'source_offset=384':'source_offset=480','source_declared_end_offsets=[386]':'source_declared_end_offsets=[482]',
        'end=386':'end=482',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,source_block=177,physical_speeches=10,
        progressive=9,FE=1,source_static_actors=[174,175],source_macros=0,commands=13,
        nonrelative_leaves=3,A000=1,C200=1,end_offsets=[482],
        no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
