"""Verify the five live sea-event pages and original sailing return."""

from pathlib import Path
import struct

from PIL import Image

from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_shared_notice_storage_v1 import checked_report
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, render
from scripts.run_sea_event_bubbles_focused_v2 import (
    ARM, BASE, EVIDENCE, FIELD, FOCUSED, ORIGINAL, OUT, ROM, set_condition,
)
from scripts.seal_shared_text_source_v1 import ROOT


PROOF = ROOT / 'sea_event_focused_bubbles_verification.json'
FRAMES = ((457, 9627), (463, 9827), (469, 10027), (470, 10227), (478, 10427))
RETURN = 10627


def main():
    assert not PROOF.exists()
    storage, terminal = load(EVIDENCE), load(OUT / 'terminal.json')
    sha = digest(ROM)
    assert sha == storage['research_ROM_sha256'] == terminal['candidate_sha256']
    assert digest(terminal['report']) == terminal['report_sha256']
    assert digest(terminal['commands']) == terminal['commands_sha256']
    assert terminal['donor_unchanged']
    report, raw = checked_report(terminal['report'], sha, RETURN)
    assert not any(report[k] for k in report if k.startswith('synthetic_') and k != 'synthetic_condition_fixtures')
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and donor['source'] != donor['destination']
    assert digest(donor['source']) == donor['source_sha256']
    frames = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('navigation.png')}
    snapshots = {row['frame']: row for row in report['read_only_pause_RAM_snapshots']}
    rows = {row['message_ID']: row for row in storage['cases']}

    def snapshot(frame):
        row = snapshots[frame]
        assert row['read_only_export'] and digest(row['path']) == row['sha256']
        return Path(row['path']).read_bytes()

    image = NdsImage.open(ROM)
    arm = image.read_file(ARM)
    expected = []
    for frame, mode in ((8327, 'choose-bubbles'), (9627, 'restore-selection')):
        _, fixture = set_condition(arm, snapshot(frame), {'mode': mode})
        expected.append(fixture | {'frame': frame})
    assert report['synthetic_condition_fixtures'] == expected
    journal_path = OUT / 'capture/navigation_command_journal.json'
    commands = load(journal_path)['commands_received']
    assert all(row['validation_passed'] for row in commands)
    assert [(row['frame'], row['command'].get('buttons')) for row in commands[-6:]] == [
        (frame, ['A']) for _, frame in FRAMES] + [(RETURN, None)]
    raster, _, _ = font_tools(image)
    kanji = image.read_file('/GRP/KANJI.FNT')
    expand, output = [struct.unpack_from('<I', arm, offset)[0] - BASE for offset in (0x5444C, 0x54450)]
    crop = (16, 296, 244, 344)
    observed = []
    for number, frame in FRAMES:
        ram = snapshot(frame)
        plain, text = (ram[at:at + 256].split(b'\0')[0] for at in (expand, output))
        row = rows[number]
        assert text.hex() == row['display_hex'] and plain.hex() == row['staged_hex']
        assert ram[FIELD - BASE:FIELD - BASE + 4] == (FOCUSED if frame == 9627 else ORIGINAL)
        ink, glyphs = render(raster, arm, kanji, text)
        with Image.open(frames[frame]['path']) as screen:
            pixels = screen.convert('RGB').crop(crop)
        assert bytes(color == (0, 8, 0) for color in pixels.get_flattened_data()) == bytes(value == 1 for value in ink)
        observed.append(dict(message_ID=number, frame=frame, capture=frames[frame], crop=crop,
            complete_glyphs=len(glyphs), native_ink_matches_live_foreground_and_margins=True,
            staged_body_hex=plain.hex(), display_hex=text.hex()))
    assert rows[478]['native_formatter_addresses'] == [0x01FF9FAC]
    assert snapshot(RETURN) == raw and raw[FIELD - BASE:FIELD - BASE + 4] == ORIGINAL
    assert frames[RETURN]['framebuffer_sha256'] != frames[FRAMES[-1][1]]['framebuffer_sha256']
    save(PROOF, dict(candidate_sha256=sha, actual_emulator=True, hardware=False, observed=observed,
        original_notice_then_recognition_question_hearsay_and_evasive_order=True,
        original_compiler_generated_captain_wrap_visible=True, selector_word_restored=True,
        return_to_sailing_capture=frames[RETURN], fixture=expected, normal_random_event_selection=False,
        evidence={str(path): digest(path) for path in (
            EVIDENCE, OUT / 'terminal.json', Path(terminal['report']), journal_path, Path(__file__))},
        startup_and_registered_integration_pending=True, new_editorial_credit=0))
    print('Five complete live body masks, A transitions and restored sailing pass.')


if __name__ == '__main__':
    main()
