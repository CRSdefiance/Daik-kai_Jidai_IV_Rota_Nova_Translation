"""Actual helper/discount/duration and Rename glyphs, complete frames and state."""

import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_dialogue_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from scripts.finish_refit_display_v712 import load
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.native_refit_fixture_v834 import assign
from scripts.prepare_refit_release_v834 import ROOT
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_full_fleet_battle_v652 import fleet_models
from scripts.verify_full_fleet_victory_v654 import funds
from scripts.verify_refit_release_v834 import OLD, ROM
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save

BASE = 0x02000000
CAP = Path('work/emulation_v193')


def cstring(raw, pointer):
    return raw[pointer - BASE:pointer - BASE + 512].split(b'\0')[0]


def main():
    reports, shots, receipts, ram = {}, {}, {}, {}
    for case, path, frames in (('helper_before', OLD, 18300), ('helper_after', ROM, 18300),
                              ('rename_after', ROM, 14600), ('newgame_after', ROM, 4000)):
        folder = CAP / f'refit_dialogue_v834_{case}'
        reports[case], shots[case], receipts[case] = load(folder, sha(path.read_bytes()), frames)
        snapshots = {}
        for row in reports[case].get('read_only_capture_RAM_snapshots', []) + reports[case].get('read_only_pause_RAM_snapshots', []):
            raw = Path(row['path']).read_bytes()
            assert len(raw) == 0x400000 and sha(raw) == row['sha256'] and row['read_only_export']
            assert row['frame'] not in snapshots or snapshots[row['frame']] == raw
            snapshots[row['frame']] = raw
        ram[case] = snapshots
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    old_arm = NdsImage.open(OLD).read_file('/__arm9__.bin')
    rom = NdsImage.open(ROM)
    kanji = rom.read_file('/GRP/KANJI.FNT')
    entries = current_entries(rom.read_file('/COMMON/MESFILE.DK4'), arm)
    owner, printed, wrapped = [struct.unpack_from('<I', arm, n)[0] for n in (0x552A0, 0x5444C, 0x54450)]
    assert reports['helper_before']['scripted_input_schedule'] == reports['helper_after']['scripted_input_schedule']
    journals = [read(CAP / f'refit_dialogue_v834_{c}/navigation_command_journal.json') for c in ('helper_before', 'helper_after')]
    assert journals[0]['commands_received'] == journals[1]['commands_received']
    fixtures = []
    for case, a in (('helper_before', old_arm), ('helper_after', arm)):
        report = reports[case]
        assert report['controlled_refit_helper_adapter']['original_harness_file_unchanged']
        assert not any(v for k, v in report.items() if k.startswith('synthetic_') and k != 'synthetic_refit_helper_fixtures')
        fixture, = report['synthetic_refit_helper_fixtures']
        expected, replay = assign(a, ram[case][3200], {'mode': 'qualified_helper'})
        assert replay == {k: v for k, v in fixture.items() if k != 'frame'}
        assert len(fixture['changes']) == 3 and fixture['frame'] == 3200
        assert fixture['expected_original_offer_ID'] == 1256 and fixture['source_discount_percent'] == 6
        assert sha(expected) == fixture['after_RAM_sha256']
        fixtures.append(fixture)
    for case in ('rename_after', 'newgame_after'):
        assert not any(v for k, v in reports[case].items() if k.startswith('synthetic_'))
    for case in ('helper_before', 'helper_after', 'rename_after'):
        donor = reports[case]['battery_save_preloaded']
        assert donor['source'] != donor['destination'] and donor['copied_byte_exact_before_cold_boot']
        assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    assert not reports['newgame_after'].get('battery_save_preloaded')
    holds = []
    helper_holds = {12500: 1266, 14200: 1256, 14700: 1263, 15100: 1246, 15500: 1267, 15900: 1266, 16300: 1266}

    def glyphs(case, frame, number):
        raw = ram[case][frame]
        template, visible = cstring(raw, owner + 0x2030), cstring(raw, wrapped)
        assert template == entries[number].text, (case, frame, number, template)
        expanded = entries[number].text
        arguments = {1263: '６'.encode('cp932'), 1246: '１８８０'.encode('cp932'), 1267: '２ days'.encode('cp932')}
        if number in arguments:
            expanded = expanded.replace(b'%s', arguments[number]).replace(b'%%', b'%')
        assert cstring(raw, printed) == expanded
        assert b' '.join(visible.split()) == b' '.join(expanded.split())
        lines = [s.strip().decode('cp932') for s in visible.split(b'\n')]
        plane = raster(arm, visible, 0x01FFCE40 - BASE, size=(228, 64), instruction_limit=2000000)
        assert plane == independent_font(arm, kanji, lines)
        expected = {(16 + i % 228, 296 + i // 228) for i, v in enumerate(plane) if v == 1}
        shadow = {(16 + i % 228, 296 + i // 228) for i, v in enumerate(plane) if v == 15}
        image = shots[case][frame]
        actual = {(x, y) for y in range(294, 366) for x in range(16, 244) if image.getpixel((x, y)) == (0, 8, 0)}
        assert expected == actual, (case, frame, number, len(expected - actual), len(actual - expected))
        shadow_colours = {image.getpixel(p) for p in shadow}
        assert len(shadow_colours) <= 1
        holds.append({'case': case, 'frame': frame, 'message_id': number, 'lines': lines,
                      'complete_actual_native_independent_glyphs_and_blank_ink_equal': True,
                      'template_and_original_substitutions_exact': True,
                      'consistent_visible_left_margin_and_complete_first_final_letters': True})
        return plane, next(iter(shadow_colours)) if shadow_colours else None

    planes = {f: glyphs('helper_after', f, n) for f, n in helper_holds.items()}
    for f, n in ((12800, 1264), (13400, 1265), (14000, 1264)):
        glyphs('rename_after', f, n)
    # Recover every paper pixel from actual baseline frames with no native ink
    # at that position. The native before-plane masks include historical spaces.
    witnesses = []
    modified_holds = set(helper_holds) - {15100}  # Unchanged Yes/No price panel has its own footer.
    for f in sorted(modified_holds):
        visible = cstring(ram['helper_before'][f], wrapped)
        plane = raster(old_arm, visible, 0x01FFCE40 - BASE, size=(228, 64), instruction_limit=2000000)
        witnesses.append((shots['helper_before'][f], plane))
        witnesses.append((shots['helper_after'][f], planes[f][0]))
    for f in (12800, 13400):
        visible = cstring(ram['rename_after'][f], wrapped)
        plane = raster(arm, visible, 0x01FFCE40 - BASE, size=(228, 64))
        witnesses.append((shots['rename_after'][f], plane))
    paper = Image.new('RGB', (228, 72))
    always_covered = []
    for y in range(294, 366):
        for x in range(16, 244):
            colours = set()
            for image, plane in witnesses:
                value = plane[(y - 296) * 228 + x - 16] if 296 <= y < 360 else 0
                if value == 0:
                    colours.add(image.getpixel((x, y)))
            if not colours:
                # No paper is visible here in any witness. This position must
                # be replaced by independently verified ink in every model.
                index = (y - 296) * 228 + x - 16
                assert 296 <= y < 360 and all(plane[index] for _, plane in witnesses)
                always_covered.append([x, y])
                colour = shots['helper_before'][14200].getpixel((x, y))
            else:
                assert len(colours) == 1, ('paper witness', x, y, colours)
                colour = next(iter(colours))
            paper.putpixel((x - 16, y - 294), colour)
    unchanged = []
    assert shots['helper_before'].keys() == shots['helper_after'].keys()
    for f, image in shots['helper_after'].items():
        expected = shots['helper_before'][f].copy()
        if f in modified_holds:
            expected.paste(paper, (16, 294))
            plane, shadow_colour = planes[f]
            for i, value in enumerate(plane):
                if value:
                    expected.putpixel((16 + i % 228, 296 + i // 228), (0, 8, 0) if value == 1 else shadow_colour)
        else:
            unchanged.append(f)
        assert image.tobytes() == expected.tobytes(), ('whole paired frame', f)
    rename_old, rename_shots, rename_receipt = load(CAP / 'refit_dialogue_v832_name_entry', sha(OLD.read_bytes()), 14600)
    rename_controls = []
    for f, image in shots['rename_after'].items():
        old = rename_shots[f].copy()
        if f in (12800, 14000):
            old.paste(paper, (16, 294))
            visible = cstring(ram['rename_after'][f], wrapped)
            plane = raster(arm, visible, 0x01FFCE40 - BASE, size=(228, 64))
            for i, value in enumerate(plane):
                assert value in (0, 1)
                if value:
                    old.putpixel((16 + i % 228, 296 + i // 228), (0, 8, 0))
        else:
            rename_controls.append(f)
        assert old.tobytes() == image.tobytes(), ('Rename whole frame', f)
    _, startup, startup_receipt = load(CAP / 'refit_editorial_v831_newgame_after', sha(OLD.read_bytes()), 4000)
    assert startup.keys() == shots['newgame_after'].keys()
    assert all(im.tobytes() == startup[f].tobytes() for f, im in shots['newgame_after'].items())
    def state(a, raw):
        cpu = machine(a)
        cpu.mem_write(BASE, raw)
        call(cpu, 0xCB1B4, ())
        calendar = cpu.reg_read(UC_ARM_REG_R0)
        tick = struct.unpack('<I', cpu.mem_read(calendar + 8, 4))[0]
        return {'funds': funds(a, raw), 'calendar_tick': tick, 'fleet': fleet_models(a, raw, 1)}
    states = []
    for f in (3200, 13800, 14200, 14700, 15100, 15500, 16300, 18300):
        a, b = state(old_arm, ram['helper_before'][f]), state(arm, ram['helper_after'][f])
        assert a == b and len(b['fleet']) == 5
        assert b['funds'] == (25975 if f < 15500 else 24095)
        assert b['calendar_tick'] == (6871 if f < 16300 else 6967)
        states.append({'frame': f, **b})
    assert state(arm, ram['rename_after'][3200]) == state(arm, ram['rename_after'][14600])
    selected = [('helper_after', f) for f in (13800, 14200, 14700, 15100, 15500, 16300, 18300)]
    selected += [('rename_after', f) for f in (12800, 13100, 13400, 13700, 14600)]
    sheet = Image.new('RGB', (4 * 256, 3 * 412), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, (case, f) in enumerate(selected):
        x, y = i % 4 * 256, i // 4 * 412
        draw.text((x + 6, y + 6), f'V834 {case} {f}', fill='white')
        sheet.paste(shots[case][f], (x, y + 28))
    image_path = ROOT / 'actual_refit_dialogue_review_sheet.png'
    sheet.save(image_path)
    save(ROOT / 'actual_gameplay_verification.json', {
        'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()), 'receipts': receipts,
        'earlier_Rename_reference': rename_receipt, 'earlier_New_Game_reference': startup_receipt,
        'paired18300_frame_helper_cold_boots_with_identical_inputs_and_disclosed3_byte_fixtures': fixtures,
        'ordinary14600_frame_Rename_without_new_gameplay_fixture': True,
        'actual_complete_dialogue_holds': holds,
        'all_paired_helper_frames_match_complete_expected_two_screen_models': True,
        'unchanged_helper_menu_startup_selection_and_exit_controls': unchanged,
        'all_Rename_frames_match_complete_expected_models': True, 'unchanged_Rename_controls': rename_controls,
        'all7_ordinary_no_save_New_Game_frames_exact': True,
        'native_paper_all_available_unoccluded_colour_witnesses_agree': True,
        'always_covered_positions_replaced_by_verified_glyphs_in_every_model': always_covered,
        'paired_state_checks': states, 'actual_2000_cost_less6percent_equals1880_charge': True,
        'two_days_equals96_calendar_ticks_and_both_builds_match': True,
        'Rename_five_ship_names_Hull_Crew_money_calendar_unchanged': True,
        'review_sheet': str(image_path), 'review_sheet_sha256': sha(image_path.read_bytes()),
        'visual_review_pending': True,
        'scope': 'Six distinct revised/retained message IDs in actual controlled cold-boot scenes plus existing final-price confirmation. All12 have independent bounded native coverage. Qualified helper uses an isolated room/role fixture;not earned assignment,all voice-class visits,full playthrough or hardware verification.',
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V834 actual full fonts, paired screens,1880 charge/96 ticks,Rename and ordinary startup pass; visual review pending.', flush=True)


if __name__ == '__main__':
    main()
