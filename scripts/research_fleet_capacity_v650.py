"""Bind the ordinary five-ship/dock test and its newly observed prompt defects."""

import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.search_miniature_captures_v577 import scan_image, template
from scripts.verify_regional_ui_v616 import full_cells
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/fleet_capacity_v650')
RUN = Path('E:/Rota Nova translations/Generated/work/emulation_v193/fleet_capacity_v650_actual')


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    report_path = RUN / 'capture_report.json'
    report = read(report_path)
    assert report['ROM_sha256'] == pre['candidate_sha256'] and report['frames'] == 56600
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
    assert report['battery_save_preloaded']['source_sha256'] == pre['donor_sha256']
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    rom = NdsImage.open(pre['candidate'])
    arm = rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds')
    original = clean.read_file('/__arm9__.bin')
    for lo, hi in ((0xCB1A8, 0xCB1B4), (0x2E58C, 0x2E598),
                   (0x36C94, 0x36CBC), (0x181B4, 0x181C4), (0x18398, 0x183A8),
                   (0x5A9E8, 0x5AA24)):
        assert arm[lo:hi] == original[lo:hi]
    snapshots = {r['frame']: r for r in report['read_only_pause_RAM_snapshots']}
    rows = []
    for frame in (3200, 30000, 33000, 38400, 48600, 51000, 54800, 56600):
        source = snapshots[frame]
        raw = Path(source['path']).read_bytes()
        assert len(raw) == 0x400000 and sha(raw) == source['sha256'] and source['read_only_export']
        u = machine(arm)
        u.mem_write(BASE, raw)

        def get(offset, args=(), cpu=u):
            call(cpu, offset, args)
            return cpu.reg_read(UC_ARM_REG_R0)

        root, index = get(0xCB1A8), get(0x2E58C)
        assert index == 1
        fleet = root + 4 + index * 0x84
        ships = []
        # Original 0205A9E8 uses descriptor base + slot*8, and the loop bounds five.
        for slot in range(5):
            descriptor = fleet + 12 + slot * 8
            model = get(0x36C94, (descriptor,))
            if model:
                assert BASE <= model < BASE + len(raw) - 0x8C
                name = bytes(u.mem_read(model + 8, 24)).split(b'\0')[0].decode('cp932')
                ships.append({'slot': slot, 'descriptor': descriptor, 'model': model, 'name': name,
                              'Hull': get(0x183A0, (model,)), 'Crew': get(0x181BC, (model,))})
        rows.append({'frame': frame, 'RAM_sha256': source['sha256'],
                     'active_fleet_index': index, 'ships': ships})
    assert len(rows[0]['ships']) == 1 and rows[0]['ships'][0]['name'] == 'Vestaros'
    for row in rows[1:]:
        assert len(row['ships']) == 5, (row['frame'], row['ships'])
        assert [s['name'] for s in row['ships']] == ['Vestaros', 'Latina', 'Latina', 'Latina', 'Latina']
        assert [(s['Hull'], s['Crew']) for s in row['ships']] == [(48, 19), (25, 0), (25, 0), (25, 0), (25, 0)]
    pxl = PxlImage.from_bytes(rom.read_file('/_pxl/__frame.pxl'))
    batch = read('translations/frame_action_buttons_graphics_v7.json')
    templates = {r['text']: template(pxl, r['box']) for r in batch['records'][15:] if r['text'] not in ('M', 'D')}
    colors = set()
    for bank in range((pxl.pixels_offset - 20) // 32):
        w = struct.unpack_from('<H', pxl.source, 20 + bank * 32 + 18)[0]
        colors.add((w & 31, w >> 5 & 31, w >> 10 & 31))
    scans = []
    for shot in report['frames_captured']:
        path = Path(shot['path'])
        assert sha(path.read_bytes()) == shot['PNG_sha256']
        assert Image.open(path).size == (256, 384)
        scans.append({'frame': shot['frame'], 'path': str(path), 'PNG_sha256': shot['PNG_sha256'],
                      'matches': scan_image(path, templates, colors)})
    assert not any(s['matches'] for s in scans)
    entries = common_message_entries(rom.read_file('/COMMON/MESFILE.DK4'), arm, clean=False)
    source_entries = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), original)
    defects = [{'message_id': n, 'source_Japanese': source_entries[n].text.decode('cp932'),
                'current_English': entries[n].text.decode('ascii'), 'frame': f,
                'actual_word_split': split, 'repair_complete': False}
               for n, f, split in ((269, 32600, 'wa / nt'), (272, 35800, 'th / e'))]
    font = GameAsciiFont.from_arm9(arm)
    for row in defects:
        im = Image.open(RUN / f"frame_{row['frame']:06d}_navigation.png").convert('RGB')
        text = row['current_English']
        row['complete_actual_split_line_masks'] = [
            full_cells(im, font, text[:36], 16, 296, (0, 8, 0)),
            full_cells(im, font, text[36:], 16, 312, (0, 8, 0))]
    saved = Path(report['battery_save_preloaded']['destination'])
    assert saved.read_bytes().endswith(b'|-DESMUME SAVE-|')
    assert sha(saved.read_bytes()) != pre['donor_sha256']
    save(ROOT / 'full_inputs.json', report['scripted_input_schedule'])
    proof = {'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
             'report': str(report_path), 'report_sha256': sha(report_path.read_bytes()),
             'terminal_frame': 56600, 'ordinary_input_events': len(report['scripted_input_schedule']),
             'no_savestate_or_gameplay_fixture_applied': True, 'native_original_fleet_models': rows,
             'original_five_descriptor_loop_stride8_and_model_getters_exact_clean_code': True,
             'ordinary_four_Latina_purchases_five_ship_fleet_verified': True,
             'dock_transfer_previews_not_claimed_persisted_model_changes': True,
             'five_miniature_complete_mask_scan': scans,
             'no_complete_miniature_match_only_in_this_sampled_input_path': True,
             'Confirm_parent_and_global_non_use_not_proven': True,
             'captain_modal_word_wrap_defects': defects,
             'five_ship_test_save': {'path': str(saved), 'sha256': sha(saved.read_bytes()),
                                    'ordinary_Save_overwrite_in_isolated_copy': True,
                                    'cold_reload_not_yet_verified': True,
                                    'zero_crew_support_ships_need_staffing_before_battle': True},
             'source_donor_unchanged': True, 'screenshots': len(scans),
             'ROM_patch_registry_release_pointers_unchanged': True,
             'all18_plaques_incomplete_22_historical_scopes_preserved': True,
             'full_goal_complete': False,
             'scripts': {p: sha(Path(p).read_bytes()) for p in
                         ('scripts/run_fleet_capacity_v650.py', 'scripts/research_fleet_capacity_v650.py')}}
    save(ROOT / 'fleet_capacity_proof.json', proof)
    print('V650: terminal ordinary run;five native ships;all sampled miniature masks searched;two modal wrap defects open.')


if __name__ == '__main__':
    main()
