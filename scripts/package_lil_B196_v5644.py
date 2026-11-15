"""Package the registered cumulative build and its exact clean-input patch."""
from collections import Counter
from pathlib import Path
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.lil_B196_completion_text_v5642 import DETAILS,NEXT
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('releases/all_routes_unified_v5637')
if __name__=='__main__':
    assert not ROOT.exists()
    vp=Path('work/analysis/editorial_handoff_verification_v5643/verified_handoff.json')
    rp=Path('work/analysis/lil_B196_release_v5638/registered_release_verification.json')
    fp=Path('translations/lil_B196_contextual_final_review_v1.json')
    verified,release,final=map(read,[vp,rp,fp]);ledger=Path('translations/editorial_review_current_v1.json');d=read(ledger)
    assert sha(ledger.read_bytes())==verified['ledger_sha256']
    for key in ['candidate','patch']:assert release[key+'_sha256']==verified[key+'_sha256']==sha(Path(release[key]).read_bytes())
    manifest=read(release['manifest']);assert len(manifest['batches'])==581 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(final['records'])==36 and d['completed_editorial_families'][-1]['records']==final['records']
    assert Counter(r['editorial_decision'] for r in final['records'])=={'revise':15,'retain-wording':21}
    rows=[r for family in d['completed_editorial_families'] for r in family['records']]
    assert len(rows)==len({historical_key(r) for r in rows})==6191 and d['goal_status']=='active' and not d['full_goal_complete']
    scope=read(d['unfinished_editorial_scope_v5642']['path'])
    assert scope['next_Lil_B197_clean_review_pending']['reviewed_objects']==0
    assert scope['untranslated_Alexandria_alias_v5139b']['caller_and_display_fidelity_open']
    assert read('translations/release_stack.json')['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    text=f'''# Translation DS cumulative editorial checkpoint V5637

Experimental verified cumulative build. Full editorial goal active;promoted main V4701 preserved.

- ROM: {release['candidate']}
- ROM SHA-256: {release['candidate_sha256']}
- Clean-input patch: {release['patch']}
- Patch SHA-256: {release['patch_sha256']}
- Required clean Japanese input SHA-256: {release['clean_input_sha256']}
- Registered profile: {release['profile']}
- Immutable construction baseline: {release['canonical_base']}
- Baseline SHA-256: {release['canonical_base_sha256']}
- Full batch/check manifest: {release['manifest']}
- Previous cumulative build: out/all_routes_combined_v5580_candidate.nds

The patch reconstructs the complete ROM byte for byte from the exact clean Japanese input. The result equals the reviewed one-block reference. All581 manuscript batches,114 accepted layers and18 passing release checks are included. Only /data/SC2.DK4 block196 changes from V5580. Every other file,story,font,graphic and component stays exact.

{DETAILS}

Coverage is6,191 completed contextual rereads:3,889 revisions and2,302 justified retentions. Source/prose coverage is6,194,including three incomplete shared records. Counted route coverage4,592 is a subset,not a full-project denominator. B197 clean-source review is next and currently adds no credit.

For user smoke testing,check New Game,an existing town save and ordinary story transitions. Observe the bargaining scene if naturally encountered. The six paired B22 content boots cover first Buy,all Pass and deepest Buy with original conditions and ordinary input. They provide13 distinct speech panels and13 menu observations. Eleven other speeches remain native offline coverage. Actual Buy outcomes were218/1588;Pass was selected at all six menus. Do not infer individually played Buy outcomes at the four middle offers,natural event196 eligibility,earned affordability,complete item/Charm semantics,a full route or hardware behavior. Two fresh cumulative startup boots match V5580 across31 sampled full frames/five actor checks. All prior ROMs,translations,proofs and failures are preserved. No promotion or pruning occurred.

{NEXT}

Final review: {fp}

Current handoff: docs/editorial_handoff_current.md

Verified handoff: {vp}
'''
    ROOT.mkdir(parents=True);(ROOT/'README.md').write_text(text,encoding='utf-8',newline='\n')
    evidence={str(p):sha(p.read_bytes()) for p in [vp,rp,fp,Path('docs/editorial_handoff_current.md'),Path(__file__)]}
    save(ROOT/'verification.json',dict(profile=release['profile'],candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],clean_input_sha256=release['clean_input_sha256'],canonical_base=release['canonical_base'],canonical_base_sha256=release['canonical_base_sha256'],
        manifest=release['manifest'],manifest_sha256=release['manifest_sha256'],changed_internal_files=release['file_changes'],changed_blocks={'/data/SC2.DK4':[196]},
        whole_clean_patch_and_reference_reconstruction_exact=True,all581_manifest_batches114_accepted18_checks_pass=True,
        completed=6191,source_prose=6194,revised=3889,retained=2302,unique_completed_historical_keys=6191,
        newly_completed_B196_objects=36,actual_speech_panels=13,offline_only_speeches=11,actual_menu_cases=13,
        actual_Buy_menu_offsets=[218,1588],actual_Pass_menu_offsets=[218,582,832,1156,1370,1588],
        all_prior_root_and_nested_history_preserved=True,main_V4701_preserved=True,full_goal_active=True,full_goal_complete=False,
        next_B197_clean_review_pending=True,evidence=evidence,README_sha256=sha((ROOT/'README.md').read_bytes())))
    print('V5637 package verified:581 batches/114 accepted/18 checks,exact clean-input patch,6191 unique completed reviews;full goal active.B197 next.')
