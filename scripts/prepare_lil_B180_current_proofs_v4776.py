"""Prepare current-input successors without changing prior source proofs."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B180_current_tools_v4776')
if __name__=='__main__':
    assert not ROOT.exists()
    common={'lil_B180_source_v4758/all11_clean_current_complete_context':'lil_B180_source_v4773/all11_clean_current_complete_context',
            'from scripts.current_common_native_context_v2677 import CurrentContext':'from scripts.current_build_native_context_v4774 import CurrentContext'}
    tools=[]
    tools.append(derive('scripts/prove_lil_B180_dispatches_v4760b.py','scripts/prove_lil_B180_dispatches_v4776.py',{
        **common,'lil_B180_dispatches_v4760b':'lil_B180_dispatches_v4776','lil_B180_voices_v4759/current_native_input':'lil_B180_voices_v4775/current_native_input'}))
    tools.append(derive('scripts/prove_lil_B180_branches_v4761.py','scripts/prove_lil_B180_branches_v4777.py',{
        'lil_B180_source_v4758/all11_clean_current_complete_context':'lil_B180_source_v4773/all11_clean_current_complete_context',
        'lil_B180_branches_v4761':'lil_B180_branches_v4777'}))
    tools.append(derive('scripts/prove_lil_B180_entry_v4762b.py','scripts/prove_lil_B180_entry_v4778.py',{
        **common,'lil_B180_entry_v4762b':'lil_B180_entry_v4778','lil_B180_voices_v4759/current_native_input':'lil_B180_voices_v4775/current_native_input',
        'original_completion_flag_in_historical_opening':'original_completion_flag_in_current_opening',
        'historical_snapshot_is_Lil_London_not_current_B180_eligibility':'current_opening_snapshot_is_not_B180_eligibility'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_current_proofs.json',dict(tools=tools,
        context='Fresh V4766 opening snapshot,not B180 activation;zero historical initialized-RAM overlays',
        zero_new_reviews_or_ROM_changes=True,full_goal_complete=False))
    print('Prepared current-input dispatch/relative-branch/event-entry successors;all prior proofs preserved.')
