"""Persist complete prose and speech/menu display progress without premature release credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v1 import checkpoint
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B191_B210_clean_20261104')
MANUSCRIPT = Path('translations/hodram_B191_B210_contextual_editorial_manuscript_v1.json')
NAMES = Path('translations/hodram_B191_B210_scoped_names_andterms_v1.json')
DISPLAY = Path('work/analysis/Hodram_B191_B210_formatting_20261104/speech_display_approved_20261104')
RELEASE = Path('work/analysis/Hodram_B171_B190_release_verified_20261104/registered_release_verification.json')


if __name__ == '__main__':
    doc, names, visual, native, release = map(load, [MANUSCRIPT, NAMES, DISPLAY / 'visual_approval.json', DISPLAY / 'all352_native_pages.json', RELEASE])
    assert len(doc['records']) == 373 and (doc['proposed_revisions'], doc['wording_retentions']) == (154, 219)
    assert len(names['records']) == 70 and visual['final_speech_pages_visually_approved'] and visual['all21_caption_visual_checks_pass']
    assert native['pages'] == 355 and native['all355_final_pages_directly_viewed']
    assert all(r['review']['formatting'] is False for r in doc['records'])
    summary = ('B191–B210: all 373 contextual comparisons saved, with 154 proposed revisions and 219 justified retentions; '
        '70 scoped name/term retentions. All 352 speeches/355 final pages and 21 captions pass native and direct visual review. '
        'Four layout findings corrected without prose changes or QA waivers. Scoped name display, stored reconstruction, representative gameplay and registered integration remain. '
        'No new ROM or completion credit; 9933 completed, experimental d14c24ba/main unchanged. Full scope and all evidence preserved; no guide photos.')
    text = '''# Hodram B191–B210: complete contextual prose and speech/menu display review

All 373 complete-exchange comparisons are saved: 154 proposed revisions and 219 individually justified retentions. All twenty clean exchanges, including conditional endings and ten menus, are reviewed against the existing English and the previously sealed source-grounded drafts. Seventy scoped name/term decisions are retentions and add no dialogue credit. Every record has exact clean/current references, source meaning, context, an individual finding and four approved prose gates. All fifth formatting gates remain false until the remaining name/storage/representative/release requirements are satisfied.

The corrections include unnatural this man/this woman self-references, invented father and lord relationships/titles, the unsupported Sir before Rocco, the omitted Indian/celestial details of Ian's book, a wrong seller gender, the missing halves of the repeated Namahage chant, the uncertain versus categorical bargaining claims and the full Jam Jack Ludwyan signature. Carlo had the stranger brought to the inn; the source does not say he personally carried them. The old man offers a book without too, which had implied another gift. Cristina's lack of a particular man she wants to win over is not a claim that no man is worth effort. Shachihoko, giyaman/glass and the oshiro/castle recognition retain cultural context. The parrot now repeats the preceding actual English words and does not identify itself as a parrot before Hodram does.

Existing wording that works is preserved with a specific reason on each record. Examples include ordinary short reactions, courteous dialogue, the barkeep's give-it-a-try idiom, skeptical merchant banter and compact Charm/Spirit notices. Existing Dream? retains ambiguity better than the initial draft's A dream, then. The current caterpillar fungus wording remains an accurate intelligible common synonym of the bound Cordyceps commodity term; this is not a new UI rename or global older-label fidelity approval. Coins remains natural in the price offers, and all original amounts and conditional outcomes are preserved.

Manuscript: `translations/hodram_B191_B210_contextual_editorial_manuscript_v1.json`. Scoped identities/terms: `translations/hodram_B191_B210_scoped_names_andterms_v1.json`. Exact source/current/draft comparison parts and consistency checks are under `work/analysis/Hodram_B191_B210_clean_20261104/`; `complete373_prose_consistency_v1.json` checks logical paragraphs, ASCII/CP932, source macro counts, names and linked parrot echoes. No new prose was shortened to fit a text box.

All 352 speech objects (316 progressive/36 FE) have fresh consumer-specific plans and complete native glyph, input-canary, width, consumption and pagination checks. Their 355 final pages were directly viewed on forty readable speech sheets; one additional earlier Ian page is preserved as superseded. Four layout findings are resolved: two page boundaries now preserve complete sentences, a 15-character opening/three-row paragraph becomes two natural rows with the same words, and Jam's FE letter uses the validated scoped guard allowance after the initial native consumer failed to consume its long row. The native FE viewport remains 228px. Full-width I in Istanbul/Ian, full-width 50000 digits, punctuation and the complete signature now render consistently through the normal font.

The premature-opening fix uses a byte-bound ordinary but/I boundary. The unchanged base audit returns zero warnings or errors for it; no waiver is applied. Earlier preference versions and the unused v19 waiver experiment are historical and must not be used as current inputs. Current planner: `scripts/plan_hodram_B191_B210.py`; current preferences: `work/analysis/Hodram_B191_B210_formatting_20261104/guard_and_opening_preferences_v4.json`. Current plans and combined native/visual approval: `work/analysis/Hodram_B191_B210_formatting_20261104/speech_display_approved_20261104/`.

The first native runner stopped on a missing FE helper import, before a complete block receipt. The corrected v8 runner completed seventeen block receipts before the concrete B208 letter failure. Those complete proofs remain valid: 287 byte-identical records were reused and only 65 remaining/reformatted records checked fresh. All 352 final records have 1408 qualified alignment cases; the resume contributes 260 fresh cases and reuses 1148 exact cases from this batch's completed receipts. No completed block was replayed for the later failure. The final resume is terminal/exit0, with 65 records/67 pages; its evidence is `work/analysis/Hodram_B191_B210_native_20261104/remaining65/compiled_native_pages.json`. Use `scripts/check_editorial_compiled_pages_v8.py`; preserve the failed runners and outputs as history.

All 21 captions pass native source/current/reviewed object, index/count, complete glyph, normal/selected style, centering, guard, bound and modal-provider checks. Four distinct complete menus were tested fresh and six byte-identical repeated Buy/Pass menus reused the exact complete-object proof. The four menu sheets were directly viewed. Let Ian decide restores the delegation meaning, and I'll take them! replaces the unnatural Bought! acceptance. Existing Buy, Pass, Got it., So what? and Pricey are retained with individual reasons. Evidence: `work/analysis/Hodram_B191_B210_menus_20261104/complete_choice_objects.json`. These are offline native/menu-loop checks; actual controller/highlight behavior and original conditional activation are not claimed.

Next: bind/reuse the 43 actors' complete name glyph planes against the current runtime and complete the scoped name display review. Prepare all 373 exact stored objects, reconstruct twenty whole blocks with complete original controls, and run the necessary stored/relative/archive checks. Then use representative initialized gameplay and focused actual controller tests for the distinct three-choice menu, price decisions, corrected FE letter and page transitions. Distinguish observed scenes from offline-only branches. Integrate through the registered cumulative six-stage workflow only after necessary checks pass, verify the exact clean-input patch and candidate-own startup, then add once-only credit. Do not replay completed prose or these display checks unless dependencies change or a concrete failure requires it.

All current jobs are terminal; no live handle remains. No ROM or emulator gameplay run was created this turn. Completed coverage remains 9933 (6004 revisions/3929 retentions); historical source/prose/draft counters remain 9936. The registered experimental candidate remains d14c24ba and canonical main remains unchanged. Preserve all earlier translations, ROMs, retentions, failures and evidence. The full editorial objective remains active; graphics artwork and the later older-record technical re-audit stay separate. No promotion, commit/push, pruning or guide photos.
'''
    checkpoint(mutation=ROOT / 'prose_display_ledger_mutation_v1', batch_key='Hodram_B191_B210_clean_next_20261104',
        batch_updates=dict(current_English_comparisons=373, remaining_current_English_comparisons=0,
            proposed_revisions=154, justified_retentions=219, complete_four_prose_gate_reviews=373,
            scoped_name_andterm_retentions=70, scoped_name_andterm_editorial_decisions_pending=False,
            native_speech_records=352, final_native_andvisually_approved_pages=355, layout_corrections=4,
            FE_guard_corrections=1, page_phrase_corrections=2, premature_opening_corrections=1,
            direct_speech_QA_sheets=40, direct_menu_QA_sheets=4, typed_caption_native_andvisual_pass=True,
            fresh_distinct_menus=4, exact_complete_menu_reuses=6, all21_caption_bindings_pass=True,
            all_speech_native_andvisual_checks_pass=True, native_qualified_alignment_cases=1408,
            within_batch_exact_record_proofs_reused=287, final_resume_records_fresh=65,
            scoped_name_native_andvisual_pass=False, stored_reconstruction_gameplay_andregistered_release_pending=True,
            all_individual_fifth_formatting_gates_pending=True, actual_new_batch_gameplay=False,
            manuscript=str(MANUSCRIPT), manuscript_sha256=sha(MANUSCRIPT.read_bytes()),
            scoped_names=str(NAMES), scoped_names_sha256=sha(NAMES.read_bytes()),
            speech_display_checkpoint=str(DISPLAY / 'visual_approval.json'), speech_display_checkpoint_sha256=sha((DISPLAY / 'visual_approval.json').read_bytes()),
            no_QA_waiver_orprose_shortening=True, no_live_job=True, new_credit=0, full_goal_complete=False, guide_photos=False),
        summary=summary, document='docs/editorial_hodram_B191_B210_prose_display_20261104.md', document_text=text, completed=9933,
        protected={'translations/release_stack.json': release['registry_sha256'], release['candidate']: release['candidate_sha256'],
            'out/raphael_natural_v2_accepted_base.nds': '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'})
    print('Saved 373-comparison/355-page checkpoint; no completion credit; 9933 preserved; full goal active.')
