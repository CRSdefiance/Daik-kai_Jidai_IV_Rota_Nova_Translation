"""Package cumulative name checkpoint,exact patch and immutable-input evidence without promotion."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.shady_man_completion_text_v6275 import SUMMARY,NEXT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('releases/all_routes_unified_v6270')
if __name__=='__main__':
    assert not ROOT.exists();vp=Path('work/analysis/editorial_handoff_verification_v6276/verified_handoff.json');rp=Path('work/analysis/shady_man_label_release_v6271/registered_release_verification.json');v,r=map(read,[vp,rp]);assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==v['ledger_sha256'] and v['actor173_Shady_Man_integrated']
    for key in ['candidate','patch']:assert sha(Path(r[key]).read_bytes())==r[key+'_sha256']==v[key+'_sha256']
    assert sha(Path(r['exact_patch_reconstruction']).read_bytes())==r['candidate_sha256'];manifest=read(r['manifest']);assert len(manifest['batches'])==595 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    registry=read('translations/release_stack.json');assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    expected={'work/clean.nds':'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d','out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe','out/all_routes_combined_v4701_candidate.nds':'dbfb4e413047e54e50dc771f48fe0e5457e40e60e0991111474185c41858052e','out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds':'0c6e5a686b4fefb98a4d25ebb3c0e8c90ffa20e3f43240ca1629d8f6d40c85f2','out/all_routes_combined_v6220_candidate.nds':'07e7f9ba8d12de33b4b1cf0bc006f2fddbf7b031d488233982ba050354201b0f'}
    for p,h in expected.items():assert sha(Path(p).read_bytes())==h,p
    scope=read(v['scope_inventory']['path']);assert scope['actor173_name_review_current_v6275']['closed_source_context_label_lead']==173 and scope['B206_next_native_relocation_actual_release_v6275']['prose_objects']==28
    text=f'''# Translation DS cumulative editorial checkpoint V6270

Experimental cumulative build. Main V4701 remains promoted;the full editorial goal is active.

- ROM: {r['candidate']}
- ROM SHA-256: {r['candidate_sha256']}
- Clean-input patch: {r['patch']}
- Patch SHA-256: {r['patch_sha256']}
- Required clean Japanese input SHA-256: {r['clean_input_sha256']}
- Registered profile: {r['profile']}
- Immutable construction baseline: {r['canonical_base']}
- Baseline SHA-256: {r['canonical_base_sha256']}
- Full manifest: {r['manifest']}
- Previous cumulative build: out/all_routes_combined_v6220_candidate.nds

Actor173's recurring label changes from Suspicious Person to Shady Man. Eight complete Japanese seller exchanges support the natural localization. Only one owned terminated primary string prefix changes. All other names and every dialogue line,pointer,font,graphic,component and staged allocation extent remain exact to V6220. Earlier Man/Woman/Stranger remain.

All595 manifest batches/114 accepted layers/18 release checks,57 semantic rejection controls and110 regressions pass. The clean-input patch reconstructs the full ROM exactly. Offline native checks cover both name consumers for all207 actors,all621 name fields,eight voices,96 substitution/literal alignments and the complete label plane. Representative actual display shows10 changed headers in18 complete Japanese source panels. The disclosed B22 fixture is not natural event206 activation or full-route/hardware coverage. Small timing/RNG differences are retained explicitly. Catalogue UI is unvisited;its native getters and font bounds are checked offline. Current New Game/town cold boots match31 full sampled RGB frames and five actor/captain controls;town uses an inherited test battery.

Counts remain6387 contextual rereads/6390 source-prose/3989 integrated revisions/2398 retentions,with no duplicate dialogue or name credit. B206's28 prose decisions remain uncredited,pending English native/menu/relocation/actual/release checks. All207 names/aliases remain in the broader retrospective review. Preserve every earlier ROM,translation,draft,producer,proof,failure and unresolved lead.

{SUMMARY}

{NEXT}

Name manuscript: translations/shady_man_label_manuscript_v2.json

Verified handoff: {vp}

Current handoff: docs/editorial_handoff_current.md
'''
    ROOT.mkdir(parents=True);(ROOT/'README.md').write_text(text,encoding='utf-8',newline='\n');save(ROOT/'immutable_input_audit.json',dict(inputs=expected,all_clean_canonical_main_rollback_parent_inputs_unchanged=True,all_generated_ROMs_translations_history_proofs_and_failures_preserved=True,ROMs_deleted=0))
    save(ROOT/'verification.json',dict(profile=r['profile'],candidate=r['candidate'],candidate_sha256=r['candidate_sha256'],patch=r['patch'],patch_sha256=r['patch_sha256'],clean_input_sha256=r['clean_input_sha256'],canonical_base=r['canonical_base'],canonical_base_sha256=r['canonical_base_sha256'],manifest=r['manifest'],manifest_sha256=r['manifest_sha256'],changed_internal_files=r['changed_internal_files'],changed_primary_label={'173':'Shady Man'},all595_batches114_accepted18_checks57_negatives110_regressions_pass=True,whole_clean_input_patch_and_approved_reference_reconstruct_exactly=True,completed=6387,source_prose=6390,revised=3989,retained=2398,no_duplicate_dialogue_or_name_credit=True,all207_name_and_alias_scope_open_206_other_actors_not_newly_approved=True,B206_uncredited_prose_objects=28,actual_changed_headers=10,actual_complete_nameplates=18,actual_complete_Japanese_source_speeches=18,actual_source_name_scene_boots=1,actual_source_name_scene_frames=16001,actual_registered_startup_boots=2,actual_registered_startup_frames=21402,timing_and_RNG_differences_unmasked=True,actual_catalogue_UI_not_visited_offline_native_consumers_and_font_bounds_checked=True,main_V4701_preserved=True,all_previous_artifacts_preserved=True,full_goal_active=True,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [vp,rp,Path('translations/shady_man_label_manuscript_v2.json'),Path('scripts/shady_man_completion_text_v6275.py'),Path(__file__)]}));print('Packaged V6270 cumulative ROM/clean patch/manifest and source-native-actual evidence. All protected inputs exact;full goal active.')
