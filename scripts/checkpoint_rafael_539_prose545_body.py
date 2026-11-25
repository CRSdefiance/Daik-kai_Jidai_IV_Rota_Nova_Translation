"""Checkpoint the full prose pass and native/visual body review without release credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v3 import checkpoint

ROOT=Path('work/analysis/Rafael_B61_B80_formatting_20261104')
RELEASE=Path('work/analysis/Rafael_B51_B60_release_verified_20261104/registered_release_verification.json')

if __name__=='__main__':
    manuscript=Path('translations/rafael_B61_B80_contextual_editorial_manuscript_v3.json')
    approval_path=ROOT/'body_display_approval_v10.json';approval=load(approval_path)
    native_path=ROOT/'combined_native_v10.json';native=load(native_path);release=load(RELEASE)
    plan_path=ROOT/'automatic_v10/automatic_plans.json'
    assert approval['all_final_pages_directly_viewed'] and approval['body_records']==539 and approval['body_pages']==545
    assert len(native['records'])==539 and native['pages']==545 and not native['direct_visual_review_pending']
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in load(manuscript)['records'])
    summary=('Rafael and all tutorials remain first. B61–B80 now has all 539 contextual prose reviews: '
        '210 proposed revisions/329 justified retentions. All 545 final body pages pass native and direct visual review on 35 readable sheets. '
        'Fourteen layout refinements remove two needless pages;16 I fixes,14 ellipsis fixes andscoped punctuation fixes preserve prose. '
        'Five Charlotte FE speeches/one funds notice are distinguished;the measured FE single-letter/extra-row defect is corrected offline. '
        'Names/headers,storage,focused CG/transitions andregistered integration remain;all fifth gates andnew credit stay pending. '
        '10774 integrated completions;verified eb62870b/main/ROMs/full scope preserved. No live jobs or guide photos.')
    document=Path('docs/editorial_rafael_539_prose545_body_20261104.md')
    text=f'''# Rafael: full539 prose and545 body-page review — 2026-11-04

Rafael early story and all tutorial work remain first. Preserve all completed translations, justified retentions, credit, ROMs and evidence. All storylines, earlier translations, shared shop/town dialogue, random scenes, names/roles and remaining player prose remain in scope. No promotion, pruning or guide photos. Deferred graphics artwork and the later older-record technical re-audit remain separate.

## Current verified release

Experimental cumulative ROM: `{release['candidate']}`, SHA256 `{release['candidate_sha256']}`. Its669 entries/114 accepted layers/eight final stages/26 checks, exact clean-input patch and own Rafael startup remain verified. Reuse `{RELEASE}` and `docs/editorial_rafael249_registered_and539_next_20261104.md`; do not repeat them. Registry SHA256 `{release['registry_sha256']}`.

Integrated totals remain10774 complete/6356 revisions/4418 retentions. No new completion credit is granted here. Main remains `{release['canonical_base']}`, SHA256 `{release['canonical_sha256']}`. All generated ROMs and earlier translations are preserved. This turn generated no ROM and changed no release profile. No jobs from this work are live.

## Full prose pass

`{manuscript}` contains all539 individual source/current/draft contextual comparisons,210 proposed revisions/329 individually justified retentions. Every source/current reference and complete preamble remains bound; first four gates pass and all fifth gates remain false. Original draft/comparison versions and the full539 source packet are frozen under `work/analysis/Rafael_B61_B80_clean_20261104`. B68 is preserved control-only content. Numerical block order is not chronology.

The remaining250 comparisons were completed as whole exchanges:108 festival/Maria speeches give30 revisions/78 retentions;116 reward/Eirene/Spain speeches give45/71;26 Mediterranean alternatives give12/14. Findings include omitted wako followed by an unexplained question, might-consider changed to a guaranteed promise, Maria speaker intent reversed, invented Lord titles/instructions/sedition, wrong first-person referents and missing source qualifiers. The existing direct loss to Valdes already worked and was retained. Preserve private Eirene/public Arcadius, Romani identity/reported prejudice/approximate dates, actual stated ages, hypothetical relationships, completed versus threatened annexation and source imperial/royal wording.

The trade-house term and item186 Bamboo Assembly Plan are bound in `work/analysis/Rafael_B61_B80_clean_20261104/trade_house_andBamboo_Assembly_Plan_binding_v1.json`. Estado is localized from the clean explicit trading-sphere/network definition, not an invented city/country/rank. Actor40 full-middle フォン/current Ｆong and global207/full-catalogue review remain open.

## Formatting, glyphs and honest native coverage

Final formatting input: `{ROOT/'formatting_input_v3.json'}`. Final plan: `{plan_path}`. Planner: `scripts/plan_rafael_B61_B80_v2.py`; preferences: `{ROOT/'visual_preferences_v9.json'}`. All539 automatic checks pass,545 native pages,zero unqualified warnings/errors. Keep the source-locked inherited planner/native addresses and registered right-bound correction. English remains logical paragraphs, with no authored wraps/padding and no shortened prose.

Native/visual proof: `{native_path}` and `{approval_path}`. All545 final body pages have exact direct visual bindings to35 readable contact sheets;563 candidate pages including18 retired/replaced pages were inspected. Every final glyph,leading/trailing character,substitution alignment,control,canary,bound andpagination is checked.533 progressive speeches andsix FE speeches are present:five Charlotte CG speeches andone Pereira military-funds notice. FE is a consumer designation,not a blanket system-speaker label.

Fourteen layout refinements improve phrase/page continuity and remove two unnecessary pages. Keep the measured native216px progressive/228px FE geometry andfour rows. Sixteen full-width I letters,14 visually inconsistent CP932 ellipses and19 specifically scoped copied full-width punctuation characters are normalized in proposed English. Pauses/reactions and character meaning remain; no graphics font artwork is edited. One exact grammatical article soft boundary inB69R143 allows three readable rows instead of four short rows. Its source/current/English hashes,exact line,original QA warning and individual reason are preserved; no global QA rule is relaxed. B65R35 andB75R238 necessary two-page layouts have explicit coherent-boundary retentions.

Concrete FE failure: B69R87 drew Ther on row0,an isolated e on row12,andthe intended second line on row24. `{ROOT/'Charlotte_FE_R87_row_finding_v1.json'}` andits directly viewed diagnostic preserve that finding. The final scoped guard reserve keeps the complete words on exactly two native rows;all glyph/bounds/canary checks pass. This is an offline text-display correction,not an actual CG/gameplay capture.

The initial full native run91157 terminated1 at the first named FE speech because its inherited expected-value assertion still named Hodram. That harness expectation was source-locked to verified Rafael/Castor/Castor Co. defaults without changing native addresses or weakening memory/canary checks. Its compatible completed blocks61–68 were retained. Run12690 terminated1 on the actual R87 row mismatch;its six completed compatible records were retained. No failed run is called a whole-batch pass. `native_resume_v3/exact_reused_native_records.json` qualifies289 records/294 pages;the later R70 layout replaces one of those. Fresh run33026/PID95500 terminated0:250 records/251 pages/1000 alignments. The one-record final deltasv8/v10 terminated0. Final composite545 pages andevery visual binding pass;reuse did not relabel old RAM as new gameplay.

## Continue from here

Reuse all completed source,prose,default macros,body plans,native pixels andvisual checks. Do not regenerate all545 pages. All22 source/public name-role decisions and exact native getter dependencies are qualified on eb62870b in `translations/rafael_B61_B80_scoped_names_andterms_v1.json` and `work/analysis/Rafael_B61_B80_latest_runtime_20261104/dependency_qualification.json`;physical scoped header/name planes remain to qualify.

Next verify scoped names/headers,then reconstruct all20 source scene blocks with complete controls/relative branches/B68 preserved. Check stored catalogue bodies,all allocations/loaders and final stored glyph/pages, reusing exact proofs where dependencies match. Use representative gameplay and focused tests for distinct pagination,normal/FE transitions andespecially the complete B69 CG/action sequence. Its precise gesture remains unconfirmed;invent no kiss or other action from punctuation. All539 new scene lines are currently offline-only;no natural scene activation,full route,hardware or full-catalogue UI coverage is claimed.

Once necessary checks pass,finalize all individual gates andintegrate this substantial539 batch through the complete registered eight-stage cumulative workflow, with an exactly reconstructable clean-input patch. Preserve all accepted/runtime/name/tutorial/graphics layers andthe exclusive Fernan F correction. Credit the batch exactly once only after release verification. Do not promote main without required user acceptance. Then keep remaining early tutorials/help/town work ahead of further later-route expansion;all wider scope remains active.
'''
    checkpoint(mutation=ROOT/'539_prose545_body_checkpoint_mutation_v1',batch_key='Rafael_SC0_B61_B80_clean_20261104',
        batch_updates=dict(new_credit=0,source_first_logical_drafts=539,remaining_independent_drafts=0,
            contextual_prose_comparisons=539,remaining_contextual_comparisons=0,proposed_revisions=210,justified_retentions=329,
            comparison=str(manuscript),comparison_sha256=sha(manuscript.read_bytes()),current_bound_records=539,
            current_bound_uncompared_records=0,remaining_current_bound_butunread_records=0,
            proposed_fullwidth_I_glyph_corrections=16,glyph_correction_records=13,
            proposed_scoped_punctuation_normalizations=19,ellipsis_glyph_consistency_fixes=14,
            final_formatting_input=str(ROOT/'formatting_input_v3.json'),final_formatting_input_sha256=sha((ROOT/'formatting_input_v3.json').read_bytes()),
            final_body_plan=str(plan_path),final_body_plan_sha256=sha(plan_path.read_bytes()),
            final_native_body=str(native_path),final_native_body_sha256=sha(native_path.read_bytes()),
            body_display_approval=str(approval_path),body_display_approval_sha256=sha(approval_path.read_bytes()),
            final_body_pages=545,all_final_body_pages_directly_viewed=True,readable_review_sheets=35,
            layout_refinements=14,unnecessary_pages_removed_without_shortened_prose=2,
            progressive_speeches=533,Charlotte_FE_speeches=5,military_funds_FE_notices=1,
            concrete_Charlotte_FE_single_letter_extra_row_defect_corrected_offline=True,
            CG_gesture_andEstado_final_wording_pending=True,CG_gesture_unconfirmed=True,Estado_final_wording_pending=False,
            all_individual_fifth_gates_pending=True,actual_gameplay_records=0,
            scoped_header_name_planes_storage_actual_CG_transitions_andregistered_integration_pending=True,
            fresh_formatting_stored_visual_gameplay_andregistered_integration_pending=True,
            no_live_jobs=True,next_action='Qualify scoped names/headers;reconstruct/store/check20 blocks;focused CG/pagination/transitions;registered eight-stage integration andonce-only credit.'),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            next_independent_drafts=539,next_contextual_comparisons=539,current_batch='Rafael_SC0_B61_B80_clean_20261104',
            current_body_pages_native_andvisually_reviewed=545,registered_cumulative_build_live=False,
            current_batch_not_yet_integrated=True,Rafael_early_story_andall_tutorials_first=True,
            full_editorial_scope_preserved=True,guide_photos=False)},
        summary=summary,document=document,document_text=text,completed=10774,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    print('Checkpointed539 prose reviews/545 native andviewed body pages;10774 completions/main unchanged. Scoped names/storage/actual CG/transitions/integration remain. No live jobs.',flush=True)
