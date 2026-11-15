"""Record registered integration and startup, retaining actual-activity gates."""

import struct
from pathlib import Path
from shutil import copy2

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.personal_chatter_editorial import CONFIG
from dk4tool.rom.nds import NdsImage
from scripts.finish_refit_display_v712 import load
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.prepare_personal_release_v838 import MANUSCRIPT, OLD, ROOT
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v838_candidate.nds')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/personal_chatter_v838_deck_interactive2')
DOC = Path('docs/personal_chatter_v838_integration.md')
LEDGER = Path('translations/editorial_review_current_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V838 Deck dialogue integration and activity access')


def context(arm, raw):
    cpu = machine(arm)
    cpu.mem_write(0x02000000, raw)
    def get(at, *args):
        call(cpu, at, args)
        return cpu.reg_read(UC_ARM_REG_R0)
    model, calendar = get(0xCB1A8), get(0xCB1B4)
    fleet = model + 4 + get(0x2E58C) * 0x84
    last = struct.unpack_from('<I', arm, 0x13D70)[0]
    controller = model + struct.unpack_from('<I', arm, 0x13D74)[0]
    return {'native_fleet_town_or_sea115': get(0x34674, fleet),
            'calendar_tick': struct.unpack_from('<I', raw, calendar + 8 - 0x02000000)[0],
            'last_Deck_entry_tick': struct.unpack_from('<I', raw, last - 0x02000000)[0],
            'last_controller_tick': get(0x82B98, controller)}


