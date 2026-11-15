"""Verify the native mutiny menu, dialogue, return to sailing, and exact-ROM startup."""

import argparse
from hashlib import sha256
from pathlib import Path
import struct
from types import FunctionType

from ndspy.code import MainCodeFile
from PIL import Image

from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_shared_notice_storage_v1 import checked_report, startup_proof
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools
from scripts.run_mutiny_replay_v1 import FIELD, ORIGINAL, OUT, set_condition
from scripts.run_mutiny_startup_v1 import PARENT, STARTUP
from scripts.stage_mutiny_review_v1 import ARM, BASE, OUTPUT, PROOF, ROM, ROOT, render_portrait


LIVE = OUT / 'mutiny_live_verification.json'
BOOT = STARTUP / 'own_startup_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = ROOT / 'repo_qa_mutiny.xml'
SPEECHES = ((516, 9627), (517, 9827), (549, 10327), (565, 10527), (572, 10727))
OBSERVED = [number for number, _ in SPEECHES]


def portrait_ink(path, crop):
    with Image.open(path) as screen:
        pixels = screen.convert('RGB').crop(crop)
    return bytes(color == (0, 8, 0) for color in pixels.get_flattened_data())


def menu_masks(menu, frames):
    width = menu['research']['minimum_width_units'] * 6
    assert width == 72 and menu['research']['modal_rectangle'] == [76, 54, 180, 138]
    assert digest(menu['sheet']['path']) == menu['sheet']['sha256']
    with Image.open(menu['sheet']['path']) as source:
        sheet = source.convert('RGB')
    masks = []
    for frame, styles in ((10027, (1, 1, 1)), (10127, (1, 15, 1))):
        with Image.open(frames[frame]['path']) as source:
            screen = source.convert('RGB')
        for option, style in enumerate(styles):
            index = 2 * option + int(style == 15)
            native = menu['captions'][index]
            assert native['option'] == option and native['style'] == style
            y_sheet = 55 * index + 17
            tile = sheet.crop((5, y_sheet, 5 + 3 * width, y_sheet + 36))
            plane = tile.resize((width, 12), Image.Resampling.NEAREST)
            ink = bytes(color == (0, 8, 0) for color in plane.get_flattened_data())
            y = 262 + option * 20
            crop = (90, y - 4, 166, y + 16)
            colors = screen.crop(crop).get_flattened_data()
            assert set(colors) <= {(205, 198, 180), (0, 165, 172), (8, 8, 8)}
            assert ((0, 165, 172) in colors) == (style == 15)
            expected = bytearray(76 * 20)
            for row in range(12):
                at = (row + 4) * 76 + 2
                expected[at:at + width] = ink[row * width:(row + 1) * width]
            assert bytes(color == (8, 8, 8) for color in colors) == expected
            masks.append(dict(frame=frame, option=option, style=style, english=native['text'],
                crop=crop, exact_native_ink_and_margins=True, native_plane_sha256=native['plane_sha256']))
    return masks


def verify_live():
    assert not LIVE.exists()
    staged = load(PROOF)
    sha = digest(ROM)
    terminal = load(OUT / 'terminal.json')
    assert sha == staged['research_ROM_sha256'] == terminal['candidate_sha256']
    assert terminal['donor_unchanged'] and digest(terminal['report']) == terminal['report_sha256']
    assert digest(terminal['commands']) == terminal['commands_sha256']
    report, final = checked_report(terminal['report'], sha, 11727)
    frames = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('navigation.png')}
    snapshots = {row['frame']: row for row in report['read_only_pause_RAM_snapshots']}

    def snapshot(frame):
        entry = snapshots[frame]
        assert entry['read_only_export'] and digest(entry['path']) == entry['sha256']
        return Path(entry['path']).read_bytes()

    image = NdsImage.open(ROM)
    arm, kanji = image.read_file(ARM), image.read_file('/GRP/KANJI.FNT')
    raster, _, _ = font_tools(image)
    fixtures = []
    for frame, mode in ((8327, 'select-mutiny'), (9627, 'restore-mutiny-selection')):
        _, receipt = set_condition(arm, snapshot(frame), {'mode': mode})
        fixtures.append(receipt | {'frame': frame})
    assert report['synthetic_condition_fixtures'] == fixtures
    assert final[FIELD - BASE:FIELD - BASE + 4] == ORIGINAL
    assert not any(report[k] for k in report if k.startswith('synthetic_') and k != 'synthetic_condition_fixtures')
    expand, output = (struct.unpack_from('<I', arm, p)[0] - BASE for p in (0x5444C, 0x54450))
    cases = {row['message_ID']: row for row in staged['native_portrait_cases']}
    storage = {row['message_ID']: row for row in staged['stored']}
    crop = (16, 296, 244, 360)
    observed = []
    for n, frame in SPEECHES:
        raw = snapshot(frame)
        plain, display = (raw[at:at + 256].split(b'\0', 1)[0] for at in (expand, output))
        assert plain.hex() == storage[n]['staged_hex'] and display.hex() == cases[n]['display_hex']
        pixels, glyphs = render_portrait(raster, arm, kanji, display)
        assert sha256(pixels).hexdigest() == cases[n]['native_ink_sha256']
        assert bytes(value == 1 for value in pixels) == portrait_ink(frames[frame]['path'], crop)
        observed.append(dict(message_ID=n, frame=frame, crop=crop, capture=frames[frame], RAM=snapshots[frame],
            complete_glyphs=len(glyphs), exact_native_foreground_and_margins=True, lines=cases[n]['visible_lines']))
    assert portrait_ink(frames[10927]['path'], crop) != portrait_ink(frames[10727]['path'], crop)

    masks = menu_masks(staged['native_menu'], frames)
    for frame in (10027, 10127):
        raw = snapshot(frame)
        for row in staged['menu_allocation']['changes']:
            assert struct.unpack_from('<I', raw, row['field'])[0] == row['target_pointer']
    journal = OUT / 'capture/navigation_command_journal.json'
    commands = load(journal)['commands_received']
    assert all(row['validation_passed'] for row in commands)
    by_frame = {row['frame']: row['command'] for row in commands}
    assert by_frame[10027]['buttons'] == ['DOWN'] and by_frame[10127]['buttons'] == ['A']
    assert by_frame[10727]['buttons'] == ['A']
    save(LIVE, dict(candidate_sha256=sha, actual_emulator_gameplay=True, hardware=False, fixture=fixtures,
        native_prerequisite_for_mutiny_not_observed=True, observed=observed, all_three_menu_choices=masks,
        original_DOWN_selects_appease_A_commits=True, original_cook_and_sailor_acceptance=True,
        original_A_dismissal_and_return_to_sailing=frames[10927], representative_paths_not_taken=['Quell Mutiny', 'Do Nothing'],
        evidence={str(p): digest(p) for p in (PROOF, OUT / 'terminal.json', Path(terminal['report']), journal, Path(__file__))}))
    print('Five complete live dialogue panels, six choice caption masks, and the appeal branch and return pass.')


