"""Verify the original screen pixels and exact startup of both label fixes."""

from hashlib import sha256
from json import loads
from pathlib import Path
from types import FunctionType
from xml.etree import ElementTree

from PIL import Image, ImageChops

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_arrival_month_labels_v1 as replay
from scripts import verify_setup_save_equipment_v1 as startup
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask


stage, base = replay.stage, replay.base
ROOT, ROM = stage.ROOT, stage.ROM
PROOF = ROOT / 'startup_input.json'
BOOT = ROOT / 'own_startup_verification.json'
LIVE = ROOT / 'arrival_month_gameplay_verification.json'
QA = Path('work/arrival_month_labels_repo_qa_20261111.xml')
BIOGRAPHIES = replay.prior.STARTUP.parent
TRADE = (10400, 10700, 11000, 11300, 11600, 11900, 12200, 12800, 13100, 13400, 13700)
GOLDEN = 21200
TRADE_DIFF, GOLDEN_DIFF = (170, 169, 175, 178), (186, 249, 250, 259)
COLOR = (230, 230, 230)


def check_capture(folder, expected_sha):
    terminal_path = folder / 'terminal.json'
    terminal = base.load(terminal_path)
    report_path, commands = Path(terminal['report']), Path(terminal['commands'])
    assert base.digest(report_path) == terminal['report_sha256']
    assert base.digest(commands) == terminal['commands_sha256']
    assert base.digest(folder / 'inputs.json') == terminal['inputs_sha256']
    assert terminal['original_save_unchanged']
    report = base.load(report_path)
    assert report['ROM_sha256'] == terminal['candidate_sha256'] == expected_sha
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames'] == 22100
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    journal = report_path.with_name('navigation_command_journal.json')
    received = base.load(journal)['commands_received']
    assert all(row['validation_passed'] for row in received)
    assert [row['command'] for row in received] == [loads(line) for line in commands.read_text(encoding='utf-8').splitlines()]
    return terminal, report, (terminal_path, report_path, commands, journal)


def main():
    assert not BOOT.exists() and not LIVE.exists()
    proof = base.load(stage.PROOF)
    assert base.digest(ROM) == proof['research_ROM_sha256']
    assert base.load(PROOF)['registered_input']['candidate_sha256'] == proof['parent_sha256']
    FunctionType(startup.verify_startup.__code__, vars(startup) | globals())()
    old, new = [check_capture(folder, digest) for folder, digest in
                ((replay.prior.SALE, proof['parent_sha256']), (replay.SALE, proof['research_ROM_sha256']))]
    for key in ('commands_sha256', 'inputs_sha256'):
        assert old[0][key] == new[0][key]
    assert old[1]['battery_save_preloaded']['source_sha256'] == new[1]['battery_save_preloaded']['source_sha256']
    for report in (old[1], new[1]):
        fixture, = report['synthetic_golden_route_display_fixtures']
        assert fixture['frame'] == 12800 and fixture['before_purchase_cost'] == 572 and fixture['fixture_purchase_cost'] == 1
        assert fixture['only_temporary_trade_model_purchase_cost_word_changed']
    frames = [{row['frame']: row for row in run[1]['frames_captured'] if row['path'].endswith('_navigation.png')}
              for run in (old, new)]
    assert frames[0].keys() == frames[1].keys() and len(frames[0]) == 40
    changed, identical = [], []
    arm = base.NdsImage.open(ROM).read_file(stage.ARM)
    font = GameAsciiFont.from_arm9(arm)
    for frame, before in sorted(frames[0].items()):
        after = frames[1][frame]
        for row in (before, after):
            assert base.digest(row['path']) == row['PNG_sha256']
        with Image.open(before['path']) as source, Image.open(after['path']) as target:
            image = target.convert('RGB')
            diff = ImageChops.difference(source.convert('RGB'), image).getbbox()
        if frame in TRADE:
            ink, bounds = complete_mask(font, 'Arr.', image, 140, 169, COLOR)
            assert diff == TRADE_DIFF and ink == 37 and bounds == [140, 169, 164, 180]
            assert bounds[2] < 176
        elif frame == GOLDEN:
            ink, bounds = complete_mask(font, 'Arrival', image, 168, 249, COLOR)
            assert diff == GOLDEN_DIFF and ink == 78 and bounds == [168, 249, 210, 260]
            assert bounds[3] == 260
        else:
            assert diff is None and before['framebuffer_sha256'] == after['framebuffer_sha256']
            identical.append(frame)
            continue
        changed.append(dict(frame=frame, before=before, after=after, difference_bounds=list(diff),
                            complete_native_glyph_ink=ink, text_bounds=bounds))
    assert len(changed) == 12 and len(identical) == 28 and 22100 in identical
    for row in proof['records']:
        pos = row['field'] - stage.BASE
        value = bytes.fromhex(row['revised_hex'])
        assert arm[pos:pos + 8] == value and value.split(b'\0', 1)[0].decode('ascii') == row['visible']
        assert arm[pos + 8:pos + 8 + len(bytes.fromhex(row['next_string_hex']))].hex() == row['next_string_hex']
    tests = list(ElementTree.parse(QA).iter('testsuite'))
    assert sum(int(t.get('tests', 0)) for t in tests) == 34
    assert not any(int(t.get(k, 0)) for t in tests for k in ('errors', 'failures', 'skipped'))
    evidence = [*old[2], *new[2], stage.PROOF, BOOT, QA, Path(__file__)]
    base.save(LIVE, dict(candidate_sha256=proof['research_ROM_sha256'], parent_sha256=proof['parent_sha256'],
        actual_gameplay=True, hardware=False, observed_changes=changed, whole_frame_equal=identical,
        calendars_and_other_pixels_unchanged=True, original_Guild_return_exact=True,
        visible_records=[row['id'] for row in proof['records']], repository_tests=34,
        actual_trade_before_fixture=True, focused_golden_route_cost_fixture=True,
        evidence={str(path): sha256(Path(path).read_bytes()).hexdigest() for path in evidence}))
    print('Both full label masks pass. 12 frames differ only at the label and 28 are exact.')


if __name__ == '__main__':
    main()
