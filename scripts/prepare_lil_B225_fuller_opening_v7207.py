"""Retrospectively fill one source-bound opening without touching prose or global wrapping rules."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B225_fuller_opening_tools_v7207')
if __name__=='__main__':
    assert not ROOT.exists();a='scripts/plan_lil_B225_layout_v7191b.py';b='scripts/plan_lil_B225_layout_v7191c.py';assert not Path(b).exists()
    old="(36-length)**2*(2 if line==0 else 1)";new="(36-length)**2*((3 if row['id']=='DK4_MES_B225_R0016' else 2) if line==0 else 1)"
    row=derive(a,b,{'layout_v7191b':'layout_v7191c',old:new});ROOT.mkdir(parents=True);save(ROOT/'source_locked_one_record_fuller_opening.json',dict(tool=row,only_R16_first_row_raggedness_weight_changes_2_to3=True,all_prose_wording_source_controls_native_geometry_guards_andI_rules_unchanged=True,initial_actual_capture55_holds_preserved_not_revoked_as_rendering_failure=True,no_new_ROM_orcredit=True,full_goal_complete=False))
