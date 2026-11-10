"""Seal the complete contextual and native visual review without integration credit."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint

A = Path('work/analysis')
PROSE = Path('translations/rafael_B177_B180_contextual_review_v2.json')
DOC = Path('translations/rafael_B177_B180_formatting_manuscript_v2.json')
NAMES = Path('translations/rafael_B177_B180_scoped_names_review_v1.json')
IDENTITY = A / 'Rafael_B177_B180_current1424_20261105/names_and_terms_v1.json'
PREF = Path('translations/rafael_B177_B180_visual_preferences_v8.json')
PLAN = A / 'Rafael_B177_B180_automatic_layout_v8_20261105/automatic_plans.json'
BASE_PLAN = A / 'Rafael_B177_B180_automatic_layout_v4_20261105/automatic_plans.json'
NATIVE = [A / f'Rafael_B177_B180_native_v{i}_20261105/compiled_native_pages.json' for i in (1, 2, 3)]
TERMINALS = [A / f'Rafael_B177_B180_native_gc_v{i}_20261105/completion.json' for i in (1, 2, 3)]
MENUS = A / 'Rafael_B177_B180_native_menus_v2_20261105/complete_choice_objects.json'
CAPTIONS = A / 'Rafael_B177_B180_caption_visual_v1_20261105/receipt.json'
PACKAGE = A / 'Weekend_testing_package_Rafael1424_20261105/package_verification.json'
RELEASE = A / 'Rafael1424_extended_release_verified_v2_20261105/registered_release_verification.json'
OUT = A / 'Rafael_B177_B180_offline_review_v1_20261105'


def digest(path):
    return sha(Path(path).read_bytes())


def verified_pages(row):
    display = row['complete_native_English_display']
    assert len(row['native_alignment']['cases']) == 4
    if row['kind'] == 'system-FE':
        assert display['all_first_internal_final_ASCII_CP932_codes_andindependent_logical_plane_exact']
        assert digest(display['native_logical_plane']) == display['native_logical_plane_sha256']
        pages = [display]
    else:
        assert display['all_visible_first_internal_final_characters_in_order'] and display['no_blank_or_overlap_page']
        pages = display['pages']
        assert all(p['native_independent_plane_equal'] for p in pages)
    for page in pages:
        for key in ['native_plane', 'preview']:
            assert digest(page[key]) == page[key + '_sha256']
    return len(pages)


def main():
    assert not OUT.exists()
    prose, doc, names, identity, plans, baseline, menus, captions, package, release = map(
        load, [PROSE, DOC, NAMES, IDENTITY, PLAN, BASE_PLAN, MENUS, CAPTIONS, PACKAGE, RELEASE])
    assert len(prose['records']) == len(doc['records']) == 183
    assert (prose['proposed_revisions'], prose['justified_retentions']) == (133, 50)
    assert len(prose['current_glyph_defect_records']) == 7 and len(prose['glyph_only_revisions']) == 3
    assert all(r['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
        for r in doc['records'] + names['records'])
    assert len(names['records']) == 9 and doc['runtime'] == identity['runtime'] == names['runtime']
    assert doc['marked_FI_substitutions'] == 4
    assert plans['manuscript_sha256'] == digest(DOC) and plans['visual_preferences_sha256'] == digest(PREF)
    assert not plans['failures'] and not any(i['severity'] != 'info' for r in plans['records'] for i in r['base_QA']['issues'])

    full, revised, final_one = map(load, NATIVE)
    for native, terminal, alignments in zip([full, revised, final_one], TERMINALS, [700, 40, 4], strict=True):
        done = load(terminal)
        assert done['terminal'] and done['completed_without_exception'] and done['all_locked_sources_unchanged']
        assert native['runtime'] == doc['runtime'] and native['font_sha256'] == full['font_sha256']
        assert native['fresh_compiled_alignments'] == alignments
        assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
        assert native['complete_consumption_andpagination_exact']
    assert full['plan_sha256'] == digest(BASE_PLAN)
    assert (len(full['records']), full['pages'], len(revised['records']), revised['pages'], final_one['pages']) == (175, 186, 10, 15, 2)

    native = {row['id']: row for proof in [full, revised, final_one] for row in proof['records']}
    baseline_plans = {r['id']: r for r in baseline['records']}
    records = [native[row['id']] for row in plans['records']]
    drafts = {r['id']: r for r in doc['records']}
    changed = set()
    pages = 0
    for planned, bound in zip(plans['records'], records, strict=True):
        key = planned['id']
        assert bound['compiled_hex'] == planned['encoded_hex'] and bound['logical_English'] == drafts[key]['english']
        assert all(bound[k] == drafts[key][k] for k in ['source_reference', 'current_reference', 'kind'])
        page_count = verified_pages(bound)
        assert page_count == planned['expected_native_pages']
        pages += page_count
        if baseline_plans[key]['encoded_hex'] != planned['encoded_hex']:
            changed.add(key)
    assert len(records) == 175 and pages == 186
    assert len(changed) == 10 and changed == {row['id'] for row in revised['records']}
    assert final_one['records'][0]['id'] == 'DK4_MES_B179_R0122'
    body_sheets = full['review_sheets'] + [s for s in revised['review_sheets'] if s['block'] != 179] + final_one['review_sheets']
    assert len(full['review_sheets']) == 17 and len(body_sheets) == 21

    assert menus['all_checks_pass'] and menus['physical_caption_records'] == 8
    assert (menus['native_provider_alignments'], menus['bridged_modal_returns'], menus['complete_reviewed_caption_style_planes']) == (24, 72, 16)
    assert captions['planes'] == 28 and captions['provider_sha256'] == digest(MENUS)
    menu_sheets = [obj['review_sheet'] for obj in menus['objects']]
    menu_sheets.append(dict(path=captions['sheet'], sha256=captions['sheet_sha256']))
    for sheet in body_sheets + menu_sheets:
        assert digest(sheet['path']) == sheet['sha256']
    for obj in menus['objects']:
        receipt = load(obj['receipt'])
        assert digest(obj['receipt']) == obj['receipt_sha256'] and receipt['runtime'] == doc['runtime']
        assert receipt['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
        assert len(receipt['compiler_negatives_rejected']) == 7 and digest(obj['compiled_path']) == obj['compiled_sha256']
        original = load(receipt['manuscript'])
        assert original['records'] == [drafts[key] for key in obj['record_ids']]

    OUT.mkdir()
    proof = OUT / 'compiled_native_pages.json'
    evidence = {str(path): digest(path) for path in [PROSE, DOC, NAMES, IDENTITY, PREF, PLAN, BASE_PLAN,
        *NATIVE, *TERMINALS, MENUS, CAPTIONS, PACKAGE, RELEASE, Path(__file__)]}
    save(proof, {**full, 'manuscript': str(DOC), 'manuscript_sha256': digest(DOC),
        'plan': str(PLAN), 'plan_sha256': digest(PLAN), 'records': records, 'pages': pages,
        'fresh_compiled_alignments': 44, 'final_required_compiled_alignments': 700,
        'exact_reused_records': 165, 'exact_reused_pages': 171, 'final_fresh_records': 10,
        'final_fresh_pages': 15, 'retired_baseline_record_IDs': sorted(changed),
        'review_sheets': body_sheets, 'direct_visual_review_pending': False,
        'all_final_186_body_pages_directly_viewed': True, 'caption_sheets_directly_viewed': menu_sheets,
        'all_16_reviewed_caption_style_planes_directly_viewed': True, 'actual_gameplay': False,
        'stored_script_and_representative_gameplay_pending': True, 'new_credit': 0, 'evidence': evidence})
    assert package['ROM_sha256'] == release['candidate_sha256'] == doc['current_ROM_sha256']

    summary = ('Rafael B177–B180 contextual review covers 183 records: 133 proposed revisions and 50 justified retentions. '
        'Seven current glyph defects have corrections, including three wording-preserving fixes. All four prose gates pass. '
        'All 175 speeches and 186 final native pages passed and were visually reviewed. All eight choice labels passed '
        'provider and both caption style checks, and nine public names or roles were individually retained. '
        'Stored script, focused gameplay, final gates and integration remain pending. The 558 B161–B176 records remain at clean inventory. '
        'The 13,269 integrated count, 5d40f920 candidate, weekend packages and designated main are unchanged.')
    detail = f"""# Rafael B177–B180 contextual and offline display checkpoint

