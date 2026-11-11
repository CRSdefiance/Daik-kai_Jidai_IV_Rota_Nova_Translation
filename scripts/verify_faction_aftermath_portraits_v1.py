"""Verify the disband notice, both fleet voices and original sailing return."""

import argparse
import inspect
from pathlib import Path
from types import FunctionType

from scripts import replay_faction_aftermath_portraits_v1 as replay
from scripts import verify_diplomatic_letter_portraits_v1 as earlier
from scripts import verify_rumor_and_cooperation_v1 as prior
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_plaque_release_v247 import find_mask


ROOT, ROM, PROOF = replay.stage.ROOT, replay.stage.ROM, replay.stage.PROOF
PREDECESSOR = replay.predecessor.ROOT
LIVE = ROOT / 'faction_aftermath_portraits_gameplay_verification.json'
BOOT = ROOT / 'own_startup_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = Path('work/faction_aftermath_portraits_repo_qa_20261111.xml')
OBSERVED = (2691, 2703)


def verify_live():
    proof = prior.load(PROOF)
    assert prior.digest(ROM) == proof['research_ROM_sha256']
    image = prior.NdsImage.open(ROM)
    arm = image.read_file(replay.ARM)
    raster, _, _ = prior.font_tools(image)
    font = prior.GameAsciiFont.from_arm9(arm)
    kanji = image.read_file('/GRP/KANJI.FNT')
    terminal = replay.OUT / 'terminal.json'
    term = prior.load(terminal)
    path = Path(term['report'])
    assert prior.digest(path) == term['report_sha256'] and term['candidate_sha256'] == prior.digest(ROM)
    report, final_ram = prior.checked_report(path, term['candidate_sha256'], replay.FINAL)
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot']
    assert prior.digest(donor['source']) == donor['source_sha256'] == term['donor_sha256']
    assert all(not value for key, value in report.items() if key.startswith('synthetic_') and key != 'synthetic_condition_fixtures')
    frames = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('_navigation.png')}
    snaps = {row['frame']: row for row in report['read_only_pause_RAM_snapshots']}

    def raw(frame):
        row = snaps[frame]
        assert row['read_only_export'] and prior.digest(row['path']) == row['sha256']
        return Path(row['path']).read_bytes()

    plan = replay.OUT / 'commands.json'
    journal = replay.OUT / 'capture/navigation_command_journal.json'
    commands = prior.load(plan)
    assert prior.digest(plan) == term['commands_sha256']
    applied = prior.load(journal)['commands_received']
    assert all(row['validation_passed'] for row in applied)
    assert [row['command'] for row in applied] == commands == replay.commands()
    fixture = replay.fixture_controller(ROM)
    active = [dict(fixture(arm, raw(frame), request)[1], frame=frame)
              for frame, request in ((replay.sailing.PAUSE, commands[0]['condition_fixture']),
                  (9627, commands[3]['condition_fixture']), (10627, commands[-2]['condition_fixture']))]
    assert report['synthetic_condition_fixtures'] == active
    assert final_ram[replay.ENTRY:replay.STOP] == raw(replay.sailing.PAUSE)[replay.ENTRY:replay.STOP]
    assert final_ram[replay.ENTRY:replay.STOP] == arm[replay.ENTRY:replay.STOP]

    source = checked_text(inspect.getsource(prior.portrait_match), {
        'arm, kanji, raster, font, proof):': 'arm, kanji, raster, font, proof, name):',
        "'Trader', captured(frames[frame])": 'name, captured(frames[frame])',
        "text='Trader'": 'text=name',
    })
    env = vars(prior).copy()
    exec(compile(source, __file__ + '::exact-aftermath-portrait-and-nameplate-comparison', 'exec'), env)
    portraits = [env['portrait_match'](frame, n, frames, raw, snaps, arm, kanji, raster, font, proof, name)
                 for frame, n, name in ((9827, 2691, 'Barbarossa Hayreddin'), (10027, 2703, 'Salid Ajar'))]
    assert [row['message_ID'] for row in portraits] == list(OBSERVED)
    assert all(not row['original_arguments'] for row in portraits)
    notice = prior.dark_text(font, 'Hayreddin Clan has disbanded.', prior.captured(frames[9627]), (12, 292, 245, 320))
    returned = prior.captured(frames[10227])
    footer = [find_mask(font, label, returned, (0, 365, 256, 384)) for label in ('Rotate', 'Menu', 'Inspect', 'Sails')]

    def faction_state(snapshot):
        cpu, get = prior.get_machine(arm, snapshot)
        companies, actors = get(0xCB160), get(0xCB184)
        assert get(0x397D8, companies) == 2 and get(0x7F244) == 1
        assert bytes(cpu.mem_read(replay.BASE, len(snapshot))) == snapshot
        return dict(faction_location=get(0x3CD24, companies + 4 + 76 * replay.FACTION),
                    fleet_commander_affiliations=[get(0x7E958, actors + 4 + 32 * n) for n in (34, 51)])

    states = {frame: faction_state(raw(frame)) for frame in (8327, 9827, 10027, 10227, replay.FINAL)}
    assert [row['fleet_commander_affiliations'] for row in states.values()] == [
        [10, 10], [21, 10], [21, 21], [21, 21], [21, 21]]
    assert [row['faction_location'] for row in states.values()] == [25, 25, 25, 115, 115]
    prior.save(LIVE, dict(candidate_sha256=term['candidate_sha256'], observed_ids=list(OBSERVED),
        portraits=portraits, native_disband_notice=dict(capture=frames[9627], text=notice),
        return_to_sailing=dict(capture=frames[10227], native_sailing_footer=footer),
        original_fleet_and_faction_outcome=states, original_sailing_instructions_restored=True,
        fixture=active, actual_natural_defeat=False, hardware=False,
        evidence={str(p): prior.digest(p) for p in (path, terminal, plan, journal, PROOF, Path(__file__))}))
    print('Verified both native fleet portraits, the dissolution outcome, and the sailing return.')


def verify_startup():
    FunctionType(earlier.verify_startup.__code__, vars(earlier) | globals())()


def approve(viewed):
    FunctionType(prior.approve.__code__, vars(prior) | globals())(viewed)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('live', 'startup', 'approve'))
    parser.add_argument('--viewed-sheets', nargs='+')
    args = parser.parse_args()
    if args.action == 'approve':
        approve(args.viewed_sheets)
    elif args.action == 'live':
        verify_live()
    else:
        verify_startup()

