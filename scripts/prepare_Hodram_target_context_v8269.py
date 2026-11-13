"""Prepare own V8259 captain1 capture/context without reusing Lil RAM or weakening target-runtime guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_target_context_tools_v8269')
if __name__=='__main__':
    assert not ROOT.exists();receipts=[]
    receipts.append(derive('scripts/capture_Hodram_current_v8186.py','scripts/capture_Hodram_V8259_v8269.py',{
      'Hodram_B137_B45_B46_context_runs_v8186':'Hodram_B137_B45_B46_context_runs_v8269',
      'work/analysis/Rafael_B50_release_v8173/registered_release_verification.json':'work/analysis/Gerhard_surname_release_v8260/registered_release_verification.json',
      'all-routes-unified-v8172':'all-routes-unified-v8259',
      'Hodram_B137_B45_B46_route{route}_v8186_V8172':'Hodram_B137_B45_B46_route{route}_v8269_V8259',
    }))
    receipts.append(derive('scripts/Gerhard_registered_route_context_v8262.py','scripts/Hodram_target_route_context_v8270.py',{
      "self.doc['expected_original_captain_ID'] in [2]":"self.doc['expected_original_captain_ID'] in [1]",
      'its own exact registered name-correction ROM snapshot':'its own exact registered V8259 Hodram captain1 ROM snapshot',
    }))
    receipts.append(derive('scripts/bind_Hodram_current_v8187.py','scripts/bind_Hodram_V8259_v8270.py',{
      'scripts.papal_trade_route_native_context_v7626':'scripts.Hodram_target_route_context_v8270',
      'Hodram_current_binding_v8187':'Hodram_current_binding_v8270',
      'Hodram_B137_B45_B46_context_runs_v8186':'Hodram_B137_B45_B46_context_runs_v8269',
      'current_V8172_Hodram_native_v8187':'current_V8259_Hodram_native_v8270',
      'work/analysis/Rafael_B50_release_v8173/registered_release_verification.json':'work/analysis/Gerhard_surname_release_v8260/registered_release_verification.json',
      'all-routes-unified-v8172':'all-routes-unified-v8259',
      "registered_profile=plan['profile']":"registered_profile=plan['profile'],registered_candidate=True",
      'V8172 Hodram':'V8259 Hodram','Own V8172 Hodram':'Own V8259 Hodram',
      'all_strict2b6_COMMON_directory_and123264_payload_guards_pass':'all_strict_targetARM9_inverse_Blades_COMMON_directory_and123264_payload_guards_pass',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_context_derivations.json',dict(derivations=receipts,
        original_native_constants_andall_target_ARM9_inverse_Blades_COMMON_directory_pool_actor_and4MiB_guards_preserved=True,
        own_captain1_capture_required_no_borrowed_captain2_RAM=True,new_credit=0,full_goal_complete=False))
