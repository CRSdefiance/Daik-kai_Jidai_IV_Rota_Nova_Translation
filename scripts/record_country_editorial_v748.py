"""Record the full country family, explicit fixture scope and remaining placeholders."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.record_memory_streams_v682 import copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/country_editorial_v748')
ROM = Path('out/all_routes_combined_v748_candidate.nds')
LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/country_editorial_v748_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V748 Country briefings')


def main():
    native, registered, gameplay, patch = (read(ROOT / name) for name in (
        'native_review.json', 'registered_verification.json', 'gameplay_verification.json', 'patch_proof.json'))
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert len(native['all21_native_printf_macro_wrap_and_complete_font_planes']) == 21
    assert registered['complete_native_copy_count'] == 240 and all(registered['meaningful_rejection_controls'].values())
    assert {r['message_id'] for r in gameplay['actual_native_country_displays']} == {688, 708}
    assert len(gameplay['ordinary_New_Game_terminal4000_frame_cold_boot_and7_whole_frame_pairs']) == 7
    assert patch['whole_ROM_byte_exact']
    assert sha(ROM.read_bytes()) == manifest['candidate_sha256'] == gameplay['candidate_sha256'] == patch['candidate_sha256']
    doc = read('translations/country_editorial_manuscript_v1.json')
    revised, retained = native['revised_IDs'], native['retained_wording_IDs']
    assert len(revised) == 15 and len(retained) == 6
    ledger = read(LEDGER)
    assert ledger['records_editorially_completed'] == 32 and ledger['records_revised_and_integrated'] == 21
    assert not (ROOT / 'editorial_ledger_at_V747.json').exists()
    save(ROOT / 'editorial_ledger_at_V747.json', ledger)
    ledger['completed_editorial_families'].append({
        'id': 'Square-country-briefings', 'native_message_IDs': list(range(688, 709)),
        'records': [{'message_id': r['message_id'],
            'decision': 'revised-and-integrated' if r['decision'] == 'revise' else 'retain-wording',
            'manuscript': 'translations/country_editorial_manuscript_v1.json',
            'complete_clean_source_native_selector_and_font_verified': True,
            'complete_controlled_gameplay_display_verified': r['message_id'] in (688, 708),
            'ordinary_regional_travel_or_earned_share_not_claimed': True} for r in doc['records']],
        'editorial_and_integration_review_complete_with_targeted_fixture_gameplay_sample': True,
        'proof': str(ROOT / 'proof.json'), 'candidate_sha256': manifest['candidate_sha256']})
    ledger['records_editorially_completed'] = 53
    ledger['records_revised_and_integrated'] = 36
    ledger['retained_wordings_editorially_completed'] = 17
    ledger['records_with_source_and_prose_pass'] = 53
    image = NdsImage.open(ROM)
    common, arm = image.read_file('/COMMON/MESFILE.DK4'), image.read_file('/__arm9__.bin')
    entries = common_message_entries(common, arm, clean=False)
    placeholders = [r.message_id for r in entries if b'Here is some local information.' in r.text]
    assert len(placeholders) == 19 and 708 not in placeholders
    ledger['current_integrated_candidate'] = {
        'path': str(ROM), 'sha256': manifest['candidate_sha256'], 'profile': manifest['profile'],
        'MESFILE_sha256': sha(common), 'ARM9_sha256': sha(arm), 'patch_sha256': patch['patch_sha256'],
        'status': 'experimental', 'manifest': str(ROM.with_suffix('.manifest.json')),
        'initial_source_pins_retained_as_V743_reference_not_overwritten': True}
    ledger['latest_checkpoint'] = 'V748 all21 country briefings reviewed:15 revised,6 retained; Britain distinction and New World placeholder/blank page corrected'
    ledger['coverage_units'][0]['completed_families'].append('Square-country-briefings')
    ledger['coverage_units'][0]['next'] = 'Independent faction/person rumors709 onward and19 remaining exact local-information placeholders; source/caller review before route scenes.'
    for finding in ledger['findings']:
        if finding['id'] == 'COMMON-688-Britain-England-confusion':
            finding['status'] = 'source-reviewed-revised-integrated-and-controlled-display-verified-V748'
    ledger['findings'].append({'id': 'COMMON-708-placeholder-and-padding-only-extra-page', 'native_message_id': 708,
        'status': 'full-source-meaning-restored-native-and-controlled-display-verified-V748',
        'detail': 'Old109-byte placeholder consumes73 bytes on the first native page, leaving36 spaces; actual baseline6050 is blank. Revised complete country briefing is one page and exits normally.'})
    ledger['findings'].append({'id': 'COMMON-remaining-local-information-placeholders', 'native_message_ids': placeholders,
        'status': 'queued-clean-source-restoration-and-context-review',
        'detail': 'Exact current-byte scan only, not a claim that all other translation defects have been enumerated.'})
    save(LEDGER, ledger)
    save(ROOT / 'proof.json', {
        'candidate': str(ROM), 'candidate_sha256': manifest['candidate_sha256'], 'profile': manifest['profile'],
        'reviewed_country_IDs': list(range(688, 709)), 'revised_IDs': revised, 'retained_wordings': retained,
        'verification_reports': {str(ROOT / f): sha((ROOT / f).read_bytes()) for f in (
            'native_review.json', 'registered_verification.json', 'gameplay_verification.json', 'patch_proof.json')},
        'pre_capture_pending_fields_superseded_by_completed_gameplay_report': True,
        'all_prior21_revisions470_batches114_accepted_layers675_graphics_preserved': True,
        'all_canonical_bytes_source_saves_and_original_harness_core_preserved_no_promotion': True,
        'graphics_audit_and_original18_objects_unchanged': True,
        'editorial_ledger_sha256': sha(LEDGER.read_bytes()), 'remaining_exact_placeholder_IDs': placeholders,
        'full_goal_complete': False})
    DOC.write_text(
        '# V748: complete country-briefing editorial review\n\n'
        'All21 native country briefings688-708 are reviewed:15 revisions and six '
        'retained wordings. The cumulative review is53 entries,36 revisions integrated '
        'and17 wordings retained. Other shared dialogue, every route and remaining '
        'player-facing prose remain open.\n\n'
        '## Editorial decisions\n\n'
        'Britain is distinguished from constituent England. Dutch and Swedish '
        'independence, the Hanseatic discovery context, eastern-trade control, '
        'the source\'s all-churches claim, the Sultan\'s authority, the religious '
        'refusal, karma, Ming decline and dismay, Korea\'s unification and the '
        'Caribbean introduction retain their full meanings in natural English. '
        'Portugal keeps its recent maritime-dominance claim in a fluent sentence. '
        'The Cortes/Aztec/New World briefing708 is restored from Japanese instead '
        'of Here is some local information. The game\'s historical framing is '
        'preserved rather than silently modernized or qualified. Six already '
        'natural wordings remain:693,696,698,699,703,706.\n\n'
        '## Native and release evidence\n\n'
        '- The original5FA60 selector runs63 supplied flag/region cases in both '
        'clean/current code. A nonzero current-company town value selects688+region; '
        'zero selects709+region, the distinct rumor family. No adjacency is treated '
        'as sequential conversation. All21 paragraphs have individual v2 source, '
        'context, localization, naturalness and formatting gates.\n'
        '- All21 complete228x64 native font planes, including blank cells and '
        'first/final letters, match independently decoded source fonts and were '
        'visually inspected. The existing guarded portrait formatter normalizes '
        'paragraph whitespace after original macro/printf expansion. An existing '
        '28-byte dispatcher is rewritten in place to add only688-708 at direct '
        'parent54014 while preserving675-681. All18340 ID/five-parent dispatch '
        'cases differ only in the21 new direct cases. No helper, executable section, '
        'cache, startup payload, arena or pool grows.\n'
        '- All118 selections across blocks8/9 plus two neighboring boundaries '
        'pass complete warm/cold native copies:240 cases with SDK I/O bridged '
        'to exact bytes. All3668 IDs, NUL-owner identities and original block '
        'allocations are preserved. Seven malformed-input controls pass. Only '
        'COMMON, native ARM9 message-offset fields and28 owned dispatch bytes '
        'differ from V747. All39 other COMMON blocks, prior21 prose revisions, '
        '675 graphics, ARM7, overlays and every other internal file remain exact.\n'
        '- Registered470-batch/114-accepted-layer integration and final guards '
        'pass; the exact clean-source xdelta reconstructs every candidate byte.\n\n'
        '## Targeted gameplay and its limits\n\n'
        'Four terminal6500-frame cold boots pair V747/V748 for selected country '
        'indices0 and20. At5800 an explicit seven-byte RAM fixture sets a one-percent '
        'current-company market entry, a regional-selector table byte and the SDK '
        'RNG seed. Istanbul and all other bytes remain unchanged. Original getters, '
        'full-RAM receipts and actual native display bind country688 and708. These '
        'are controlled regional-dialogue tests in Istanbul; normal market-share '
        'acquisition or travel to Britain/the New World is not claimed. Core and '
        'original harness files remain unchanged; the named fixture adapter records '
        'its exact in-memory harness token changes and hashes. Original saves are '
        'unchanged.\n\n'
        'Both actual5900 paragraphs have exact full glyph/blank-paper masks; the '
        'entire source/current resident native block is byte-exact and uniquely '
        'bound in RAM (block8 for688, block9 for708). Every pixel outside the '
        'dialogue plane matches its paired baseline at those holds. Country0 '
        'also matches12 complete control/exit/town frames. Country20 matches '
        'seven pre-display whole frames. Its old placeholder has a separate '
        'pagination defect: the first native paint consumes73 of109 bytes, '
        'leaving36 spaces, and the actual6050 baseline page contains no text ink. '
        'New708 closes directly to the shop menu and then the town.\n\n'
        'Because the old blank page shifts subsequent input phase, later '
        'country20 captures are not claimed whole-frame equal to that baseline. '
        'Five new exit/return frames instead match the paired country0 return '
        'control at every pixel outside the fixed town-header region. The entire '
        'header has identical geometry under a bijective four-color substitution '
        'between the two regional fixtures; the color-selection cause was not '
        'separately traced. No ROM palette/art asset changed. This records the '
        'actual evidence rather than waiving a failed whole-frame comparison.\n\n'
        'A separate terminal4000-frame ordinary New Game cold boot, with no save '
        'or fixture, matches seven complete V747 reference frames. The other19 '
        'briefings have complete source/native-font/selector evidence, not '
        'claimed ordinary regional visits. No hardware or full-route playthrough '
        'is claimed.\n\n'
        '## Reproduction and user review\n\n'
        f'- Candidate: `{ROM}`\n- Candidate SHA-256: `{manifest["candidate_sha256"]}`\n'
        f'- Canonical base: `{manifest["base_rom"]}`\n- Base SHA-256: `{manifest["base_sha256"]}`\n'
        f'- Profile: `{manifest["profile"]}` (experimental)\n'
        f'- Patch: `{ROM.with_suffix(".xdelta")}`\n- Patch SHA-256: `{patch["patch_sha256"]}`\n'
        f'- Clean patch-input SHA-256: `{patch["clean_source_sha256"]}`\n\n'
        'The adjacent manifest lists every inherited layer and canonical-base '
        'change. User cold-boot review should cover New Game, ordinary shop '
        'dialogue, country briefings and closing them without an empty extra '
        'page. Explicit acceptance is still required for canonical promotion. '
        'Controlled screenshots are saved under Screenshots/Test fixtures/V748 '
        'Country briefings. The separate graphics audit, original18 plaque '
        'objects, Online exclusions, preserved brown marks and later older-record '
        'follow-up remain unchanged.\n\n'
        '## Remaining work and diagnostic corrections\n\n'
        f'The current exact placeholder scan leaves19 IDs: {placeholders}. '
        'These remain queued, alongside broader shared and route review. The '
        'scan is not proof that other text is correct. Initial preview tails '
        'prompted number-neutral fluent Portugal and shorter Queen/Caribbean '
        'phrasing without removing facts. The first seed3 fixture verified only '
        'one random result and actually displayed657; those runs earn no country '
        'display credit. Seed2 is confirmed by final actual688/708 masks; the '
        'number and call sites of intervening UI random draws were not traced. '
        'The initial same-input comparison also exposed the real old708 blank '
        'page; its component reproduction and revised return checks are recorded '
        'explicitly. No producer was edited while its test was running.\n', encoding='utf-8')
    summary = ('\n\n## V748: country briefings and a placeholder page restored\n\n'
        'All21 country entries688-708 reviewed:15 revised,6 retained. Britain/England '
        'is corrected and complete Cortes/Aztec/New World708 replaces a placeholder. '
        'All21 full native font planes,18340 dispatch cases,240 complete native '
        'copies and seven rejection controls pass. Four controlled6500-frame '
        'cold boots verify full688/708 and both resident cache blocks. Old708\'s '
        '36-space extra blank page is reproduced and removed; return evidence '
        'distinguishes its changed input phase and a cross-fixture header color '
        'substitution. Ordinary New Game matches seven V747 frames. Registered '
        '470/114 combined V748 and exact clean patch preserve prior prose/art. '
        'Total53 reviewed,36 revised,17 retained;19 exact local-information '
        'placeholders, remaining shared prose and all routes stay open. '
        'Experimental; canonical/saves/graphics audit unchanged. See '
        '[V748 checkpoint](country_editorial_v748_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert '## V748: country briefings and a placeholder page restored' not in text
        path.write_text(text.rstrip() + summary, encoding='utf-8')
    save('out/editorial_review_latest.json', {**ledger['current_integrated_candidate'], 'details': str(DOC), 'full_goal_complete': False})
    shots = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V748 Country briefings')
    for row in gameplay['actual_native_country_displays']:
        copy(Path(row['capture']['path']), shots / f'COMMON_{row["message_id"]}_controlled_regional_dialogue.png')
    for frame in (6050, 6500):
        copy(Path(f'E:/Rota Nova translations/Generated/work/emulation_v193/country_v748_region20_final_new/frame_{frame:06d}_cold_boot.png'),
             shots / f'COMMON_708_return_{frame}_controlled.png')
    save(shots / 'provenance.json', {'candidate_sha256': manifest['candidate_sha256'],
        'market_presence_region_and_RNG_fixture_in_Istanbul': True,
        'ordinary_travel_progress_and_publication_approval_not_claimed': True,
        'source_gameplay_proof': str(ROOT / 'gameplay_verification.json'),
        'files': {p.name: sha(p.read_bytes()) for p in shots.glob('*.png')}})
    files = [DOC, LEDGER, ROOT / 'proof.json', ROOT / 'editorial_ledger_at_V747.json',
        Path('translations/country_editorial_manuscript_v1.json'), Path('translations/country_editorial_release_v1.json'),
        Path('dk4tool/patch/country_editorial.py'),
        *(ROOT / f for f in ('source_context_packet.json', 'review.md', 'native_review.json', 'registered_verification.json',
                            'gameplay_verification.json', 'patch_proof.json', 'fixture_preflight_region0.json', 'fixture_preflight_region20.json',
                            'native_previews_1_2x.png', 'native_previews_2_2x.png')),
        *(Path('scripts') / f for f in ('prepare_country_editorial_v748.py', 'verify_and_register_country_v748.py',
                                      'verify_country_release_v748.py', 'verify_country_gameplay_v748.py',
                                      'native_country_briefing_fixture_v748.py', 'run_country_capture_v748.py')), Path(__file__)]
    for path in files:
        copy(path, ARCHIVE / path.name)
    save(ARCHIVE / 'provenance.json', {'candidate': str(ROM), 'candidate_sha256': manifest['candidate_sha256'],
        'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir() if p.is_file() and p.name != 'provenance.json'},
        'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    print('V748 recorded:53 reviewed,36 revisions integrated,17 retained;19 exact placeholders queued.', flush=True)


if __name__ == '__main__':
    main()
