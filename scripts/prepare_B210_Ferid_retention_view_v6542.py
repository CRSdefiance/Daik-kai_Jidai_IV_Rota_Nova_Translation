"""Prepare cumulative retention and the unchanged visual-review receipt workflow."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/B210_Ferid_retention_view_tools_v6542')
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True);proofs=[]
    proofs.append(derive('scripts/pin_lil_B209_v6490.py','scripts/pin_B210_Ferid_v6542.py',{'lil_B209_retention_v6490':'B210_Ferid_retention_v6542','lil_B209_release_v6489':'B210_Ferid_release_v6542','B209':'B210 and Ferid name','V6488':'V6541'}))
    proofs.append(derive('scripts/record_lil_B209_startup_view_v6492.py','scripts/record_B210_Ferid_startup_view_v6544.py',{'lil_B209_startup_v6492':'B210_Ferid_startup_v6544','V6439':'V6488','B209':'B210'}))
    save(ROOT/'derivation_receipt.json',dict(proofs=proofs,native_constants_and_prior_producers_preserved=True,full_goal_complete=False))
