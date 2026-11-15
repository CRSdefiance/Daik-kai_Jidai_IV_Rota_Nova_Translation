"""Preserve the A-wait observation; add one ordinary A to observe its actual return."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B207_initializer_tools_v7701c')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/capture_Maria_B207_initializer_v7701.py','scripts/capture_Maria_B207_initializer_v7701c.py',{
        'maria_B207_original_initializer_v7701':'maria_B207_original_initializer_v7701c',
        'Maria_B207_original_initializer_route{route}_v7701':'Maria_B207_original_initializer_route{route}_v7701c',
        "folder.mkdir(parents=True);(folder/'source_contract.json').write_bytes(contract.read_bytes())":"folder.mkdir(parents=True);source_inputs=inp;inp=folder/'ordinary_Maria_inputs_with_A4200.json';save(inp,read(source_inputs)+[dict(start=4200,duration=5,buttons=['A'])]);(folder/'source_contract.json').write_bytes(contract.read_bytes())",
        "inputs_sha256=sha(inp.read_bytes()),observer=":"inputs_sha256=sha(inp.read_bytes()),source_inputs=str(source_inputs),source_inputs_sha256=sha(source_inputs.read_bytes()),ordinary_A4200_completes_observed_original_2000_wait=True,preserved_wait_only_capture='work/analysis/maria_B207_original_initializer_v7701/route3/terminal.json',observer=",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_ordinary_A_wait_continuation.json',dict(derivation=result,no_native_command_condition_orstate_forcing=True,wait_only_capture_preserved=True,new_credit=0,full_goal_complete=False))
