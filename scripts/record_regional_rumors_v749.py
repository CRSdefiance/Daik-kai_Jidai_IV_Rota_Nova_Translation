"""Record regional editorial coverage without closing the complete-game goal."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.record_memory_streams_v682 import copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/regional_rumors_v749')
ROM = Path('out/all_routes_combined_v749_candidate.nds')
LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/regional_rumors_v749_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V749 Regional rumors')


def main():
    native, registered, gameplay, patch = (read(ROOT / name) for name in (
        'native_review.json', 'registered_verification.json', 'gameplay_verification.json', 'patch_proof.json'))
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert len(native['all21_native_printf_macro_wrap_and_complete_font_planes']) == 21
    assert registered['complete_native_copy_count'] == 122 and all(registered['meaningful_rejection_controls'].values())
    assert {r['message_id'] for r in gameplay['actual_native_rumor_displays']} == {709, 729}
    assert len(gameplay['ordinary_New_Game_terminal4000_frame_and7_whole_frame_pairs']) == 7
    assert patch['whole_ROM_byte_exact']
    assert sha(ROM.read_bytes()) == manifest['candidate_sha256'] == gameplay['candidate_sha256'] == patch['candidate_sha256']
    doc = read('translations/regional_rumors_manuscript_v1.json')
    revised, retained = native['revised_IDs'], native['retained_wording_IDs']
    assert len(revised) == 12 and len(retained) == 9
    ledger = read(LEDGER)
    assert ledger['records_editorially_completed'] == 53 and ledger['records_revised_and_integrated'] == 36
    assert not (ROOT / 'editorial_ledger_at_V748.json').exists()
    save(ROOT / 'editorial_ledger_at_V748.json', ledger)
    ledger['completed_editorial_families'].append({
        'id': 'Square-regional-faction-and-person-rumors', 'native_message_IDs': list(range(709, 730)),
        'records': [{'message_id': r['message_id'],
            'decision': 'revised-and-integrated' if r['decision'] == 'revise' else 'retain-wording',
            'manuscript': 'translations/regional_rumors_manuscript_v1.json',
            'complete_clean_source_native_selector_and_font_verified': True,
            'complete_controlled_gameplay_display_verified': r['message_id'] in (709, 729),
            'ordinary_regional_travel_not_claimed': True} for r in doc['records']],
        'editorial_and_integration_review_complete_with_targeted_fixture_gameplay_sample': True,
        'proof': str(ROOT / 'proof.json'), 'candidate_sha256': manifest['candidate_sha256']})
    ledger.update({'records_editorially_completed': 74, 'records_revised_and_integrated': 48,
        'retained_wordings_editorially_completed': 26, 'records_with_source_and_prose_pass': 74})
    image = NdsImage.open(ROM)
    common, arm = image.read_file('/COMMON/MESFILE.DK4'), image.read_file('/__arm9__.bin')
    entries = common_message_entries(common, arm, clean=False)
    placeholders = [r.message_id for r in entries if b'Here is some local information.' in r.text]
    assert placeholders == [732, 733, 736, 737, 738, 739, 740, 741]
    ledger['current_integrated_candidate'] = {
        'path': str(ROM), 'sha256': manifest['candidate_sha256'], 'profile': manifest['profile'],
        'MESFILE_sha256': sha(common), 'ARM9_sha256': sha(arm), 'patch_sha256': patch['patch_sha256'],
        'status': 'experimental', 'manifest': str(ROM.with_suffix('.manifest.json')),
        'initial_source_pins_retained_as_V743_reference_not_overwritten': True}
    ledger['latest_checkpoint'] = 'V749 all21 regional rumors reviewed:12 revised,9 retained;11 placeholders restored and709 padding-only page removed'
    ledger['coverage_units'][0]['completed_families'].append('Square-regional-faction-and-person-rumors')
    ledger['coverage_units'][0]['next'] = 'Source/caller review of trend, relief and traveling-promoter dialogue730 onward, including8 remaining exact local-information placeholders; then broader shared prose and all routes.'
    for finding in ledger['findings']:
        if finding['id'] == 'COMMON-remaining-local-information-placeholders':
            finding['native_message_ids'] = placeholders
            finding['detail'] = 'V749 restores11 additional regional rumors. Eight exact phrase matches remain; this scan is not a complete defect inventory.'
    ledger['findings'].append({'id': 'COMMON-709-placeholder-and-padding-only-extra-page', 'native_message_id': 709,
        'status': 'full-source-meaning-restored-native-and-controlled-display-verified-V749',
        'detail': 'Old107-byte placeholder consumes73 bytes on its first native page, leaving34 spaces; actual baseline6050 is blank. Complete new Clifford rumor closes to the shop menu at the first A press.'})
    save(LEDGER, ledger)
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': manifest['candidate_sha256'],
        'profile': manifest['profile'], 'reviewed_rumor_IDs': list(range(709, 730)), 'revised_IDs': revised, 'retained_wordings': retained,
        'verification_reports': {str(ROOT / f): sha((ROOT / f).read_bytes()) for f in (
            'native_review.json', 'registered_verification.json', 'gameplay_verification.json', 'patch_proof.json')},
        'pre_capture_pending_fields_superseded_by_completed_gameplay_report': True,
        'all_prior36_revisions470_batches114_accepted_layers675_graphics_preserved': True,
        'all_canonical_bytes_source_saves_and_original_harness_core_preserved_no_promotion': True,
        'graphics_audit_and_original18_objects_unchanged': True, 'final_native_preview_and_gameplay_images_visually_inspected': True,
        'editorial_ledger_sha256': sha(LEDGER.read_bytes()), 'remaining_exact_placeholder_IDs': placeholders,
        'full_goal_complete': False})
    review = ['# Regional rumors: final clean-source editorial review', '',
        'Twelve revisions; nine retained wordings. All21 original selector/native-font checks and a two-entry gameplay sample pass.', '']
    for row in doc['records']:
        review += [f'## {row["message_id"]}: {row["decision"]}', '', row['japanese'].replace('\n', ' / '), '',
            '**V748:** ' + row['current_English'], '', '**V749:** ' + row['english'].removesuffix('{PAD}'), '',
            '**Meaning:** ' + row['source_meaning'], '', '**Reason:** ' + row['localization_note'], '']
    (ROOT / 'review.md').write_text('\n'.join(review), encoding='utf-8')
    DOC.write_text(
        '# V749: regional faction and person rumors\n\n'
        'All21 independent regional rumors709-729 are reviewed:12 revisions and9 retained wordings. '
        'Eleven placeholders are replaced with complete source meanings. Cumulative coverage is74 reviewed entries, '
        '48 revised and integrated,26 retained wordings. The full shared/route/prose goal remains active.\n\n'
        '## Translation and formatting\n\n'
        'Restore Clifford\'s former piracy and knighthood as hearsay; surprise at young women trading; '
        'Speyer\'s efforts and the wish for realism; Sweden\'s trade/privateering-funded self-sufficiency; '
        'Centurione\'s former wide operations; Hayreddin\'s inherited name and the earlier man\'s Ottoman title; '
        'Silveira\'s miserliness; fearful silence about Espinosa; confidence in Uddin and rumored royalty; '
        'Kuhn\'s ruthless profit and confidential aside; the speaker\'s wish for a female ruler; '
        'and Escante\'s expected appointment over both Mexico and Peru. Every exact Japanese selection, '
        'current V748 bytes, gloss and adaptation reason is in the manuscript and source packet. '
        'Nine natural wordings remain; old full-width Latin I bytes are normalized through the proven safe ASCII path. '
        'Initial short final lines in711/715/729 were caught in previews and revised before the build. '
        'All prose is one authored paragraph; only the existing consumer formatter makes line breaks.\n\n'
        '## Native, integration and gameplay evidence\n\n'
        '- Original5FA60 executes63 supplied share/region cases in both clean/current code. Zero current-company '
        'share selects709+region; nonzero selects688+region. These are independently selected topics. '
        'All21 full228x64 native font planes match decoded game glyphs and blank cells.\n'
        '- All18340 native ID/five-parent dispatch cases change only21 new direct-portrait cases. '
        'The existing28-byte dispatcher extends its range while retaining675-681 and688-708. '
        'No executable section, helper, pool, arena, cache allocation or startup payload grows. '
        'All3668 IDs and NUL owners remain; only block9 and ARM9 message offsets/owned dispatcher bytes '
        'change from V748. All40 other COMMON blocks,675 graphics and every other file remain exact. '
        'Complete122 warm/cold native copies across block9 and its two boundaries and seven malformed-input controls pass.\n'
        '- Registered470-batch/114-accepted-layer combined build passes all final guards. '
        'The clean-input xdelta reconstructs every ROM byte exactly.\n'
        '- Four terminal6500-frame cold boots pair V748/V749 for region indices0/20. '
        'An explicit five-byte RAM region/RNG fixture retains Istanbul and original zero market share. '
        'The original getters/selector and complete4MiB receipts bind actual709/729. '
        'Full glyph and blank-paper masks at5900 and unique entire resident4032-byte cache blocks match. '
        'All pixels outside the dialogue plane match each paired baseline; region20 also matches12 whole control/return '
        'frames. These are controlled regional-dialogue displays in Istanbul, not ordinary regional travel.\n'
        '- Old709 uses107 bytes; its first paint consumes73, leaving34 spaces. The actual6050 baseline is blank. '
        'New709 closes directly. Its later input phase therefore differs from the old baseline. '
        'Five new709 exit/return frames match the already-paired new729 control outside the fixed town-header region; '
        'the whole header geometry matches under a bijective four-color substitution. The header color-selection '
        'cause and intervening UI RNG draw sequence were not separately traced; no palette asset changes.\n'
        '- A separate ordinary4000-frame New Game cold boot without save or fixtures matches seven complete V748 '
        'frames, including the opening story. Other19 rumors have source/selector/full-font evidence, '
        'not claimed live travel. No hardware or complete-route claim is made.\n\n'
        '## Reproduction\n\n'
        f'- Candidate: `{ROM}`\n- Candidate SHA-256: `{manifest["candidate_sha256"]}`\n'
        f'- Canonical base: `{manifest["base_rom"]}`\n- Base SHA-256: `{manifest["base_sha256"]}`\n'
        f'- Profile: `{manifest["profile"]}` (experimental)\n'
        f'- Patch: `{ROM.with_suffix(".xdelta")}`\n- Patch SHA-256: `{patch["patch_sha256"]}`\n'
        f'- Clean patch-input SHA-256: `{patch["clean_source_sha256"]}`\n\n'
        'The manifest lists every inherited layer and canonical-base changed file. The incremental changes '
        'from V748 are COMMON and ARM9 only. User cold-boot review should cover New Game, normal shops, '
        'regional rumors and closing their text without an extra empty page. Canonical promotion still '
        'requires explicit user acceptance. ROM and patch are on E through out; controlled screenshots '
        'are under Screenshots/Test fixtures/V749 Regional rumors, with provenance.\n\n'
        '## Remaining scope and diagnostic history\n\n'
        f'Eight exact local-information placeholders remain: {placeholders}. Review trends, relief, '
        'promoter travel and surrounding native callers next. This phrase scan does not establish correctness '
        'of other prose. All routes and remaining shared/help/player-facing prose remain open. '
        'The separate graphics audit, original18 plaque objects, Online exclusions and preserved brown marks '
        'are unchanged. Revisit older record-based checks after the full goal. Initial four capture probes '
        'reached6500 but terminated with EOF because the final stop command was absent; they earn no '
        'completed-run credit. Final directories retain separate successful reports with both commands, '
        'unchanged harness/core hashes and terminal exit0. No producer was modified while running.\n', encoding='utf-8')
    summary = ('\n\n## V749: regional rumors and another blank page restored\n\n'
        'All21 rumors709-729 reviewed:12 revised,9 retained;11 placeholders restored. '
        'All21 complete native font planes,18340 dispatch cases,122 native copies and seven rejection controls pass. '
        'Four controlled6500-frame cold boots verify full709/729 and resident cache blocks. '
        'Old709\'s34-space extra blank page is reproduced and removed; exit evidence records changed input phase '
        'and the bounded header color substitution. Ordinary New Game matches seven V748 frames. '
        'Registered470/114 combined V749 and exact clean patch preserve prior prose/art. '
        'Total74 reviewed,48 revised,26 retained;8 exact placeholders, remaining shared prose and all routes open. '
        'Experimental; canonical/saves/separate graphics audit unchanged. See '
        '[V749 checkpoint](regional_rumors_v749_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert '## V749: regional rumors and another blank page restored' not in text
        path.write_text(text.rstrip() + summary, encoding='utf-8')
    save('out/editorial_review_latest.json', {**ledger['current_integrated_candidate'], 'details': str(DOC), 'full_goal_complete': False})
    shots = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V749 Regional rumors')
    for row in gameplay['actual_native_rumor_displays']:
        copy(Path(row['capture']['path']), shots / f'COMMON_{row["message_id"]}_controlled_regional_dialogue.png')
    for frame in (6050, 6500):
        copy(Path(f'E:/Rota Nova translations/Generated/work/emulation_v193/rumors_v749_region0_final_new/frame_{frame:06d}_cold_boot.png'),
            shots / f'COMMON_709_return_{frame}_controlled.png')
    save(shots / 'provenance.json', {'candidate_sha256': manifest['candidate_sha256'],
        'region_and_RNG_fixture_in_Istanbul_original_zero_share_preserved': True,
        'ordinary_travel_progress_and_publication_approval_not_claimed': True,
        'source_gameplay_proof': str(ROOT / 'gameplay_verification.json'),
        'files': {p.name: sha(p.read_bytes()) for p in shots.glob('*.png')}})
    files = [DOC, LEDGER, ROOT / 'proof.json', ROOT / 'editorial_ledger_at_V748.json',
        Path('translations/regional_rumors_manuscript_v1.json'), Path('translations/regional_rumors_release_v1.json'),
        Path('dk4tool/patch/regional_rumors.py'),
        *(ROOT / f for f in ('source_context_packet.json', 'review.md', 'native_review.json', 'registered_verification.json',
            'gameplay_verification.json', 'patch_proof.json', 'fixture_preflight_region0.json', 'fixture_preflight_region20.json',
            'native_previews_1_2x.png', 'native_previews_2_2x.png', 'inputs_rumor_final.json', 'inputs_newgame.json')),
        *(Path('scripts') / f for f in ('prepare_regional_rumors_v749.py', 'verify_and_register_regional_rumors_v749.py',
            'verify_regional_rumor_release_v749.py', 'verify_regional_rumor_gameplay_v749.py',
            'native_regional_rumor_fixture_v749.py', 'run_regional_rumor_capture_v749.py')), Path(__file__)]
    for path in files:
        copy(path, ARCHIVE / path.name)
    save(ARCHIVE / 'provenance.json', {'candidate': str(ROM), 'candidate_sha256': manifest['candidate_sha256'],
        'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir() if p.is_file() and p.name != 'provenance.json'},
        'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    print('V749 recorded:74 reviewed,48 revisions integrated,26 retained;8 exact placeholders queued.', flush=True)


if __name__ == '__main__':
    main()
