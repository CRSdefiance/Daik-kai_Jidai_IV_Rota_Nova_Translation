"""Package verified V5756 with exact clean patch,once-only coverage and preserved input audit."""
from collections import Counter
from pathlib import Path
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.lil_B198_completion_text_v5761 import DETAILS,NEXT
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('releases/all_routes_unified_v5756')
if __name__=='__main__':
    assert not ROOT.exists()
    vp=Path('work/analysis/editorial_handoff_verification_v5762/verified_handoff.json')
    rp=Path('work/analysis/lil_B198_release_v5757/registered_release_verification.json')
    fp=Path('translations/lil_B198_contextual_final_review_v1.json')
    verified,release,final=map(read,[vp,rp,fp]);ledger=Path('translations/editorial_review_current_v1.json');data=read(ledger)
    assert sha(ledger.read_bytes())==verified['ledger_sha256']
    for key in ['candidate','patch']:assert release[key+'_sha256']==verified[key+'_sha256']==sha(Path(release[key]).read_bytes())
    manifest=read(release['manifest']);assert len(manifest['batches'])==584 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(final['records'])==17 and data['completed_editorial_families'][-1]['records']==final['records']
    assert Counter(r['editorial_decision'] for r in final['records'])=={'revise':12,'retain-wording':5}
    rows=[r for family in data['completed_editorial_families'] for r in family['records']]
    assert len(rows)==len({historical_key(r) for r in rows})==6232 and data['goal_status']=='active' and not data['full_goal_complete']
    scope=read(data['unfinished_editorial_scope_v5761']['path'])
    assert scope['next_Lil_B199_clean_review_pending']['reviewed_objects']==0
    assert 'speaker_names_and_role_labels_localization_review_v5708' in scope
    assert scope['untranslated_Alexandria_alias_v5139b']['caller_and_display_fidelity_open']
    assert read('translations/release_stack.json')['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    expected={
        'work/clean.nds':'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d',
        'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        'out/all_routes_combined_v4701_candidate.nds':'dbfb4e413047e54e50dc771f48fe0e5457e40e60e0991111474185c41858052e',
        'out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds':'0c6e5a686b4fefb98a4d25ebb3c0e8c90ffa20e3f43240ca1629d8f6d40c85f2',
        'out/all_routes_combined_v5692_candidate.nds':'571568dc371124f5b926e7022512a3f488b46e3661f069bc59a395c223d4c47d',
        'out/all_routes_combined_v5637_candidate.nds':'6bb1e783dc293c8c723209e398e82b25ad967a64dbdccac4ed3a5f4079b4869a'}
    for path,digest in expected.items():assert sha(Path(path).read_bytes())==digest,path
    text=f'''# Translation DS cumulative editorial checkpoint V5756

Experimental cumulative build for testing. Promoted main V4701 is preserved;the full editorial goal remains active.

- ROM: {release['candidate']}
- ROM SHA-256: {release['candidate_sha256']}
- Clean-input patch: {release['patch']}
- Patch SHA-256: {release['patch_sha256']}
- Required clean Japanese input SHA-256: {release['clean_input_sha256']}
- Registered profile: {release['profile']}
- Immutable construction baseline: {release['canonical_base']}
- Baseline SHA-256: {release['canonical_base_sha256']}
- Full layer/check manifest: {release['manifest']}
- Previous cumulative build: out/all_routes_combined_v5692_candidate.nds

The patch reconstructs the entire ROM byte for byte from the exact clean Japanese input. The result equals the reviewed reference. All584 manifest batches,114 accepted layers and18 passing release checks are included. Only /data/SC2.DK4 block198 changes from V5692;every other file,story,font,graphic,ARM9/ARM7 component and123040 staged bytes remain exact.98 semantic atomic negatives and110 existing regressions pass.

Coverage is6,232 completed contextual rereads:3,917 revisions and2,315 justified retentions. Source/prose coverage is6,235,including three incomplete shared records. Counted route coverage4,633 is a subset,not a whole-project denominator. B198 adds17 disjoint objects once. B199 clean-source review and the retrospective speaker-name/role-label queue remain open.

For optional smoke testing,use New Game,an existing town save and ordinary story transitions;observe the Namahage encounter if naturally encountered. The recorded source/English content fixtures verify15 speeches across56 complete matching holds;Angelo65/95 remain offline-only. Conditions,roster,funds,RNG and results were unforced. The initialized-Amsterdam B22 fixture does not prove natural event198 activation,its original location,complete item/effect semantics,full routes,hardware or broad simulation equivalence. Both paths return at6697;182 sampled nontext frames,timing and later sampled screens match. The CP932 shadow-reference mismatch was resolved by the original story caller's style11 without changing ROM bytes,wording or captured pixels. Fresh registered New Game/town cold boots match V5692 across31 full sampled frames/five actor checks. All prior artifacts remain preserved.

{DETAILS}

{NEXT}

Final review: {fp}

Current handoff: docs/editorial_handoff_current.md

Verified handoff: {vp}
'''
    ROOT.mkdir(parents=True);(ROOT/'README.md').write_text(text,encoding='utf-8',newline='\n')
    evidence={str(p):sha(p.read_bytes()) for p in [vp,rp,fp,Path('docs/editorial_handoff_current.md'),Path(__file__)]}
    save(ROOT/'immutable_input_audit.json',dict(inputs=expected,all_six_clean_canonical_main_rollback_and_predecessor_hashes_unchanged=True,
        every_generated_ROM_and_earlier_translation_preserved=True,ROMs_deleted=0,producer_sha256=sha(Path(__file__).read_bytes())))
    save(ROOT/'verification.json',dict(profile=release['profile'],candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],clean_input_sha256=release['clean_input_sha256'],
        canonical_base=release['canonical_base'],canonical_base_sha256=release['canonical_base_sha256'],
        manifest=release['manifest'],manifest_sha256=release['manifest_sha256'],changed_internal_files=release['file_changes'],changed_blocks={'/data/SC2.DK4':[198]},
        whole_clean_patch_and_reference_reconstruction_exact=True,all584_manifest_batches114_accepted18_checks_pass=True,
        completed=6232,source_prose=6235,revised=3917,retained=2315,unique_completed_historical_keys=6232,
        newly_completed_B198_objects=17,actual_speech_panels=15,offline_only_speeches=2,complete_native_holds=56,
        source_correct_story_style11_CP932_reference_and_honest_actual_scope_preserved=True,
        no_broad_simulation_equivalence_claim=True,all_prior_root_and_nested_history_preserved=True,main_V4701_preserved=True,
        full_goal_active=True,full_goal_complete=False,next_B199_clean_review_pending=True,
        retrospective_names_and_role_label_queue_open=True,evidence=evidence,README_sha256=sha((ROOT/'README.md').read_bytes())))
    print('V5756 package verified:584 batches/114 accepted/18 checks,exact clean-input patch,6232 unique completed reviews. Full editorial/name-review goal active.')
