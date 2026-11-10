"""Bind the existing strict target-runtime startup procedure to the exact registered candidate."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Gerhard_registered_startup_tools_v8261')
if __name__=='__main__':
    assert not ROOT.exists();receipts=[]
    receipts.append(derive('scripts/capture_Gerhard_research_v8217.py','scripts/capture_Gerhard_registered_v8261.py',{
      'own unregistered research-ROM':'own registered cumulative-ROM',
      'Gerhard_research_context_runs_v8217':'Gerhard_registered_context_runs_v8261',
      'work/analysis/Gerhard_reference_v8215/research_image_receipt.json':'work/analysis/Gerhard_surname_release_v8260/registered_release_verification.json',
      "rom=Path(ref['research_ROM']);v=dict(candidate_sha256=ref['research_ROM_sha256']);manifest=dict(profile='Gerhard-Adernkatz-RESEARCH-ONLY')":"rom=Path(ref['candidate']);v=dict(candidate_sha256=ref['candidate_sha256']);manifest=dict(profile=ref['profile'])",
      "assert not ref['registered_candidate'] and sha(rom.read_bytes())==v['candidate_sha256']":"assert ref['whole_clean_input_ROM_reconstruction_byte_exact'] and sha(rom.read_bytes())==v['candidate_sha256']",
      'Gerhard_research_route{route}_v8217_reference8215':'Gerhard_registered_route{route}_v8261_candidate8259',
      'exact_research_ROM_only_no_RAM_or_savestate_fixture':'exact_registered_ROM_only_no_RAM_or_savestate_fixture',
      'registered_candidate=False':'registered_candidate=True',
      'research_reference':'registered_release',
      'own research-ROM NewGame terminal;actual captain/payload/native binding pending;not registered oroptional scene.':'own registered-ROM NewGame terminal;actual captain/payload/native binding pending;not optional scene coverage.',
    }))
    old="assert not reference['registered_candidate'] and self.doc['current_ROM']==reference['research_ROM'] and self.doc['current_ROM_sha256']==reference['research_ROM_sha256']"
    new="""release=read('work/analysis/Gerhard_surname_release_v8260/registered_release_verification.json')
        assert not reference['registered_candidate'] and self.doc['registered_candidate'] and self.doc['current_ROM']==release['candidate'] and self.doc['current_ROM_sha256']==reference['research_ROM_sha256']==release['candidate_sha256']
        assert sha(Path(release['manifest']).read_bytes())==release['manifest_sha256'] and release['whole_clean_input_ROM_reconstruction_byte_exact'] and release['all18_registered_release_checks_pass']"""
    receipts.append(derive('scripts/Gerhard_research_route_context_v8218.py','scripts/Gerhard_registered_route_context_v8262.py',{
      'its own exact unregistered name-correction ROM snapshot':'its own exact registered name-correction ROM snapshot',old:new,
      'research_reference=reference':'research_reference=reference,registered_release=release',
      'registered_candidate=False':'registered_candidate=True',
    }))
    old="assert not reference['registered_candidate'] and sha(Path(plan['candidate']).read_bytes())==reference['research_ROM_sha256']==plan['candidate_sha256'] and plan['profile']=='Gerhard-Adernkatz-RESEARCH-ONLY'"
    new="assert reference['whole_clean_input_ROM_reconstruction_byte_exact'] and sha(Path(plan['candidate']).read_bytes())==reference['candidate_sha256']==plan['candidate_sha256'] and plan['profile']==reference['profile']=='all-routes-unified-v8259'"
    receipts.append(derive('scripts/bind_Gerhard_research_v8218.py','scripts/bind_Gerhard_registered_v8262.py',{
      'own research-ROM':'own registered-ROM',
      'scripts.Gerhard_research_route_context_v8218':'scripts.Gerhard_registered_route_context_v8262',
      'Gerhard_research_binding_v8218':'Gerhard_registered_binding_v8262','Gerhard_research_context_runs_v8217':'Gerhard_registered_context_runs_v8261',
      'Gerhard_reference8215_own_native_v8218':'current_V8259_Lil_native_v8262',
      'work/analysis/Gerhard_reference_v8215/research_image_receipt.json':'work/analysis/Gerhard_surname_release_v8260/registered_release_verification.json',old:new,
      "reference['research_ARM9_sha256']":"reference['ARM9_sha256']",'registered_candidate=False':'registered_candidate=True',
      'research_profile':'profile','own_research_capture_context':'own_registered_capture_context','own_research_startup_andstrict':'own_registered_startup_andstrict',
      'own_Gerhard_research_context.png':'own_Gerhard_registered_context.png','Research8215 Lil':'Registered8259 Lil',
      'Own research8215 captain2':'Own registered8259 captain2','No optional scene orregistered release.':'No optional scene coverage.',
    }))
    receipts.append(derive('scripts/verify_Gerhard_research_startup_v8219.py','scripts/verify_Gerhard_registered_startup_v8263.py',{
      'Own research startup':'Own registered startup','scripts.Gerhard_research_route_context_v8218':'scripts.Gerhard_registered_route_context_v8262',
      'Gerhard_research_startup_view_v8219':'Gerhard_registered_startup_view_v8263',
      'Gerhard_research_binding_v8218/own_research_startup_andstrict_captain2_context.json':'Gerhard_registered_binding_v8262/own_registered_startup_andstrict_captain2_context.json',
      "assert not current['registered_candidate']":"assert current['registered_candidate']",
      'own_research_context':'own_registered_context','own-research-eight-getters':'own-registered-eight-getters',
      "NdsImage.open(ref['research_ROM'])":"NdsImage.open(current['candidate'])",
      "research_ROM=ref['research_ROM'],research_ROM_sha256=ref['research_ROM_sha256']":"registered_ROM=current['candidate'],registered_ROM_sha256=current['candidate_sha256']",
      'research_startup=str(CURRENT),research_startup_sha256':'registered_startup=str(CURRENT),registered_startup_sha256',
      'fresh_ordinary_research_coldboot_frames':'fresh_ordinary_registered_coldboot_frames','research_capture':'registered_capture',
      'native_eight_getters_from_actual_own_research_snapshot':'native_eight_getters_from_actual_own_registered_snapshot',
      'original_research_input':'original_registered_input','no_research_RAM_data_overlay':'no_registered_RAM_data_overlay',
      'fullreference_loaders_callers_actual_focused_scenes_policy_atomic_registered_release_pending':'Hodram28_stored_names_actual_policy_registered_andfull_editorial_goal_pending',
      'registered_current_V8172_andmainV4701_unchanged':'registered_current_V8259_andmainV4701_unchanged',
      'own_research_startup6_RGBpairs_actor_equal8_fresh_getters_direct_view.json':'own_registered_startup6_RGBpairs_actor_equal8_fresh_getters_direct_view.json',
      'Research startup4001':'Registered startup4001',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_startup_tools.json',dict(derivations=receipts,
        all_current_instruction_actor_pool_ARM9_inverse_Blades_COMMON_directory_and4MiB_guards_preserved=True,
        fresh_registered_capture_then_binding_then_direct_view_required_before_final_view_receipt=True,new_credit=0,full_goal_complete=False))
    print('Prepared fresh registered4001-frame Lil startup,strict target context and8getters;native guards unchanged.')
