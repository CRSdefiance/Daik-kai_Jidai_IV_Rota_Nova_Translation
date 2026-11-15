"""Package and audit the verified cumulative checkpoint and exact clean patch."""
from pathlib import Path
from collections import Counter
from scripts.verify_village_wrap_v608 import read,save
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.lil_B188_completion_text_v5268 import DETAILS,NEXT
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('releases/all_routes_unified_v5263')
if __name__=='__main__':
    assert not ROOT.exists()
    vp=Path('work/analysis/editorial_handoff_verification_v5269/verified_handoff.json')
    rp=Path('work/analysis/lil_B188_release_v5264/registered_release_verification.json')
    fp=Path('translations/lil_B188_contextual_final_review_v1.json')
    verified,release,final=map(read,[vp,rp,fp]);ledger=Path('translations/editorial_review_current_v1.json');d=read(ledger)
    assert sha(ledger.read_bytes())==verified['ledger_sha256']
    for key in ['candidate','patch']:
        assert release[key+'_sha256']==verified[key+'_sha256']==sha(Path(release[key]).read_bytes())
    manifest=read(release['manifest'])
    assert len(manifest['batches'])==572 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(final['records'])==11 and d['completed_editorial_families'][-1]['records']==final['records']
    assert Counter(r['editorial_decision'] for r in final['records'])=={'revise':4,'retain-wording':7}
    rows=[r for family in d['completed_editorial_families'] for r in family['records']]
    assert len(rows)==len({historical_key(r) for r in rows})==6054
    assert d['goal_status']=='active' and not d['full_goal_complete']
    scope=read(d['unfinished_editorial_scope_v5268']['path'])
    assert scope['next_Lil_B189_clean_only_v5272']['objects']==17 and scope['next_Lil_B189_clean_only_v5272']['uncredited']
    assert scope['untranslated_Alexandria_alias_v5139b']['caller_and_display_fidelity_open']
    assert read('translations/release_stack.json')['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    text=f'''# Translation DS cumulative editorial checkpoint V5263

Experimental verified build. Full editorial goal active;promoted main V4701 preserved.

- ROM: {release['candidate']}
- ROM SHA-256: {release['candidate_sha256']}
- Clean-input patch: {release['patch']}
- Patch SHA-256: {release['patch_sha256']}
- Required clean Japanese input SHA-256: {release['clean_input_sha256']}
- Registered profile: {release['profile']}
- Immutable construction baseline: {release['canonical_base']}
- Baseline SHA-256: {release['canonical_base_sha256']}
- Complete batch/check manifest: {release['manifest']}
- Previous cumulative build: out/all_routes_combined_v5219_candidate.nds

The patch reconstructs the whole ROM byte for byte from the exact clean Japanese input. The ROM equals the reviewed one-block reference. All572 manuscript batches,114 accepted layers and18 release checks remain included.

{DETAILS}
{NEXT}

Coverage is6,054 completed contextual rereads:3,829 revisions and2,225 justified retentions. Source/prose coverage is6,057,including three incomplete shared records. Counted route coverage4,455 is a subset,not a full-project denominator. B189's17 clean-only glosses have zero completion credit.

For user smoke testing,check New Game,an existing town save and ordinary story transitions. Observe the Daimyo/Guildmaster glass-collection scene if naturally encountered. The two B22 content tests provide focused scene/display evidence;they do not prove natural event188 eligibility,a full route or hardware behavior. All prior ROMs,translations,proofs and diagnostics remain preserved. No promotion or pruning occurred.

Final review: {fp}

Current handoff: docs/editorial_handoff_current.md

Verified handoff: {vp}
'''
    ROOT.mkdir(parents=True);(ROOT/'README.md').write_text(text,encoding='utf-8',newline='\n')
    evidence={str(p):sha(p.read_bytes()) for p in [vp,rp,fp,Path('docs/editorial_handoff_current.md')]}
    save(ROOT/'verification.json',dict(profile=release['profile'],candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],clean_input_sha256=release['clean_input_sha256'],
        canonical_base=release['canonical_base'],canonical_base_sha256=release['canonical_base_sha256'],
        manifest=release['manifest'],manifest_sha256=release['manifest_sha256'],changed_internal_files=release['file_changes'],changed_blocks={'/data/SC2.DK4':[188]},
        whole_clean_patch_and_reference_reconstruction_exact=True,all572_manifest_batches114_accepted18_checks_pass=True,
        completed=6054,source_prose=6057,revised=3829,retained=2225,unique_completed_historical_keys=6054,
        all_prior_root_and_nested_history_preserved=True,main_V4701_preserved=True,full_goal_active=True,full_goal_complete=False,
        next17_B189_clean_only_objects_uncredited=True,untranslated_Alexandria_alias_open=True,evidence=evidence,producer_sha256=sha(Path(__file__).read_bytes())))
    for p,h in evidence.items():assert sha(Path(p).read_bytes())==h
    print('V5263 package audited:6054 unique completed identities;4 revisions/7 retentions counted once. Next17 clean-only objects uncredited;full goal active.')
