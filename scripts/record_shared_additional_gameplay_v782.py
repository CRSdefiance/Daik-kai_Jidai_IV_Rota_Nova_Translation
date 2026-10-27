"""Archive two more verified families while preserving the full remaining goal."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.register_shared_release_v782 import CONFIG, MANUSCRIPT, ROOT
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v782_candidate.nds')
LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/shared_dialogue_v782_additional_gameplay.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V782 Shared dialogue integration/Supplemental crew and warning tests')
SHOTS = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V782 Shared dialogue')


def copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    assert sha(source.read_bytes()) == sha(target.read_bytes())


def main():
    config = read(CONFIG)
    for p, h in config['dependencies'].items():
        assert sha(Path(p).read_bytes()) == h, p
    assert sha(MANUSCRIPT.read_bytes()) == config['manuscript_sha256']
    digest = sha(ROM.read_bytes())
    patch = read(ROOT/'patch_proof.json')
    assert digest == patch['candidate_sha256'] == '9f55817772d2b1e940462f69103536654f0cbedbe959fb42670fc601f2d6e31d'
    assert sha(ROM.with_suffix('.xdelta').read_bytes()) == patch['patch_sha256']
    names = ['recruit_capacity_gameplay_verification.json', 'recruit_shortfall_gameplay_verification.json', 'warning_gameplay_verification.json']
    reports = [read(ROOT/p) for p in names]
    assert all(p['candidate_sha256'] == digest and not p['batch_completion_credit'] for p in reports)
    assert [{h['message_id'] for h in p['holds']} for p in reports] == [{1042}, {1035}, {1022}]
    assert all(len(p['holds']) == 2 for p in reports)
    assert all(h['complete_independent_font_and_blank_paper_exact'] and h['all_other_pixels_exact'] for p in reports for h in p['holds'])
    assert all(v['no_1000_coin_charge'] and v['no_new_job_scheduled'] for v in reports[2]['original_financial_and_job_cancellation_outcomes'])
    assert reports[1]['fixture_receipt_reproduced_from_prefixture_RAM_in_both_ROMs']
    assert reports[2]['both_fixture_receipts_reproduced_from_prefixture_RAM_in_both_ROMs']
    protected = read(ROOT/'checkpoint.json')['protected_files_unchanged']
    for p, h in protected.items():
        assert sha(Path(p).read_bytes()) == h, p
    controls = sum(len(p['whole_screen_controls']) for p in reports)
    states = sum(len(p['paired_state_model_object_task_frames']) for p in reports)
    phases = sum(len(p['original_whole_screen_blink_phase_controls']) for p in reports)
    assert (controls, states, phases) == (61, 60, 2)
    remaining = ['Missing-information1020', 'Village-coordinate1028/1029', 'Anchorage/destination fleet1030-1034', 'Private barmaid1049-1069']
    summary = ('V782 now has six complete actual holds across warning1022,required-crew-shortfall1035 and capacity1042;'
               '61 strict whole-screen controls,two complete original blink-phase controls and60 state/model/object/task pairs pass. '
               'Shortfall and warning fixtures reproduce exactly on V780/V782,original saves stay exact,and normal town returns pass. '
               'Warning cancellation charges no1000 coins and schedules no job. '
               'Missing-information,village-coordinate,fleet and private-chat actual samples remain required. '
               '367 completed,420 source/prose and53 drafts remain unchanged;the full editorial goal and separate graphics audit stay open.')
    ledger = read(LEDGER)
    assert ledger['records_editorially_completed'] == 367 and ledger['records_with_source_and_prose_pass'] == 420
    assert ledger['records_revised_and_integrated'] == 259 and ledger['retained_wordings_editorially_completed'] == 108
    if not (ROOT/'editorial_ledger_before_additional_gameplay.json').exists():
        save(ROOT/'editorial_ledger_before_additional_gameplay.json', ledger)
    pending = ledger['pending_integrated_candidate']
    assert pending['sha256'] == digest
    pending.pop('verified_actual_family', None)
    pending.update({'details': str(DOC), 'verified_actual_families': ['warning1022', 'required-shortfall1035', 'capacity1042'],
                    'remaining_actual_families': remaining, 'supplemental_verification': str(ROOT/'supplemental_gameplay_checkpoint.json')})
    ledger['active_source_prose_drafts']['status'] = '750-752-context-unmapped;1020-1069-native-reviewed-integrated;three-actual-families-verified;four-actual-families-pending'
    ledger['active_source_prose_drafts']['note'] = 'All50 new entries retain native approval but receive no completed-entry credit until the remaining actual families pass.53 drafts remain.'
    ledger['coverage_units'][0]['next'] = 'Complete missing-information1020,village1028/1029,fleet1030-1034 and private-barmaid1049-1069 actual samples;then close50-entry batch. Continue COMMON1070 onward,resolve750-752,review all routes and remaining prose,and preserve the separate graphics audit and older-record follow-up.'
    ledger['latest_checkpoint'] = summary
    checkpoint = {'id': 'V782-additional-required-crew-and-warning-gameplay', 'documentation': str(DOC),
                  'candidate_sha256': digest, 'new_actual_IDs': [1022, 1035], 'combined_actual_IDs': [1022, 1035, 1042],
                  'new_actual_complete_holds': 4, 'combined_actual_complete_holds': 6,
                  'strict_whole_screen_controls': controls, 'original_whole_screen_phase_controls': phases,
                  'paired_state_model_object_task_frames': states, 'new_editorially_completed': 0,
                  'remaining_gates': remaining, 'full_goal_complete': False}
    if not any(p['id'] == checkpoint['id'] for p in ledger['research_checkpoints']):
        ledger['research_checkpoints'].append(checkpoint)
    save(LEDGER, ledger)
    latest = read('out/editorial_review_latest.json')
    latest.update({'latest_research_checkpoint': str(DOC), 'pending_integrated_candidate': pending})
    save('out/editorial_review_latest.json', latest)
    DOC.write_text('''# V782: required-crew and warning scenes verified

Two more actual families now pass: required-crew shortfall **1035** and the
low-success warning **1022**. Together with capacity prompt 1042, there are six
complete holds across three original consumer families. The same registered V782
ROM and exact clean-input patch are unchanged. V782 remains experimental; V780
remains the last candidate whose entire editorial batch has finished its checks.

The batch still needs actual missing-information1020, village coordinates1028/1029,
anchorage/destination fleet rumors1030–1034, and private barmaid topics1049–1069.
No new entries receive completion credit yet. Totals remain 367 complete
(259 revised/108 retained), 420 source/prose reviewed, and 53 drafts. The whole
editorial goal, all route work, other prose, and the separate graphics audit
remain unfinished.

## Required crew: five short

Paired V780/V782 cold boots use copies of the protected Istanbul donor. The
authorized fixture invokes the original ship crew setter181B4 and copies only
Vestaros's crew halfword back to the emulator. One byte actually changes, 39 to 0.
Required crew 39, capacity 124, cash, health, cargo, location and other RAM are
unchanged at insertion. The normal game recruits 34 and computes a shortage of 5.
This is an isolated test state, not an earned crew loss or a normal journey.

The source-faithful prompt reads: "You're still 5 short of the crew you need.
Shall I recruit more?" The original full-width digit and every English letter are
verified in both complete holds6800/7200. Sixteen strict screen controls and16
state/model/object/task pairs match. Cancellation goes through Assign Sailors and
the unassigned-sailors confirmation, then returns normally to town at8800.

One cyan row blink differs at8000. A separate original-build cold boot reproduces
the identical fixture and input schedule and captures7900–8000. The entire V782
screen matches complete original frames; no rectangle is excluded to hide the
highlight. Its full-frame matches and provenance are recorded in the verifier.

## Low-success warning: original Bribe flow

The final V3 fixture changes three room/assignment bytes, Gerhard's XP word, and
one calendar word(+768 native ticks,16 source calendar days). Original Speech209
beats the original Tavern threshold15. Opponents, cash, menu flags, code and
source saves are unchanged. At9400, while target selection is being reached,
one Gerhard condition byte changes from0 to3. Original Speech becomes104; Pasha's
unchanged leader Speech is152. The original success calculation gives28, below
the Bribe warning threshold50. This is a disclosed prerequisite test, not earned
qualification, elapsed story time, illness, or a successful scheme.

The player normally opens Schemes, chooses Bribe, chooses Pasha, and chooses a
town's broker. The original routine selects voice-table warning1022:
"The chances of success seem very low... Do you want to proceed?"
Two complete holds 12200/12600 pass exact native glyphs, leading/trailing letters,
line breaks, margins, blank paper and outside-dialogue pixels. Thirty-four strict
whole-screen controls and33 state/model/object/task pairs match the baseline.
No additional animation exception is needed. Selecting No returns through the
normal Tavern menu to town at 13400. Cash stays 8371; no 1000-coin scheme charge is
committed and the complete original job records remain unchanged.

Both final fixture receipts reproduce byte for byte from the read-only RAM
snapshots saved before each fixture. The original harness and each active adapter
remain unchanged throughout their captures. All captures are targeted automated
emulator tests, without savestates, physical hardware or full-route claims.

## Earlier probes and the next lead

Earlier warning probes kept Schemes hidden; they receive no warning credit. The
original date-dependent availability threshold was380 against Speech209. A native
trace shows the16-day state yields threshold15. An initial visual reading of8371
as837 was wrong; the original8371 already satisfies the1000-coin requirement.
A funds-only test is preserved as an unused probe. The final V3 fixture leaves
cash unchanged. An earlier opponent-XP attempt failed its native assertion and
was never applied to an emulator. Its rejected source is preserved.

The next missing-information investigation executes the original57068 helper
against all five selectable local factions. Each currently has2–4 eligible known
towns, so ordinary selection will not reach1020 in this save. The helper's second
argument is an output array, not a region number. Its exact returned town lists
are recorded in missing_information_native_lead.json. A further bounded source
state will be needed; no actual1020 activation is claimed.

## Preservation and archive

Across all three actual families there are61 strict whole-screen controls, two
complete original blink-phase controls and60 state/model/object/task pairs. The
earlier seven ordinary startup/New Game comparisons remain valid. The frozen
production manuscript/configuration dependencies, combined ROM, patch, canonical
base, clean ROM and original donor saves retain their exact hashes. The user's
COMMON676/677 formatting repair remains covered by the existing V782 proof.

Verified screenshots are saved under E:/Rota Nova translations/Screenshots/Test
fixtures/V782 Shared dialogue. Supplemental evidence is archived beside the V782
integration archive. Test states are not promoted to finished guide screenshots.
The18 plaques, excluded Online bodies, preserved brown marks and older-record
follow-up remain open and unchanged. No new ROM, commit or GitHub push is made.
''', encoding='utf-8')
    for file in ('docs/todo.md', 'docs/known_issues.md', 'docs/translation_progress.md'):
        path = Path(file)
        text = path.read_text(encoding='utf-8')
        heading = '## V782: additional required-crew and warning gameplay'
        if heading not in text:
            path.write_text(text+'\n\n'+heading+'\n\n'+summary+' See [additional V782 gameplay](shared_dialogue_v782_additional_gameplay.md).\n', encoding='utf-8')
    checkpoint.update({'reports': [{'path': str(ROOT/p), 'sha256': sha((ROOT/p).read_bytes())} for p in names],
                       'ROM_patch_and_frozen_production_dependencies_unchanged': True, 'protected_files_unchanged': protected,
                       'previous_goal_turn_classification': 'Progress:50-entry registered integration and first actual family. This turn adds two verified actual families.',
                       'producer_sha256': sha(Path(__file__).read_bytes())})
    save(ROOT/'supplemental_gameplay_checkpoint.json', checkpoint)
    artifacts = [ROOT/p for p in names[1:]]+[ROOT/p for p in (
        'supplemental_gameplay_checkpoint.json', 'effective_shortfall_gameplay_verifier.py', 'effective_warning_gameplay_verifier.py',
        'shortfall_fixture_preflight.json', 'warning_fixture_preflight.json', 'warning_fixture_v2_preflight.json',
        'warning_fixture_v3_preflight.json', 'warning_opponent_probe_REJECTED.py', 'missing_information_native_lead.json')]
    artifacts += [Path('scripts')/p for p in (
        'native_recruit_shortfall_fixture_v782.py', 'run_recruit_shortfall_capture_v782.py',
        'native_warning_fixture_v782.py', 'run_warning_capture_v782.py', 'native_warning_fixture_v782_v2.py',
        'run_warning_capture_v782_v2.py', 'native_warning_fixture_v782_v3.py', 'run_warning_capture_v782_v3.py',
        'verify_shared_shortfall_gameplay_v782.py', 'verify_shared_warning_gameplay_v782.py', 'record_shared_additional_gameplay_v782.py')]
    artifacts += [DOC, LEDGER]
    for source in artifacts:
        copy(source, ARCHIVE/source.name)
    for report in reports[1:]:
        for name in report['capture_reports']:
            path = Path(name)
            copy(path, ARCHIVE/path.parent.name/path.name)
        for phase in report['original_whole_screen_blink_phase_controls']:
            path = Path(phase['capture_report'])
            copy(path, ARCHIVE/path.parent.name/path.name)
        for hold in report['holds']:
            copy(Path(hold['capture']['path']), SHOTS/f'ID{hold["message_id"]}_{hold["frame"]}_V782_VERIFIED_TEST.png')
        capture = read(report['capture_reports'][1])
        frame = report['normal_town_return_frame']
        row = next(r for r in capture['frames_captured'] if r['frame'] == frame)
        copy(Path(row['path']), SHOTS/f'Return_{frame}_V782_VERIFIED_TEST.png')
    save(ROOT/'supplemental_archive_receipt.json', {'archive': str(ARCHIVE), 'screenshots': str(SHOTS),
                                                   'every_copy_SHA256_verified': True, 'no_new_completion_credit': True})
    print('Two more families archived;6 holds across3 families,61 strict screens,60 state pairs. Four actual families remain;full goal active.', flush=True)


if __name__ == '__main__':
    main()
