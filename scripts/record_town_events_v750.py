"""Record reviewed entries, open category/specialty work and exact integrated evidence."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.record_memory_streams_v682 import copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/town_events_v750')
ROM = Path('out/all_routes_combined_v750_candidate.nds')
LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/town_events_v750_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V750 Town events')


def main():
    native, registered, gameplay, patch, context = (read(ROOT / name) for name in (
        'native_review.json', 'registered_verification.json', 'gameplay_verification.json', 'patch_proof.json', 'native_context.json'))
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert len(native['all257_complete_printf_wrap_and_native_font_cases']) == 257
    assert registered['complete_native_copy_count'] == 122 and all(registered['meaningful_rejection_controls'].values())
    assert {r['message_id'] for r in gameplay['actual_dialogue_observations']} == {738, 739, 740, 741}
    assert len(gameplay['actual_dialogue_observations']) == 10
    assert sum(map(len, gameplay['whole_two_screen_equal_baseline_controls'].values())) == 50
    assert len(gameplay['ordinary_New_Game_terminal4000_frame_and7_whole_frame_pairs']) == 7
    assert patch['whole_ROM_byte_exact']
    assert sha(ROM.read_bytes()) == manifest['candidate_sha256'] == gameplay['candidate_sha256'] == patch['candidate_sha256']
    assert context['script_sha256'] == sha(Path('scripts/verify_town_event_context_v750.py').read_bytes())
    doc = read('translations/town_events_release_manuscript_v1.json')
    assert len(doc['records']) == 11 and len(native['revised_IDs']) == 8 and len(native['retained_wording_IDs']) == 3
    ledger = read(LEDGER)
    assert ledger['records_editorially_completed'] == 74 and ledger['records_revised_and_integrated'] == 48
    save(ROOT / 'editorial_ledger_at_V749.json', ledger)
    family = 'Square-trend-relief-promoter-entries731-741'
    ledger['completed_editorial_families'].append({'id': family, 'native_message_IDs': list(range(731, 742)),
        'records': [{'message_id': r['message_id'], 'decision': 'revised-and-integrated' if r['decision'] == 'revise' else 'retain-wording',
            'manuscript': 'translations/town_events_release_manuscript_v1.json',
            'complete_clean_source_native_context_and_font_verified': True,
            'complete_fixture_gameplay_display_verified': r['message_id'] in (738, 739, 740, 741)} for r in doc['records']],
        'broader_trend_family653_655_and730_remains_open': True,
        'editorial_and_integration_review_complete_with_targeted_fixture_gameplay_sample': True,
        'proof': str(ROOT / 'proof.json'), 'candidate_sha256': manifest['candidate_sha256']})
    ledger.update({'records_editorially_completed': 85, 'records_revised_and_integrated': 56,
        'retained_wordings_editorially_completed': 29, 'records_with_source_and_prose_pass': 93,
        'records_with_source_prose_drafts_including730_pending_naturalness': 94})
    image = NdsImage.open(ROM)
    common, arm = image.read_file('/COMMON/MESFILE.DK4'), image.read_file('/__arm9__.bin')
    entries = common_message_entries(common, arm, clean=False)
    placeholders = [r.message_id for r in entries if b'Here is some local information.' in r.text]
    assert placeholders == []
    ledger['current_integrated_candidate'] = {'path': str(ROM), 'sha256': manifest['candidate_sha256'], 'profile': manifest['profile'],
        'MESFILE_sha256': sha(common), 'ARM9_sha256': sha(arm), 'patch_sha256': patch['patch_sha256'],
        'status': 'experimental', 'manifest': str(ROM.with_suffix('.manifest.json')),
        'initial_source_pins_retained_as_V743_reference_not_overwritten': True}
    ledger['latest_checkpoint'] = 'V750 entries731-741 reviewed:8 revised,3 retained;last8 exact local-information placeholders restored;730 category prose and broader trend/specialty contexts remain open'
    ledger['coverage_units'][0]['completed_families'].append(family)
    ledger['coverage_units'][0]['next'] = 'Finish related trend entries653-655, readable category expansion730 and local-specialty/shop replies742-746; continue shared dialogue then all routes. Source drafts exist for these9 entries; formatting/context gates remain open as recorded.'
    for finding in ledger['findings']:
        if finding['id'] == 'COMMON-remaining-local-information-placeholders':
            finding.update({'native_message_ids': [], 'status': 'exact-phrase-restorations-integrated-V750',
                'detail': 'V750 restores the last8 exact local-information phrase matches. This bounded zero-result scan does not prove every other placeholder, wording or formatting defect is fixed.'})
    ledger['findings'].extend([
        {'id': 'COMMON-730-compact-category-arguments', 'native_message_id': 730, 'status': 'open-source-prose-draft-and18-format-only-cases',
            'detail': 'Original category getter supplies compact labels such as Cond., Delic., Med; full-sentence category meaning/readability still needs a source-faithful solution. Exact730 bytes are preserved and it is not counted complete.'},
        {'id': 'COMMON-653-655-related-trend-family', 'native_message_ids': [653, 654, 655], 'status': 'source-context-reviewed-drafts-not-integrated',
            'detail': 'Executed original5FB54 proves these earlier entries belong to the same trend selector. Draft653/654 uses number-neutral product/cargo phrasing;655 wording is retained. All124 product expansions and final native layout remain queued.'},
        {'id': 'COMMON-739-741-question-and-apology-formatting', 'native_message_ids': [739, 740, 741],
            'status': 'source-native-and-both-branches-gameplay-verified-integrated-V750',
            'detail': 'Question739 uses the original Yes/No parent with generated guarded lines.741 was revised after preview left you. alone; final apology fits one line. Original flags change after blocking dialogue closes, verified in actual RAM.'}])
    master = read('translations/town_events_editorial_manuscript_v1.json')
    for row in master['records']:
        if row['message_id'] in range(731, 742):
            row['status'] = 'reviewed-and-integrated-V750-see-release-manuscript-and-proof'
            row['integrated_evidence'] = str(ROOT / 'proof.json')
    save('translations/town_events_editorial_manuscript_v1.json', master)
    ledger['active_source_prose_drafts'] = {'native_message_IDs': [653, 654, 655, 730, 742, 743, 744, 745, 746],
        'manuscripts': ['translations/town_events_editorial_manuscript_v1.json', str(ROOT / 'related_trend_entries_653_655.json')],
        'not_completed_or_integrated_as_revisions': True}
    save(LEDGER, ledger)
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': manifest['candidate_sha256'], 'profile': manifest['profile'],
        'reviewed_IDs': list(range(731, 742)), 'revised_IDs': native['revised_IDs'], 'retained_wordings': native['retained_wording_IDs'],
        'verification_reports': {str(ROOT / f): sha((ROOT / f).read_bytes()) for f in (
            'native_context.json', 'native_review.json', 'registered_verification.json', 'gameplay_verification.json', 'patch_proof.json')},
        '730_original_bytes_preserved_format_only_not_counted_complete': True,
        'all257_native_font_planes_verified_and2_representative_preview_sheets_visually_inspected': True,
        'four_changed_messages_actual_gameplay_and_menu_town_return_images_visually_inspected': True,
        'all_prior48_revisions470_batches114_accepted_layers675_graphics_preserved': True,
        'all_canonical_bytes_source_saves_harness_core_preserved_no_promotion': True,
        'graphics_audit_and_original18_objects_unchanged': True,
        'editorial_ledger_sha256': sha(LEDGER.read_bytes()), 'remaining_exact_local_information_placeholder_IDs': [],
        'full_goal_complete': False})
    review = ['# Town events731-741: final review', '', 'Eight revisions; three retained wordings. Other draft entries remain open.', '']
    for row in doc['records']:
        review += [f'## {row["message_id"]}: {row["decision"]}', '', row['japanese'].replace('\n', ' / '), '',
            '**V749:** ' + row['current_English'], '', '**V750:** ' + row['english'].removesuffix('{PAD}'), '',
            '**Meaning:** ' + row['source_meaning'], '', '**Reason:** ' + row['localization_note'], '']
    (ROOT / 'integrated_review.md').write_text('\n'.join(review), encoding='utf-8')
    DOC.write_text(
        '# V750: trade trends, relief and traveling promoter\n\n'
        'Entries731-741 complete editorial/integration review:8 revisions and3 retained wordings. '
        'The last8 exact Here is some local information placeholders are restored. Cumulative coverage is85 '
        'completed entries,56 revisions integrated,29 retained wordings. Nine additional source/prose drafts '
        'are open:653-655,730,742-746. Full-game review remains active.\n\n'
        '## Source and wording\n\n'
        'Restore a continuing trend, uncertainty about a fading product craze, prevention of death from '
        'starvation, expected relief from stock shortages, the promoter\'s arrival acknowledgment, '
        'request for passage to any other town square, enthusiastic acceptance and courteous refusal. '
        '731/734/735 retain natural wording, using safe ASCII I where needed. Every exact Japanese and '
        'current byte selection, gloss, speaker/caller context and adaptation is recorded. '
        'The final apology is I see. I\'m sorry to impose on you. Native previews caught the first draft\'s '
        'isolated you.; the revised paragraph fits one line.\n\n'
        '## Native contracts and integration\n\n'
        '- Original clean/current code executes288 trend,432 relief and6 promoter cases each. '
        'The trend selector includes earlier653-655, discovered by executing conditional literal loads '
        'rather than assuming neighboring entries were the whole family. Initial incorrect expected '
        'branch IDs were caught and corrected before release; no ROM was changed by those probes. '
        'Relief cases cover all12 supplied town requests,18 goods categories and both sides of the '
        'five-entry threshold with the original scaling input supplied as zero. Promoter cases cover '
        '24/25 request thresholds, both answers and same/different-town arrival flags. '
        'These are declared getter/dialogue-result bridges, not earned gameplay.\n'
        '- All257 full native font planes pass:124 products for each of731/733 and9 static paragraphs. '
        'Whole glyphs and blank cells, including leading/trailing letters and every generated break, match '
        'decoded original fonts.739 uses the proven generated guarded-line compiler at original Yes/No '
        'parent53FCC. Other paragraphs use the existing post-substitution portrait wrapper. '
        'All18340 dispatch cases change only direct IDs730-741. Original730 bytes are preserved as a packed '
        'neighbor; its18 category expansions pass bounded wrapping only. It remains editorially incomplete '
        'because compact category arguments such as Cond., Delic. and Med need full-sentence localization.\n'
        '- Complete122 native warm/cold copies and seven malformed-input controls pass. All3668 IDs, '
        'NUL owners and cache allocations remain. Only COMMON block9, ARM9 native message offsets and '
        'the owned28-byte dispatcher differ from V749. All40 other blocks, prior48 prose revisions, '
        '675 graphics, every other internal file, startup/helper/pool/arena extents remain exact. '
        'No executable section or staged payload grows. Registered470-batch/114-accepted-layer build '
        'passes final guards; clean-input xdelta reconstructs every ROM byte exactly.\n\n'
        '## Actual gameplay verification\n\n'
        'Six terminal6501-frame cold boots pair V749/V750 for acceptance, refusal and arrival. '
        'The isolated request fixture changes four original event/stock bytes in Istanbul and supplies '
        'Olive Oil with the original request parameter25. The arrival fixture changes one travel-flag byte, '
        'leaving the original tracked different-town value74. Original saves are not edited; fixtures change no code, inventory, money or '
        'location. This tests original event paths, not earned travel or ordinary relief.\n\n'
        'Ten actual holds cover full738/739/740/741. Every glyph and blank plane pixel matches; every '
        'other pixel, including Yes/No buttons and portrait, matches its paired baseline. Whole resident '
        '4032-byte native blocks are unique and exact. Fifty whole two-screen control/menu/town-return '
        'pairs match. Original acceptance sets the travel flag, refusal leaves it clear, and arrival clears '
        'it and updates the tracked city. Actual RAM confirms these transitions after the blocking dialogue '
        'closes; the first verification expectation incorrectly checked effects during the dialogue hold '
        'and was corrected from source control order. Original675/676 displays remain exact.\n\n'
        'An ordinary4000-frame New Game cold boot without save or fixtures matches seven complete V749 '
        'frames through the opening story. The other seven new entries have full source/native evidence, '
        'not claimed live trend/relief events. No hardware or full-route playthrough is claimed.\n\n'
        '## Reproduction and remaining work\n\n'
        f'- Candidate: `{ROM}`\n- SHA-256: `{manifest["candidate_sha256"]}`\n'
        f'- Canonical base: `{manifest["base_rom"]}`\n- Base SHA-256: `{manifest["base_sha256"]}`\n'
        f'- Profile: `{manifest["profile"]}` (experimental)\n'
        f'- Patch: `{ROM.with_suffix(".xdelta")}`\n- Patch SHA-256: `{patch["patch_sha256"]}`\n'
        f'- Clean input SHA-256: `{patch["clean_source_sha256"]}`\n\n'
        'The manifest lists all inherited layers and canonical-base changes. User cold-boot review should '
        'cover New Game, shop text, promoter Yes/No responses, arrival and closing to menus. '
        'Explicit user acceptance is still required for canonical promotion. ROM/patch are on E through out; '
        'controlled screenshots have provenance under Screenshots/Test fixtures/V750 Town events.\n\n'
        'Finish source-faithful full category naming730, product-variable653-655 and specialty/shop '
        'contexts742-746 next. Zero exact local-information matches does not prove all other placeholders '
        'or prose correct. All routes and remaining shared/help/player-facing prose remain open. '
        'Separate graphics audit,18 plaque objects, Online exclusions, brown marks and the later older-record '
        'follow-up remain unchanged. The first unpublished V750 draft and its superseded manifest/config '
        'are preserved as research only. No producer was modified while its build/capture was live.\n', encoding='utf-8')
    summary = ('\n\n## V750: trends, relief and promoter passage\n\n'
        'Eleven entries731-741 reviewed:8 revised,3 retained;last8 exact local-information placeholders restored. '
        'Original288 trend/432 relief/6 promoter cases per clean/current,257 complete native font planes, '
        '122 native copies and seven rejection controls pass. Six paired6501-frame controlled cold boots '
        'verify10 full738-741 holds,Yes/No controls,post-dialogue flag/city transitions and50 unchanged '
        'menu/town/control frames. Ordinary New Game matches seven V749 frames. Registered470/114 combined '
        'V750 and exact clean patch preserve prior prose/art with no growth. Total85 completed,56 revised,29 retained; '
        'nine additional source drafts and broad shared/routes remain open.730 has formatting-only coverage, '
        'not editorial completion. Experimental; canonical/saves/graphics audit unchanged. '
        'See [V750 checkpoint](town_events_v750_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert '## V750: trends, relief and promoter passage' not in text
        path.write_text(text.rstrip() + summary, encoding='utf-8')
    save('out/editorial_review_latest.json', {**ledger['current_integrated_candidate'], 'details': str(DOC), 'full_goal_complete': False})
    shots = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V750 Town events')
    seen = set()
    for row in gameplay['actual_dialogue_observations']:
        if row['message_id'] in seen:
            continue
        seen.add(row['message_id'])
        copy(Path(row['capture']['path']), shots / f'COMMON_{row["message_id"]}_{row["mode"]}_controlled.png')
    copy(Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_v750_accept_new/frame_006500_cold_boot.png'), shots / 'town_return_controlled.png')
    save(shots / 'provenance.json', {'candidate_sha256': manifest['candidate_sha256'], 'explicit_original_event_RAM_fixtures': True,
        'ordinary_transport_relief_progress_or_publication_approval_not_claimed': True,
        'gameplay_proof': str(ROOT / 'gameplay_verification.json'), 'files': {p.name: sha(p.read_bytes()) for p in shots.glob('*.png')}})
    files = [DOC, LEDGER, ROOT / 'proof.json', ROOT / 'editorial_ledger_at_V749.json',
        Path('translations/town_events_editorial_manuscript_v1.json'), Path('translations/town_events_release_manuscript_v1.json'),
        Path('translations/town_events_editorial_release_v1.json'), Path('dk4tool/patch/town_events_editorial.py'),
        *(ROOT / f for f in ('source_context_packet.json', 'review.md', 'integrated_review.md', 'native_context.json', 'native_review.json',
            'runtime_names.json', 'registered_verification.json', 'gameplay_verification.json', 'patch_proof.json',
            'related_trend_entries_653_655.json', 'category_full_names_review_pending.json',
            'native_previews_1_2x.png', 'native_previews_2_2x.png', 'fixture_preflight_request.json', 'fixture_preflight_arrival.json')),
        *(Path('scripts') / f for f in ('prepare_town_events_v750.py', 'verify_town_event_context_v750.py',
            'prepare_town_event_release_v750.py', 'verify_town_event_release_v750.py', 'verify_town_event_gameplay_v750.py',
            'native_promoter_travel_fixture_v750.py', 'run_promoter_travel_capture_v750.py')), Path(__file__)]
    for path in files:
        copy(path, ARCHIVE / path.name)
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': manifest['candidate_sha256'],
        'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir() if p.is_file() and p.name != 'provenance.json'},
        'full_goal_complete': False})
    for name, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / name).read_bytes()) == digest
    print('V750 recorded:85 completed entries,56 revised,29 retained;9 source drafts still open;full goal active.', flush=True)


if __name__ == '__main__':
    main()
