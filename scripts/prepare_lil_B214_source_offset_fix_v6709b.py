"""Keep both coordinate systems explicit; preserve the first source-audit producer and proof."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B214_source_offset_fix_v6709b')
if __name__=='__main__':
    assert not ROOT.exists()
    proof=derive('scripts/audit_lil_B214_source_v6709.py','scripts/audit_lil_B214_source_v6709b.py',{"source_actual_v6709')":"source_actual_v6709b')",'unvisited_original_command_offsets=sorted(set(commands)-seen)':'unvisited_original_command_offsets=sorted(commands[a][\'source_offset\'] for a in set(commands)-seen),unvisited_fixture_command_offsets=sorted(set(commands)-seen)'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_offset_coordinate_correction.json',dict(derivation=proof,first_proof_retained=True,original_field_contained_fixture_coordinates_now_both_separately_named=True,all_body_name_masks_actual_visitation_and_run_unchanged=True,new_run_ROM_or_credit=False,full_goal_complete=False))
