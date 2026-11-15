"""Seal the400-record prose/offline checkpoint without integration or gameplay credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.review_hodram_B311_B324_contextual_v1 import ROOT, CURRENT, OBJECTS, OUT as PROSE
from scripts.draft_hodram_B311_B324_clean_v1 import OUT as DRAFTS, MEANINGS
from scripts.prepare_hodram_B311_B324_formatting_v1 import FORMATTING, MACROS, TERMS, ROLES, NAMES, NAME_REVIEW
from scripts.save_editorial_progress_checkpoint_v7 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import PACKAGE

RELEASE = Path('work/hodram_B301_B310_release_v1/registered_release_verification.json')
REGISTRY = Path('translations/release_stack.json')
INITIAL = ROOT/'automatic_plans_v1/automatic_plans.json'
FINAL = ROOT/'visual_plan_v4/automatic_plans.json'
NATIVE = ROOT/'native_final_v4/compiled_native_pages.json'
STYLES = ROOT/'native_style_delta_v4/compiled_style_objects.json'
APPROVAL = ROOT/'offline_visual_approval_v4.json'
DOCUMENT = Path('docs/editorial_Hodram_B311_B324_offline_20261107.md')

def main():
    assert not APPROVAL.exists()
    prose, current, objects, doc, before, after, native, styles, view, package, release = map(load, [
        PROSE, CURRENT, OBJECTS, FORMATTING, INITIAL, FINAL, NATIVE, STYLES,
        ROOT/'initial_visual_review_v1.json', PACKAGE, RELEASE])
    assert len(prose['records']) == 400 and prose['counts'] == dict(revision=175, retention=225)
    assert all(r['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
               for r in prose['records'])
    assert not prose['remaining_contextual_comparisons']
    assert len(native['records']) == 387 and native['pages'] == 389 and not native['actual_gameplay']
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert native['complete_consumption_andpagination_exact']
    assert native['manuscript_sha256'] == digest(FORMATTING) and native['plan_sha256'] == digest(FINAL)
    assert native['runtime'] == current['runtime'] == objects['runtime'] == styles['runtime']
    assert native['runtime']['candidate_sha256'] == release['candidate_sha256']
    assert len(styles['objects']) == 38 and styles['plan_sha256'] == digest(FINAL)
    assert len(styles['compiler_negatives']) == 38 and objects['native_style_getter_cases'] == 304
    assert load(NAMES)['current_native_getters'] == 22 and load(NAME_REVIEW)['scoped_actors'] == 11
    assert load(ROLES)['runtime'] == load(MACROS)['runtime'] == load(TERMS)['runtime'] == current['runtime']
    assert len(load(MACROS)['logical_macro_records']) == 3
    assert len(prose['findings_requiring_fresh_display_checks']) == 10
    assert view['all389_initial_body_pages_directly_viewed'] and view['all_six_menu_sheets_directly_viewed']
    assert view['all_ten_scoped_name_strings_directly_viewed'] and view['candidate_count'] == 39
    old, new = [{r['id']: r for r in p['records']} for p in [before, after]]
    assert old.keys() == new.keys() and not after['failures']
    assert all(old[k]['logical_English'] == new[k]['logical_English'] for k in old)
    assert not any(i['severity'] in ['error', 'warning'] for r in after['records'] for i in r['base_QA']['issues'])
    changed = {k for k in old if old[k]['encoded_hex'] != new[k]['encoded_hex']}
    assert len(changed) == 27 and changed <= view['observed_layout_candidates'].keys()
    candidate_retentions = set(view['observed_layout_candidates']) - changed
    assert len(candidate_retentions) == 12
    rejected = load(ROOT/'layout_trial_retentions_v4.json')
    preferences = load(ROOT/'formatting_v1/visual_preferences_v4.json')
    original_rows = {r['id']: r for r in doc['records']}
    decisions = []
    for key, finding in view['observed_layout_candidates'].items():
        row = original_rows[key]
        if key in changed:
            reason = preferences['records'][key]['reason']
        elif key in rejected['records']:
            reason = rejected['records'][key]['reason']
        elif key == 'DK4_MES_B314_R0010':
            reason = rejected['item_question_retention']['reason']
        else:
            assert key in {'SC1_B313_STYLE_856_0', 'SC1_B313_STYLE_1252_0'}
            reason = 'The required count-on-you pair already fits the initial native continuation, so the formatter returns exactly the same bytes. Retain the checked layout.'
        decisions.append(dict(id=key, source_reference=row['source_reference'], current_reference=row['current_reference'],
            source_hex=row['source_hex'], current_hex=row['current_hex'], logical_English=row['english'],
            initial_lines=old[key]['lines'], final_lines=new[key]['lines'],
            decision='layout-revision' if key in changed else 'layout-retention', finding=reason,
            all_words_andpunctuation_exact=True, initial_encoded_hex=old[key]['encoded_hex'], final_encoded_hex=new[key]['encoded_hex']))
    final_rows = {r['id']: r for r in native['records']}
    assert final_rows.keys() == new.keys()
    assert all(final_rows[k]['compiled_hex'] == new[k]['encoded_hex'] for k in new)
    delta_sheets = load(ROOT/'layout_delta_sheets_v2/contact_manifest.json')
    assert len(delta_sheets['sheets']) == 3 and len(delta_sheets['pages']) == 39
    assert all(digest(s['path']) == s['sha256'] for s in delta_sheets['sheets'])
    final_small_sheet = ROOT/'native_missing_v4/B318_part1.png'
    assert final_small_sheet.is_file()
    # The final union selects only exact source/current/prose/runtime/font/compiled matches.
    assert list(native['origins_counts'].values()) == [360, 25, 2]
    save(APPROVAL, dict(records=400, body_records=387, final_native_pages=389,
        initial_native=str(ROOT/'native_initial_v1/compiled_native_pages.json'), initial_all389_pages_directly_viewed=True,
        all39_trial_pages_directly_viewed=True, trial_sheets=delta_sheets['sheets'],
        final_two_new_pages_directly_viewed=True, final_two_page_sheet=str(final_small_sheet),
        final_two_page_sheet_sha256=digest(final_small_sheet), final_all389_pages_directly_viewed_or_exact_reused=True,
        final_native=str(NATIVE), final_native_sha256=digest(NATIVE), layouts_revised=27, layouts_retained=12,
        layout_decisions=decisions, glyph_consistency_records=prose['findings_requiring_fresh_display_checks'],
        all_initial_andnew_pages_font_leading_trailing_characters_bounds_andpagination_reviewed=True,
        two_necessary_two_page_turns_keep_complete_final_sentences_on_second_page=True,
        no_authored_ordinary_breaks_orprose_shortening=True,
        eleven_scoped_name_retentions_ten_native_strings_viewed=True,
        thirteen_captions_six_native_menus_viewed=True,
        source_style_compilation_andall304_target_slots_qualified=True,
        source_preambles_actor0_FE_andruntime_substitutions_preserved=True,
        stored_allocation_reconstruction_andrepresentative_gameplay_pending=True,
        all400_fifth_gates_still_false=True, integrated_credit=0, actual_story_gameplay_utterances=0,
        no_new_ROM_orregistered_profile=True, full_goal_complete=False,
        evidence={str(p): digest(p) for p in [PROSE, FORMATTING, INITIAL, FINAL, NATIVE, STYLES,
            ROOT/'initial_visual_review_v1.json', ROOT/'layout_delta_sheets_v2/contact_manifest.json',
            ROOT/'layout_trial_retentions_v4.json', ROOT/'scoped_names_visual_approval_v1.json', Path(__file__)]}))
    summary = ('Hodram B311–B324 has all400 contextual decisions saved:175 proposed revisions and225 justified retentions. '
        'All387 bodies/389 final offline pages,13 captions/six menus andten name strings are native-checked and visually reviewed. '
        'Twenty-seven layouts improve;12 trial layouts are retained with reasons, andten question/silence glyph targets pass native checks. '
        'Stored reconstruction,representative gameplay andregistered integration remain. Integrated coverage stays18,367; main is unchanged.')
    document = f'''# Hodram B311–B324 offline checkpoint

{summary}

The [400-record contextual manuscript](../{PROSE.as_posix()}) contains exact clean/current references, individual findings and all four prose gates. All400 clean meanings and independent English drafts were sealed before extracting eligible current dialogue. Scope is151 ordinary speeches,236 physical alternatives/304 slots in38 voice objects and13 captions in six menus across14 complete exchanges. The [fresh exclusion reconciliation](../{(ROOT/'credited_reconciliation_after_B301_B310_v1.json').as_posix()}) checks all18,367 completed keys with zero overlap. No source, prose or integration credit is added at this checkpoint.

Corrections restore reported map/pirate information, celadon, apparent fatigue/injury, the captain’s admitted lapse, the random-recruitment callback, northern Europe, outward expedition funding and regional fleet command without an invented modern rank or ore-return requirement. Pain cries no longer acquire unsupported profanity; Pant and Mutter become vocal sounds. Samwell retains his uncertain Indian-python joke. The guide has a small boat, not an invented rowboat. The monk’s medicine, concealed illness, generosity and death retain the witness’s perspective without a named toxin or new medical explanation. Working urgent replies, greetings, the natural passed-away euphemism, religious praise and Hodram’s promise are retained with reasons.

The [offline visual approval](../{APPROVAL.as_posix()}) records every one of39 layout dispositions:27 revisions and12 retentions. The first trial’s weak final the is rejected. Later trials that create sparse openings, an isolated is-needed row, a new fine/job split or extra rows are also rejected. All words and punctuation remain unchanged. Both necessary two-page speeches now put their complete closing sentence on the second page. The item question keeps its initial fuller opening; its public Goryeo Incense Burner title remains intact and celadon explicit. No authored ordinary line breaks or allocation-driven prose shortening is introduced.

Every initial389 page was directly viewed on22 readable sheets; all39 trial pages on three sheets and the final two adjusted Rafael-encounter pages were viewed too. The [final native union](../{NATIVE.as_posix()}) qualifies360 exact initial records,25 exact trial records andtwo freshly checked final layouts against source/current references, prose, runtime, font, bytes, four alignment cases, complete glyphs, canaries and pagination. Initial native checks execute1,548 alignment cases; trial checks execute148 and the last two executeeight. These are offline checks, not gameplay. A suspected contact-sheet clipping artifact at SC1 B317 C1114 physical230 was opened individually; the full image and native events confirm complete the-ruins text. No missing glyph is established there.

All38 complete voice objects/304 slots and342 semantic rejection checks pass initially; changed compiled layouts receive fresh native target-slot checks through the final [style proof](../{STYLES.as_posix()}). All13 captions in five two-choice/one three-choice objects pass their original native providers and all six menu sheets were viewed. Eleven scoped names are retained with reasons;22 original getters pass. Allten distinct progressive name strings were viewed, withfive fresh planes andfive byte-compatible cached planes. Source actor0 is genuinely Rafael in B314/B318. Roles207/208/209/211/214/218 are bound in this candidate’s own startup:207 resolves to Hodram and unassigned companion roles fall back to Sailor151. No party assignment, roster, RNG or event override occurs. Future participants, full catalogue UI and other middle-field consumers remain unvisited. Three macro-bearing speeches pass all four original alignments, including the null-actor FE injury/treatment notice. Fourteen FE panels retain their distinct condition, sound, pause, time, handover or funding meaning.

Current registered parent remains B301–B310, SHA-256 `{release['candidate_sha256']}`. Its own fresh Hodram4,001-frame startup matches ten previously reviewed RGB captures and exports fresh RAM; it does not activate this batch’s optional scenes. There are zero observed B311–B324 story utterances yet. All400 fifth gates remain false pending storage and representative gameplay. No new ROM or profile is built here. Continue with the final v4 plan, final native union, style proof, names, menus and visual approval; do not restart clean translation, comparison or completed display checks.

Next build the source-bound mixed-object storage reconstruction, check allocation, branch relocation, complete native catalogue lookups and loaders, then run representative bounded fixtures and distinct transitions. Reuse the resolved9,216-byte QA-block limit only while its relevant consumer dependencies match; split synthetic QA sequences at complete block boundaries and never shorten production dialogue to satisfy a fixture. Then integrate through the registered cumulative workflow, exact clean-input patch and candidate-owned startup. Read build continuity, the live registry and applicable known issues before creating a ROM. All previous candidates, main, accepted baseline/layers, ASCII right-bound correction, clean input and weekend ZIP are preserved.

Integrated totals stay18,367:11,136 revisions and7,231 retentions. Historical source/prose/draft totals stay18,370. Full scope remains active across all routes, unfinished contextual passes, shared town/shop/random exchanges, labels and player-facing prose, with Rafael/tutorial priority. No guide-photo collection or main promotion. Deferred graphics artwork and the later older-record technical re-audit remain separate. No native/build process remains live.
'''
    evidence_paths = [MEANINGS, DRAFTS, PROSE, CURRENT, OBJECTS, FORMATTING, MACROS, TERMS, ROLES, NAMES, NAME_REVIEW,
        INITIAL, FINAL, NATIVE, STYLES, APPROVAL, ROOT/'own_parent_startup_v1/own_route_context.json', Path(__file__)]
    checkpoint(mutation=ROOT/'offline_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Hodram B311–B324: all400 contextual decisions and389 offline pages complete; storage/gameplay/integration pending.',
            next_action='Continue final v4 plan/native union: reconstruct and validate mixed storage, use bounded representative gameplay, then registered cumulative integration.',
            current_batch_not_yet_integrated=True, all_current_batch_fifth_gates_pending=True, registered_integration_pending=True,
            native_job_live=False, registered_build_live=False, registered_cumulative_build_live=False, guide_photos=False),
        additional_updates={'Hodram_B311_B324_clean_next_20261107': dict(new_credit=0,
            source_meanings_saved=400, localized_drafts_saved=400, current_English_comparisons=400,
            remaining_current_English_comparisons=0, source_meanings_pending=False, localized_drafts_pending=False,
            all_four_prose_gate_records=400, proposed_revisions=175, justified_retentions=225,
            no_current_English_dialogue_extracted=False, current_English_extracted_only_after_all_source_drafts_sealed=True,
            scoped_names_pending=False, scoped_name_retentions=11, scoped_native_name_getters=22,
            scoped_terms_pending=False, fresh_native_body_pages_pending=False, offline_native_pages=389,
            offline_native_body_records=387, all_final_offline_body_pages_visually_reviewed=True,
            reviewed_menu_captions=13, reviewed_menu_objects=6, reviewed_distinct_name_strings=10,
            layout_revisions=27, justified_layout_retentions=12, punctuation_consistency_records=10,
            stored_reconstruction_pending=True, representative_gameplay_pending=True, current_story_gameplay_utterances=0,
            registered_integration_pending=True, all_five_review_gates_pending=True, all_formatting_gates_pending=True,
            native_job_live=False, registered_build_live=False, contextual_manuscript=str(PROSE),
            contextual_manuscript_sha256=digest(PROSE), offline_visual_approval=str(APPROVAL),
            offline_visual_approval_sha256=digest(APPROVAL), evidence={str(p): digest(p) for p in evidence_paths})},
        summary=summary, document=DOCUMENT, document_text=document, completed=18367,
        protected={str(REGISTRY): release['registry_sha256'], release['canonical_base']: release['canonical_sha256'],
            release['candidate']: release['candidate_sha256'], release['patch']: release['patch_sha256'],
            package['zip']: package['zip_sha256']})
    print('Saved400 contextual decisions and389 reviewed offline pages; zero integration credit. Registered18,367 and full goal preserved.')

if __name__ == '__main__':
    main()
