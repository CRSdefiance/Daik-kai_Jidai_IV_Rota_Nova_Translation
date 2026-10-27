"""Record seven reviewed responses and retain the two unresolved source drafts."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/town_responses_v751')
ROM = Path('out/all_routes_combined_v751_candidate.nds')
LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/town_responses_v751_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V751 Town responses')


def main():
    native, registered, gameplay, patch, context = (read(ROOT / name) for name in (
        'native_review.json', 'registered_verification.json', 'gameplay_verification.json', 'patch_proof.json', 'native_context.json'))
    manifest = read(ROM.with_suffix('.manifest.json'))
    doc = read('translations/town_responses_manuscript_v1.json')
    ids = [653, 654, 655, 743, 744, 745, 746]
    assert [r['message_id'] for r in doc['records']] == ids
    assert len(native['all376_complete_native_font_cases']) == 376
    assert len(native['revised_IDs']) == 5 and len(native['retained_wording_IDs']) == 2
    assert registered['complete_native_copy_count'] == 240 and all(registered['meaningful_rejection_controls'].values())
    assert {r['message_id'] for r in gameplay['actual_dialogue_observations']} == {653, 654, 655}
    assert len(gameplay['actual_dialogue_observations']) == 6
    assert sum(map(len, gameplay['whole_two_screen_equal_baseline_controls'].values())) == 51
    assert len(gameplay['ordinary_New_Game_terminal4000_frame_and7_whole_frame_pairs']) == 7
    assert patch['whole_ROM_byte_exact']
    assert sha(ROM.read_bytes()) == manifest['candidate_sha256'] == gameplay['candidate_sha256'] == patch['candidate_sha256']
    assert context['script_sha256'] == sha(Path('scripts/verify_town_responses_context_v751.py').read_bytes())
    ledger = read(LEDGER)
    assert ledger['records_editorially_completed'] == 85 and ledger['records_revised_and_integrated'] == 56
    save(ROOT / 'editorial_ledger_at_V750.json', ledger)
    family = 'Square-related-trend-and-specialty-shop-responses'
    ledger['completed_editorial_families'].append({'id': family, 'native_message_IDs': ids,
        'records': [{'message_id': r['message_id'], 'decision': 'revised-and-integrated' if r['decision'] == 'revise' else 'retain-wording',
            'manuscript': 'translations/town_responses_manuscript_v1.json',
            'complete_clean_source_context_and_native_font_verified': True,
            'complete_fixture_gameplay_display_verified': r['message_id'] in (653, 654, 655)} for r in doc['records']],
        '730_category_sentence_and742_question_remain_open': True,
        'editorial_and_integration_review_complete_with_targeted_fixture_gameplay_sample': True,
        'proof': str(ROOT / 'proof.json'), 'candidate_sha256': manifest['candidate_sha256']})
    ledger.update({'records_editorially_completed': 92, 'records_revised_and_integrated': 61,
        'retained_wordings_editorially_completed': 31})
    ledger['current_integrated_candidate'] = {'path': str(ROM), 'sha256': manifest['candidate_sha256'], 'profile': manifest['profile'],
        'MESFILE_sha256': read('translations/town_responses_editorial_release_v1.json')['target_common_sha256'],
        'ARM9_sha256': read('translations/town_responses_editorial_release_v1.json')['target_arm9_sha256'],
        'patch_sha256': patch['patch_sha256'], 'status': 'experimental', 'manifest': str(ROM.with_suffix('.manifest.json')),
        'initial_source_pins_retained_as_V743_reference_not_overwritten': True}
    ledger['latest_checkpoint'] = 'V751 seven related trend/specialty/shop responses reviewed:5 revised,2 retained; all124 product variants verified; source drafts730/742 remain open'
    ledger['coverage_units'][0]['completed_families'].append(family)
    ledger['coverage_units'][0]['next'] = 'Finish readable full category arguments730 and dynamic Yes/No question742; continue further shared shop/town prose, then Lil and all remaining routes. These two open drafts are not the whole remaining-game inventory.'
    ledger['active_source_prose_drafts'] = {'native_message_IDs': [730, 742],
        'manuscripts': ['translations/town_events_editorial_manuscript_v1.json'], 'not_completed_or_integrated_as_revisions': True}
    for finding in ledger['findings']:
        if finding['id'] == 'COMMON-653-655-related-trend-family':
            finding.update({'status': 'source-native-all124-products-and-actual-gameplay-verified-integrated-V751',
                'detail': 'Three number-neutral merchant paragraphs preserve source intent. All124 product names per message pass full font planes and non-orphaned final rows. Actual original trend choices653/654/655 are displayed with explicit town trend/seed fixtures.'})
    ledger['findings'].append({'id': 'COMMON-742-specialty-question-runtime-formatting', 'native_message_id': 742,
        'status': 'source-context-reviewed-draft-formatting-and-integration-pending',
        'detail': 'OriginalBAD0C-BADB4 fragment proves item/product argument order, question742, acceptance743/refusal744 and the product flag. Full item eligibility/transfer is not executed by that bridge. Preserve exact742 bytes while resolving dynamic Yes/No formatting.'})
    master_path = Path('translations/town_events_editorial_manuscript_v1.json')
    master = read(master_path)
    by_id = {r['message_id']: r for r in doc['records']}
    for row in master['records']:
        i = row['message_id']
        if i in by_id:
            for field in ('english', 'speaker', 'context', 'localization_note', 'decision', 'review'):
                row[field] = by_id[i][field]
            row.update({'status': 'reviewed-and-integrated-V751-see-release-manuscript-and-proof',
                'integrated_evidence': str(ROOT / 'proof.json')})
        elif i == 742:
            row['review']['context'] = True
            row['native_context_evidence'] = str(ROOT / 'native_context.json')
    save(master_path, master)
    save(LEDGER, ledger)
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': manifest['candidate_sha256'], 'profile': manifest['profile'],
        'reviewed_IDs': ids, 'revised_IDs': native['revised_IDs'], 'retained_wordings': native['retained_wording_IDs'],
        'verification_reports': {str(ROOT / f): sha((ROOT / f).read_bytes()) for f in (
            'native_context.json', 'native_review.json', 'legacy_filter_equivalence.json', 'registered_verification.json',
            'gameplay_verification.json', 'patch_proof.json', 'disposable_save_provenance.json')},
        'all376_font_planes_verified_and2_representative_preview_sheets_visually_inspected': True,
        'three_actual_trend_messages_and_return_images_visually_inspected': True,
        'all_prior56_revisions470_batches114_accepted_layers675_graphics_preserved': True,
        'all_canonical_bytes_source_saves_harness_core_preserved_no_promotion': True,
        'graphics_audit_and_original18_objects_unchanged': True,
        '730_and742_remain_open_and742_bytes_preserved_exactly': True,
        'editorial_ledger_sha256': sha(LEDGER.read_bytes()), 'full_goal_complete': False})
    review = ['# Final town-response editorial review', '', 'Five revisions, two retained wordings. All source selections are exact.', '']
    for row in doc['records']:
        review += [f'## {row["message_id"]}: {row["decision"]}', '', row['japanese'].replace('\n', ' / '), '',
            '**V750:** ' + row['current_English'], '', '**V751:** ' + row['english'].removesuffix('{PAD}'), '',
            '**Meaning:** ' + row['source_meaning'], '', '**Reason:** ' + row['localization_note'], '', '**Context:** ' + row['context'], '']
    (ROOT / 'review.md').write_text('\n'.join(review), encoding='utf-8')
    DOC.write_text(
        '# V751: related trend and specialty/shop responses\n\n'
        'Seven entries653-655 and743-746 complete review:5 revised and2 retained wordings. '
        'Cumulative coverage is92 entries,61 revisions integrated,31 retained wordings. '
        'Category730 and dynamic specialty question742 remain open within this source packet; '
        'the wider shared, route and other player-facing prose inventory also remains open.\n\n'
        '## English and source context\n\n'
        '653 uses natural sales patter, We\'re selling ... like hotcakes!, preserving very good present sales '
        'without a stock-out or quantity claim.654 preserves arrival with the product, urgent sale and the trade house, '
        'using cargo for both plural and mass goods.655 keeps the merchant\'s rally to sell and earn a large profit '
        'as Let\'s sell ... and profit handsomely! The first draft produced short now/quickly/fortune tails for many '
        'products. Final wording is number-neutral and every expansion has a complete final row longer than8 '
        'characters when multiline.743 naturally thanks the accepting player as so kind;744 retains the stinginess '
        'insult.745 Anything else? and746 Just browsing? retain natural wording. Source Japanese, exact current/clean '
        'bytes, individual v2 gates, glosses, adaptation reasons and native references are in the manuscript.\n\n'
        'The original trend selector\'s288 supplied cases per clean/current code carry forward from V750, '
        'with exact source spans rechecked. Two original specialty response fragments per build prove the item '
        'and product argument order in742, both response choices and the product-flag write. The bridge stops '
        'before recursive propagation and supplies UI/getter/mutator results; it does not establish whole item '
        'eligibility, transfer or earned acquisition.745/746 are bound by original literal loads and direct '
        'portrait calls in the shop loop and two shop paths.742 is preserved byte-exact and remains incomplete.\n\n'
        '## Native formatting and preservation\n\n'
        '- All376 complete native font planes pass:124 products for each variable message and four static replies. '
        'Every glyph, blank cell, leading/trailing letter and generated break matches decoded game fonts. '
        'Two representative preview sheets were visually inspected. Static replies use the established guarded '
        'compiler; the three variable messages wrap after substitution.\n'
        '- All18340 ID/five-parent dispatch cases change only653-655 at the original direct portrait parent. '
        'An existing40-byte filter is rewritten in place. The reversed-subtract test preserves457-480 and the '
        'existing801/fallback behavior;25 complete native inherited-output controls pass. At the original copy '
        'entry r3 is overwritten by its own constant before input use, so the early legacy branch\'s changed '
        'caller-clobbered r3 value is not an argument change. No section, helper, startup payload, pool, arena '
        'or native cache grows. No zero-filled mutable caption buffer/resource-pointer slot is reused.\n'
        '- All240 native warm/cold copies across blocks8/9 and two boundaries, seven malformed-input controls, '
        'all3668 ID/NUL-owner invariants and original block allocations pass. Only COMMON blocks8/9, ARM9 '
        'native message offsets and the owned40 filter bytes differ from V750. All39 other blocks, prior56 '
        'revisions,675 graphics, every other internal file and platform components remain exact. '
        'Registered470-batch/114-accepted-layer integration passes all final guards. '
        'The clean-input xdelta reconstructs every ROM byte exactly.\n\n'
        '## Actual gameplay\n\n'
        'Six terminal6501-frame cold boots pair V750/V751 for town trend levels50/150 and SDK seeds2/3. '
        'A declared six-byte RAM fixture sets one original Istanbul trend pair to Olive Oil and the SDK seed; '
        'all other RAM, event tracking, inventory, money and location are unchanged. Original UI confirms '
        'Trends and chooses655,653,654 in the three cases. Six complete4600/4800 holds match every glyph and '
        'blank-plane pixel. All other pixels, including portraits and UI, match the paired baseline. '
        'Entire resident4028-byte native cache blocks are unique and exact, and the original town getter '
        'returns the intended trend value. Fifty-one whole two-screen menu/control/town-return pairs match. '
        'The exact UI RNG draw sequence is not claimed. These are controlled original trend selections, '
        'not earned creation of trends. Four specialty/shop replies have complete source/native-font '
        'coverage, not claimed earned item handovers.\n\n'
        'An ordinary4000-frame New Game cold boot without a save or fixtures matches seven complete V750 '
        'frames through the opening story. No hardware or full-route playthrough is claimed.\n\n'
        '## Reproduction\n\n'
        f'- Candidate: `{ROM}`\n- SHA-256: `{manifest["candidate_sha256"]}`\n'
        f'- Canonical base: `{manifest["base_rom"]}`\n- Base SHA-256: `{manifest["base_sha256"]}`\n'
        f'- Profile: `{manifest["profile"]}` (experimental)\n'
        f'- Patch: `{ROM.with_suffix(".xdelta")}`\n- Patch SHA-256: `{patch["patch_sha256"]}`\n'
        f'- Clean input SHA-256: `{patch["clean_source_sha256"]}`\n\n'
        'The manifest lists all inherited layers and canonical-base changes. Cold-boot user review should '
        'cover New Game, town shop text, trend replies, closing them and returning to town. Explicit user '
        'acceptance is still required for canonical promotion. ROM/patch and evidence are on E; fixture '
        'screenshots have separate provenance. The graphics audit,18 plaque objects, Online exclusions, '
        'brown marks and later older-record follow-up remain unchanged.\n\n'
        '## Diagnostic history and next work\n\n'
        'Initial probes cancelled the Trends submenu instead of confirming it and earn no dialogue credit. '
        'A separate first-row touch probe selected the Palace and also earns no credit. Final runs use '
        'ordinary A confirmation at4401 and hold the original dialogue. Automatic approval review rejected '
        'one initial run over save-mutation risk. Harness source reads the donor and writes a different '
        'isolated destination. All final runs additionally use an explicit disposable donor copy; both '
        'the protected original and disposable donor retain their exact hashes. No approval blocker remains. '
        'No producer was edited while its build or capture was live.\n\n'
        'Finish natural full category arguments730 and post-substitution Yes/No formatting742 next, then '
        'continue broader shared dialogue and every route. Zero bytes in C1A0 are a mutable caption buffer, '
        'and C680 is a resource pointer slot; they are not storage for future code or tables. Any future '
        'full-name pointers must bind actual section RAM addresses, not flat ARM9 file offsets. '
        'The full editorial goal remains active.\n', encoding='utf-8')
    summary = ('\n\n## V751: related trend and specialty/shop replies\n\n'
        'Seven entries653-655/743-746 reviewed:5 revised,2 retained. All376 complete product/static native '
        'font planes,18340 dispatch cases,25 inherited-output controls,240 native copies and seven rejection '
        'controls pass. Six controlled6501-frame paired cold boots verify all three revised trend messages, '
        'six whole text holds, resident cache and51 unchanged control/return frames. Ordinary New Game '
        'matches seven V750 frames. Registered470/114 combined V751 and exact clean patch preserve prior '
        'prose/art with no allocation growth. Total92 reviewed,61 revised,31 retained;730/742 and broad '
        'shared/routes remain open. Original/disposable saves retain exact hashes. Experimental; canonical '
        'and separate graphics audit unchanged. See [V751 checkpoint](town_responses_v751_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert '## V751: related trend and specialty/shop replies' not in text
        path.write_text(text.rstrip() + summary, encoding='utf-8')
    save('out/editorial_review_latest.json', {**ledger['current_integrated_candidate'], 'details': str(DOC), 'full_goal_complete': False})
    shots = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V751 Town responses')
    seen = set()
    for row in gameplay['actual_dialogue_observations']:
        if row['message_id'] in seen:
            continue
        seen.add(row['message_id'])
        copy(Path(row['capture']['path']), shots / f'COMMON_{row["message_id"]}_controlled.png')
    copy(Path('E:/Rota Nova translations/Generated/work/emulation_v193/responses_v751_50_2_final_new/frame_006500_cold_boot.png'), shots / 'town_return_controlled.png')
    save(shots / 'provenance.json', {'candidate_sha256': manifest['candidate_sha256'],
        'explicit_town_trend_and_RNG_data_fixtures': True, 'ordinary_trend_progress_or_publication_approval_not_claimed': True,
        'gameplay_proof': str(ROOT / 'gameplay_verification.json'), 'files': {p.name: sha(p.read_bytes()) for p in shots.glob('*.png')}})
    files = [DOC, LEDGER, ROOT / 'proof.json', ROOT / 'editorial_ledger_at_V750.json',
        Path('translations/town_responses_manuscript_v1.json'), Path('translations/town_responses_editorial_release_v1.json'),
        Path('dk4tool/patch/town_responses_editorial.py'),
        *(ROOT / f for f in ('source_context_packet.json', 'review.md', 'native_context.json', 'native_review.json', 'runtime_names.json',
            'legacy_filter_equivalence.json', 'registered_verification.json', 'gameplay_verification.json', 'patch_proof.json',
            'disposable_save_provenance.json', 'native_previews_1_2x.png', 'native_previews_2_2x.png', 'inputs_trend_final.json', 'inputs_newgame.json')),
        *(Path('scripts') / f for f in ('verify_town_responses_context_v751.py', 'prepare_town_responses_v751.py',
            'verify_town_responses_release_v751.py', 'verify_town_responses_gameplay_v751.py', 'verify_town_filter_equivalence_v751.py',
            'native_town_trend_fixture_v751.py', 'run_town_trend_capture_v751.py')), Path(__file__)]
    for path in files:
        copy(path, ARCHIVE / path.name)
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': manifest['candidate_sha256'],
        'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir() if p.is_file() and p.name != 'provenance.json'},
        'full_goal_complete': False})
    for name, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / name).read_bytes()) == digest
    print('V751 recorded:92 reviewed entries,61 revised,31 retained;730/742 and full-game review remain open.', flush=True)


if __name__ == '__main__':
    main()
