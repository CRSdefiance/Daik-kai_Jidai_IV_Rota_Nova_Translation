"""Bind measured name byte offsets without altering native numerical constants."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/B210_Ferid_runner_derivation_v6541b')
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    proof=derive('scripts/verify_lil_B209_startup_v6492.py','scripts/verify_B210_Ferid_startup_v6544.py',{
        'lil_B209_startup_v6492':'B210_Ferid_startup_v6544','lil_B209_runs_v6491':'B210_Ferid_runs_v6543','all_routes_combined_v6488':'all_routes_combined_v6541','all_routes_combined_v6439':'all_routes_combined_v6488','lil_B208_runs_v6442':'lil_B209_runs_v6491','Current6488':'Current6541','V6439':'V6488','B209':'B210',
        "assert arm==prior.read_file('/__arm9__.bin')":"assert sha(arm)=='aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05' and sha(prior.read_file('/__arm9__.bin'))=='4f4e41d26a0b24610a38a9da03dc549e4afec82121a1c72f35665104bb7ea351'; assert [i for i,(a,b) in enumerate(zip(arm,prior.read_file('/__arm9__.bin'),strict=True)) if a!=b]==read('work/analysis/Al_Ferid_name_research_v6518/research_image_receipt.json')['changed_ARM9_byte_offsets']"})
    preserved={p:sha(Path(p).read_bytes()) for p in ['scripts/build_B210_Ferid_v6541.py','scripts/run_B210_Ferid_regressions_v6541.py','scripts/run_B210_Ferid_startup_v6543.py','scripts/prepare_B210_Ferid_release_runners_v6541.py']};save(ROOT/'derivation_receipt.json',dict(proof=proof,preserved_first_three_runners_and_failed_derivation=preserved,original_rejected_for_new_high_integer_constants_before_verifier_write=True,uses_measured_exact_name_byte_offset_census=True,no_native_address_or_old_producer_mutation=True,full_goal_complete=False));print('Startup verifier derived with measured exact name-data offsets;all native constants preserved. Initial failed preparation retained.')
