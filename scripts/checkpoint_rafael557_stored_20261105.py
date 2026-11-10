"""Record complete offline storage checks without granting pending gameplay/release credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael557_stored_checkpoint_v1_20261105')
PROSE=Path('translations/rafael_B141_B160_contextual_review_v3.json')
DOC=Path('translations/rafael_B141_B160_formatting_manuscript_v3.json')
PREF=Path('translations/rafael_B141_B160_visual_preferences_v10.json')
INPUT=Path('work/analysis/Rafael557_storage_inputs_v1_20261105')
BODY=Path('work/analysis/Rafael557_body_visual_review_v1_20261105/body_visual_review.json')
REBUILT=Path('work/analysis/Rafael557_reconstruction_v1_20261105/reconstruction.json')
STORED=Path('work/analysis/Rafael557_stored_native_v1_20261105/stored_native_verification.json')
CATALOGUE=Path('work/analysis/Rafael557_stored_catalogue_v1_20261105/all_stored_effective_body_bindings.json')
LOADERS=Path('work/analysis/Rafael557_loaders_v1_20261105/verification.json')
JOIN=Path('work/analysis/Rafael867_parent_modes_join_v1_20261105/qualification.json')
PACKAGE=Path('work/analysis/Weekend_testing_package_v1_20261105/package_verification.json')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,native,body,rebuilt,stored,catalogue,loaders,package=map(load,[DOC,INPUT/'native.json',BODY,REBUILT,STORED,CATALOGUE,LOADERS,PACKAGE])
    assert len(doc['records'])==557 and all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in doc['records'])
    assert len(native['records'])==len(stored['records'])==len(catalogue['records'])==549
    assert native['pages']==stored['complete_stored_pages']==558 and body['all558_final_body_pages_directly_viewed']
    assert stored['fresh_parity_dependent_pages']==281 and stored['exact_compiled_pages_reused']==277
    assert stored['fresh_relocated_native_relative_cases']==1190 and len(stored['relative_cases'])==238
    assert stored['reconstruction_sha256']==sha(REBUILT.read_bytes()) and stored['native_sha256']==sha((INPUT/'native.json').read_bytes())
    assert catalogue['stored_sha256']==sha(STORED.read_bytes()) and catalogue['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    assert (loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(343,40,646)
    assert loaders['reconstruction_sha256']==sha(REBUILT.read_bytes()) and len(rebuilt['changed_blocks'])==20
    assert rebuilt['all_other_files_components_exact'] and rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact']
    assert sha(Path(rebuilt['research_ROM']).read_bytes())==rebuilt['research_ROM_sha256']=='da7e399b110dfe2514ae19bd4bfb55458ff5ea8fd8d53b636b56e84b45175a79'
    release=load('work/analysis/Rafael867_extended_release_verified_v3_20261105/registered_release_verification.json')
    assert rebuilt['parent_sha256']==release['candidate_sha256']==package['ROM_sha256']
    assert sha(Path(package['zip']).read_bytes())==package['zip_sha256']
    ROOT.mkdir(parents=True)
    evidence={str(p):sha(p.read_bytes()) for p in [PROSE,DOC,PREF,INPUT/'input_qualification.json',INPUT/'native.json',INPUT/'menu.json',
        INPUT/'styles.json',INPUT/'qualified_public_names.json',BODY,REBUILT,STORED,CATALOGUE,LOADERS,JOIN,PACKAGE,Path(__file__)]}
    receipt=ROOT/'offline_completion.json'
    save(receipt,dict(records=557,speeches=549,captions=8,body_pages=558,proposed_revisions=235,justified_retentions=322,
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),all_four_prose_gates_pass=True,all_fifth_gates_still_false=True,
        all_body_pages_captions_andscoped_public_names_checked_anddirectly_viewed=True,
        complete_stored_native_catalogue_andloaders_pass=True,source_current_andtarget_references_in_bound_per_record_proofs=True,
        actual_source_variants=0,offline_only_source_variants=549,actual_gameplay=False,registered_integration_pending=True,new_credit=0,
        research_ROM=rebuilt['research_ROM'],research_ROM_sha256=rebuilt['research_ROM_sha256'],research_only_not_a_candidate=True,
        no_live_jobs=True,weekend_package_unchanged=True,full_goal_complete=False,evidence=evidence))
    summary=('Rafael B141–B160 now passes complete offline display and stored-script checks: 557 reviews (235 revisions, 322 justified retentions), '
        '549 speeches/558 directly viewed pages, eight captions and 20 public names. All stored glyphs/pages, 1,190 native branch cases, '
        '549 catalogue lookups and 343 archive loads pass. Research da7e399b changes only its 20 owned SC0 blocks over registered 3bf3; complete inverses pass. '
        'Representative gameplay, all fifth gates and registered integration remain pending; zero new credit. No live jobs. '
        'Integrated 12,712/current 3bf3/main 3cb8 and the delivered weekend package are unchanged. Rafael/tutorial priority and full scope remain active.')
    text=f'''# Rafael557 stored-script checkpoint — November 5, 2026

The previous goal turn finished and delivered the requested weekend package. This turn completes the pending native remainder, final page-review join and stored-script validation. No completed editorial batch was restarted and no integration credit was added.

The complete B141–B160 review remains **557 objects: 235 proposed revisions and 322 justified retentions**. The four individual prose gates pass; every fifth gate remains false. Exact clean/current references, complete preambles, findings and reasons are in `{PROSE}` and `{DOC}`. No new prose was authored during this storage turn.

## Completed display and storage

- Final paragraph plans: `{INPUT/'plans.json'}`; preferences: `{PREF}`. All 549 bodies/558 pages pass. The completed native join reuses 206 original records, 337 exact final records from the successful remainder, and six fresh layout revisions. Original failed and retired trials remain preserved.
- `{BODY}` binds all **558 final pages** to 42 directly opened, readable sheets (585 previews including retired trials). Scoped changes keep invite Julio, Dr. Hans, Zamorin Nagalpur, Let's try it, carried away and Governor Escante's together. The rejected tablet-title trial remains documented. All six FE row checks pass; physical widths and registered runtime are unchanged.
- `{INPUT/'input_qualification.json'}` binds the body evidence, eight caption records/four complete two-choice objects, all 32 caption-state planes and 20 public names. Existing caption proofs use two-record manuscript subsets; each complete subset is byte-for-byte equal to the current records. The complete source/current command census proves no 4100 objects and five label-free 2000 controls. No style execution is invented for the empty category.
- `{REBUILT}` records **20 rebuilt blocks, 1,081 commands and 238 relocated sites**. Research ROM SHA-256: `{rebuilt['research_ROM_sha256']}`. Only SC0 differs from registered 3bf3. Complete clean/current block, archive and serialized-ROM inverses pass; all unowned files/components, accepted graphics, code, font and ASCII right-bound/runtime/name stages remain exact. This research image is pinned and is not a registered candidate.
- `{STORED}` proves all **549 stored bodies/558 pages**: 281 fresh parity-dependent pages and 277 exact compiled-page reuses. Every fresh stored plane equals its already viewed plane; complete leading/internal/trailing glyphs, canaries, consumption and pagination pass. FU expands to Rafael Castor under the original wrapper, including scratch-ring guards. **1,190 native branch cases** pass.
- `{CATALOGUE}` proves all **549 full-buffer catalogue lookups**, including 24 earlier catalogue-selected bodies, return the newly stored bytes exactly with stack, input and unowned-memory guards.
- `{LOADERS}` proves **343 whole archive loads/cache hits**, 344 original EV0 actions and 686 handoff modes: 40 fresh changed-block cases and 646 exact reuses. The first attempt correctly rejected a stale 351-only comparison context before creating output. `{JOIN}` then joined all 686 exact parent cases from the separate checked 261/255/351 batches against registered 3bf3 and matched every executed instruction. No unchanged native case was rerun or relabelled as fresh.

Sealed summary: `{receipt}`. All validation processes are terminal exit 0. No live native/emulator jobs remain.

## Continue here

Next prepare representative disclosed initialized gameplay sequences from these exact stored commands. Cover complete early combat/investment and map exchanges, both FU records (B143R67/B146R6), the fixed B148R121 FE notice, ordinary/FE transitions, representative two-page speeches, all four menus and scoped speaker headers. Use ordinary controller inputs; distinguish selected initialized scenes from natural conditional activation. All 549 speech variants currently remain offline-only. Reuse the completed body/menu/name/storage/catalogue/loader proofs where their dependencies match.

After focused checks and direct review pass, seal all five per-record gates and integrate through a registered cumulative successor with all accepted layers/eight final stages, exactly reconstructable clean-input patch and required own startup checks. The **557 batch is not integrated**. Totals stay **12,712 = 7,283 revisions + 5,429 retentions**. Current registered candidate 3bf3, main 3cb8 and the weekend ZIP remain unchanged; do not silently replace the delivered package or promote main.

All other routes, prior unfinished contextual passes, shared shop/town/random scenes, speaker-name review and remaining prose remain in scope. Keep the two full-catalogue de corrections under an appropriate exclusive owner, the global name/full-catalogue UI review, deferred graphics artwork and later older-record technical re-audit separate. Preserve every ROM and earlier translation. No guide-photo collection, pruning or commit/push.
'''
    checkpoint(mutation='work/analysis/Rafael557_stored_ledger_checkpoint_20261105',batch_key='Rafael_SC0_B141_B160_clean_20261105',
        batch_updates=dict(new_credit=0,manuscript=str(PROSE),manuscript_sha256=sha(PROSE.read_bytes()),
            formatting_manuscript=str(DOC),formatting_manuscript_sha256=sha(DOC.read_bytes()),
            automatic_plans=str(INPUT/'plans.json'),automatic_plans_sha256=sha((INPUT/'plans.json').read_bytes()),
            visual_preferences=str(PREF),visual_preferences_sha256=sha(PREF.read_bytes()),
            planned_speeches=549,planned_pages=558,native_body_records=549,native_body_pages=558,
            remaining_native_records=0,remaining_native_pages=0,all558_body_pages_directly_viewed=True,
            current_FU_expansion_parity_width_anddisplay_pending=False,current_FU_native_andstored_display_qualified=True,
            current_FU_expansion_parity_andwidth_qualified=True,stored_speeches=549,stored_pages=558,
            fresh_stored_parity_pages=281,exact_stored_page_reuses=277,fresh_native_relative_cases=1190,
            stored_catalogue_lookups=549,archive_loads_andcache_hits=343,fresh_parent_cases=40,exact_reused_parent_cases=646,
            all_fifth_formatting_gates_pending=True,all_five_research_gates_pass=False,
            actual_source_variants=0,offline_only_source_variants=549,representative_gameplay_pending=True,registered_integration_pending=True,
            offline_completion=str(receipt),offline_completion_sha256=sha(receipt.read_bytes()),evidence=evidence),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Rafael557: complete prose/display/stored/catalogue/loaders; representative gameplay next.',
            next_action='Prepare focused initialized scenes for tutorials, FU, FE, pagination, menus and scoped headers; then registered integration.',
            native_job_live=False,guide_photos=False)},summary=summary,
        document='docs/editorial_Rafael557_stored_checkpoint_20261105.md',document_text=text,completed=12712,
        protected={'translations/release_stack.json':release['registry_sha256'],
            'dk4tool/rom/nds.py':'27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
            'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
            release['candidate']:release['candidate_sha256'],package['zip']:package['zip_sha256']})
    print('Saved557 complete offline storage checkpoint; all fifth gates pending,zero new credit,full goal active;weekend/main unchanged.')
