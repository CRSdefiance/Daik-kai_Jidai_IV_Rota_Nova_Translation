"""Package the registered cumulative B200 checkpoint while preserving every earlier artifact."""
from collections import Counter
from pathlib import Path
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.lil_B200_completion_text_v5877 import DETAILS,NEXT
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('releases/all_routes_unified_v5872')
if __name__=='__main__':
    assert not ROOT.exists();vp=Path('work/analysis/editorial_handoff_verification_v5878/verified_handoff.json')
    rp=Path('work/analysis/lil_B200_release_v5873/registered_release_verification.json');fp=Path('translations/lil_B200_contextual_final_review_v1.json')
    verified,release,final=map(read,[vp,rp,fp]);ledger=Path('translations/editorial_review_current_v1.json');data=read(ledger)
    assert sha(ledger.read_bytes())==verified['ledger_sha256']
    for key in ['candidate','patch']:assert release[key+'_sha256']==verified[key+'_sha256']==sha(Path(release[key]).read_bytes())
    assert sha(Path(release['exact_patch_reconstruction']).read_bytes())==release['candidate_sha256']
    assert sha(Path('out/lil_B200_reference_v5853_RESEARCH_ONLY.nds').read_bytes())==release['candidate_sha256']
    manifest=read(release['manifest']);assert len(manifest['batches'])==586 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(final['records'])==19 and data['completed_editorial_families'][-1]['records']==final['records']
    assert Counter(r['editorial_decision'] for r in final['records'])=={'revise':13,'retain-wording':6}
    assert all(r.get('fresh_retained_wording_justification') for r in final['records'] if r['editorial_decision']=='retain-wording')
    rows=[r for family in data['completed_editorial_families'] for r in family['records']]
    assert len(rows)==len({historical_key(r) for r in rows})==6282 and data['goal_status']=='active' and not data['full_goal_complete']
    assert tuple(data[k] for k in ['records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(6285,3941,2341)
    scope=read(data['unfinished_editorial_scope_v5877']['path'])
    assert scope['next_Lil_B201_clean_review_pending']['reviewed_objects']==0 and scope['next_three_generic_speaker_labels_target_validation']['actor_IDs']==[164,165,172]
    assert 'speaker_names_and_role_labels_localization_review_v5708' in scope and scope['untranslated_Alexandria_alias_v5139b']['caller_and_display_fidelity_open']
    registry=read('translations/release_stack.json');assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    expected={
        'work/clean.nds':'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d',
        'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        'out/all_routes_combined_v4701_candidate.nds':'dbfb4e413047e54e50dc771f48fe0e5457e40e60e0991111474185c41858052e',
        'out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds':'0c6e5a686b4fefb98a4d25ebb3c0e8c90ffa20e3f43240ca1629d8f6d40c85f2',
        'out/all_routes_combined_v5816_candidate.nds':'da7425629ca07c31a1b17bcb3032f2fbe09eb38406209d4bda522e1790068111'}
    for path,digest in expected.items():assert sha(Path(path).read_bytes())==digest,path
    text=f'''# Translation DS cumulative editorial checkpoint V5872

Experimental cumulative build for testing. Main V4701 remains promoted. The full editorial goal is active.

- ROM: {release['candidate']}
- ROM SHA-256: {release['candidate_sha256']}
- Clean-input patch: {release['patch']}
- Patch SHA-256: {release['patch_sha256']}
- Required clean Japanese input SHA-256: {release['clean_input_sha256']}
- Registered profile: {release['profile']}
- Immutable construction baseline: {release['canonical_base']}
- Baseline SHA-256: {release['canonical_base_sha256']}
- Full manifest: {release['manifest']}
- Previous cumulative build: out/all_routes_combined_v5816_candidate.nds

The clean-input patch reconstructs the entire ROM byte for byte. The result equals the approved reference. All586 manifest batches,114 accepted layers and18 passing release checks are included. Only /data/SC2.DK4 block200 changes from V5816;every other file,story,font,graphic,ARM9/ARM7 component and123040 staged bytes remain exact.110 semantic atomic negatives and110 established regressions pass.

B200 adds19 disjoint clean-Japanese whole-exchange reviews once:13 revisions/six individually justified retentions. Preserve the rescue causative,explicit doctor denial,polite gift refusal/insistence/acceptance and exact Charm+1 notice. The source object stays unnamed in speech. Courtesy/request phrase wrapping is improved without changing any words or native display limits. All19 complete native planes/152 alignments,18 consumer/28 formatter negatives and76 final-stored macro cases pass.

Coverage is6,282 completed contextual rereads:3,941 revisions and2,341 justified retentions. Source/prose coverage is6,285,including three incomplete shared records. Counted route coverage4,683 is a subset,not a whole-project denominator. Next are target validation of Man/Woman/Stranger and the full207-entry name queue,followed by fresh B201 source review. Current Collapsed Person and couple labels remain unchanged in this ROM. No global name completion or duplicate shared-dialogue credit is claimed.

Focused Japanese/English content fixtures observed all19 speeches across73 complete native holds,with source-matched upper/portrait/name/picture regions. They use ordinary input and unforced conditions,roster,funds,RNG and results. They do not establish natural event200 activation,original location,full-route completion,hardware or complete item/stat-effect semantics. Eight speech durations differ,shifting19 start/return pairs;source/English return7676/7677.172 of182 sampled nontext regions agree. Six later differences are prompt blinking;ten subsequent sailing samples show a foreground cloud in a different position. Final PRNG states differ. Native queried state groups agree;the complete timing/cloud cause and broad future simulation equivalence are not claimed. All unmodified source and English evidence is preserved.

Two fresh registered New Game/town cold boots match V5816 across31 complete sampled screens/five actor checks. Six selected frames were viewed. The town run uses an inherited five-ship test battery,not earned progression. Source and disposable donor files remain exact. Earlier Japanese/English content runs are reused;the two startup runs alone are new this goal turn. Every earlier ROM,translation,draft,proof and failed producer remains preserved.

{DETAILS}

{NEXT}

Final review: {fp}

Current handoff: docs/editorial_handoff_current.md

Verified handoff: {vp}
'''
    ROOT.mkdir(parents=True);(ROOT/'README.md').write_text(text,encoding='utf-8',newline='\n')
    evidence={str(p):sha(p.read_bytes()) for p in [vp,rp,fp,Path('docs/editorial_handoff_current.md'),Path('scripts/lil_B200_completion_text_v5877.py'),Path(__file__)]}
    save(ROOT/'immutable_input_audit.json',dict(inputs=expected,all_protected_clean_canonical_main_rollback_and_parent_hashes_unchanged=True,
        every_generated_ROM_and_earlier_translation_preserved=True,ROMs_deleted=0,producer_sha256=sha(Path(__file__).read_bytes())))
    save(ROOT/'verification.json',dict(profile=release['profile'],candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],clean_input_sha256=release['clean_input_sha256'],
        canonical_base=release['canonical_base'],canonical_base_sha256=release['canonical_base_sha256'],manifest=release['manifest'],manifest_sha256=release['manifest_sha256'],
        changed_internal_files=release['file_changes'],changed_blocks={'/data/SC2.DK4':[200]},whole_clean_patch_and_reference_reconstruction_exact=True,
        all586_manifest_batches114_accepted18_checks_pass=True,completed=6282,source_prose=6285,revised=3941,retained=2341,unique_completed_historical_keys=6282,
        newly_completed_B200_objects=19,actual_speech_panels=19,offline_only_speeches=0,complete_native_holds=73,
        speech_duration_changes=8,shifted_start_return_pairs=19,later_prompt_blink_differences=6,later_sailing_cloud_differences=10,final_PRNG_seeds_differ=True,
        complete_timing_cloud_cause_untraced=True,no_broad_simulation_equivalence_claim=True,all_prior_root_and_nested_history_preserved=True,main_V4701_preserved=True,
        full_goal_active=True,full_goal_complete=False,next_three_generic_label_target_validation=True,next_B201_clean_review_pending=True,
        retrospective207_names_and_role_label_queue_open=True,evidence=evidence,README_sha256=sha((ROOT/'README.md').read_bytes())))
    print('V5872 package verified:586 batches/114 accepted/18 checks,exact clean-input patch,6282 unique completed reviews. Full editorial/name-review goal active.')
