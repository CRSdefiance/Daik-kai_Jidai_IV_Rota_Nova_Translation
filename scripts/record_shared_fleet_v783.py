"""Archive two actual unidentified-fleet branches and retain the private-chat gate."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_shared_metadata_v783 import ROM
from scripts.register_shared_metadata_v783 import ROOT, CONFIG, MANUSCRIPT
from scripts.verify_village_wrap_v608 import read, save


def main():
    proof = read(ROOT/'fleet_gameplay_verification.json')
    replay = read(ROOT/'verification.json')
    assert proof['candidate_sha256'] == replay['candidate_sha256'] == sha(ROM.read_bytes())
    assert replay['whole_ROM_identical_to_V782'] and replay['registered_speaker_context_replay_complete']
    assert len(proof['holds']) == 4 and {p['message_id'] for p in proof['holds']} == {1032, 1034}
    assert all(p['complete_independent_font_and_blank_paper_exact'] and p['all_other_pixels_exact'] for p in proof['holds'])
    assert (len(proof['whole_screen_controls']), len(proof['paired_state_model_object_task_frames'])) == (28, 29)
    assert proof['fixture_receipt_reproduced_from_prefixture_RAM_in_both_ROMs']
    assert not proof['batch_completion_credit'] and not proof['original_whole_screen_blink_phase_controls']
    for p, h in read(CONFIG)['dependencies'].items():
        assert sha(Path(p).read_bytes()) == h, p
    assert sha(MANUSCRIPT.read_bytes()) == read(CONFIG)['manuscript_sha256']
    for p, h in replay['protected_files_unchanged'].items():
        assert sha(Path(p).read_bytes()) == h, p
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    assert ledger['records_editorially_completed'] == 367 and ledger['records_with_source_and_prose_pass'] == 420
    backup = ROOT/'editorial_ledger_before_fleet_gameplay.json'
    if not backup.exists():
        save(backup, ledger)
    doc = Path('docs/shared_dialogue_v783_fleet_gameplay.md')
    remaining = ['Private barmaid1049-1069']
    pending = ledger['pending_integrated_candidate']
    assert pending['profile'] == 'all-routes-unified-v783'
    pending.update({'details': str(doc), 'remaining_actual_families': remaining, 'remaining_gates': remaining,
                    'fleet_verification': str(ROOT/'fleet_gameplay_verification.json')})
    if 'fleet-destination1032-and-anchorage1034' not in pending['verified_actual_families']:
        pending['verified_actual_families'].append('fleet-destination1032-and-anchorage1034')
    ledger['active_source_prose_drafts']['status'] = '750-752-context-unmapped;1020-1069-native-reviewed-integrated;all-but-private-actual-families-verified;metadata-replay-registered'
    ledger['active_source_prose_drafts']['note'] = 'V783 retains all50 as drafts until a private-barmaid actual sample passes. Destination1032 and anchorage1034 now have complete actual glyph/state/return evidence;formal variants and barmaid1030 retain source/native coverage rather than individual activation claims.'
    ledger['coverage_units'][0]['next'] = 'Complete private-barmaid1049-1069 actual sample and final50-entry batch audit in registered V783. Continue COMMON1070 onward,resolve750-752,review all routes and remaining prose,and preserve graphics/older-record follow-up.'
    summary = ('V783 now verifies actual unidentified-fleet destination1032(Ceuta) and anchorage1034(Las Palmas):'
               'four complete glyph/paper holds,28 strict whole-screen controls,29 state/model/object/task pairs and normal town return. '
               'The bounded13-byte NPC-identity/report/order fixture reproduces in both ROMs;original three314-coin purchases and no new job are verified. '
               'Combined shared-batch scope is16 holds,317 strict screens,two full-screen phase controls and314 state/model/object/task pairs. '
               'Private barmaid sample remains;367 complete,420 source/prose,53 drafts. Full editorial goal and graphics audit remain unfinished.')
    ledger['latest_checkpoint'] = summary
    checkpoint = {'id': 'V783-unidentified-destination-and-anchorage-actual-gameplay', 'documentation': str(doc),
                  'candidate_sha256': proof['candidate_sha256'], 'new_actual_IDs': [1032, 1034],
                  'new_actual_complete_holds': 4, 'combined_shared_actual_complete_holds': 16,
                  'combined_strict_whole_screen_controls': 317, 'combined_original_whole_screen_phase_controls': 2,
                  'combined_state_model_object_task_frames': 314,
                  'new_editorially_completed': 0, 'remaining_gates': remaining, 'full_goal_complete': False}
    if not any(p['id'] == checkpoint['id'] for p in ledger['research_checkpoints']):
        ledger['research_checkpoints'].append(checkpoint)
    save(ledger_path, ledger)
    latest = read('out/editorial_review_latest.json')
    latest.update({'pending_integrated_candidate': pending, 'latest_research_checkpoint': str(doc)})
    save('out/editorial_review_latest.json', latest)
    doc.write_text('''# V783: actual unidentified-fleet rumors verified

The normal Treat Everyone gossip chain reaches both unidentified-fleet variants:
destination1032, "Some strange fleet is headed to Ceuta," and anchorage1034,
"I don't know whose fleet it is, but it's anchored at Las Palmas."
Both have two complete holds with clean margins, wrapping, all letters and full
town-name substitutions. Independent original-font planes and blank-paper pixels
match, as do all outside-dialogue pixels. Twenty-eight strict complete-screen
controls and29 paired state/model/object/task snapshots pass, without a blink
exception. Normal dismissal returns to town at13800. The final images are also
visually inspected; no cropped names or large internal gaps appear.

## Declared test state and original flow

Paired13800-frame V780/V783 cold boots use protected copies of the Istanbul donor.
The authorized isolated fixture modifies13 NPC-fleet bytes only: ten existing
fleets' source "already reported" bits through353DC, two captain bytes to the
source208 unidentified sentinel, and fleet7's order from1 to6. The latter excludes
it from destination gossip while preserving its native anchorage eligibility.
All other4MiB bytes, code, player fleet, cash, location and source saves remain
exact at insertion. No unidentified-fleet history, report history or ordinary
story progression is claimed earned. RNG results are not injected.

Complete native CPU preflights show the destination selector57C90 chooses1032 with
Ceuta, sets its normal reported flag, and the anchorage selector57A5C then chooses
1034 with Las Palmas. Both fixture receipts reproduce exactly from each emulator's
prefixture3200 snapshot. The actual emulator follows ordinary Tavern controls:
the first round gives the existing treasure hint; the second gives destination
at9600/10000; the third gives anchorage at12600/13000. Three original314-coin
purchases reduce cash8371 to7429. No job is created. This is a targeted automated
emulator test, without savestates, full-route or physical-device claims.

Formal1031/1033 and the barmaid1030 rumor retain their complete source/native
town-name matrix coverage; no individual actual activation is claimed for them.
The V783 ROM and patch are unchanged and byte-identical to V782. The prior
speaker-context metadata correction is registered and complete.

## Current scope and remaining gate

The combined50-entry batch has16 actual holds across eight IDs,317 strict whole-
screen controls, two complete original blink-phase controls and314 paired state/
model/object/task frames. Its remaining actual consumer sample is private barmaid
dialogue1049-1069. No entries receive completion credit yet:367 complete,
420 source/prose reviewed and53 drafts remain. V780 is the last wholly verified
editorial batch; V783 is experimental pending this last family and final audit.
Wider shared text, all routes, remaining prose, separate graphics audit and older-
record follow-up remain unfinished.

Evidence is under work/analysis/shared_metadata_v783 and archived on E:/Rota Nova
translations/Editorial review/V783 Shared metadata replay/Fleet tests. Verified
images are saved under Screenshots/Test fixtures/V783 Shared dialogue. No fixture
image is promoted as a finished guide image. No commit or GitHub push is made.
''', encoding='utf-8')
    for file in ('docs/todo.md', 'docs/known_issues.md', 'docs/translation_progress.md'):
        path = Path(file)
        text = path.read_text(encoding='utf-8')
        heading = '## V783: unidentified-fleet destination and anchorage gameplay'
        if heading not in text:
            path.write_text(text+'\n\n'+heading+'\n\n'+summary+' See [V783 fleet gameplay](shared_dialogue_v783_fleet_gameplay.md).\n', encoding='utf-8')
    save(ROOT/'fleet_checkpoint.json', {**checkpoint,
        'verification_sha256': sha((ROOT/'fleet_gameplay_verification.json').read_bytes()),
        'ROM_patch_and_frozen_dependencies_unchanged': True,
        'producer_sha256': sha(Path(__file__).read_bytes())})
    archive = Path('E:/Rota Nova translations/Editorial review/V783 Shared metadata replay/Fleet tests')
    shots = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V783 Shared dialogue')
    sources = [ROOT/p for p in ('fleet_gameplay_verification.json', 'effective_fleet_gameplay_verifier.py',
               'fleet_fixture_preflight.json', 'fleet_navigation_commands.jsonl', 'fleet_checkpoint.json')]
    sources += [Path('scripts')/p for p in ('native_unidentified_fleet_fixture_v783.py',
                'run_unidentified_fleet_capture_v783.py', 'verify_shared_fleet_gameplay_v783.py', 'record_shared_fleet_v783.py')]
    sources += [doc, ledger_path]
    for source in sources:
        target = archive/source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
    for report_path in proof['capture_reports']:
        source = Path(report_path)
        target = archive/source.parent.name/source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
    for hold in proof['holds']:
        source = Path(hold['capture']['path'])
        target = shots/f'ID{hold["message_id"]}_{hold["frame"]}_V783_VERIFIED_TEST.png'
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
    save(ROOT/'fleet_archive_receipt.json', {'archive': str(archive), 'screenshots': str(shots),
                                           'every_copy_SHA256_verified': True, 'no_completion_credit_yet': True})
    print('Four fleet holds archived;16 combined holds,317 strict screens,314 state pairs. Private barmaid sample remains;full goal active.', flush=True)


if __name__ == '__main__':
    main()
