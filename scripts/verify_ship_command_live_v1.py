"""Bind live ship-menu glyphs and Back/No behavior to the staged ROM."""

import json
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.market_goods_info_terminator_v1 import PAYLOAD
from dk4tool.patch.ship_command_label_v1 import ALLOCATION, FIELD, NEW_POINTER
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import BASE, machine
from scripts.run_ship_command_empty_crew_v1 import OUT as LIVE
from scripts.stage_ship_command_release_v1 import ARM, CANDIDATE, OUT, STAGED, WORK


OUTPUT = OUT / 'ship_menu_actual_verification.json'


def main():
    assert not OUTPUT.exists()
    staged = load(STAGED)
    terminal_path = LIVE/'terminal.json'
    terminal = load(terminal_path)
    report_path = Path(terminal['report'])
    report = load(report_path)
    assert terminal['exit_code'] == 0 and terminal['original_donor_unchanged']
    assert digest(report_path) == terminal['report_sha256']
    assert report['ROM_sha256'] == staged['candidate_sha256'] == digest(CANDIDATE)
    assert report['frames'] == 8500 and report['cold_boot'] and not report['savestate_loaded']
    fixture, = report['synthetic_battle_recovery_proximity_fixtures']
    assert (fixture['frame'], fixture['ship_slot'], fixture['ship_name']) == (7600, 1, 'Latina')
    change, = fixture['changes']
    assert change['after'] == 0 and fixture['verified_only_original_mobile_crew_field_changed']
    journal = LIVE/'navigation_inputs.jsonl'
    assert digest(journal) == terminal['journal_sha256']
    commands = [json.loads(s) for s in journal.read_text(encoding='utf-8').splitlines()]
    assert [(c['until'], c['buttons']) for c in commands[-5:-1]] == [
        (8000,['A']), (8100,['DOWN']), (8300,['B']), (8500,['B'])]
    captured = {c['frame']:c for c in report['frames_captured'] if c['path'].endswith('navigation.png')}
    frames = {}
    for frame in (7800, 8000, 8100, 8300, 8500):
        shot = captured[frame]
        assert digest(shot['path']) == shot['PNG_sha256']
        frames[frame] = shot
    menu_path = WORK/'native_menu/native_ship_menu.json'
    menu = load(menu_path)
    planes = {(c['option'], c['style']):c for c in menu['captions']}
    background = (205,198,180)
    highlight = (0,165,172)
    foreground = (8,8,8)
    masks = []
    for frame, styles in [(8000,(1,1)), (8100,(1,15)), (8500,(1,1))]:
        with Image.open(frames[frame]['path']) as capture:
            image = capture.convert('RGB')
        for option, style in enumerate(styles):
            entry = planes[option,style]
            source = Path(entry['plane'])
            assert digest(source) == entry['plane_sha256']
            expected = bytes(bool(v) for v in source.read_bytes())
            assert len(expected) == 72*12
            y = 272+20*option
            actual = image.crop((90,y-4,166,y+16))
            region = actual.tobytes()
            found = set(actual.get_flattened_data())
            assert found <= {background, highlight, foreground}
            assert (highlight in found) == (style == 15)
            # Compare the whole crop, including the blank margin around both ends of the label.
            target = bytearray(76*20)
            for row in range(12):
                offset = (row+4)*76+2
                target[offset:offset+72] = expected[row*72:(row+1)*72]
            assert bytes(color == foreground for color in actual.get_flattened_data()) == target
            masks.append(dict(frame=frame, option=option, style=style, text=entry['text'],
                crop=[90,y-4,166,y+16], complete_ink_mask_and_blank_margins_equal_native=True,
                plane_sha256=entry['plane_sha256'], rgb_bytes=len(region)))
    assert frames[8000]['PNG_sha256'] == frames[8500]['PNG_sha256']
    assert frames[8300]['PNG_sha256'] != frames[8100]['PNG_sha256']
    native = report['read_only_native_state']
    assert native['read_only_export'] and not native['state_loaded'] and native['main_RAM_unchanged_by_export']
    itcm = native['regions']['ITCM']
    assert digest(itcm['path']) == itcm['sha256']
    offset = NEW_POINTER & 0x7FFF
    memory = Path(itcm['path']).read_bytes()
    assert memory[offset-len(PAYLOAD):offset+len(ALLOCATION)] == PAYLOAD+ALLOCATION
    final = report['read_only_RAM_snapshot']
    assert digest(final['path']) == final['sha256']
    raw = Path(final['path']).read_bytes()
    assert struct.unpack_from('<I', raw, FIELD)[0] == NEW_POINTER
    cpu = machine(NdsImage.open(CANDIDATE).read_file(ARM))
    cpu.mem_write(BASE, raw)
    call(cpu, 0x36C70, (fixture['fleet']+12+8,))
    mobile = cpu.reg_read(UC_ARM_REG_R0)
    assert mobile+0x1A == change['address']
    call(cpu, 0x55444, (mobile,))
    assert cpu.reg_read(UC_ARM_REG_R0) == 0
    save(OUTPUT, dict(candidate_sha256=staged['candidate_sha256'], terminal_frame=8500, actual_emulator_gameplay=True,
        disclosed_single_mobile_crew_value_fixture=fixture, natural_crew_loss_or_ship_abandonment_claimed=False,
        native_menu_normal_highlight_and_return_directly_viewed=True, exact_normal_and_highlight_caption_masks=masks,
        both_back_and_no_inputs_observed=True, first_back_opens_original_named_confirmation=True,
        no_returns_to_pixel_identical_menu_and_preserves_ship=True, complete_normal_and_highlight_label_pixels=True,
        actual_ITCM_both_market_and_ship_literals_exact=True, unchanged_donor=True, hardware=False,
        captures=frames, live_ITCM_sha256=itcm['sha256'], final_RAM_sha256=final['sha256'],
        evidence={str(p):digest(p) for p in [terminal_path, report_path, journal, menu_path, Path(__file__)]},
        new_credit=0, registered_integration_pending=True))
    print('Six complete live caption masks match. Back opens confirmation and No restores the menu and preserves Latina.')


if __name__ == '__main__':
    main()