All four exchanges are reviewed from clean Japanese and bound to the registered current English. The [183-record manuscript](../{PROSE.as_posix()}) has exact record references, individual findings, 133 proposed revisions and 50 justified retentions. All four prose gates pass. All fifth gates remain pending.

- **Cesare and the Elysion.** Preserve his love of the ship, his request to sail aboard and his explicit disavowal of a claim for its return. Use Cesare Tony consistently. Restore the one percent share example, three ship-price ranges, refit limit and distinct cargo versus supply holds.
- **Fernando's coin game.** Correct the last-coin strategy, the five-to-one and nine-to-five examples, the two corrupted choice labels and the stray leading character in the arithmetic reply. Restore Fernando Dias's full introduction. The couple's argument establishes a breakup and supports Man and Woman without adding marriage or another status.
- **Manuel's refit lesson.** Restore his spoken given name and use the active room and role names, including Speech, First Mate's Office, Chapel, Galley, Nursery, Surgeon, Sickbay, Cabin, Lounge and Lumber Room. Preserve the assignments that make each room useful and the distinction between work at sea and at the shipyard.
- **Sailing lesson.** Preserve the instructor's informal voice and the source mechanics. Medium and larger ships can fit a spritsail. Only large ships can fit a jigger spanker. Preserve the equipment orientation and wind comparison.

