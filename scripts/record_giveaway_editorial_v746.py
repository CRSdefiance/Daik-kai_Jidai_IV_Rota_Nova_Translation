"""Record a complete source-reviewed family and narrowly scoped gameplay evidence."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.record_memory_streams_v682 import copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/giveaway_editorial_v746')
ROM = Path('out/all_routes_combined_v746_candidate.nds')
LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/giveaway_editorial_v746_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V746 Giveaway confirmations and announcements')
REVISED = [660, 662, 663, 664, 665, 668, 671]
FAMILY = list(range(659, 675))


def main():
    registered = read(ROOT / 'registered_verification.json')
    gameplay = read(ROOT / 'gameplay_verification.json')
    patch = read(ROOT / 'patch_proof.json')
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert registered['complete_copy_case_count'] == 122
    assert all(registered['meaningful_rejection_controls'].values())
    assert {r['message_id'] for r in gameplay['fixture_native_message_displays']} == {665, 673, 674}
    assert len(gameplay['all15_unique_confirm_and_announcement_entries_post_runtime_wrapper_native_planes']) == 15
    assert len(gameplay['whole_two_screen_equal_baseline_frames']) == 15
    assert len(gameplay['New_Game7_whole_frame_pairs_exact']) == 7
    assert patch['whole_ROM_byte_exact']
    assert sha(ROM.read_bytes()) == manifest['candidate_sha256'] == patch['candidate_sha256'] == gameplay['candidate_sha256']
    before = read(LEDGER)
    assert before['records_editorially_completed'] == 9 and before['records_revised_and_integrated'] == 7
    assert not (ROOT / 'editorial_ledger_at_V745.json').exists()
    save(ROOT / 'editorial_ledger_at_V745.json', before)
    ledger = read(LEDGER)
    records = []
    for i in FAMILY:
        records.append({
            'message_id': i, 'decision': 'revised-and-integrated' if i in REVISED else 'retain-wording',
            'source_and_prose_review': 'translations/shop_town_editorial_manuscript_v1.json',
            'revised_manuscript': 'translations/giveaway_editorial_manuscript_v1.json' if i in REVISED else None,
            'complete_native_source_selection_and_copies_verified': True,
            'complete_post_runtime_wrapper_font_plane_verified': i != 674,
            'complete_fixture_gameplay_display_verified': i in (665, 673, 674),
            'ordinary_earned_role_gameplay_not_claimed': True,
            'context': 'Original role10 Distribute Goods sequence; eight confirmation/announcement voice slots, missing confirmation slot3 fallback659, direct customer674.'})
    ledger['completed_editorial_families'].append({
        'id': 'Square-free-distribution-confirmations-and-announcements', 'native_message_IDs': FAMILY,
        'records': records, 'editorial_and_integration_review_complete_with_targeted_fixture_gameplay_sample': True,
        'proof': str(ROOT / 'proof.json'), 'candidate_sha256': manifest['candidate_sha256'],
        'all_voice_slots_original_native_selector_verified_not_all_actors_played': True})
    ledger['records_editorially_completed'] = 25
    ledger['records_revised_and_integrated'] = 14
    ledger['retained_wordings_editorially_completed'] = 11
    ledger['initial32_native_IDs_still_pending_context_or_formatting'] = list(range(675, 682))
    image = NdsImage.open(ROM)
    ledger['current_integrated_candidate'] = {
        'path': str(ROM), 'sha256': manifest['candidate_sha256'], 'profile': manifest['profile'],
        'MESFILE_sha256': sha(image.read_file('/COMMON/MESFILE.DK4')),
        'ARM9_sha256': sha(image.read_file('/__arm9__.bin')), 'patch_sha256': patch['patch_sha256'],
        'status': 'experimental', 'manifest': str(ROM.with_suffix('.manifest.json')),
        'initial_source_pins_retained_as_V743_reference_not_overwritten': True}
    ledger['latest_checkpoint'] = 'V746 distribution family: seven revisions, nine retained wordings; source/native variants and disclosed role-fixture gameplay verified'
    ledger['coverage_units'][0]['completed_families'].append('Square-free-distribution-confirmations-and-announcements')
    ledger['coverage_units'][0]['next'] = 'Independent promotion pitches675-681, including two split siblings and post-substitution layouts; country briefing688 queued.'
    save(LEDGER, ledger)
    reports = {str(ROOT / f): sha((ROOT / f).read_bytes()) for f in (
        'native_review.json', 'registered_verification.json', 'gameplay_verification.json', 'patch_proof.json')}
    save(ROOT / 'proof.json', {
        'candidate': str(ROM), 'candidate_sha256': manifest['candidate_sha256'], 'profile': manifest['profile'],
        'seven_revised_native_IDs': REVISED, 'nine_retained_wordings': [i for i in FAMILY if i not in REVISED],
        'all16_source_and_prose_decisions_reviewed': True, 'verification_reports': reports,
        'native_review_and_registered_reports_are_pre_capture_snapshots_superseded_by_gameplay_report': True,
        'actual_fixture_sequence665_673_674_and_native_all_voice_variants_verified': True,
        'all_other_ROM_files_and_all675_graphics_preserved_from_V745': True,
        'all114_accepted_baked_layers_and470_batches_retained': True,
        'original18_graphics_audit_objects_and_graphics_context_gaps_untouched': True,
        'canonical_baseline_unchanged_and_no_layer_promotion': True,
        'editorial_ledger_sha256': sha(LEDGER.read_bytes()), 'full_goal_complete': False})
    DOC.write_text(
        '# V746: giveaway confirmation and announcement editorial review\n\n'
        'The16-entry distribution family659-674 is source-reviewed: seven revisions '
        '(660,662,663,664,665,668,671) and nine retained wordings. Each retains the '
        'original voice and meaning while making the English natural. The running '
        'total is25 editorial entries complete:14 revisions integrated and11 retained '
        'wordings. Seven entries675-681 remain from the first32-entry prose pass. '
        'All routes and remaining player-facing prose remain open; the goal is active.\n\n'
        '## Source and display verification\n\n'
        '- Clean Japanese, canonical and current bytes are locked per revised entry. '
        'Original role10 distribution code, confirmation/announcement tables, all eight '
        'voice slots and null-actor fallback are verified in clean and current code. '
        'Confirmation slot3 is absent and falls back to659.675-681 are independently '
        'selected pitches and are outside this batch.\n'
        '- All seven new paragraphs pass native macro expansion and complete stored '
        '228x64 font planes. The inherited queued portrait wrapper normalizes LF/guards '
        'and wraps again after expansion: all15 unique confirmation/announcement '
        'entries additionally pass complete final-runtime-wrapper font planes, '
        'including every blank cell, first/final character and unchanged word sequence. '
        'The actual665 display wraps after "as"; it is complete and matches the '
        'existing formatter. Stored preview rows alone are not gameplay layout proof.\n'
        '- All59 block8 entries and two neighboring boundaries pass both warm/cold '
        'original native copies:122 complete cases, with SDK I/O bridged to exact bytes. '
        'Five malformed-policy/source/family/break/macro rejection controls pass.\n'
        '- Two terminal8001-frame DeSmuME cold boots use identical controls and protected '
        'Istanbul donor-save copies. A disclosed three-byte Chapel/Manuel assignment '
        'fixture is applied at3200; each receipt is reproduced from the captured4MiB '
        'RAM. Only unused room type and two assignment slots change. Native getters '
        'verify Manuel23, style7 and original two-slot cargo. This does not demonstrate '
        'earned qualifications, ordinary refitting or normal role acquisition.\n'
        '- Actual confirmation665 at4800/5200, retained announcement673 at6800 and '
        'customer674 at7200 have exact complete glyph/blank-paper masks. Full block8 '
        'is byte-exact and uniquely resident at each hold. Choice buttons and all '
        'pixels outside dialogue text match baseline. The other15 unique complete '
        'two-screen frames match, including distribution and Square return. Cargo '
        'decreases2 to0 through original controls. Six other revised voices have '
        'native component evidence, not claimed ordinary actor playthroughs.\n'
        '- A separate terminal4000-frame New Game cold boot uses no save or fixture; '
        'all seven comparable complete frames match V745. No hardware test or full '
        'playthrough is claimed. Original donor save is unchanged.\n'
        '- Registered470-batch/114-layer builder and final guards pass. Only COMMON '
        'and ARM9 native message-offset metadata differ from V745. All previous '
        'business revisions, all675 graphics, executable code, fonts, cache sizes, '
        'overlays and all other internal files remain exact. The clean-source xdelta '
        'reconstructs every candidate byte.\n\n'
        '## Reproduction and handoff identity\n\n'
        f'- Candidate: `{ROM}`\n- Candidate SHA-256: `{manifest["candidate_sha256"]}`\n'
        f'- Canonical base: `{manifest["base_rom"]}`\n- Base SHA-256: `{manifest["base_sha256"]}`\n'
        f'- Profile: `{manifest["profile"]}` (experimental)\n'
        f'- Patch: `{ROM.with_suffix(".xdelta")}`\n- Patch SHA-256: `{patch["patch_sha256"]}`\n'
        f'- Clean patch-input SHA-256: `{patch["clean_source_sha256"]}`\n'
        '- Changed components relative to V745: `/COMMON/MESFILE.DK4` and '
        '`/__arm9__.bin` message-offset fields. The neighboring manifest records '
        'every inherited layer and canonical-base change.\n\n'
        'The fixture adapter reuses the frozen V623 algorithm with private globals '
        'accepting only exact V745/V746 ARM9 hashes. The historical source, its '
        'original guard tuple, emulator core and headless harness are unchanged. '
        'Receipts pin both fixture-body and adapter hashes.\n\n'
        'User cold-boot review should check New Game and the Distribute Goods '
        'confirmation, announcement, customer reply and return. Canonical promotion '
        'requires explicit user acceptance. Fixture screenshots are stored under '
        '`Screenshots/Test fixtures/V746 Giveaway`, separately from ordinary guide '
        'candidates. The graphics audit, its18 original plaques and four excluded '
        'Online bodies are unchanged.\n\n'
        '## Verification correction\n\n'
        'The first gameplay expectation used stored LF positions and correctly '
        'failed. RAM showed the inherited queued wrapper reflowing the same words. '
        'The final verifier executes that wrapper for all15 entries, independently '
        'predicts every font cell and binds its output to actual screenshots. No '
        'ROM change or waived missing-character check was needed.\n', encoding='utf-8')
    summary = ('\n\n## V746: giveaway dialogue editorial review\n\n'
        'Seven revisions and nine retained wordings complete the16-entry distribution '
        'family659-674. All15 unique confirmation/announcement entries pass final '
        'runtime-wrapper font planes;122 native copies and five rejection controls '
        'pass. Paired8001-frame cold boots with a disclosed three-byte role fixture '
        'verify full665/673/674,15 unchanged control/return frames and cargo2 to0. '
        'A fixture-free New Game run matches seven complete V745 frames. Combined '
        'V746 retains all470 batches,114 accepted layers, prior prose and675 graphics; '
        'the clean patch reconstructs byte-exact.25 editorial entries complete, '
        '14 revisions integrated;675-681, all routes and remaining prose stay open. '
        'Experimental; canonical, source saves and separate graphics audit unchanged. '
        'See [V746 checkpoint](giveaway_editorial_v746_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        p = Path('docs') / name
        text = p.read_text(encoding='utf-8')
        assert '## V746: giveaway dialogue editorial review' not in text
        p.write_text(text.rstrip() + summary, encoding='utf-8')
    save('out/editorial_review_latest.json', {
        **ledger['current_integrated_candidate'], 'details': str(DOC), 'full_goal_complete': False})
    shots = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V746 Giveaway')
    for row in gameplay['fixture_native_message_displays']:
        copy(Path(row['capture']['path']), shots / f'COMMON_{row["message_id"]}_frame_{row["frame"]}_fixture_Istanbul.png')
    save(shots / 'provenance.json', {
        'candidate_sha256': manifest['candidate_sha256'], 'source_gameplay_proof': str(ROOT / 'gameplay_verification.json'),
        'disclosed_three_byte_Chapel_and_Manuel_assignment_fixture': True,
        'ordinary_earned_crew_role_and_hardware_verification_not_claimed': True,
        'candidate_experimental': True, 'publication_approval_not_inferred': True,
        'files': {p.name: sha(p.read_bytes()) for p in shots.glob('*.png')}})
    sources = [DOC, LEDGER, ROOT / 'editorial_ledger_at_V745.json', ROOT / 'proof.json',
               *(ROOT / f for f in ('native_review.json', 'registered_verification.json', 'gameplay_verification.json',
                                    'patch_proof.json', 'fixture_adapter_preflight.json', 'inputs_distribution.json',
                                    'native_giveaway_previews_2x.png')),
               Path('translations/giveaway_editorial_manuscript_v1.json'),
               Path('translations/giveaway_editorial_release_v1.json'), Path('dk4tool/patch/giveaway_editorial.py'),
               *(Path('scripts') / f for f in ('prepare_giveaway_editorial_v746.py', 'verify_giveaway_release_v746.py',
                                              'verify_giveaway_gameplay_v746.py', 'native_missionary_fixture_v746.py',
                                              'run_giveaway_capture_v746.py')), Path(__file__),
               *ROOT.glob('native_runtime_message_*.png')]
    for source in sources:
        copy(source, ARCHIVE / source.name)
    save(ARCHIVE / 'provenance.json', {
        'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir() if p.is_file() and p.name != 'provenance.json'},
        'candidate': str(ROM), 'candidate_sha256': manifest['candidate_sha256'], 'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    print('V746 recorded: seven revised + nine retained; totals25 complete,14 revised,11 retained.', flush=True)


if __name__ == '__main__':
    main()