def verify_startup():
    assert not BOOT.exists() and not CHECKPOINT.exists()
    staged, manuscript, live = map(load, (PROOF, OUTPUT, LIVE))
    sha = digest(ROM)
    assert staged['research_ROM_sha256'] == live['candidate_sha256'] == sha
    assert all(digest(path) == expected for path, expected in (staged['evidence'] | live['evidence']).items())
    assert [row['message_ID'] for row in live['observed']] == OBSERVED
    assert len(live['all_three_menu_choices']) == 6
    assert len(staged['stored']) == 65 and len(staged['native_portrait_cases']) == 77
    assert staged['selector_scope']['tested'] == 6552 and staged['storage']['all_41_blocks_fit_8KiB']
    assert len(manuscript['localized_IC_first_person']['cases']) == 14
    sheets = (*staged['contact_sheets'], staged['native_menu']['sheet'])
    assert all(digest(sheet['path']) == sheet['sha256'] for sheet in sheets)
    report_path = STARTUP / 'capture/capture_report.json'
    terminal = load(STARTUP / 'terminal.json')
    assert terminal['candidate_sha256'] == sha and terminal['report_sha256'] == digest(report_path)
    report, raw = checked_report(report_path, sha, 31000)
    parent_path = PARENT / 'capture/capture_report.json'
    predecessor = load(parent_path)
    assert predecessor['ROM_sha256'] == staged['registered_input']['candidate_sha256']
    assert predecessor['scripted_input_schedule'] == report['scripted_input_schedule']
    assert predecessor['core_options'] == report['core_options']
    old, new = ({s['frame']: s for s in run['frames_captured']} for run in (predecessor, report))
    frames = (1600, 2200, 3340, 4000, 16000, 31000)
    assert all(old[n]['framebuffer_sha256'] == new[n]['framebuffer_sha256'] for n in frames)
    arm = NdsImage.open(ROM).read_file(ARM)
    check_names = FunctionType(startup_proof.__code__, {**startup_proof.__globals__, 'STARTUP': report_path})
    startup = check_names(arm, sha)
    payload = bytes(MainCodeFile(arm, BASE).sections[3].data[:-48])
    assert len(payload) == 123264 and raw[POOL - BASE:POOL - BASE + len(payload)] == payload
    startup.update(candidate_sha256=sha, cold_boot=True, savestate=False, actual_captain_getter=3,
        read_only_snapshot=report['read_only_RAM_snapshot'], complete_deployed_payload_exact=True,
        exact_predecessor_capture_sha256=digest(parent_path))
    save(BOOT, startup)
    save(CHECKPOINT, dict(candidate_sha256=sha, approved_for_registered_successor=True, live_messages=OBSERVED,
        stored_dialogue=65, menu_labels=3, portrait_pages=65, native_portrait_expansions=77, native_menu_caption_planes=6,
        native_selector_cases=6552, crew_voice_choices=1449,
        evidence={str(p): digest(p) for p in (PROOF, OUTPUT, BOOT, LIVE, QA, Path(__file__))}))
    print('Exact startup, six parent frame matches, 24 protected getters and reviewed display evidence pass.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=('live', 'startup'))
    {'live': verify_live, 'startup': verify_startup}[parser.parse_args().phase]()
