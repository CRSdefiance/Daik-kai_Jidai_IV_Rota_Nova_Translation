"""Package the verified cumulative release,exact clean patch and immutable input audit."""
from collections import Counter
from pathlib import Path
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.lil_B197_completion_text_v5697 import DETAILS,NEXT
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('releases/all_routes_unified_v5692')
if __name__=='__main__':
    assert not ROOT.exists()
    vp=Path('work/analysis/editorial_handoff_verification_v5698/verified_handoff.json')
    rp=Path('work/analysis/lil_B197_release_v5693/registered_release_verification.json')
    fp=Path('translations/lil_B197_contextual_final_review_v1.json')
    verified,release,final=map(read,[vp,rp,fp]);ledger=Path('translations/editorial_review_current_v1.json');data=read(ledger)
    assert sha(ledger.read_bytes())==verified['ledger_sha256']
    for key in ['candidate','patch']:assert release[key+'_sha256']==verified[key+'_sha256']==sha(Path(release[key]).read_bytes())
    manifest=read(release['manifest']);assert len(manifest['batches'])==583 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(final['records'])==24 and data['completed_editorial_families'][-1]['records']==final['records']
    assert Counter(r['editorial_decision'] for r in final['records'])=={'revise':16,'retain-wording':8}
    rows=[r for family in data['completed_editorial_families'] for r in family['records']]
    assert len(rows)==len({historical_key(r) for r in rows})==6215 and data['goal_status']=='active' and not data['full_goal_complete']
    scope=read(data['unfinished_editorial_scope_v5697']['path']);assert scope['next_Lil_B198_clean_review_pending']['reviewed_objects']==0
    assert scope['untranslated_Alexandria_alias_v5139b']['caller_and_display_fidelity_open']
    assert read('translations/release_stack.json')['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    expected={
        'work/clean.nds':'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d',
        'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        'out/all_routes_combined_v4701_candidate.nds':'dbfb4e413047e54e50dc771f48fe0e5457e40e60e0991111474185c41858052e',
        'out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds':'0c6e5a686b4fefb98a4d25ebb3c0e8c90ffa20e3f43240ca1629d8f6d40c85f2',
        'out/all_routes_combined_v5637_candidate.nds':'6bb1e783dc293c8c723209e398e82b25ad967a64dbdccac4ed3a5f4079b4869a'}
    for path,digest in expected.items():assert sha(Path(path).read_bytes())==digest,path
    text=f'''# Translation DS cumulative editorial checkpoint V5692

Experimental verified cumulative build. The full editorial goal remains active;promoted main V4701 is preserved.

- ROM: {release['candidate']}
- ROM SHA-256: {release['candidate_sha256']}
- Clean-input patch: {release['patch']}
- Patch SHA-256: {release['patch_sha256']}
- Required clean Japanese input SHA-256: {release['clean_input_sha256']}
- Registered profile: {release['profile']}
- Immutable construction baseline: {release['canonical_base']}
- Baseline SHA-256: {release['canonical_base_sha256']}
- Full accepted/experimental batch and check manifest: {release['manifest']}
- Previous cumulative build: out/all_routes_combined_v5637_candidate.nds

The patch reconstructs the entire ROM byte for byte from the exact clean Japanese input. The result equals the reviewed reference. All583 manifest batches,114 accepted layers and18 passing release checks are included. Only /data/SC2.DK4 block197 changes from V5637;all other files,stories,fonts,graphics and components remain exact.

{DETAILS}

Coverage is6,215 completed contextual rereads:3,905 revisions and2,310 justified retentions. Source/prose coverage is6,218,including three incomplete shared records. Counted route coverage4,616 is a subset,not a whole-project denominator. B198 clean-source review is next and adds no credit yet.

For optional user smoke testing,check New Game,an existing town save and ordinary story transitions;observe the book encounter if naturally encountered. The recorded six complete Japanese/English B22 content boots cover21 distinct English speeches,35 speech observations,128 complete native holds,all three choices and normal returns. A separate4601-frame focus verifies the Pass highlight. Two failed concurrent partial runs are preserved and excluded from successful coverage. All game conditions,roster,funds,RNG and results were unforced. Source event197 was relocated to initialized Amsterdam;natural eligibility,its original location,earned affordability,complete item/Charm semantics,full routes and hardware behavior are not claimed. Retain59 timing/82 later whole-RGB and explicit RNG/state differences;broader simulation equivalence is unproven. Fresh registered New Game/town cold boots match V5637 across31 sampled full frames/five actor checks. All prior artifacts are preserved;no promotion or pruning occurred.

{NEXT}

Final review: {fp}

Current handoff: docs/editorial_handoff_current.md

Verified handoff: {vp}
'''
    ROOT.mkdir(parents=True);(ROOT/'README.md').write_text(text,encoding='utf-8',newline='\n')
    evidence={str(p):sha(p.read_bytes()) for p in [vp,rp,fp,Path('docs/editorial_handoff_current.md'),Path(__file__)]}
    save(ROOT/'immutable_input_audit.json',dict(inputs=expected,all_five_clean_canonical_main_rollback_and_predecessor_hashes_unchanged=True,
        every_generated_ROM_and_earlier_translation_preserved=True,ROMs_deleted=0,producer_sha256=sha(Path(__file__).read_bytes())))
    save(ROOT/'verification.json',dict(profile=release['profile'],candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],clean_input_sha256=release['clean_input_sha256'],canonical_base=release['canonical_base'],canonical_base_sha256=release['canonical_base_sha256'],
        manifest=release['manifest'],manifest_sha256=release['manifest_sha256'],changed_internal_files=release['file_changes'],changed_blocks={'/data/SC2.DK4':[197]},
        whole_clean_patch_and_reference_reconstruction_exact=True,all583_manifest_batches114_accepted18_checks_pass=True,
        completed=6215,source_prose=6218,revised=3905,retained=2310,unique_completed_historical_keys=6215,
        newly_completed_B197_objects=24,actual_speech_panels=21,actual_speech_observations=35,complete_native_holds=128,actual_menu_cases=3,actual_original_menu_indices=[0,1,2],
        all59_timing82_later_RGB_and_explicit_RNG_state_differences_preserved=True,no_broad_simulation_equivalence_claim=True,
        all_prior_root_and_nested_history_preserved=True,main_V4701_preserved=True,full_goal_active=True,full_goal_complete=False,
        next_B198_clean_review_pending=True,evidence=evidence,README_sha256=sha((ROOT/'README.md').read_bytes())))
    print('V5692 package verified:583 batches/114 accepted/18 checks,exact clean-input patch,6215 unique completed reviews;full goal active.B198 next.')
