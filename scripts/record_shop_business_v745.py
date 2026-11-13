"""Record the integrated editorial family with explicit ordinary/native scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.record_memory_streams_v682 import copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/shop_business_v745')
ROM = Path('out/all_routes_combined_v745_candidate.nds')
LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/shop_business_v745_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V745 Integrated retail and business replies')


def main():
    registered = read(ROOT / 'registered_verification.json')
    gameplay = read(ROOT / 'gameplay_verification.json')
    patch = read(ROOT / 'patch_proof.json')
    assert registered['native_copy_case_count'] == 122 and all(registered['meaningful_rejection_controls'].values())
    assert len(gameplay['ordinary_native_message_displays']) == 2
    assert len(gameplay['whole_two_screen_equal_baseline_frames']) == 17
    assert len(gameplay['New_Game11_whole_frame_pairs_exact']) == 11
    assert patch['whole_ROM_byte_exact']
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert sha(ROM.read_bytes()) == manifest['candidate_sha256'] == gameplay['candidate_sha256'] == patch['candidate_sha256']
    before = read(LEDGER)
    assert before['records_revised_and_integrated'] == 0
    assert not (ROOT / 'editorial_ledger_at_V744.json').exists()
    save(ROOT / 'editorial_ledger_at_V744.json', before)
    ledger = read(LEDGER)
    ids = [657, 658, 682, 683, 684, 686, 687]
    family = [656, 657, 658, 682, 683, 684, 685, 686, 687]
    record_rows = []
    manuscript = read('translations/shop_business_editorial_manuscript_v1.json')
    for row in manuscript['records']:
        i = row['message_id']
        record_rows.append({'message_id': i, 'decision': 'revised-and-integrated',
                            'manuscript': 'translations/shop_business_editorial_manuscript_v1.json',
                            'ordinary_display_verified': i in (657, 658),
                            'complete_native_source_macro_and_font_verified': True,
                            'context': 'Original Square merchant portrait family and native town-state selector; gameplay sampling covers 657/658 and return.'})
    for i in (656, 685):
        record_rows.append({'message_id': i, 'decision': 'retain-wording',
                            'source_and_prose_review': 'translations/shop_town_editorial_manuscript_v1.json',
                            'unchanged_visible_text_native_copy_verified': True,
                            'context': 'Original retail direct branch 656 or original town-state business selector 685.'})
    ledger['completed_editorial_families'] = [{
        'id': 'Square-retail-and-business-responses', 'native_message_IDs': family,
        'records': sorted(record_rows, key=lambda r: r['message_id']),
        'editorial_and_integration_review_complete_with_targeted_gameplay_sample': True,
        'proof': str(ROOT / 'proof.json'), 'candidate_sha256': manifest['candidate_sha256'],
        'no_claim_of_observing_all_town_events': True,
    }]
    ledger['records_editorially_completed'] = 9
    ledger['records_revised_and_integrated'] = 7
    ledger['retained_wordings_editorially_completed'] = 2
    ledger['initial32_native_IDs_still_pending_context_or_formatting'] = [i for i in range(656, 688) if i not in family]
    image = NdsImage.open(ROM)
    ledger['current_integrated_candidate'] = {
        'path': str(ROM), 'sha256': manifest['candidate_sha256'], 'profile': manifest['profile'],
        'MESFILE_sha256': sha(image.read_file('/COMMON/MESFILE.DK4')),
        'ARM9_sha256': sha(image.read_file('/__arm9__.bin')),
        'patch_sha256': patch['patch_sha256'], 'status': 'experimental',
        'manifest': str(ROM.with_suffix('.manifest.json')),
        'initial_source_pins_retained_as_V743_reference_not_overwritten': True,
    }
    ledger['latest_checkpoint'] = 'V745 integrated retail/business family; seven revisions, two retained wordings, targeted ordinary and native verification'
    for finding in ledger['findings']:
        if finding.get('native_message_id') in ids:
            finding['status'] = 'reviewed-revised-integrated-V745-with-family-gameplay-sample'
    ledger['coverage_units'][0]['completed_families'] = ['Square-retail-and-business-responses']
    ledger['coverage_units'][0]['next'] = 'Confirm/distribution announcements and independent product pitches 659-681; country briefing688 queued.'
    save(LEDGER, ledger)
    reports = {str(ROOT / f): sha((ROOT / f).read_bytes()) for f in (
        'native_review.json', 'registered_verification.json', 'gameplay_verification.json', 'patch_proof.json')}
    save(ROOT / 'proof.json', {
        'candidate': str(ROM), 'candidate_sha256': manifest['candidate_sha256'],
        'profile': manifest['profile'], 'seven_revised_native_IDs': ids,
        'two_retained_wordings': [656, 685], 'source_and_individual_v2_review_gates_complete': True,
        'source_and_native_checks': reports,
        'all_other_ROM_files_and_all675_graphics_preserved_from_V712': True,
        'all114_accepted_baked_layers_and470_batches_retained': True,
        'original18_graphics_audit_objects_and_graphics_context_gaps_untouched': True,
        'canonical_baseline_unchanged_and_no_layer_promotion': True,
        'editorial_ledger_sha256': sha(LEDGER.read_bytes()),
        'full_goal_complete': False,
    })
    DOC.write_text(
        '# V745: integrated retail and business editorial review\n\n'
        'Seven revised merchant replies are integrated: 657, 658, 682, 683, 684, 686 '
        'and 687. Two already natural replies, 656 and 685, retain their wording. The '
        'family restores the sailor observation, naturalizes the business responses '
        'and corrects collapsing people versus unsupported deaths. The remaining '
        '23 of the first 32 entries are still pending context/formatting completion; '
        'the split cooking/fashion pitches remain queued. The full editorial goal is active.\n\n'
        '## Verification\n\n'
        '- All seven complete 228x64 native font planes match independently decoded '
        'glyphs, including every blank cell and first/final letter. Original native '
        'macro expansion preserves each literal English byte.\n'
        '- Generated balanced wraps use the proven COMMON consumer, with generated '
        'initial/continuation guards and pair-phase repair. Prose contains no authored '
        'line breaks or layout spaces. Longer text borrows terminal padding inside '
        'the existing cache block; all block allocations, global IDs and NUL owners '
        'remain fixed.\n'
        '- All 59 selections in block 8 plus its two neighbor boundaries pass warm '
        'and cold original native copies: 122 complete cases. File I/O is bridged '
        'to exact bytes for these component tests. Five policy/source/packed-sibling/'
        'authored-break/macro rejection controls pass.\n'
        '- Two terminal 6500-frame DeSmuME cold boots use identical ordinary controls '
        'and protected copies of the Istanbul donor save. Actual 657 at frame 5600 '
        'and 658 at frame 5900 have complete glyph masks and blank paper. Whole '
        'resident block 8 is byte-exact at both holds. Every pixel outside the '
        'dialogue paper matches baseline. The other 17 complete two-screen captures '
        'match, including dialogue exit and town return. No gameplay fixture or '
        'savestate is used.\n'
        '- A terminal 4000-frame ordinary New Game cold boot matches all 11 comparable '
        'whole frames from the V733 reference, covering title/selection/opening. '
        'The other five revised event replies have complete native component coverage; '
        'their ordinary disaster/event activations are not claimed observed.\n'
        '- Registered builder: all 470 batches, 114 baked accepted layers and final '
        'guards pass. Only COMMON and ARM9 native offset fields differ from V712. '
        'Every other internal file, all 675 graphics, executable code, fonts, cache '
        'allocations, startup/late-copy payloads and original saves are preserved. '
        'The exact clean-source xdelta reconstructs every candidate byte.\n\n'
        '## Reproduction and handoff identity\n\n'
        f'- Candidate: `{ROM}`\n'
        f'- Candidate SHA-256: `{manifest["candidate_sha256"]}`\n'
        f'- Canonical build base: `{manifest["base_rom"]}`\n'
        f'- Base SHA-256: `{manifest["base_sha256"]}`\n'
        f'- Profile: `{manifest["profile"]}` (experimental)\n'
        f'- Patch: `{ROM.with_suffix(".xdelta")}`\n'
        f'- Patch SHA-256: `{patch["patch_sha256"]}`\n'
        f'- Patch input clean SHA-256: `{patch["clean_source_sha256"]}`\n'
        '- Changed components relative to V712: `/COMMON/MESFILE.DK4`, '
        '`/__arm9__.bin` native message offset fields. The neighboring manifest '
        'lists every inherited layer, changed file and record relative to the canonical base.\n\n'
        'User cold-boot review should check New Game and ordinary Square replies, '
        'including the complete sailor and business lines and their exit transitions. '
        'Canonical promotion still requires explicit user acceptance. The graphics '
        'audit remains separate and incomplete; this prose release does not close it.\n\n'
        '## Diagnostic corrections\n\n'
        'The initial 100000-instruction font budget was insufficient; all final calls '
        'complete with the larger budget and return ABI checks. Source assertions '
        'rejected a mistakenly selected adjacent lore helper and inverted default/'
        'normal literals; the final business selector is the original 5FA98 routine '
        'with all 13 supplied states verified in clean and current code. An assumed '
        'immediate instruction spelling was replaced with actual ARM rotation decoding. '
        'The FNT iterator excludes the virtual ARM9 component, which is now checked '
        'separately. These were research/verifier corrections, not reasons to alter '
        'native game code.\n', encoding='utf-8')
    summary = ('\n\n## V745: seven retail/business revisions integrated\n\n'
        'The first merchant family is reviewed: seven revised replies and two retained '
        'wordings. All seven complete native font planes, 122 warm/cold source copies '
        'and five rejection controls pass. Ordinary cold boots verify full 657/658, '
        '17 unchanged shop/return frames and 11 unchanged New Game pairs. Five other '
        'event replies retain native-component coverage rather than claimed ordinary '
        'activations. Registered 470-batch/114-layer combined V745 preserves all other '
        'files and 675 graphics; clean patch reconstructs byte-exact. Only COMMON and '
        'ARM9 message offset metadata change from V712. Nine editorial entries complete '
        'within this family; 23 initial entries, all routes and remaining prose still '
        'open. Experimental, canonical and original saves unchanged; graphics audit '
        'separate. See [V745 checkpoint](shop_business_v745_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        p = Path('docs') / name
        text = p.read_text(encoding='utf-8')
        assert '## V745: seven retail/business revisions integrated' not in text
        p.write_text(text.rstrip() + summary, encoding='utf-8')
    save('out/editorial_review_latest.json', {
        **ledger['current_integrated_candidate'], 'details': str(DOC), 'full_goal_complete': False})
    guide = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V745 Square shopkeeper')
    for frame in (5600, 5900):
        row = next(r for r in gameplay['ordinary_native_message_displays'] if r['frame'] == frame)
        copy(Path(row['capture']['path']), guide / f'COMMON_{row["message_id"]}_ordinary_Istanbul.png')
    save(guide / 'provenance.json', {
        'candidate_sha256': manifest['candidate_sha256'], 'source_gameplay_proof': str(ROOT / 'gameplay_verification.json'),
        'ordinary_cold_boot_donor_save_copy_no_fixture': True, 'candidate_experimental': True,
        'publication_approval_not_inferred': True,
        'files': {p.name: sha(p.read_bytes()) for p in guide.glob('*.png')}})
    for source in (DOC, LEDGER, ROOT / 'proof.json', ROOT / 'native_review.json',
                   ROOT / 'registered_verification.json', ROOT / 'gameplay_verification.json',
                   ROOT / 'patch_proof.json', ROOT / 'editorial_ledger_at_V744.json',
                   Path('translations/shop_business_editorial_manuscript_v1.json'),
                   Path('translations/shop_business_editorial_release_v1.json'),
                   Path('dk4tool/patch/shop_business_editorial.py'),
                   Path('scripts/prepare_shop_business_release_v745.py'),
                   Path('scripts/verify_shop_business_release_v745.py'),
                   Path('scripts/verify_shop_business_gameplay_v745.py'), Path(__file__),
                   ROOT / 'native_business_previews_2x.png'):
        copy(source, ARCHIVE / source.name)
    save(ARCHIVE / 'provenance.json', {
        'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir() if p.is_file() and p.name != 'provenance.json'},
        'candidate': str(ROM), 'candidate_sha256': manifest['candidate_sha256'], 'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    print('V745 recorded: seven revised + two retained merchant entries; full editorial goal remains active.', flush=True)


if __name__ == '__main__':
    main()
