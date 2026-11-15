"""Package the verified cumulative build,clean-input patch and preserved full scope."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.lil_B204_completion_text_v6165 import DETAILS,NEXT
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('releases/all_routes_unified_v6160')
if __name__=='__main__':
    assert not ROOT.exists();vp=Path('work/analysis/editorial_handoff_verification_v6166/verified_handoff.json');rp=Path('work/analysis/lil_B204_release_v6161/registered_release_verification.json');fp=Path('translations/lil_B204_contextual_final_review_v1.json');cp=Path('translations/lil_B204_editorial_release_v1.json');bp=Path('work/analysis/current_V6160_native_v6168/verified_current_context_binding.json')
    v,r,f,c,b=map(read,[vp,rp,fp,cp,bp]);ledger=Path('translations/editorial_review_current_v1.json');d=read(ledger);assert sha(ledger.read_bytes())==v['ledger_sha256']
    for k in ['candidate','patch']:assert sha(Path(r[k]).read_bytes())==v[k+'_sha256']==r[k+'_sha256']
    assert sha(Path(r['exact_patch_reconstruction']).read_bytes())==r['candidate_sha256']==sha(Path('out/lil_B204_reference_v6138_RESEARCH_ONLY.nds').read_bytes())
    manifest=read(r['manifest']);assert len(manifest['batches'])==593 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    registry=read('translations/release_stack.json');assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    rows=[x for family in d['completed_editorial_families'] for x in family['records']];assert len(rows)==len({historical_key(x) for x in rows})==6370 and d['completed_editorial_families'][-1]['records']==f['records'] and len(f['records'])==20
    assert tuple(d[k] for k in ['records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(6373,3981,2389)
    scope=read(d['unfinished_editorial_scope_v6165']['path']);assert 'speaker_names_and_role_labels_localization_review_v5708' in scope and scope['next_Lil_B205_clean_review_pending']['reviewed_objects']==0 and d['active_source_prose_drafts']['native_message_IDs']==[750,751,752]
    assert d['goal_status']=='active' and not d['full_goal_complete'] and v['all_sessions_terminal_and_reaped'] and b['candidate_sha256']==r['candidate_sha256']
    frozen=dict(read('releases/all_routes_unified_v6110/immutable_input_audit.json')['inputs']);frozen.update(c['dependencies']);frozen['out/all_routes_combined_v6110_candidate.nds']='7269fc058192b6783b26f4db384330be8b614de229e57496d21338169a886f71'
    for p in [vp,rp,fp,cp,bp,Path(b['native_input']),Path(b['context_plan']),Path(__file__),Path('scripts/lil_B204_completion_text_v6165.py')]:frozen[str(p)]=sha(p.read_bytes())
    for path,h in frozen.items():assert sha(Path(path).read_bytes())==h,path
    text=f'''# Translation DS cumulative editorial checkpoint V6160

Experimental cumulative build. Main V4701 remains promoted. The full editorial goal remains active.

- ROM: {r['candidate']}
- ROM SHA-256: {r['candidate_sha256']}
- Clean-input patch: {r['patch']}
- Patch SHA-256: {r['patch_sha256']}
- Required clean Japanese input SHA-256: {r['clean_input_sha256']}
- Profile: {r['profile']}
- Immutable canonical baseline: {r['canonical_base']}
- Baseline SHA-256: {r['canonical_base_sha256']}
- Manifest: {r['manifest']}
- Previous cumulative build: out/all_routes_combined_v6110_candidate.nds

All593 manifest batches,114 accepted layers and18 release checks are present. The exact full batch list is in the manifest. Only /data/SC2.DK4 block204 changes from V6110. All110 established regressions and78 pre-mutation semantic negative controls pass. The clean-input patch reconstructs the whole ROM exactly.

All20 revised scene panels are observed in a disclosed content fixture,with77 complete native text holds. Current startup/town tests match31 full frames and five actor/captain controls. The user can cold-boot New Game,ordinary town/refit and the Japanese castle scene to provide broader natural-route feedback;natural event204 activation,earned progression,full effects/routes and hardware have not been verified here.

{DETAILS}

{NEXT}

Final review: {fp}

Current handoff: docs/editorial_handoff_current.md

Verified handoff: {vp}

The next review can use the current registered-ROM native input at {b['native_input']},bound to V6160's own frame4000 snapshot with strict6097 guards. This is technical research context,not a new gameplay visit or review credit.
'''
    ROOT.mkdir(parents=True);(ROOT/'README.md').write_text(text,encoding='utf-8',newline='\n')
    save(ROOT/'immutable_input_audit.json',dict(inputs=frozen,all_protected_clean_canonical_main_rollback_parent_and_frozen_dependencies_verified=True,every_generated_ROM_translation_proof_draft_and_failure_preserved=True,ROMs_deleted=0,producer_sha256=sha(Path(__file__).read_bytes())))
    save(ROOT/'verification.json',dict(profile=r['profile'],candidate=r['candidate'],candidate_sha256=r['candidate_sha256'],patch=r['patch'],patch_sha256=r['patch_sha256'],clean_input_sha256=r['clean_input_sha256'],canonical_base=r['canonical_base'],canonical_base_sha256=r['canonical_base_sha256'],manifest=r['manifest'],manifest_sha256=r['manifest_sha256'],changed_internal_files=r['file_changes'],changed_blocks={'/data/SC2.DK4':[204]},changed_components=[],whole_clean_patch_and_reference_reconstruction_exact=True,all593_manifest_batches114_accepted18_checks_pass=True,regression_tests_passed=110,precommit_negative_controls_passed=78,completed=6370,source_prose=6373,revised=3981,retained=2389,newly_completed_B204_objects=20,new_revisions=12,new_justified_retentions=8,actual_English_panels=20,complete_native_holds=77,new_emulator_runs=3,new_frames=34403,current_same_code_Japanese_prefix_and_older_full_source_baselines_distinct=True,source_ARM9_COMMON_item_name_and_timing_RNG_state_limits_preserved=True,current_native_input=b['native_input'],current_native_input_sha256=b['native_input_sha256'],all_prior_history_preserved=True,main_V4701_preserved=True,broader207_names_and_full_editorial_goal_active=True,full_goal_complete=False,next_B205_clean_inventory_pending=True,README_sha256=sha((ROOT/'README.md').read_bytes()),immutable_input_audit_sha256=sha((ROOT/'immutable_input_audit.json').read_bytes())))
    print('V6160 package verified:593/114/18,exact clean-input patch,6370 unique completed reviews. B205 and the full editorial/name-review goal remain active.')
