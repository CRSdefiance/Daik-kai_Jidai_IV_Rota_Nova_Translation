"""Derive the one-write positive validator against the full B227 immutable closure."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B227_positive_tools_v7321')
if __name__=='__main__':
    assert not ROOT.exists()
    r=derive('scripts/validate_lil_B226_atomic_v7274.py','scripts/validate_lil_B227_atomic_v7321.py',{'B226':'B227','lil_B226_final_paths_v7267':'lil_B227_final_paths_v7315','lil_B226_atomic_v7274':'lil_B227_atomic_v7321','seal_lil_B226_references_v7269':'seal_lil_B227_references_v7317','lil_B226_atomic_tools_v7273':'lil_B227_atomic_tools_v7320','prepare_lil_B226_atomic_v7273':'prepare_lil_B227_atomic_v7320',"len(proof['changed_records'])==20":"len(proof['changed_records'])==9",'positive_records=20':'positive_records=9','source1196_bytes_inverse_including_tail2_recovered':'source668_bytes_inverse_including_tail2_recovered','all20_actual20_pages79_body79_headers_bound':'all9_actual9_pages35_body35_headers_bound','20 speeches/20 pages,complete1196-byte':'9 speeches/9 pages,complete668-byte'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_positive_validator.json',r)
