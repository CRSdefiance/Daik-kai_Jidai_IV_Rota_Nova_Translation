"""Package the verified registered B199 cumulative build without promotion or pruning."""
from collections import Counter
from pathlib import Path
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.lil_B199_completion_text_v5821 import DETAILS,NEXT
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('releases/all_routes_unified_v5816')
if __name__=='__main__':
    assert not ROOT.exists()
    vp=Path('work/analysis/editorial_handoff_verification_v5822/verified_handoff.json')
    rp=Path('work/analysis/lil_B199_release_v5817/registered_release_verification.json')
    fp=Path('translations/lil_B199_contextual_final_review_v1.json')
    verified,release,final=map(read,[vp,rp,fp]);ledger=Path('translations/editorial_review_current_v1.json');data=read(ledger)
    assert sha(ledger.read_bytes())==verified['ledger_sha256']
    for key in ['candidate','patch']:assert release[key+'_sha256']==verified[key+'_sha256']==sha(Path(release[key]).read_bytes())
    assert sha(Path(release['exact_patch_reconstruction']).read_bytes())==release['candidate_sha256']
    manifest=read(release['manifest']);assert len(manifest['batches'])==585 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(final['records'])==31 and data['completed_editorial_families'][-1]['records']==final['records']
    assert Counter(r['editorial_decision'] for r in final['records'])=={'revise':11,'retain-wording':20}
    assert all(r.get('fresh_retained_wording_justification') for r in final['records'] if r['editorial_decision']=='retain-wording')
    rows=[r for family in data['completed_editorial_families'] for r in family['records']]
    assert len(rows)==len({historical_key(r) for r in rows})==6263 and data['goal_status']=='active' and not data['full_goal_complete']
    assert tuple(data[k] for k in ['records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(6266,3928,2335)
    scope=read(data['unfinished_editorial_scope_v5821']['path'])
    assert scope['next_Lil_B200_clean_review_pending']['reviewed_objects']==0
    assert 'speaker_names_and_role_labels_localization_review_v5708' in scope
    assert scope['untranslated_Alexandria_alias_v5139b']['caller_and_display_fidelity_open']
    assert read('translations/release_stack.json')['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    expected={
        'work/clean.nds':'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d',
        'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        'out/all_routes_combined_v4701_candidate.nds':'dbfb4e413047e54e50dc771f48fe0e5457e40e60e0991111474185c41858052e',
        'out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds':'0c6e5a686b4fefb98a4d25ebb3c0e8c90ffa20e3f43240ca1629d8f6d40c85f2',
        'out/all_routes_combined_v5692_candidate.nds':'571568dc371124f5b926e7022512a3f488b46e3661f069bc59a395c223d4c47d',
        'out/all_routes_combined_v5756_candidate.nds':'16024cbdced2dad8e7390514f431d1edcfb9ecaedba6bc7edea459056571f3c5'}
    for path,digest in expected.items():assert sha(Path(path).read_bytes())==digest,path
    assert sha(Path('out/lil_B199_reference_v5800_RESEARCH_ONLY.nds').read_bytes())==release['candidate_sha256']
    text=f'''# Translation DS cumulative editorial checkpoint V5816

Experimental cumulative build for testing. Main V4701 remains promoted. The full editorial goal is active.

- ROM: {release['candidate']}
- ROM SHA-256: {release['candidate_sha256']}
- Clean-input patch: {release['patch']}
- Patch SHA-256: {release['patch_sha256']}
- Required clean Japanese input SHA-256: {release['clean_input_sha256']}
- Registered profile: {release['profile']}
- Immutable construction baseline: {release['canonical_base']}
- Baseline SHA-256: {release['canonical_base_sha256']}
- Full layer/check manifest: {release['manifest']}
- Previous cumulative build: out/all_routes_combined_v5756_candidate.nds

The patch reconstructs the entire ROM byte for byte from the exact clean Japanese input. The result equals the reviewed reference. All585 manifest batches,114 accepted layers and18 passing release checks are included. Only /data/SC2.DK4 block199 changes from V5756;every other file,story,font,graphic,ARM9/ARM7 component and123040 staged bytes remain exact. The batch passes101 semantic atomic negatives and110 established regressions.

Coverage is6,263 completed contextual rereads:3,928 revisions and2,335 justified retentions. Source/prose coverage is6,266,including three incomplete shared records. Counted route coverage4,664 is a subset,not a whole-project denominator. B199 adds31 disjoint objects once:11 revisions/20 individually justified retentions. B200 clean-source review and the retrospective207-name/role-label queue remain open. The screenshot labels Man in a Couple/Woman in a Couple have draft Man/Woman replacements supported by five representative whole source exchanges;their target native/display/release validation is still pending. No global speaker-name completion is claimed.

Focused source/English content fixtures observed all31 speeches across120 complete matching native holds and182 matching sampled nontext regions. They preserve source-controlled portraits,names,pictures,controls and end results. Six speech durations differ,shifting34 start/return pairs;source/English return10776/10778. Six later screenshot differences are bounded to the advance-prompt blink. Final PRNG seeds differ;the complete timing cause is untraced. Native getters agree for the measured company/fleet/ship/actor/town/item/goods/task/calendar scope. No broad future-simulation or full-RAM equivalence is claimed. These initialized-Amsterdam B22 fixtures do not establish natural event199 activation,its original location,complete item/effect semantics,full routes or hardware verification. Following B120 adds no editorial credit.

Two fresh registered New Game/town cold boots match V5756 across31 complete sampled screens/five actor checks. Six selected current frames were viewed. The town run uses an inherited five-ship test battery;it is not earned progression. Original and disposable donor files remain exact. Content runs from earlier checkpoints were reused;only the two startup runs are new in this goal turn. Every earlier ROM,translation,draft,proof and failure is preserved.

{DETAILS}

{NEXT}

Final review: {fp}

Current handoff: docs/editorial_handoff_current.md

Verified handoff: {vp}
'''
    ROOT.mkdir(parents=True);(ROOT/'README.md').write_text(text,encoding='utf-8',newline='\n')
    evidence={str(p):sha(p.read_bytes()) for p in [vp,rp,fp,Path('docs/editorial_handoff_current.md'),Path('scripts/lil_B199_completion_text_v5821.py'),Path(__file__)]}
    save(ROOT/'immutable_input_audit.json',dict(inputs=expected,all_six_clean_canonical_main_rollback_and_predecessor_hashes_unchanged=True,
        every_generated_ROM_and_earlier_translation_preserved=True,ROMs_deleted=0,producer_sha256=sha(Path(__file__).read_bytes())))
    save(ROOT/'verification.json',dict(profile=release['profile'],candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],clean_input_sha256=release['clean_input_sha256'],
        canonical_base=release['canonical_base'],canonical_base_sha256=release['canonical_base_sha256'],
        manifest=release['manifest'],manifest_sha256=release['manifest_sha256'],changed_internal_files=release['file_changes'],changed_blocks={'/data/SC2.DK4':[199]},
        whole_clean_patch_and_reference_reconstruction_exact=True,all585_manifest_batches114_accepted18_checks_pass=True,
        completed=6263,source_prose=6266,revised=3928,retained=2335,unique_completed_historical_keys=6263,
        newly_completed_B199_objects=31,actual_speech_panels=31,offline_only_speeches=0,complete_native_holds=120,
        speech_duration_changes=6,shifted_start_return_pairs=34,later_prompt_blink_differences=6,final_PRNG_seeds_differ=True,
        complete_timing_cause_untraced=True,no_broad_simulation_equivalence_claim=True,all_prior_root_and_nested_history_preserved=True,main_V4701_preserved=True,
        full_goal_active=True,full_goal_complete=False,next_B200_clean_review_pending=True,
        retrospective_names_and_role_label_queue_open=True,evidence=evidence,README_sha256=sha((ROOT/'README.md').read_bytes())))
    print('V5816 package verified:585 batches/114 accepted/18 checks,exact clean-input patch,6263 unique completed reviews. Full editorial/name-review goal active.')
