"""Save the completed255 research gates while holding credit for registered integration."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint

ROOT = Path('work/analysis/Rafael255_checked_v2_20261105')
FINAL = Path('translations/rafael_B101_B120_contextual_final_review_v1.json')

if __name__ == '__main__':
    proof, actual, final = map(load, [ROOT/'research_completion.json', ROOT/'actual_review.json', FINAL])
    assert proof['all255_individual_five_gates_pass'] and len(final['records']) == 255
    assert all(all(r['review'].values()) for r in final['records'])
    assert (actual['source_speech_variants_observed'], actual['native_body_pages_observed'],
            actual['actual_choice_labels'], actual['offline_only_speech_variants']) == (75, 77, 12, 168)
    assert len(actual['menu_transitions']) == 4 and actual['total_frames'] == 29362
    failed = load('work/analysis/Rafael261_registered_build_20261105/completion.json')
    assert failed['terminal'] and not failed['driver_completed_without_exception']
    assert not Path(failed['out']).exists()
    summary = ('Rafael early story and all tutorials remain first. B101–B120 now passes all255 individual five-gate research reviews: '
        '135 revisions/120 justified retentions,248 native/viewed/stored pages,12 captions and18 scoped names. '
        'Two initialized emulator runs/29362 frames observe75 speech variants/77 pages andall12 captions; '
        '168 variants remain offline-only. All four three-choice menus showevery cursor state andordinary A-to-dialogue transitions; '
        'dynamic207/208 headers,both complete personality objects,andthe repaired FE period/four-row bean premise pass. '
        'All seven readable actual body sheets,one full-context sheet andone menu sheet viewed. '
        'Research gates are sealed;255 andearlier261 awaitregistered integration,withzero newcredit. '
        'Original679 remains terminal1/MemoryError withno candidate;no retry running. '
        'Next prepare one qualified cumulative attempt carryingboth ready batches,retainingthe verified678 prefix,all114 accepted layers, '
        'original core andeight final stages.11845 integrated;verifiedcc71/main unchanged. Fullscope/ROMs/evidence preserved;no guidephotos orpromotion.')
    document = '''# Rafael255 research complete — November 5, 2026

Rafael’s early storyline and all tutorials remain the execution priority. Every other route, unfinished contextual pass, shared town/shop exchange, random scene, name and remaining player-facing text stays in scope. Preserve all ROMs and evidence. No guide photos or main promotion.

`translations/rafael_B101_B120_contextual_final_review_v1.json` seals **255 individual five-gate research reviews:135 revisions and120 justified retentions**. Wording, decisions and individual findings remain exactly those reviewed before gameplay. The required top-level review-gate declaration was missing from the scoped-name manuscript; the finalizer correctly rejected it. V1 and its two partial receipts are preserved. V2 adds that declaration, passes the unchanged validator and seals all18 scoped names. This was a review-document metadata defect, not a new game-text defect.

Authoritative receipt: `work/analysis/Rafael255_checked_v2_20261105/research_completion.json`. Reuse the [storage checkpoint](editorial_Rafael255_storage_checkpoint_20261105.md) for clean-source/prose decisions, complete mixed inventory, all248 native/viewed/stored pages, twelve captions, both eight-slot tables, catalogue/loaders, eighteen changed blocks and complete inverses. None requires repetition merely because research gates are now sealed.

## Newly completed representative gameplay

`work/analysis/Rafael255_checked_v2_20261105/actual_review.json` binds two initialized cold boots totaling29362 frames. They observe75 unique speech variants on77 pages plus all12 captions:87 editorial objects. The remaining168 speech variants, including twelve other personality variants, are explicitly offline-only. All243 speech variants had already passed offline checks. This is actual emulator rendering of copied native commands after ordinary New Game; it is not original event activation, earned chronology, a natural route playthrough or hardware verification. The unchanged startup background is not evidence of each scene’s original location.

The tests cover the complete Julio granddaughter/shield exchange, the priest’s cross misunderstanding, nearby town leads and village exchange, all eleven newly scoped public names, both dynamic source selectors207/208 and both complete personality commands. Fifteen offline-bound actor identities match fourteen visible name strings; numeric actor identity is not inferred from pixels. Janus4, Yukihisa12 andEmilio14 remain unvisited in this batch and retain exact qualified prior proofs. No role/roster assignment was overridden.

All four native three-choice menus display complete, centered captions with all three cursor positions. Ordinary A acceptance is followed by the expected next fixture speech in each case. Source and relocated-storage offsets remain distinct. Original conditional responses, numeric return registers, cancellation and stat effects are unvisited; offline provider/branch checks remain separately identified.

The repaired FE period and four-row bean premise display completely. Both observed two-page transitions preserve complete text and ordering. Pixel checks bind162 complete body holds and138 header holds. Seven readable body contact sheets, one six-sample full-context sheet andone twelve-cursor-state menu sheet were directly viewed; the original full captures are preserved. The Julio joke, priest exchange and village dialogue remain coherent in sequence; no further prose changes were needed. See `complete_visual_approval.json` beside the research receipt. These QA captures do not resume guide-photo collection.

## Integration remains

Neither255 nor the earlier261 has new completion credit. Original registered679 is still terminal1 after the preserved MemoryError; no candidate or manifest exists and no retry is running. Its failure is not a text defect or a pending wait. Preserve the original core, nine pipeline drivers, all114 accepted layers and all eight final stages.

Next prepare one registered cumulative attempt for the ready261+255 batches, using verified678 as the actual registered predecessor. Keep failed679’s profile and evidence intact. The B85–B100 andB101–B120 owned blocks are disjoint; combine only those owned blocks, never overwrite a newer entire SC0 archive with an older-parent research archive. Qualify exact local text/runtime dependencies to reuse completed native/display tests. A combined successor has not yet been prepared, registered or launched. Require its complete manifest, exact clean-input patch and own startup binding before once-only coverage credit.

Integrated totals remain11845=6836 revisions+5009 retentions; historical source/prose11848 unchanged. Verified experimental parent remainscc71ec06; main remains3cb827e4. Deferred graphics artwork and the later older-record technical re-audit remain separate. Full goal active.
'''
    protected = {
        'translations/release_stack.json': '11021a16ab4b1157d9e34fc71f214fdb2b9eeb565325122444e59e261d0bcec0',
        'dk4tool/rom/nds.py': '27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
        'out/raphael_natural_v2_accepted_base.nds': '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        'out/all_routes_combined_help97_rafael330_20261105_candidate.nds': 'cc71ec06ce5345dcc71f8b631232f4d8d501152f6989374741616260fa0ca448',
    }
    checkpoint(mutation='work/analysis/Rafael255_research_checkpoint_20261105',
        batch_key='Rafael_SC0_B101_B120_clean_20261105',
        batch_updates=dict(manuscript=str(FINAL), manuscript_sha256=sha(FINAL.read_bytes()),
            individual_five_gate_passes=255, all255_individual_five_gates_pass=True,
            fifth_gates_pending=False, representative_actual_checks_pending=False,
            research_completion=str(ROOT/'research_completion.json'),
            research_completion_sha256=sha((ROOT/'research_completion.json').read_bytes()),
            actual_review=str(ROOT/'actual_review.json'), actual_review_sha256=sha((ROOT/'actual_review.json').read_bytes()),
            actual_speech_variants=75, actual_pages=77, actual_captions=12, offline_only_speech_variants=168,
            registered_integration_pending=True, new_credit=0),
        additional_updates={'editorial_execution_priority_20261104': dict(new_credit=0,
            current_batch='Rafael255 allfive research gates complete;pending261+255 cumulative integration',
            next_action='Prepare andqualify one registered cumulative261+255 successor ofverified678;failed679 isterminal,not a registered predecessor.',
            registered_build_live=False, source_prose_anddisplay_checks_reused=True)},
        summary=summary, document='docs/editorial_Rafael255_research_complete_20261105.md',
        document_text=document, completed=11845, protected=protected)
    print('Checkpoint saved:255 five-gate research reviews,87 observed objects/168 offline-only speech variants;11845 integrated,no live build ormain change.')
