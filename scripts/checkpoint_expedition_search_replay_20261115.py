"""Verify the representative Search report and transition on the staged candidate."""

from hashlib import sha256
from json import loads
from pathlib import Path
from struct import unpack_from
from unicodedata import normalize

from scripts import replay_crew_and_shore_reports_v1 as precedent
from scripts import stage_expedition_report_wraps_20261115 as stage
from scripts.navigate_hot_spring_crew_v1652 import visible_paper
from scripts.verify_captain_biographies_v1 import captured
from scripts.verify_crew_and_shore_reports_v1 import fleet_state
from scripts.verify_personal_gameplay_v841 import get_machine


base = stage.base
OUTPUT = stage.ROOT / 'search_compatibility_verification.json'
PAPER = (16, 296, 244, 360)
ARM_BASE = 0x02000000


def main():
    assert not OUTPUT.exists()
    staged = base.load(stage.STORED)
    assert base.digest(stage.ROM) == staged['candidate_sha256']
    folder = stage.ROOT / 'shore_attack'
    terminal_path = folder / 'terminal.json'
    terminal = base.load(terminal_path)
    report_path, commands = Path(terminal['report']), Path(terminal['commands'])
    assert base.digest(report_path) == terminal['report_sha256']
    assert base.digest(commands) == terminal['commands_sha256']
    report = base.load(report_path)
    plan, historical_report, _, donor, _, expected_commands, end = precedent.history('attack')
    assert base.digest(donor) == plan['source_donor_sha256']
    assert report['ROM_sha256'] == staged['candidate_sha256'] and report['frames'] == end
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    assert report['battery_save_preloaded']['source_sha256'] == base.digest(donor)
    journal_path = report_path.with_name('navigation_command_journal.json')
    journal = base.load(journal_path)['commands_received']
    assert all(row['validation_passed'] for row in journal)
    assert [row['command'] for row in journal] == expected_commands == [
        loads(line) for line in commands.read_text(encoding='utf-8').splitlines()]
    snapshots = {row['frame']: row for row in report['read_only_pause_RAM_snapshots']}
    frames = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('_navigation.png')}
    image = base.NdsImage.open(stage.ROM)
    arm = image.read_file(stage.ARM)
    raster, _, _ = stage.font_tools(image)
    font_resource = image.read_file('/GRP/KANJI.FNT')
    owner, wrapped, modal = [unpack_from('<I', arm, off)[0] - ARM_BASE for off in (0x552A0, 0x54450, 0x54894)]
    evidence = {str(path): base.digest(path) for path in (
        terminal_path, report_path, commands, journal_path, historical_report, donor, Path(__file__))}

    def snapshot(frame):
        entry = snapshots[frame]
        raw = Path(entry['path']).read_bytes()
        assert entry['read_only_export'] and len(raw) == 0x400000
        assert sha256(raw).hexdigest() == entry['sha256']
        evidence[entry['path']] = entry['sha256']
        return raw

    def text(raw, offset):
        return raw[offset:offset + 512].split(b'\0', 1)[0]

    fixtures = report['synthetic_battle_recovery_proximity_fixtures']
    apply = precedent.fixtures(staged['target_ARM9_sha256'])
    requests = {row['frame']: row['command']['battle_fixture'] for row in journal if 'battle_fixture' in row['command']}
    assert len(requests) == len(fixtures)
    for fixture in fixtures:
        frame = fixture['frame']
        _, reproduced = apply(arm, snapshot(frame), requests[frame])
        assert fixture == reproduced | {'frame': frame}

    before, follow, returned = map(snapshot, (14657, 14877, 15097))
    original = base.load(Path('translations/editorial_checkpoints/SharedText_20261110_v1/'
                              'crew_and_shore_reports_context_v2.json'))
    group = next(row for row in original['native_context'] if row['first_ID'] == 2243)
    _, get = get_machine(arm, before)
    identity = get(0x82478, get(0xCB1A8) + 0x2090, group['original_role_argument'])
    actor = get(0xCB184) + (0x19E4 if identity == get(0x7F244) else 4 + 32 * identity)
    number = get(0x53F4C, actor, group['table'])
    assert number == 2244
    common = image.read_file(stage.COMMON)
    directory = sha256(arm[stage.DIRECTORY_OFFSET:stage.TABLE_OFFSET]).hexdigest()
    stored = stage.owned_entries(common, arm, directory)
    assert text(before, owner + 0x2030) == stored[number].text
    displayed = text(before, wrapped)
    pixels, glyphs = stage.render_portrait(raster, arm, font_resource, displayed)
    frame = frames[14657]
    screen = captured(frame)
    evidence[frame['path']] = frame['PNG_sha256']
    assert bytes(pixel == (0, 8, 0) for pixel in screen.crop(PAPER).get_flattened_data()) == pixels
    assert normalize('NFKC', text(follow, modal).decode('cp932')).strip() == 'Sailors lost: 11.'
    initial, final = [fleet_state(arm, raw) for raw in (before, returned)]
    assert sum(initial['crew']) - sum(final['crew']) == 11
    resume = frames[15097]
    captured(resume)
    evidence[resume['path']] = resume['PNG_sha256']
    assert final['original_mode'] == [0, 0, 0] and not visible_paper(resume['path'])
    base.save(OUTPUT, dict(candidate_sha256=staged['candidate_sha256'], native_message=number, native_actor=identity,
        complete_glyphs=len(glyphs), display_hex=displayed.hex(), mask_sha256=sha256(pixels).hexdigest(),
        original_sailor_loss=11, original_return_to_sailing=True, exact_fixture_count=len(fixtures),
        case_scope='Existing Search replay uses copied save and disclosed condition setup. The changed report variants are offline.',
        hardware=False, evidence=evidence))
    print('Verified the Search report, its 11-sailor follow-up and the original return to sailing.')


if __name__ == '__main__':
    main()
