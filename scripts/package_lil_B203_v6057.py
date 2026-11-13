"""Package the cumulative checkpoint and audit protected inputs and full scope."""
from collections import Counter
from pathlib import Path
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.lil_B203_completion_text_v6055 import DETAILS,NEXT
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('releases/all_routes_unified_v6050')
if __name__=='__main__':
    assert not ROOT.exists()
    vp=Path('work/analysis/editorial_handoff_verification_v6056/verified_handoff.json')
    rp=Path('work/analysis/lil_B203_release_v6051/registered_release_verification.json')
    fp=Path('translations/lil_B203_contextual_final_review_v1.json')
    verified,release,final=map(read,[vp,rp,fp]);ledger=Path('translations/editorial_review_current_v1.json');data=read(ledger)
    assert sha(ledger.read_bytes())==verified['ledger_sha256']
    for key in ['candidate','patch']:assert release[key+'_sha256']==verified[key+'_sha256']==sha(Path(release[key]).read_bytes())
    assert sha(Path(release['exact_patch_reconstruction']).read_bytes())==sha(Path('out/lil_B203_reference_v6037_RESEARCH_ONLY.nds').read_bytes())==release['candidate_sha256']
    manifest=read(release['manifest']);assert len(manifest['batches'])==591 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(final['records'])==22 and data['completed_editorial_families'][-1]['records']==final['records'] and Counter(r['editorial_decision'] for r in final['records'])=={'revise':9,'retain-wording':13}
    assert all(r.get('fresh_retained_wording_justification') for r in final['records'] if r['editorial_decision']=='retain-wording')
    assert all(r['current_native_extent']==r['integrated_native_extent'] and 'current_native_extent' in r['historical_source_prose_predecessor_fields'] for r in final['records'])
    rows=[r for f in data['completed_editorial_families'] for r in f['records']]
    assert len(rows)==len({historical_key(r) for r in rows})==6349 and data['goal_status']=='active' and not data['full_goal_complete']
    assert tuple(data[k] for k in ['records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(6352,3968,2381)
    scope=read(data['unfinished_editorial_scope_v6055']['path'])
    assert scope['next_Lil_B204_clean_review_pending']['reviewed_objects']==0 and 'speaker_names_and_role_labels_localization_review_v5708' in scope and scope['untranslated_Alexandria_alias_v5139b']['caller_and_display_fidelity_open']
    assert 'following_B43_source_item_term_observed_v6032' in scope
    registry=read('translations/release_stack.json');assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    expected={
        'work/clean.nds':'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d',
        'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        'out/all_routes_combined_v4701_candidate.nds':'dbfb4e413047e54e50dc771f48fe0e5457e40e60e0991111474185c41858052e',
        'out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds':'0c6e5a686b4fefb98a4d25ebb3c0e8c90ffa20e3f43240ca1629d8f6d40c85f2',
        'out/all_routes_combined_v5998_candidate.nds':'ae90b1e25f4c45d2a83e047cb97b14435eda9f2bd6825f5401f3800f2921993e'}
    for path,digest in expected.items():assert sha(Path(path).read_bytes())==digest,path
    text=f'''# Translation DS cumulative editorial checkpoint V6050

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
- Previous cumulative build: out/all_routes_combined_v5998_candidate.nds

The patch reconstructs the entire ROM byte for byte and equals the approved reference. All 591 batches, 114 accepted layers and 18 release checks are included. Only SC2 block 203 changes from V5998; every other file, component, name field, font, graphic and native code remains exact. All 76 atomic semantic rejection cases and 110 established regressions pass.

B203 adds 22 disjoint whole-exchange clean-Japanese reviews once: nine revisions and thirteen justified retentions. Exact source, predecessor, current encoded text, controls, reasons and native/gameplay evidence are retained. Current and integrated native extents match the final mapped commands; predecessor extents remain historical. Coverage is 6,349 completed contextual rereads and 6,352 source-prose reviews, with 3,968 integrated revisions and 2,381 justified retentions. Counted route coverage of 4,750 is a subset, not a whole-project denominator.

Speaker-name localization remains explicitly in scope across 207 entries. Man, Woman and Stranger remain included from V5891. Lil Argot, Mikhail Letzel versus full Mikhail Volk Letzel, and the Japanese-supported Mysterious Old Man label are retained contextually here without new name bytes or global name-review credit. Unknown nationality remains metadata. The medicinal-book explanation contains no invented title or medical profession.

The Japanese and revised English scene-content runs observe all 22 stored text objects and 40 commands, with 86 complete source-matched native holds. Six actual/paired sheets were viewed. The existing generated acquisition notice is whole-frame equal at frame 8350 and receives no extra stored-dialogue credit. These disclosed initialized-town ROM fixtures preserve ordinary inputs and unforced conditions/results; they do not establish natural event activation, original location, earned inventory, complete payment/item effects, full routes or hardware coverage. One speech duration differs by one frame, 23 start/return pairs shift, and 18 later advance-prompt samples differ. There are no interval RNG differences. Queried final native groups, actor and PRNG agree. No broad simulation-equivalence or causal claim is made.

Two fresh New Game/town checks match V5998 across 31 whole frames and five actor controls. Town uses an inherited five-ship test battery, not earned progression. The six selected views were reviewed. Full natural-route and hardware testing remain outside these targeted checks. All artifacts, earlier translations and failed producers are preserved.

{DETAILS}

{NEXT}

Final review: {fp}

Current handoff: docs/editorial_handoff_current.md

Verified handoff: {vp}
'''
    ROOT.mkdir(parents=True);(ROOT/'README.md').write_text(text,encoding='utf-8',newline='\n')
    evidence={str(p):sha(p.read_bytes()) for p in [vp,rp,fp,Path('docs/editorial_handoff_current.md'),Path(__file__),Path('scripts/lil_B203_completion_text_v6055.py')]}
    save(ROOT/'immutable_input_audit.json',dict(inputs=expected,all_protected_clean_canonical_main_rollback_and_parent_hashes_unchanged=True,every_generated_ROM_and_earlier_translation_preserved=True,ROMs_deleted=0,producer_sha256=sha(Path(__file__).read_bytes())))
    save(ROOT/'verification.json',dict(profile=release['profile'],candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],clean_input_sha256=release['clean_input_sha256'],canonical_base=release['canonical_base'],canonical_base_sha256=release['canonical_base_sha256'],manifest=release['manifest'],manifest_sha256=release['manifest_sha256'],changed_internal_files=release['file_changes'],changed_blocks={'/data/SC2.DK4':[203]},whole_clean_patch_and_reference_reconstruction_exact=True,all591_manifest_batches114_accepted18_checks_pass=True,completed=6349,source_prose=6352,revised=3968,retained=2381,unique_completed_historical_keys=6349,newly_completed_B203_objects=22,actual_speech_panels=22,actual_speech_observations=22,complete_native_holds=86,actual_menu_cases=0,generated_acquisition_observed_without_extra_dialogue_credit=True,measured_timing_RNG_state_and_later_RGB_differences_preserved=True,no_broad_simulation_equivalence_claim=True,all_prior_root_and_nested_history_preserved=True,main_V4701_preserved=True,full_goal_active=True,full_goal_complete=False,next_B204_clean_review_pending=True,retrospective207_names_and_role_label_queue_open=True,evidence=evidence,README_sha256=sha((ROOT/'README.md').read_bytes())))
    print('V6050 package verified:591 batches/114 accepted/18 checks,exact clean-input patch,6349 unique completed reviews. Full editorial/name-review goal active.')