The exact [public names and roles](../{NAMES.as_posix()}) were reviewed individually. Three original getter pairs were fresh and six exact dependencies were reused. No name table changes. Nameplate and full-catalogue render observations outside the named getter scope remain separate. Four FI substitutions are still dynamic and rendered Rafael in all four native alignments. Seven current records have unintended glyphs and three keep every word while correcting the letter form. Two source ellipses remain as intentional silence.

**Display.** The [final wrapping plans](../{PLAN.as_posix()}) pass without warnings or errors. All 186 final body pages were viewed on readable contact sheets. Ten records received revised wrapping or wording after the first full render, and the other 165 records reused exact compiled bytes and rendering proofs. The final version gives Manuel's at-sea and shipyard instructions separate pages. All price ranges, key phrases and final page starts were reread. The original FE unlock notice was checked on its separate painter. No ordinary break was hand-authored, and no viewport or engine changes were needed. The [combined native proof](../{proof.as_posix()}) binds the final render and visual coverage.

Four typed choices preserve both indices and original branches. The current B177 object had spaces and zeros between labels after the terminator. Only that exact registered input was read with the historical slot allowance. New outputs still require strict zero alignment. The two old B178 mixed-glyph labels were checked with the original provider and excluded from the ASCII bitmap comparison. All eight revised or retained English labels have both native style planes checked and viewed. The 72 modal return cases are bridged offline observations. This batch has no actual story, menu-input or town gameplay coverage yet.

**Next.** Prove stored relocation, command and allocation invariants, including exact guarded ownership for the legacy B177 slot. Check representative page turns, the FE unlock and actual choices or returns in a focused emulator fixture. Record unvisited branches. Integrate only after all required gates pass, then verify the clean-input patch and credit the batch once. The other 558 B161–B176 records remain at clean inventory. Keep the full goal active, with Rafael and tutorials first.

The integrated total is 13,269. The registered candidate remains 5d40f920. The designated main and both weekend ZIPs are preserved. Deferred artwork and the later older-record technical re-audit remain separate.
"""
    checkpoint(mutation=OUT/'ledger_mutation', batch_key='Rafael_SC0_B161_B180_clean_20261105',
        batch_updates=dict(new_credit=0, independently_drafted_records=183, independent_draft_blocks=[177,178,179,180],
            remaining_clean_meanings_anddrafts=558, source_only_no_current_English_extracted=False,
            all_current_comparisons_andfive_gates_pending=False, current_comparisons=183, remaining_current_comparisons=558,
            four_prose_gate_passes=183, proposed_revisions=133, justified_retentions=50,
            manuscript=str(PROSE), manuscript_sha256=digest(PROSE), formatting_manuscript=str(DOC),
            formatting_manuscript_sha256=digest(DOC), final_visual_preferences=str(PREF), final_layout=str(PLAN),
            final_layout_sha256=digest(PLAN), final_offline_native_proof=str(proof), final_offline_native_proof_sha256=digest(proof),
            native_body_records=175, native_body_pages_directly_viewed=186, native_caption_records=8,
            reviewed_caption_planes_directly_viewed=16, exact_current_glyph_defects=7, glyph_only_revisions=3,
            individually_retained_public_names=9, stored_relocation_pending=True, representative_gameplay_pending=True,
            all_fifth_formatting_gates_pending=True, registered_integration_pending=True, evidence=evidence),
        additional_updates={'editorial_execution_priority_20261104': dict(new_credit=0,
            current_batch='Rafael B177–B180 contextual and offline display review complete; stored and representative tests next.',
            new_source_meanings=183, new_independent_drafts=183, new_current_comparisons=183,
            current_batch_not_yet_integrated=True, native_job_live=False, registered_build_live=False, guide_photos=False,
            next_action='Use the exact final page and choice receipts for B177–B180 stored relocation and representative tests.')},
        summary=summary, document='docs/editorial_Rafael_B177_B180_offline_checkpoint_20261105.md',
        document_text=detail, completed=13269, protected={
            'translations/release_stack.json':release['registry_sha256'],
            'dk4tool/rom/nds.py':'27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
            release['canonical_base']:release['canonical_sha256'], release['candidate']:release['candidate_sha256'],
            package['zip']:package['zip_sha256'], 'out/Translation_DS_Weekend_Test_2026-11-05.zip':
                load(A/'Weekend_testing_package_v1_20261105/package_verification.json')['zip_sha256']})
    print('Saved 183 contextual decisions and verified 186 final body pages and all eight captions. No new release or credit.')


if __name__ == '__main__':
    main()
