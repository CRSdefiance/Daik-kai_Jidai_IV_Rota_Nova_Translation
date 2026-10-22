"""Record verified promotion prose without closing the wider editorial goal."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.record_memory_streams_v682 import copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/product_pitches_v747')
ROM = Path('out/all_routes_combined_v747_candidate.nds')
LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/product_pitches_v747_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V747 Independent product pitches')


def main():
    native = read(ROOT / 'native_review.json')
    registered = read(ROOT / 'registered_verification.json')
    gameplay = read(ROOT / 'gameplay_verification.json')
    patch = read(ROOT / 'patch_proof.json')
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert native['complete_native_printf_wrap_cases'] == 11289
    assert registered['complete_native_copy_count'] == 122
    assert all(registered['meaningful_rejection_controls'].values())
    assert len(gameplay['actual_original_introduction675_then_cooking676_complete']) == 4
    assert len(gameplay['New_Game_terminal4000_frame_fixture_free_cold_boot_and7_whole_frame_pairs']) == 7
    assert patch['whole_ROM_byte_exact']
    assert sha(ROM.read_bytes()) == manifest['candidate_sha256'] == gameplay['candidate_sha256'] == patch['candidate_sha256']
    ledger = read(LEDGER)
    assert ledger['records_editorially_completed'] == 25 and ledger['records_revised_and_integrated'] == 14
    assert not (ROOT / 'editorial_ledger_at_V746.json').exists()
    save(ROOT / 'editorial_ledger_at_V746.json', ledger)
    ids = list(range(675, 682))
    ledger['completed_editorial_families'].append({
        'id': 'Square-product-demonstrations-and-merchant-reaction', 'native_message_IDs': ids,
        'records': [{'message_id': i, 'decision': 'revised-and-integrated',
                     'manuscript': 'translations/product_pitches_editorial_manuscript_v1.json',
                     'clean_source_and_actual_category_or_reaction_caller_verified': True,
                     'complete_native_printf_runtime_wrap_and_font_plane_verified': True,
                     'complete_fixture_gameplay_display_verified': i in (675, 676),
                     'other_actor_event_and_earned_progress_not_claimed': True} for i in ids],
        'editorial_and_integration_review_complete_with_targeted_fixture_gameplay_sample': True,
        'proof': str(ROOT / 'proof.json'), 'candidate_sha256': manifest['candidate_sha256']})
    ledger['records_editorially_completed'] = 32
    ledger['records_revised_and_integrated'] = 21
    ledger['retained_wordings_editorially_completed'] = 11
    ledger['initial32_native_IDs_still_pending_context_or_formatting'] = []
    image = NdsImage.open(ROM)
    ledger['current_integrated_candidate'] = {
        'path': str(ROM), 'sha256': manifest['candidate_sha256'], 'profile': manifest['profile'],
        'MESFILE_sha256': sha(image.read_file('/COMMON/MESFILE.DK4')),
        'ARM9_sha256': sha(image.read_file('/__arm9__.bin')), 'patch_sha256': patch['patch_sha256'],
        'status': 'experimental', 'manifest': str(ROM.with_suffix('.manifest.json')),
        'initial_source_pins_retained_as_V743_reference_not_overwritten': True}
    ledger['latest_checkpoint'] = 'V747 seven product-pitch/reaction revisions complete; first32 source-reviewed entries integrated or retained, wider editorial review active'
    ledger['coverage_units'][0]['completed_families'].append('Square-product-demonstrations-and-merchant-reaction')
    ledger['coverage_units'][0]['next'] = 'Country briefing688 and surrounding shared town dialogue; source/consumer inventory before route scene review.'
    for finding in ledger['findings']:
        if finding['id'] == 'COMMON-676-677-cross-selection-prose':
            finding['status'] = 'independent_source_category_pitches_restored_and_integrated_V747'
        elif finding['id'] == 'COMMON-658-stiff-English':
            finding['note'] = 'Initial V712 wording retained here as historical evidence; revision and actual ordinary display completed at V745.'
    save(LEDGER, ledger)
    save(ROOT / 'proof.json', {
        'candidate': str(ROM), 'candidate_sha256': manifest['candidate_sha256'], 'profile': manifest['profile'],
        'seven_revised_native_IDs': ids, 'source_and_individual_natural_dialogue_v2_gates_complete': True,
        'verification_reports': {str(ROOT / f): sha((ROOT / f).read_bytes()) for f in (
            'native_review.json', 'registered_verification.json', 'gameplay_verification.json', 'patch_proof.json')},
        'pre_capture_native_and_registered_snapshots_superseded_by_gameplay_report': True,
        'all_prior14_revisions470_batches114_baked_layers675_graphics_preserved': True,
        'canonical_and_original_saves_unchanged_no_promotion': True,
        'graphics_audit_original18_objects_and_remaining_context_work_unchanged': True,
        'editorial_ledger_sha256': sha(LEDGER.read_bytes()), 'full_goal_complete': False})
    DOC.write_text(
        '# V747: independent product demonstrations and merchant reaction\n\n'
        'Seven revised entries675-681 complete the first32-entry shared shop/town '
        'editorial group:21 revisions integrated and11 wordings retained across '
        'V745-V747. Country briefing688, remaining shared prose and every route '
        'scene still need review. The full editorial goal remains active.\n\n'
        '## Meaning and source context\n\n'
        '675 invites inspection and boasts of the best quality. Its English is '
        'number-neutral for both singular/mass and plural product names.676 restores '
        'a complete cooking demonstration and call to a nearby woman;677 separately '
        'introduces fashion/decor and invites ladies and gentlemen. The stray '
        'Discover joining those independent selections is removed.678 preserves '
        'the aroma/flavor and fatigue-relief boast as natural sales patter.679 '
        'retains inventions/industry, a worthwhile lecture and missed-profit warning. '
        '680 preserves the promoter\'s cure-all claim and idiomatic skeptical '
        'invitation; it is not a verified item-effect claim.681 retains product '
        'interest and the proposed selling area, with both substitutions in order '
        'and selling some valid for every product number.\n\n'
        'Original5E568 introduces675; the original category switch selects676,677,'
        '678,679 or680. Categories0-3 select676,4-5 select678,13 selects680,15-17 '
        'select679, and remaining categories select677. All20 supplied category '
        'prefixes match clean/current code. The separate yes/no travel request at '
        '5E618 is739, outside this batch.681 receives actual product/city name '
        'getters from the original5E8FC sequence. Adjacent storage does not establish '
        'a sequential conversation.\n\n'
        '## Formatting and verification\n\n'
        '- Prose is one paragraph under natural-dialogue-v2. No translator-authored '
        'alignment or LF is copied from old English. The existing bounded portrait '
        'formatter now handles numeric IDs675-681 only at original direct parent '
        '02054014, after native macro/printf expansion. A4-byte branch and an '
        'unreferenced28-byte historical table stub are reused. All18340 dispatch '
        'cases across3668 IDs/five parents preserve prior selection except these '
        'seven direct cases. All current sections/overlays have no pointer/direct '
        'branch into the old stub. No section, startup payload, pool, cache or '
        'arena grows; native formatter/font code remains unchanged.\n'
        '- Native getters supply all124 commodity and90 city names from captured '
        'current RAM.124 intro substitutions, all11160 product/city pairs for681 '
        'and five static pitches pass guarded original printf, exact complete '
        'word preservation, four-row bounds and35-cell rows:11289 cases. Eleven '
        'complete228x64 native font planes cover all static pitches and every '
        'observed dynamic row-count/length-parity class; all are visually reviewed. '
        'This is an exhaustive layout matrix with sampled full glyph planes, '
        'not11289 gameplay observations.\n'
        '- All59 block8 selections and two neighbor boundaries pass complete warm/'
        'cold original copies:122 cases with exact bridged SDK I/O. Seven malformed '
        'policy/source/family/break/substitution/macro controls are rejected. All '
        'prior prose and675 graphics remain exact to V746; only COMMON and ARM9 '
        'message-offset metadata plus the32 owned dispatcher bytes differ.\n'
        '- Two terminal6501-frame cold boots use protected copies of the Istanbul '
        'save and a disclosed three-byte fixture: tracked promotion city/product '
        'and one temporary town-stock product. Original native getters confirm '
        'Istanbul, Olive Oil and category1; other4MiB RAM bytes are unchanged at '
        'insertion. The event is not claimed earned through ordinary progression. '
        'Original675 at3800/4000 and676 at4200/4400 have complete glyph/blank-paper '
        'masks, exact resident block8 and unchanged pixels outside the original '
        '228-pixel text plane. All remaining complete paired frames, Square menus '
        'and town return match. Five other entries have source/native coverage '
        'rather than claimed ordinary event activations.\n'
        '- A separate terminal4000-frame ordinary New Game cold boot, without save '
        'or fixture, matches seven complete V746 frames. Registered470-batch/'
        '114-accepted-layer integration and final guards pass. The exact clean-source '
        'xdelta reconstructs every candidate byte. No hardware or full-route '
        'playthrough claim is made.\n\n'
        '## Identity and review\n\n'
        f'- Candidate: `{ROM}`\n- SHA-256: `{manifest["candidate_sha256"]}`\n'
        f'- Base: `{manifest["base_rom"]}`\n- Base SHA-256: `{manifest["base_sha256"]}`\n'
        f'- Profile: `{manifest["profile"]}` (experimental)\n'
        f'- Exact patch: `{ROM.with_suffix(".xdelta")}`\n- Patch SHA-256: `{patch["patch_sha256"]}`\n'
        f'- Clean patch input SHA-256: `{patch["clean_source_sha256"]}`\n\n'
        'The neighboring manifest records all inherited batches and canonical-base '
        'changes. User review should cold-boot New Game and inspect the product '
        'introduction/demonstration, substituted names and return. Explicit user '
        'acceptance is still required for canonical promotion. The unresolved '
        'graphics audit,18 original plaque objects, excluded Online bodies and '
        'preserved brown marks are unchanged. Fixture screenshots are under '
        'Screenshots/Test fixtures/V747 Product pitches.\n\n'
        '## Research corrections\n\n'
        'Original native selection assertions corrected an early literal-offset '
        'assumption:677 is the category-selected fashion pitch;739 is the later '
        'travel question. Native name getters corrected an assumed Olive Oil '
        'category2 to actual1. The initial long draft of677 exceeded four rows; '
        'the final natural phrasing preserves both the society claim and invitation. '
        'An unpublished preview exposed this %s as unsuitable for plural products; '
        'the final template avoids grammatical number and an isolated last-word '
        'tail. Superseded drafts are preserved as research-only snapshots. One long '
        'reused Unicorn host session raised a host access violation; final complete '
        'matrix runs use fresh machines every64 cases and pass. Initial runtime '
        'timing was observed in a terminal baseline probe, then frozen paired '
        'controls add the final Square-exit B press. No failed probe is counted '
        'as final coverage.\n', encoding='utf-8')
    summary = ('\n\n## V747: independent promotion pitches reviewed\n\n'
        'Seven source-reviewed revisions675-681 restore independent food/fashion '
        'pitches, natural sales patter and number-neutral runtime product names. '
        '11289 complete native printf/wrap cases,11 full font planes,18340 dispatch '
        'cases,122 native copies and seven rejection controls pass. Paired6501-frame '
        'cold boots with a disclosed three-byte event/stock fixture verify675/676 '
        'and unchanged menu/town return; an ordinary New Game run matches seven '
        'V746 frames. Combined V747 preserves prior14 revisions,470 batches,114 '
        'accepted layers and675 graphics; clean patch byte-exact. First32 shared '
        'entries complete:21 revised,11 retained. Remaining shared prose, all '
        'routes and separate graphics audit remain open. Experimental; canonical '
        'and original saves unchanged. See [V747 checkpoint](product_pitches_v747_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert '## V747: independent promotion pitches reviewed' not in text
        path.write_text(text.rstrip() + summary, encoding='utf-8')
    save('out/editorial_review_latest.json', {**ledger['current_integrated_candidate'], 'details': str(DOC), 'full_goal_complete': False})
    shots = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V747 Product pitches')
    for row in gameplay['actual_original_introduction675_then_cooking676_complete']:
        copy(Path(row['capture']['path']), shots / f'COMMON_{row["message_id"]}_frame_{row["frame"]}_fixture_Istanbul.png')
    save(shots / 'provenance.json', {'candidate_sha256': manifest['candidate_sha256'],
        'three_byte_event_and_town_stock_fixture': True, 'ordinary_event_progress_and_publication_approval_not_claimed': True,
        'files': {p.name: sha(p.read_bytes()) for p in shots.glob('*.png')}})
    files = [DOC, LEDGER, MANUSCRIPT_PATH, CONFIG_PATH, ROOT / 'proof.json', ROOT / 'editorial_ledger_at_V746.json',
             *(ROOT / f for f in ('native_review.json', 'registered_verification.json', 'gameplay_verification.json', 'patch_proof.json',
                                  'native_layout_matrix.json', 'runtime_name_catalog.json', 'event_fixture_preflight.json',
                                  'inputs_demo.json', 'inputs_demo_final.json', 'native_previews_2x.png')),
             Path('dk4tool/patch/product_pitches_editorial.py'),
             *(Path('scripts') / f for f in ('prepare_product_pitches_v747.py', 'verify_product_pitches_v747.py',
                                            'verify_product_pitches_gameplay_v747.py', 'native_product_promotion_fixture_v747.py',
                                            'run_product_pitches_capture_v747.py')), Path(__file__)]
    for path in files:
        copy(path, ARCHIVE / path.name)
    save(ARCHIVE / 'provenance.json', {'candidate': str(ROM), 'candidate_sha256': manifest['candidate_sha256'],
        'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir() if p.is_file() and p.name != 'provenance.json'},
        'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    print('V747 recorded: first32 entries complete,21 revisions integrated; wider editorial goal active.', flush=True)


MANUSCRIPT_PATH = Path('translations/product_pitches_editorial_manuscript_v1.json')
CONFIG_PATH = Path('translations/product_pitches_editorial_release_v1.json')

if __name__ == '__main__':
    main()
