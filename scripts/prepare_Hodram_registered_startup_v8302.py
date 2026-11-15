"""Prepare own registered captain1 startup;preserve all existing name/code/pool/input guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_registered_startup_tools_v8302')
if __name__=='__main__':
    assert not ROOT.exists();receipts=[]
    receipts.append(derive('scripts/capture_Hodram_V8259_v8269.py','scripts/capture_Hodram_registered_v8302.py',{
        'Hodram_B137_B45_B46_context_runs_v8269':'Hodram_registered_context_runs_v8302',
        'work/analysis/Gerhard_surname_release_v8260/registered_release_verification.json':'work/analysis/Hodram_three_blocks_release_v8301/registered_release_verification.json',
        'all-routes-unified-v8259':'all-routes-unified-v8300',
        'Hodram_B137_B45_B46_route{route}_v8269_V8259':'Hodram_registered_route{route}_v8302_V8300',
    }))
    old="""        release=read('work/analysis/Gerhard_surname_release_v8260/registered_release_verification.json')
        assert not reference['registered_candidate'] and self.doc['registered_candidate'] and self.doc['current_ROM']==release['candidate'] and self.doc['current_ROM_sha256']==reference['research_ROM_sha256']==release['candidate_sha256']"""
    new="""        release=read('work/analysis/Hodram_three_blocks_release_v8301/registered_release_verification.json')
        asset_release=read('work/analysis/Gerhard_surname_release_v8260/registered_release_verification.json')
        assert not reference['registered_candidate'] and self.doc['registered_candidate'] and self.doc['current_ROM']==release['candidate'] and self.doc['current_ROM_sha256']==release['candidate_sha256']
        assert reference['research_ROM_sha256']==asset_release['candidate_sha256'] and sha(self.arm)==asset_release['ARM9_sha256']==release['ARM9_sha256']
        assert release['only_SC1_B45_B46_B137_change_322_otherblocks_andall_other_files_components_exact'] and release['complete_ARM9_BSS_names_Blades_and123264_staged_payload_preserved']"""
    receipts.append(derive('scripts/Hodram_target_route_context_v8270.py','scripts/Hodram_registered_route_context_v8303.py',{
        'registered V8259 Hodram':'registered V8300 Hodram',old:new,
    }))
    receipts.append(derive('scripts/bind_Hodram_V8259_v8270.py','scripts/bind_Hodram_registered_v8303.py',{
        'scripts.Hodram_target_route_context_v8270':'scripts.Hodram_registered_route_context_v8303',
        'Hodram_current_binding_v8270':'Hodram_registered_binding_v8303',
        'Hodram_B137_B45_B46_context_runs_v8269':'Hodram_registered_context_runs_v8302',
        'current_V8259_Hodram_native_v8270':'current_V8300_Hodram_native_v8303',
        'work/analysis/Gerhard_surname_release_v8260/registered_release_verification.json':'work/analysis/Hodram_three_blocks_release_v8301/registered_release_verification.json',
        'all-routes-unified-v8259':'all-routes-unified-v8300','V8259 Hodram':'V8300 Hodram',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_own_registered_startup_derivations.json',dict(derivations=receipts,
        original_captain1_ordinary_inputs_no_savestate_orhistorical_RAM_overlay=True,
        exact12byte_Gerhard_inverse_Blades8_COMMON_directory_and123264_payload_guards_preserved=True,
        own_new_candidate_ROM_hash_andmanifest_cleanpatch_release_required=True,new_credit=0,full_goal_complete=False))
    print('Own registered V8300 Hodram startup/binder prepared;no capture launched before verified release.')
