"""Prepare immutable evidence closure and one-write positive reconstruction."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B228_positive_tools_v7368')
if __name__=='__main__':
    assert not ROOT.exists() and not Path('scripts/validate_lil_B228_atomic_v7368.py').exists()
    r=derive('scripts/validate_lil_B226_atomic_v7274.py','scripts/validate_lil_B228_atomic_v7368.py',{'B226':'B228','final_paths_v7267':'final_paths_v7362','atomic_v7274':'atomic_v7368','seal_lil_B226_references_v7269':'seal_lil_B228_references_v7364','atomic_tools_v7273':'atomic_tools_v7367','prepare_lil_B226_atomic_v7273':'prepare_lil_B228_atomic_v7367',"len(proof['changed_records'])==20":"len(proof['changed_records'])==13",'positive_records=20':'positive_records=13','source1196_bytes_inverse_including_tail2_recovered':'source760_bytes_inverse_including_tail2_recovered','all20_actual20_pages79_body79_headers_bound':'all13_actual13_pages51_body51_headers_bound','20 speeches/20 pages,complete1196-byte':'13 speeches/13 pages,complete760-byte'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_positive_validator.json',dict(tool=r,unapproved_catalogue_middle_anditem50_bound_before_archive_write=True,new_credit=0,full_goal_complete=False))
