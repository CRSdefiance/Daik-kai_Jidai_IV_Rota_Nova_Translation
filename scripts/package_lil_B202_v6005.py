"""Package the cumulative checkpoint with protected-input and full-scope proofs."""
from collections import Counter
from pathlib import Path
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.lil_B202_completion_text_v6003 import DETAILS,NEXT
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('releases/all_routes_unified_v5998')
if __name__=='__main__':
    assert not ROOT.exists()
    vp=Path('work/analysis/editorial_handoff_verification_v6004/verified_handoff.json')
    rp=Path('work/analysis/lil_B202_release_v5999/registered_release_verification.json')
    fp=Path('translations/lil_B202_contextual_final_review_v1.json')
    verified,release,final=map(read,[vp,rp,fp]);ledger=Path('translations/editorial_review_current_v1.json');data=read(ledger)
    assert sha(ledger.read_bytes())==verified['ledger_sha256']
    for key in ['candidate','patch']:assert release[key+'_sha256']==verified[key+'_sha256']==sha(Path(release[key]).read_bytes())
    assert sha(Path(release['exact_patch_reconstruction']).read_bytes())==sha(Path('out/lil_B202_reference_v5985_RESEARCH_ONLY.nds').read_bytes())==release['candidate_sha256']
    manifest=read(release['manifest']);assert len(manifest['batches'])==590 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(final['records'])==19 and data['completed_editorial_families'][-1]['records']==final['records'] and Counter(r['editorial_decision'] for r in final['records'])=={'revise':6,'retain-wording':13}
    assert all(r.get('fresh_retained_wording_justification') for r in final['records'] if r['editorial_decision']=='retain-wording')
    rows=[r for f in data['completed_editorial_families'] for r in f['records']]
    assert len(rows)==len({historical_key(r) for r in rows})==6327 and data['goal_status']=='active' and not data['full_goal_complete']
    assert tuple(data[k] for k in ['records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(6330,3959,2368)
    scope=read(data['unfinished_editorial_scope_v6003']['path'])
    assert scope['next_Lil_B203_clean_review_pending']['reviewed_objects']==0 and 'speaker_names_and_role_labels_localization_review_v5708' in scope and scope['untranslated_Alexandria_alias_v5139b']['caller_and_display_fidelity_open']
    assert 'following_B43_source_item_term_observed_v5980' in scope
    registry=read('translations/release_stack.json');assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    expected={
        'work/clean.nds':'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d',
        'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        'out/all_routes_combined_v4701_candidate.nds':'dbfb4e413047e54e50dc771f48fe0e5457e40e60e0991111474185c41858052e',
        'out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds':'0c6e5a686b4fefb98a4d25ebb3c0e8c90ffa20e3f43240ca1629d8f6d40c85f2',
        'out/all_routes_combined_v5947_candidate.nds':'9327b3b7497a6d31fa234be636b2cce117673d249c0f65cce9370dbd88a05e13'}
    for path,digest in expected.items():assert sha(Path(path).read_bytes())==digest,path
    text=f'''# Translation DS cumulative editorial checkpoint V5998

Experimental cumulative build for testing. Main V4701 remains promoted. The full editorial goal remains active.

- ROM: {release['candidate']}
- ROM SHA-256: {release['candidate_sha256']}
- Clean-input patch: {release['patch']}
- Patch SHA-256: {release['patch_sha256']}
- Required clean Japanese input SHA-256: {release['clean_input_sha256']}
- Registered profile: {release['profile']}
- Immutable construction baseline: {release['canonical_base']}
- Baseline SHA-256: {release['canonical_base_sha256']}
- Full manifest: {release['manifest']}
- Previous cumulative build: out/all_routes_combined_v5947_candidate.nds

The patch reconstructs the entire ROM byte for byte and equals the approved reference. All 590 batches, 114 accepted layers and 18 release checks are included. Only SC2 block 202 changes from V5947; every other file, component, name field, font, graphic and native code remains exact. All 69 atomic semantic negatives and 110 established regressions pass.

B202 adds 19 disjoint whole-exchange clean-Japanese reviews once: six revisions and thirteen justified retentions. Source, predecessor, current encoded text, controls, reasons and native/gameplay evidence are retained in the final review. Coverage is 6,327 completed contextual rereads and 6,330 source-prose reviews, with 3,959 integrated revisions and 2,368 justified retentions. Counted route coverage of 4,728 is a subset, not a whole-project denominator. Speaker-name localization remains explicitly in scope across 207 entries. Man, Woman and Stranger are included from V5891. Lil Argot, Charles Rochefort, Guildmaster and source-defined Sailor are retained contextually here without new name bytes or global name-review credit.

One Japanese and one English scene-content run observe all 19 speeches and 35 commands, with 74 complete source-matched native holds. These targeted ROM content fixtures preserve ordinary inputs and unforced conditions/results. They do not establish natural event activation, original location, earned inventory, full item effects, complete routes or hardware coverage. All six actual/paired sheets were viewed. Speech timing, RNG and later advance-prompt differences remain explicit. Queried final state groups and whole actor agree; PRNG differs. No broad simulation-equivalence or causal claim is made.

Two fresh New Game/town checks match V5947 across 31 whole frames and five actor controls. Town uses an inherited five-ship test battery, not earned progression. The six selected views were reviewed. All artifacts, earlier translations and failed producers are preserved.

{DETAILS}

{NEXT}

Final review: {fp}

Current handoff: docs/editorial_handoff_current.md

Verified handoff: {vp}
'''
    ROOT.mkdir(parents=True);(ROOT/'README.md').write_text(text,encoding='utf-8',newline='\n')
    evidence={str(p):sha(p.read_bytes()) for p in [vp,rp,fp,Path('docs/editorial_handoff_current.md'),Path(__file__),Path('scripts/lil_B202_completion_text_v6003.py')]}
    save(ROOT/'immutable_input_audit.json',dict(inputs=expected,all_protected_clean_canonical_main_rollback_and_parent_hashes_unchanged=True,every_generated_ROM_and_earlier_translation_preserved=True,ROMs_deleted=0,producer_sha256=sha(Path(__file__).read_bytes())))
    save(ROOT/'verification.json',dict(profile=release['profile'],candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],clean_input_sha256=release['clean_input_sha256'],canonical_base=release['canonical_base'],canonical_base_sha256=release['canonical_base_sha256'],manifest=release['manifest'],manifest_sha256=release['manifest_sha256'],changed_internal_files=release['file_changes'],changed_blocks={'/data/SC2.DK4':[202]},whole_clean_patch_and_reference_reconstruction_exact=True,all590_manifest_batches114_accepted18_checks_pass=True,completed=6327,source_prose=6330,revised=3959,retained=2368,unique_completed_historical_keys=6327,newly_completed_B202_objects=19,actual_speech_panels=19,actual_speech_observations=19,complete_native_holds=74,actual_menu_cases=0,measured_timing_RNG_state_and_later_RGB_differences_preserved=True,no_broad_simulation_equivalence_claim=True,all_prior_root_and_nested_history_preserved=True,main_V4701_preserved=True,full_goal_active=True,full_goal_complete=False,next_B203_clean_review_pending=True,retrospective207_names_and_role_label_queue_open=True,evidence=evidence,README_sha256=sha((ROOT/'README.md').read_bytes())))
    print('V5998 package verified:590 batches/114 accepted/18 checks,exact clean-input patch,6327 unique completed reviews. Full editorial/name-review goal active.')
