"""Prepare source-locked cumulative build, exact patch, regression and current startup runners."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B214_release_tools_v6733')
if __name__=='__main__':
    assert not ROOT.exists();proofs=[]
    proofs.append(derive('scripts/build_lil_B213_v6686.py','scripts/build_lil_B214_v6733.py',{'B213':'B214','v6686':'v6733','v6685':'v6732'}))
    proofs.append(derive('scripts/run_lil_B213_regressions_v6686.py','scripts/run_lil_B214_regressions_v6733.py',{'B213':'B214','v6686':'v6733'}))
    proofs.append(derive('scripts/verify_lil_B213_release_v6687.py','scripts/verify_lil_B214_release_v6734.py',{'B213':'B214','v6687':'v6734','v6686':'v6733','v6641':'v6686','v6685':'v6732','reference_v6673':'reference_v6718','lil_B212_editorial':'lil_B213_editorial',"len(manifest['batches'])==605":"len(manifest['batches'])==606",'manifest_batches=605':'manifest_batches=606','all605_manifest_batches':'all606_manifest_batches','V6641':'V6686'}))
    proofs.append(derive('scripts/pin_lil_B213_v6688.py','scripts/pin_lil_B214_v6735.py',{'B213':'B214','v6688':'v6735','v6687':'v6734','V6686':'V6733'}))
    proofs.append(derive('scripts/run_lil_B213_startup_v6689.py','scripts/run_lil_B214_startup_v6736.py',{'B213':'B214','v6689':'v6736','version=6686':'version=6733'}))
    proofs.append(derive('scripts/verify_lil_B213_startup_v6690.py','scripts/verify_lil_B214_startup_v6737.py',{'B213':'B214','v6690':'v6737','v6689':'v6736','v6686':'v6733','v6641':'v6686','V6641':'V6686','Current6686':'Current6733','Current6686':'Current6733','lil_B212_runs_v6644':'lil_B213_runs_v6689'}))
    proofs.append(derive('scripts/record_lil_B213_startup_view_v6690.py','scripts/record_lil_B214_startup_view_v6737.py',{'B213':'B214','v6690':'v6737','V6641':'V6686'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_release_runners.json',dict(derivations=proofs,expected606_batches114_accepted18_checks_and110_regressions=True,clean_input_reconstruction_and_current31_frame5_actor_controls_required=True,no_new_B214_activation_claim=True,no_ROM_registry_ledger_or_credit_mutation_by_preparation=True,full_goal_complete=False));print('Seven immutable B214 release runners prepared.')