def main():
    assert not DOC.exists() and not ARCHIVE.exists()
    release = read(ROOT / 'registered_release_verification.json')
    startup = read(ROOT / 'ordinary_startup_verification.json')
    projection = read('work/analysis/personal_chatter_v837/native_projection_and_font_proof.json')
    assert release['candidate_sha256'] == startup['candidate_sha256'] == sha(ROM.read_bytes())
    assert startup['all7_full_screen_pairs_exact'] and not startup['visual_review_pending']
    assert not projection['visual_review_pending']
    report, images, receipt = load(CAP, sha(ROM.read_bytes()), 31600)
    assert report['cold_boot'] and not report['savestate_loaded']
    assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
    donor = read(ROOT / 'deck_interactive2_donor.json')
    assert sha(Path(donor['source']).read_bytes()) == sha(Path(donor['disposable_source']).read_bytes()) == donor['source_sha256']
    snapshots = {}
    for row in report['read_only_capture_RAM_snapshots'] + report['read_only_pause_RAM_snapshots']:
        raw = Path(row['path']).read_bytes()
        assert len(raw) == 0x400000 and sha(raw) == row['sha256'] and row['read_only_export']
        assert row['frame'] not in snapshots or snapshots[row['frame']] == raw
        snapshots[row['frame']] = raw
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    contexts = {str(n): context(arm, snapshots[n]) for n in (11200, 23200, 28000, 30800, 31600)}
    assert contexts['11200']['native_fleet_town_or_sea115'] == 11
    assert contexts['28000']['native_fleet_town_or_sea115'] == 115
    assert contexts['28000']['last_Deck_entry_tick'] == contexts['28000']['calendar_tick'] == 673
    assert contexts['30800']['calendar_tick'] == 1584 and contexts['30800']['last_Deck_entry_tick'] == 673
    save(ROOT / 'ordinary_Deck_navigation_receipt.json', {
        'capture_receipt': receipt, 'all_snapshot_and_donor_hashes_pass': True,
        'frames': 31600, 'actual_context_getters': contexts,
        'ordinary_Crew_Setup_Explore_and_Deck_exit_Port_resupply_departure_and_tutorial': True,
        'selected_frames_visually_reviewed': [10400,10800,11200,11600,12000,12400,12800,13200,
            13600,16000,16400,18000,19200,20400,21600,23200,24800,26000,26400,27200,28000,30800,31600],
        'food_shortage_at30800_and_letter_notice_at31600_exclude_clean_activity_baseline': True,
        'no_new_RAM_code_random_text_or_eligibility_fixtures': True,
        'actual_revised_personal_comment_holds': 0,
        'normal_return_from_revised_comment_not_claimed': True,
        'completed_entry_credit': 0, 'full_goal_complete': False})
    ledger = read(LEDGER)
    assert ledger['records_editorially_completed'] == 646 and ledger['records_with_source_and_prose_pass'] == 674
    save(ROOT / 'editorial_ledger_before_checkpoint.json', ledger)
    pending = {
        'status': 'registered-combined-ROM-exact-patch-native-font-crop-copy-and-startup-verified-actual-comments-pending',
        'path': str(ROM), 'sha256': release['candidate_sha256'], 'profile': 'all-routes-unified-v838',
        'patch': release['patch'], 'patch_sha256': release['patch_sha256'],
        'manifest': str(ROM.with_suffix('.manifest.json')), 'release_config': CONFIG,
        'manuscript': str(MANUSCRIPT), 'registered_release_proof': str(ROOT / 'registered_release_verification.json'),
        'startup_proof': str(ROOT / 'ordinary_startup_verification.json'),
        'activity_access_proof': str(ROOT / 'original_activity_entry_gate.json'),
        'ordinary_navigation_receipt': str(ROOT / 'ordinary_Deck_navigation_receipt.json'),
        'documentation': str(DOC), 'native_message_IDs': list(range(1361, 1386)),
        'proposed_revisions': 18, 'justified_retentions': 7,
        'completed_entries_added': 0, 'actual_revised_activity_samples_pending': True,
        'canonical_not_promoted': True, 'full_goal_complete': False}
    ledger['personal_chatter_v838'] = pending
    ledger['pending_integrated_candidate'] = pending
    remaining = [
        'Use a fresh isolated, adequately supplied scene fixture to activate the original personal-comment path',
        'Verify actual Janus1365 and Claudio1366 plus an odd-row multiline sample,complete letters,paper/palette/bounds and normal return',
        'Record final activity verification and family completion only after the actual gates pass']
    ledger['active_source_prose_drafts']['manuscripts'][-1] = str(MANUSCRIPT)
    ledger['active_source_prose_drafts']['status'] = 'three-older-context-unmapped-and25-Deck-integrated-native-startup-proved-actual-comments-pending'
    ledger['active_source_prose_drafts']['note'] = 'V838 integrates the25 reviewed comments and expanded original paper crop. All native/font/copy/startup gates pass;no revised comment has actual activation credit.28 reviewed pending entries remain,not the full remaining scope.'
    for key in ('personal_chatter_v835', 'personal_chatter_v836'):
        ledger[key]['continued_by_integration'] = str(DOC)
        ledger[key]['remaining_gates'] = remaining
    ledger['formatting_watchlist']['Deck_personal_comment_phase_research'].update(
        status='generated-phase-repair-integrated-in-V838-actual-comment-samples-pending',
        scope='Only the original embedded Deck consumer;all25 native full-font/crop proofs pass. Actual comment display remains open.')
    ledger['formatting_watchlist']['Deck_personal_comment_visible_crop'] = {
        'source_crop': [0,60,144,24], 'target_crop': [0,60,216,36],
        'screen_rectangle': [16,112,232,148], 'proof': 'work/analysis/personal_chatter_v837/native_projection_and_font_proof.json',
        'release': str(ROM), 'actual_comment_display_pending': True}
    finding = {'id': 'Deck-personal-comment-parent-visible-crop-v837',
        'status': 'eight-data-byte-crop-expansion-integrated-V838-actual-display-pending',
        'detail': 'Original mode3 copies144x24 from the252x96 canvas. Expand only width/height to216x36 within the original paper.36-cell word wrapping and odd-row phase serialization preserve complete words. All parent modes/frame/header/palette submissions and original first144x24 area remain;actual RGB comment samples pending.',
        'proof': 'work/analysis/personal_chatter_v837/native_projection_and_font_proof.json',
        'no_completion_credit': True}
    assert not any(f.get('id') == finding['id'] for f in ledger['findings'])
    ledger['findings'].append(finding)
    checkpoint = ('V837-V838 integrates25 source-reviewed Deck actor comments1361-1385:18 revisions and7 retentions. '
        'The original parent copied only144x24 pixels;two owned size words now expand it to216x36 inside the unchanged paper/frame/palette. '
        'All25 native complete fonts,144 visible-width phase cases,11 original activity-entry threshold cases and7336 warm/cold message copies pass. '
        'Registered V838 and its exact clean-input patch preserve471 batches,114 accepted layers,3643 other COMMON strings,all scripts/graphics/HELP/ARM7/overlays and fixed123040 staged bytes. '
        'Seven ordinary cold-boot/New Game whole frames match V834 and are visually reviewed. '
        'A separate31600-frame no-fixture Rafael test reaches ordinary Deck,Explore setup,Port/departure/tutorial and actual at-sea Deck entry at tick673. '
        'At tick1584 the original previous-entry gap is only911;food runs out and a later letter intervenes. This is excluded as a clean activity baseline. '
        'Source gate runs on Deck entry,requires sea115,nonzero previous entry and both ages>=960;93E0 converts icon IDs to actors,not room assignments. '
        'No revised personal comment is actually displayed or completed. Fresh adequately supplied isolated activity samples and normal comment return remain. '
        'V834 remains the last family-verified reference;V838 is registered pending verification.646 complete,674 source/prose reviewed,28 reviewed pending entries remain. '
        'All wider prose/raw-source work and separate graphics/all18 plaques remain unfinished;older record checks remain scheduled after the full goal.')
    ledger['latest_checkpoint'] = checkpoint
    ledger['research_checkpoints'].append({'id': 'V838-Deck-dialogue-integration',
        'documentation': str(DOC), 'proof': pending['registered_release_proof'],
        'completed_entries_added': 0, 'whole_goal_complete': False,
        'previous_goal_turn_classification': 'progress:parent crop and36-cell complete native visible-font proof',
        'this_goal_turn_classification': 'progress:registered25-comment integration,exact patch,startup and source activity-entry access evidence'})
    before = read(ROOT / 'editorial_ledger_before_checkpoint.json')
    assert ledger['current_integrated_candidate'] == before['current_integrated_candidate']
    assert ledger['unresolved_graphics_work'] == before['unresolved_graphics_work']
    save(LEDGER, ledger)
    DOC.write_text('# V838: Deck comments integrated; actual activity verification pending\n\n' + checkpoint + '\n\n'
        '## Artifacts\n\n'
        f'- Experimental combined ROM: `{ROM}`\n- SHA-256: `{pending["sha256"]}`\n'
        f'- Clean-input patch: `{pending["patch"]}`\n- Patch SHA-256: `{pending["patch_sha256"]}`\n'
        f'- Manuscript: `{MANUSCRIPT}`\n- Release config: `{CONFIG}`\n\n'
        'The combined ROM was built through the registered builder. Canonical bytes and promotion status are unchanged. '
        'Controlled native proofs intercept graphics submission;they do not certify actual RGB activity display. '
        'The first Deck run ended on EOF at10400 before receiving interactive input;it is separately recorded and excluded. '
        'The successful interactive run uses fresh outputs and donor copies. Original donor hashes remain exact.\n\n'
        '## Next verification\n\n' + '\n'.join('- ' + s for s in remaining) + '\n', encoding='utf-8')
    paragraph = '\n\n## V838: Deck dialogue integration and activity access\n\n' + checkpoint + ' See [V838 evidence](personal_chatter_v838_integration.md).\n'
    for name in ('docs/translation_progress.md', 'docs/editorial_review_goal.md', 'docs/todo.md', 'docs/known_issues.md'):
        p = Path(name)
        assert '## V838:' not in p.read_text(encoding='utf-8')
        with p.open('a', encoding='utf-8') as handle:
            handle.write(paragraph)
    sources = set(p for p in ROOT.rglob('*') if p.is_file())
    sources.update(p for p in Path('work/analysis/personal_chatter_v837').rglob('*') if p.is_file())
    sources.update(map(Path, (str(DOC), str(LEDGER), str(MANUSCRIPT), CONFIG,
        'translations/personal_chatter_editorial_manuscript_v2.json', 'translations/release_stack.json',
        'scripts/build_integrated_release.py', 'dk4tool/patch/personal_chatter_editorial.py',
        'scripts/personal_chatter_layout_v837.py', 'scripts/verify_personal_projection_v837.py',
        'scripts/prepare_personal_release_v838.py', 'scripts/verify_personal_release_v838.py',
        'scripts/run_personal_release_v838.py', 'scripts/verify_personal_activity_gate_v838.py',
        'scripts/record_personal_integration_v838.py', 'docs/translation_progress.md',
        'docs/editorial_review_goal.md', 'docs/todo.md', 'docs/known_issues.md')))
    config = read(CONFIG)
    sources.update(map(Path, config['dependencies']))
    sources.update((ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta')))
    archived = []
    for source in sorted(sources):
        target = ARCHIVE / source.absolute().relative_to(Path.cwd())
        target.parent.mkdir(parents=True, exist_ok=True)
        copy2(source, target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
        archived.append({'source': str(source), 'archive': str(target), 'sha256': sha(target.read_bytes())})
    save(ROOT / 'archive_manifest.json', {'archive': str(ARCHIVE), 'files': archived,
        'all_copies_hash_verified': True, 'ROM_already_on_E_drive': str(ROM.absolute()),
        'actual_capture_folder_already_on_E_drive': str(CAP), 'whole_goal_complete': False})
    print('V838 checkpoint saved:registered ROM/patch,7336 copies,25 fonts and7 actual startup frames pass.646 complete unchanged;actual activity gates remain.', flush=True)


if __name__ == '__main__':
    main()
