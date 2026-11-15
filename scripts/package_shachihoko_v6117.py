"""Package the verified cumulative checkpoint without promoting or pruning it."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.shachihoko_completion_text_v6115 import DETAILS,NEXT
ROOT=Path('releases/all_routes_unified_v6110')
if __name__=='__main__':
    assert not ROOT.exists()
    vp=Path('work/analysis/editorial_handoff_verification_v6116/verified_handoff.json');rp=Path('work/analysis/shachihoko_release_v6111/registered_release_verification.json')
    fp=Path('translations/shachihoko_item116_contextual_final_review_v1.json');cp=Path('translations/shachihoko_item116_editorial_release_v1.json');np=Path('work/analysis/current_speaker_labels_v6113/existing_Man_Woman_Stranger_labels_and_broader_name_scope.json')
    v,r,f,c,n=map(read,[vp,rp,fp,cp,np]);ledger=Path('translations/editorial_review_current_v1.json');data=read(ledger)
    assert sha(ledger.read_bytes())==v['ledger_sha256']
    for k in ['candidate','patch']:assert sha(Path(r[k]).read_bytes())==v[k+'_sha256']==r[k+'_sha256']
    assert sha(Path(r['exact_patch_reconstruction']).read_bytes())==r['candidate_sha256']
    manifest=read(r['manifest']);assert len(manifest['batches'])==592 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    registry=read('translations/release_stack.json');assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert v['all110_regressions35_precommit_controls_pass'] and v['all_sessions_terminal_and_reaped']
    rows=[x for family in data['completed_editorial_families'] for x in family['records']];assert len(rows)==len({historical_key(x) for x in rows})==6350
    assert f['records']==data['completed_editorial_families'][-1]['records'] and len(f['records'])==1 and len(f['coordinated_static_label_records'])==1
    assert tuple(data[k] for k in ['records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(6353,3969,2381)
    assert data['goal_status']=='active' and not data['full_goal_complete'] and data['active_source_prose_drafts']['native_message_IDs']==[750,751,752]
    scope=read(data['unfinished_editorial_scope_v6115']['path']);assert 'speaker_names_and_role_labels_localization_review_v5708' in scope and scope['speaker_name_localization_current_example_v6113']['broader207_names_roles_aliases_and_retrospective_uses_open']
    assert [x['current_label'] for x in n['current_labels']]==['Man','Woman','Stranger']
    expected=dict(read('releases/all_routes_unified_v6050/immutable_input_audit.json')['inputs'])
    expected.update({'out/all_routes_combined_v6050_candidate.nds':'2472f0c5203ca2b9692a8b4ce2ab64c0049febe598fc61fecc071adda0d3af43'})
    for path,digest in expected.items():assert sha(Path(path).read_bytes())==digest,path
    frozen={**expected,**c['dependencies']}
    for p in [vp,rp,fp,cp,np,Path(__file__),Path('scripts/shachihoko_completion_text_v6115.py')]:frozen[str(p)]=sha(p.read_bytes())
    for path,digest in frozen.items():assert sha(Path(path).read_bytes())==digest,path
    text=f'''# Translation DS cumulative editorial checkpoint V6110

Experimental build for testing. Main V4701 remains promoted. The full editorial goal remains active.

- ROM: {r['candidate']}
- ROM SHA-256: {r['candidate_sha256']}
- Clean-input patch: {r['patch']}
- Patch SHA-256: {r['patch_sha256']}
- Required clean Japanese input SHA-256: {r['clean_input_sha256']}
- Registered profile: {r['profile']}
- Construction baseline: {r['canonical_base']}
- Baseline SHA-256: {r['canonical_base_sha256']}
- Manifest: {r['manifest']}
- Previous cumulative build: out/all_routes_combined_v6050_candidate.nds

The clean-input patch reconstructs the entire ROM exactly. The registered builder includes592 batches,114 accepted layers and18 passing release checks. All110 established regressions and35 pre-mutation rejection controls pass. Only ARM9 and COMMON change from V6050; all story files, fonts, graphics and other components remain exact.

Speaker-label localization remains open across207 character entries and their aliases. The earlier Woman in a Couple label is already Woman here, with Man and Stranger also retained from V5891. Current name fields and referenced staged strings have been rechecked. The screenshot supplied by the user is historical evidence, not a new current-build gameplay capture. Preserve approved Rafael, Hodram, Joakim, Maria and Camille; infer no relationship, rank or biography from an awkward literal label.

{DETAILS}

{NEXT}

Final review: {fp}

Current handoff: docs/editorial_handoff_current.md

Verified handoff: {vp}
'''
    ROOT.mkdir(parents=True);(ROOT/'README.md').write_text(text,encoding='utf-8',newline='\n')
    save(ROOT/'immutable_input_audit.json',dict(inputs=frozen,all_protected_clean_canonical_main_rollback_and_parent_hashes_unchanged=True,all55_release_dependencies_and_frozen_checkpoint_proofs_verified=True,every_generated_ROM_and_earlier_translation_preserved=True,ROMs_deleted=0,producer_sha256=sha(Path(__file__).read_bytes())))
    save(ROOT/'verification.json',dict(profile=r['profile'],candidate=r['candidate'],candidate_sha256=r['candidate_sha256'],patch=r['patch'],patch_sha256=r['patch_sha256'],clean_input_sha256=r['clean_input_sha256'],canonical_base=r['canonical_base'],canonical_base_sha256=r['canonical_base_sha256'],manifest=r['manifest'],manifest_sha256=r['manifest_sha256'],changed_internal_files=r['file_changes'],changed_components=r['component_changes'],whole_clean_patch_and_reference_reconstruction_exact=True,all592_manifest_batches114_accepted18_checks_pass=True,regression_tests_passed=110,precommit_negative_controls_passed=35,completed=6350,source_prose=6353,revised=3969,retained=2381,newly_completed_COMMON2931_objects=1,static_title_and_generic_notice_dialogue_credit=0,actual_new_cold_boots=3,actual_frames=29822,actual_Items_holds=2,actual_complete_title_description_fields=8,native_CPU_cases=24,actual_vs_offline_scopes_distinct=True,natural_event_original_location_earned_progress_full_effects_routes_and_hardware_not_claimed=True,all_prior_root_and_nested_history_preserved=True,main_V4701_preserved=True,full_goal_active=True,full_goal_complete=False,next_B204_target_prose_pending=True,broader207_name_role_alias_queue_open=True,README_sha256=sha((ROOT/'README.md').read_bytes()),immutable_input_audit_sha256=sha((ROOT/'immutable_input_audit.json').read_bytes())))
    print('V6110 package verified:exact clean-input patch,592/114/18 checks,6350 completed reviews. Full editorial and207-name review remain active.')
