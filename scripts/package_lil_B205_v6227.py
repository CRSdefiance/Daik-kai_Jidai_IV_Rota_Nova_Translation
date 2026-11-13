"""Package the verified cumulative ROM/clean patch with complete preserved editorial scope."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.lil_B205_completion_text_v6225 import DETAILS,NEXT
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('releases/all_routes_unified_v6220')
if __name__=='__main__':
    assert not ROOT.exists();vp=Path('work/analysis/editorial_handoff_verification_v6226/verified_handoff.json');rp=Path('work/analysis/lil_B205_release_v6221/registered_release_verification.json');fp=Path('translations/lil_B205_contextual_final_review_v1.json');cp=Path('translations/lil_B205_editorial_release_v1.json');bp=Path('work/analysis/current_V6220_native_v6228/verified_current_context_binding.json')
    v,r,f,c,b=map(read,[vp,rp,fp,cp,bp]);ledger=Path('translations/editorial_review_current_v1.json');d=read(ledger);assert sha(ledger.read_bytes())==v['ledger_sha256']
    for k in ['candidate','patch']:assert sha(Path(r[k]).read_bytes())==v[k+'_sha256']==r[k+'_sha256']
    assert sha(Path(r['exact_patch_reconstruction']).read_bytes())==r['candidate_sha256']==sha(Path('out/lil_B205_reference_v6203_RESEARCH_ONLY.nds').read_bytes())
    manifest=read(r['manifest']);assert len(manifest['batches'])==594 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    registry=read('translations/release_stack.json');assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    rows=[r for family in d['completed_editorial_families'] for r in family['records']];assert len(rows)==len({historical_key(r) for r in rows})==6387 and d['completed_editorial_families'][-1]['records']==f['records'] and len(f['records'])==17
    assert tuple(d[k] for k in ['records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(6390,3989,2398)
    scope=read(d['unfinished_editorial_scope_v6225']['path']);assert 'speaker_names_and_role_labels_localization_review_v5708' in scope and scope['next_Lil_B206_clean_review_pending']['reviewed_objects']==0 and d['active_source_prose_drafts']['native_message_IDs']==[750,751,752]
    assert d['goal_status']=='active' and not d['full_goal_complete'] and v['all_sessions_terminal_and_reaped'] and b['candidate_sha256']==r['candidate_sha256']
    frozen=dict(read('releases/all_routes_unified_v6160/immutable_input_audit.json')['inputs']);frozen.update(c['dependencies']);frozen['out/all_routes_combined_v6160_candidate.nds']='69c7b87dbd3f450a97fc0ba53a2f4e961566f6bba53b98c9d580324bb2bae712'
    for p in [vp,rp,fp,cp,bp,Path(b['native_input']),Path(b['context_plan']),Path(__file__),Path('scripts/lil_B205_completion_text_v6225.py')]:frozen[str(p)]=sha(p.read_bytes())
    for p,h in frozen.items():assert sha(Path(p).read_bytes())==h,p
    text=f'''# Translation DS cumulative editorial checkpoint V6220

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
- Previous cumulative build: out/all_routes_combined_v6160_candidate.nds

All594 manifest batches,114 accepted layers and18 release checks are present. The manifest contains the complete batch list. Only /data/SC2.DK4 block205 changes from V6160. All110 repository regressions and78 pre-mutation semantic negatives pass. The clean-input patch reconstructs this entire ROM exactly.

All17 parrot-scene panels were observed in a disclosed initialized content fixture,with63 complete native text holds. Five exact mimicry echoes,two sound captions,Lil Argot/Angelo Puccini nameplates and the complete closing joke were checked. Source/revised command timings,interval RNG,queried final state groups and98 sampled postscene whole frames agree within the measured scope. Current startup/town tests match31 full frames and five actor/captain controls. Natural event205 activation,original location,earned progression,full effects/routes and hardware remain unverified.

{DETAILS}

{NEXT}

Final review: {fp}

Current handoff: docs/editorial_handoff_current.md

Verified handoff: {vp}

Future native research input: {b['native_input']}. Strict6097 guards bind V6220's own actual frame4000 snapshot and123264 deployed bytes. This reuses an existing exact capture;it is not a new gameplay visit or review credit.
'''
    ROOT.mkdir(parents=True);(ROOT/'README.md').write_text(text,encoding='utf-8',newline='\n')
    save(ROOT/'immutable_input_audit.json',dict(inputs=frozen,all_protected_clean_canonical_main_rollback_parent_and_frozen_dependencies_verified=True,every_generated_ROM_translation_proof_draft_and_failure_preserved=True,ROMs_deleted=0,producer_sha256=sha(Path(__file__).read_bytes())))
    save(ROOT/'verification.json',dict(profile=r['profile'],candidate=r['candidate'],candidate_sha256=r['candidate_sha256'],patch=r['patch'],patch_sha256=r['patch_sha256'],clean_input_sha256=r['clean_input_sha256'],canonical_base=r['canonical_base'],canonical_base_sha256=r['canonical_base_sha256'],manifest=r['manifest'],manifest_sha256=r['manifest_sha256'],changed_internal_files=r['file_changes'],changed_blocks={'/data/SC2.DK4':[205]},changed_components=[],whole_clean_patch_and_reference_reconstruction_exact=True,all594_manifest_batches114_accepted18_checks_pass=True,regression_tests_passed=110,precommit_negative_controls_passed=78,completed=6387,source_prose=6390,revised=3989,retained=2398,newly_completed_B205_objects=17,new_revisions=8,new_justified_retentions=9,actual_English_panels=17,complete_native_holds=63,new_emulator_runs=4,new_frames=47404,same_code_source_English_all34_timing_and_interval_RNG_values_equal=True,all98_postscene_RGB_samples_and7150_notice_equal=True,queried_final_groups_actor_and_PRNG_equal_with_no_broad_equivalence_claim=True,current_native_input=b['native_input'],current_native_input_sha256=b['native_input_sha256'],all_prior_history_preserved=True,main_V4701_preserved=True,broader207_names_and_full_editorial_goal_active=True,full_goal_complete=False,next_B206_clean_inventory_pending=True,README_sha256=sha((ROOT/'README.md').read_bytes()),immutable_input_audit_sha256=sha((ROOT/'immutable_input_audit.json').read_bytes())))
    print('V6220 packaged:594/114/18,exact clean-input patch,6387 unique completed reviews. Full editorial/name-review goal remains active;next B206 clean inventory.')
