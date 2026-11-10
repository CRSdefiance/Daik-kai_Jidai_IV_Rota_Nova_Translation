"""Publish321 contextual prose reviews and fresh plans without integration credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT = Path('work/Maria_B196_B215_clean_20261110')


def main():
    rp = Path('work/maria305_B176_B195_release_v1/registered_release_verification.json')
    release = load(rp)
    manuscript = Path('translations/maria_B196_B215_contextual_review_v1.json')
    namepath = Path('translations/maria_B196_B215_scoped_names_v1.json')
    planpath = ROOT/'plan_v4/automatic_plans.json'
    doc, names, plans = map(load, [manuscript, namepath, planpath])
    initial = {r['id']: r for r in load(ROOT/'plan_v1/automatic_plans.json')['records']}
    assert len(doc['records']) == 321 and doc['complete_exchanges'] == 18
    assert (doc['proposed_revisions'], doc['justified_retentions']) == (171, 150)
    assert len(names['records']) == 24
    gates = dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
    assert all(r['review'] == gates for r in doc['records'] + names['records'])
    assert len(plans['records']) == 317 and not plans['failures']
    assert not any(i['severity'] in ['error', 'warning'] for r in plans['records'] for i in r['base_QA']['issues'])
    pages = sum(r['expected_native_pages'] for r in plans['records'])
    assert pages == 325
    previous = load(ROOT/'plan_v3/automatic_plans.json')
    assert [(r['id'], r['encoded_hex']) for r in plans['records']] == [(r['id'], r['encoded_hex']) for r in previous['records']]
    changed = [r['id'] for r in plans['records'] if r['lines'] != initial[r['id']]['lines']]
    assert len(changed) == 19
    evidencepaths = [rp, manuscript, namepath, planpath, ROOT/'plan_v4/diagnostics.json',
        *[ROOT/p for p in ['clean_draft_seal_v1.json', 'all321_clean_meanings_v1.json',
            'all321_independent_drafts_v1.json', 'contextual_comparisons_v1.json',
            'current_v1/current_effective.json', 'current_objects_v1/current_objects.json',
            'scoped_names_macros_reference_v2.json', 'scoped_terms_reference_v1.json',
            'dynamic_roles_current_v1.json', 'prose_gates_v1.json',
            'formatting_v1/formatting_input.json', 'formatting_v1/native_macro_measurements.json',
            'formatting_v1/page_phrase_preferences_v4.json']], Path(__file__)]
    evidence = {str(p): digest(p) for p in evidencepaths}
    summary = ('Maria B196–B215 has 321 contextual reviews across 18 complete exchanges: '
        '171 proposed revisions, 150 justified retentions and 24 scoped name reviews. '
        'All four individual prose gates pass; fifth gates remain pending. Fresh full-width plans cover '
        '317 bodies/325 pages plus four captions, with no errors, warnings or failures. '
        'Nineteen layouts change and one premature page is reclaimed without shortening prose; '
        'native pixels, direct visual review, storage, representative gameplay and registration remain. '
        'No new ROM or completion credit; integrated 22,386, registered d5bc0dc5, main and full scope remain unchanged. No batch worker is live.')
    document = 'docs/editorial_Maria321_B196_B215_prose_layout_20261110.md'
    text = f'''# Maria321 B196–B215 prose and layout checkpoint — November 10, 2026

{summary}

The full editorial goal remains active. This continues the saved clean-only draft checkpoint; it does not restart completed work. All321 clean meanings and independent drafts were sealed before this batch's first current-story-English extraction. Source/current/native comparison is now complete for all321 objects:296 ordinary bodies,21 physical4100 alternatives across three complete eight-slot style objects, andfour captions across two two-choice menus. Exact source/current references, individual findings and justified retentions are in `{manuscript}`. Immutable authored parts, original drafts and all comparison parts remain preserved.

The selected prose corrects meaning as well as naturalness: Indian Ocean geography, a mail-versus-armor overstatement, letter identities/signatures, uncertain clues presented too confidently, the rose's actual appearance, the friend-of-a-friend report, an invented paid arrangement, and Julio's reversed departure instruction. Maria says “You can head back first.” Familiar address does not create kinship; the barkeep is not established as Francisca's father. Conditional New World replies and figurehead outcomes remain separate alternatives. Historical counterfactuals and supernatural reports remain character claims. Retentions preserve already natural dialogue, distinct voices, deliberate humor, accurate clues, religious address supported by the priest context, and allfour working captions; each has its own reason.

Names and roles have scoped native bindings:24 actors/48 original getter cases, including selector151 and fallback156 with Sailor nameplates/Retainer catalogue labels. The boy162 is distinct. Selector207/current captain3 and selector208/current-startup fallback156/voice4 are native dispatch references, not claims about future crew participation or actual conditional scenes. Thirteen item titles and Spirit are source/current/native bound; use Medusa Shield and Armadillo Hide where actually named. Do not add formal item titles to unnamed descriptive clues or respell installed Gabriel Cardocci without new source evidence. The24 name decisions retain source-compatible names/labels with individual reasons; no new name-table bytes or global metadata approval is granted.

All321 prose records and24 scoped name reviews pass source, context, localization and naturalness gates. Every formatting gate remains false. Logical paragraphs retain exact source macros and controls. Twenty compatible default-macro proof cases are reused explicitly with matching native dependencies; this is reuse, not fresh measurement. New text receives new formatting checks. Use `formatting_v1/formatting_input.json`, `formatting_v1/page_phrase_preferences_v3.json` and `plan_v3/automatic_plans.json`, relative to `{ROOT}`. Native physical widths remain216px progressive/228px FE; no font, viewport or engine changes occur.

All317 body plans pass structural/formatting QA and preserve every word, punctuation mark and macro. They produce325 planned pages, down from326. Nineteen compiled layouts change, including letter-arrival phrasal verbs, closing thoughts, quantity/place/item phrases and one reclaimed Jam letter page. Nine explicit comparisons retain better original phrase/page layouts after tighter constraints made them worse. A narrow source/current/exact-sentence retention recognizes “your eyes were drawing me in.” as a complete phrasal-verb sentence, not an orphaned preposition. It waives no native glyph, bounds or pagination assertion. Other requested pairs that produce no compiled difference are not new fixes. In particular, the initial ship/crew's wrap has not been repaired by the unmatched ship/crew preference; review that ordinary boundary as a retention or remove the inert preference before a later final plan. Do not report it as an improvement.

The initial planner's complete durable outputs were recovered after its console output was lost; no completed run was repeated merely because observation failed. Plan_v2 and its terminal assertion evidence remain preserved: forcing the complete Charles Martel name produced a weak “of” line ending, and forcing Medusa Shield added a page. Plan_v3 retains the better ordinary wraps, removes that warning and passes terminal0. Five preferred page clauses remain scoped; other overconstraints are relaxed. These are planned-text judgments only. No new native page or contact sheet has been generated or directly viewed, and actual batch gameplay coverage is zero.

**Next:** remove the inert ship/crew pair through a source-bound preference successor if needed, confirming unchanged compiled output; then prepare body-only native inputs with all317 exact plans and the complete dynamic selector/macro bindings. Run fresh native alignment/glyph/pixel/consumption/canary/row/bounds/pagination checks and directly inspect every generated page on readable contact sheets. Captions, complete styles, names, stored reconstruction/native branches/loaders, representative initialized gameplay/transitions and registered cumulative integration follow. Reuse already completed evidence only when exact relevant dependencies match. Do not mark fifth gates or add completion credit prematurely.

The user identified testing build `all_routes_rafael2952_extended_checkpoint_v1_20261106_candidate`. [The recorded Market fix](editorial_market_goods_info_fix_20261109.md) binds that exact old ROM and screenshot. The Japanese-looking Goods Info suffix is machine-code overread from an overwritten NUL, not an untranslated sentence. The registered Market allocation/pointer correction is already inherited by the Maria305 parent; do not reinvestigate it or drop it from the next build. The dedicated corrected candidate remains available, as does the newer registered Maria305 cumulative candidate.

[Registered Maria305](editorial_Maria305_B176_B195_registered_20261110.md) remains the only current registered parent:720 entries,114 accepted layers,55 release checks, exact clean-input reconstruction, own Maria/Hangzhou startup and24 protected name getters. Candidate:`{release['candidate']}`; SHA256:`{release['candidate_sha256']}`. Preserve Market's read-only16-byte allocation/both pointers, six-section ARM9, ASCII right bounds, source25v2, inherited B164R99 padding correction, all earlier archives/names/fonts/graphics and the canonical baseline. Main remains `all-routes-unified-v4701`; no promotion without required user acceptance.

Integrated22,386 =13,405 revisions+8,981 justified retentions. Historical source/prose/draft22,389. Native story remainder3,512 =Maria1,707+Lil1,805 still includes this uncredited321; separate shared/player-facing inventories remain in scope. Keep all storylines, earlier unfinished contextual passes, towns/shops/random scenes, names, glyphs and readable wrapping in scope, with early Rafael/tutorial priority. No guide photos. Deferred graphics artwork and later older-record technical re-audit remain separate. No generated ROM, translation or evidence was removed; no cleanup, promotion, commit or push occurred. No worker is live.
'''
    checkpoint(mutation=ROOT/'prose_layout_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Maria321:321 contextual reviews/four prose gates;317 bodies/325 planned pages;native/visual/storage/gameplay/release pending.',
            current_batch_not_yet_integrated=True, current_batch_registered_andcredited_once=False,
            proposed_revisions=171, justified_retentions=150, all_current_batch_fifth_gates_pending=True,
            native_job_live=False, native_sessions=[], stored_job_live=False, stored_sessions=[],
            registered_build_live=False, registered_cumulative_build_live=False,
            current_batch_evidence=evidence, guide_photos=False,
            next_action='Prepare fresh317-body native inputs; directly review every native page, then mixed objects/storage/representative gameplay/registered integration.'),
        additional_updates={'Maria_SC3_B196_B215_clean_20261110': dict(new_credit=0,
            current_English_not_read=False, contextual_comparison_pending=False, individual_contextual_comparisons=321,
            names_terms_consumers_pending=False, scoped_name_reviews=24, native_name_getter_bindings=48,
            proposed_revisions=171, justified_retentions=150, first_four_individual_prose_gates_pass=True,
            all_five_review_gates_pending=False, all_fifth_gates_pending=True, planned_body_pages=325,
            planned_body_records=317, planned_layout_changes=changed, planned_pages_reclaimed=1,
            native_pages_visually_reviewed=0, actual_batch_gameplay_records=0,
            registered_integration_pending=True, no_batch_worker_live=True, evidence=evidence, full_goal_complete=False)},
        summary=summary, document=document, document_text=text, completed=22386,
        protected={'translations/release_stack.json': release['registry_sha256'],
            release['candidate']: release['candidate_sha256'], release['manifest']: release['manifest_sha256'],
            release['patch']: release['patch_sha256'], release['canonical_base']: release['canonical_sha256']})
    save(ROOT/'current_checkpoint.json', dict(document=document, source_objects=321, revisions=171, retentions=150,
        scoped_name_reviews=24, planned_body_records=317, planned_pages=325, changed_layouts=changed,
        first_four_gates_pass=True, all_fifth_gates_pending=True, no_batch_worker_live=True,
        no_new_ROM_orcompletion_credit=True, full_goal_complete=False, evidence=evidence))
    print('Published Maria321:171 revisions/150 retentions,four prose gates,325 planned pages;integrated22386/main unchanged.')


if __name__ == '__main__':
    main()
