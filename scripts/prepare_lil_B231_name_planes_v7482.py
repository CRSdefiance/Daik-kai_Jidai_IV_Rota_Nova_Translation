"""Execute fresh native planes for the different actor19 name and its components."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B231_name_plane_tools_v7482')
if __name__=='__main__':
    assert not ROOT.exists();row=derive('scripts/prove_lil_B226_name_planes_v7244.py','scripts/prove_lil_B231_name_planes_v7482.py',{'B226':'B231','name_planes_v7244':'name_planes_v7482','current_V7230_native_v7235':'current_V7466_native_v7471','consumers_v7241/twenty_effective_bodies40_dispatches_two_actors_four_name_consumers':'consumers_v7478/sixteen_effective_bodies32_dispatches_two_actors_four_name_consumers','[2,23]':'[2,19]','Manuel Almeida':'Carlo Sinat',"'Manuel','Almeida'":"'Carlo','Sinat'", "(23,'progressive-nameplate')":"(19,'progressive-nameplate')", "(23,'full-catalogue')":"(19,'full-catalogue')",'Lil_Argot_Manuel_Almeida':'Lil_Argot_Carlo_Sinat'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_fresh_name_planes.json',dict(tool=row,all24_name_component_alignments_fresh_on_own_V7466_input=True,no_Samwell_plane_orcatalogue_middle_assumption_reused=True,Carlo_Sinat_primary_family_andnull_middle_bound_by_distinct_getters=True,new_credit=0,full_goal_complete=False))
