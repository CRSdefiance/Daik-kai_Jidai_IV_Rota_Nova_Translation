"""Locate the actual Route Map fleet-background parent; regional gate stays open."""

import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_save_load_plaques_v612 import snapshot
from scripts.verify_village_wrap_v608 import report, save

ROOT = Path('work/analysis/regional_context_v614')
ROM = Path('out/all_routes_combined_v613_candidate.nds')


def main():
    rom = NdsImage.open(ROM)
    arm, source = rom.read_file('/__arm9__.bin'), NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    u, original = machine(arm), machine(source)
    for address, size in ((0x0210E710, 36), (0x0208E12C, 344), (0x02036914, 104), (0x0208C934, 16)):
        assert bytes(u.mem_read(address, size)) == bytes(original.mem_read(address, size))
    u.emu_start(0x0210E710, 0x0210E734, count=150)
    assert u.reg_read(UC_ARM_REG_PC) == 0x0210E734 and u.reg_read(UC_ARM_REG_R0) == 0x02313C68
    pointer = struct.unpack('<I', u.mem_read(0x02313C68 + 12, 4))[0]
    assert bytes(u.mem_read(pointer, 64)).split(b'\0')[0] == b'_pxl/fleetinfo.pxl'
    run, shots, receipt = report('regional_context_v614_natural', 20400, sha(ROM.read_bytes()))
    donor = run['battery_save_preloaded']
    assert donor['source_sha256'] == sha(Path(donor['source']).read_bytes()) == 'f22ff2cd301c306813e9a1f5c0633d78c75d1d5a9acdf668bcd89a117d1ad087'
    assert not any(v for k, v in run.items() if k.startswith('synthetic_'))
    save(ROOT / 'complete_inputs.json', run['scripted_input_schedule'])
    raw = snapshot(run, 20400)
    actual = machine(arm)
    actual.mem_write(BASE, raw)
    roots = []
    for off in range(0x170000, len(raw) - 0x6C90, 4):
        if struct.unpack_from('<I', raw, off)[0] != 0x0214BECC:
            continue
        fleet = struct.unpack_from('<I', raw, off + 0x6C58)[0]
        words = struct.unpack_from('<12I', raw, off + 0x6BC0)
        if fleet < 64 and words[3] == 0x02313C68 and words[9] & 0xFFFF == 0 and words[10:12] == (256, 192):
            roots.append((BASE + off, fleet, words))
    assert len(roots) == 1
    root, selected, words = roots[0]
    ti = struct.unpack('<I', actual.mem_read(0x0214BECC - 4, 4))[0]
    name = struct.unpack('<I', actual.mem_read(ti + 4, 4))[0]
    assert bytes(actual.mem_read(name, 48)).split(b'\0')[0] == b'9CRouteMap'
    call(actual, 0xD4170, (root + 0x6BC0,))
    header = actual.reg_read(UC_ARM_REG_R0)
    resource = rom.read_file('/_pxl/fleetinfo.pxl')
    assert bytes(actual.mem_read(header, len(resource))) == resource
    image, atlas = Image.open(shots[20400]['path']).convert('RGB'), PxlImage.from_bytes(resource).render().convert('RGB')
    box = (83, 75, 125, 93)
    assert all(native5(image.getpixel((x, y))) == native5(atlas.getpixel((x, y)))
               for y in range(box[1], box[3]) for x in range(box[0], box[2]))
    call(actual, 0xCB1A8, ())
    table = actual.reg_read(UC_ARM_REG_R0)
    fleet_rows = []
    for index in range(64):
        address = table + 4 + index * 0x84
        results = []
        for offset in (0x36914, 0x36948, 0x367FC):
            call(actual, offset, (address,))
            results.append(actual.reg_read(UC_ARM_REG_R0))
        fleet_rows.append({'index': index, 'actual_record': address, 'original_36914_result': results[0],
                           'original_36948_result': results[1], 'original_finance_pointer': results[2]})
    ours = [r for r in fleet_rows if r['original_36914_result']]
    assert len(ours) == 1 and ours[0]['index'] == selected == 1
    assert ours[0]['original_36948_result'] == 1 and ours[0]['original_finance_pointer'] == 0
    # Source gives the main fleet precedence over own-company regional handling.
    # Therefore this donor cannot supply an existing own regional fleet context.
    regional = rom.read_file('/_pxl/chihofleetinfo.pxl')
    assert raw.find(regional) < 0
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()), 'new_ROM_created': False,
             'report': receipt, 'source_save_byte_exact_no_live_fixtures': True,
             'original_map_full_background_helper': 0x0208C968, 'original_draw_call': 0x0208C93C,
             'actual_parent_class': '9CRouteMap', 'actual_parent': root, 'actual_parent_vtable': 0x0214BECC,
             'selected_fleet_index': selected, 'actual_view': root + 0x6BC0, 'actual_view_words': list(words),
             'original_executed_resource_initializer': [0x0210E710, 0x0210E734], 'original_resource_owner': 0x02313C68,
             'actual_resource': '/_pxl/fleetinfo.pxl', 'actual_resident_header': header, 'whole_resource_sha256': sha(resource),
             'complete_actual_Level_region': list(box), 'complete_Level_region_native5_pixels': 756,
             'original64_fleet_getter_results': fleet_rows, 'only_existing_own_fleet_is_main': True,
             'wrong_Fleet_Info_overview_path_is_COtherFleetView': True,
             'next_action': 'Create a regional fleet through original Shipyard/Dock on an isolated developed-port save; then select that actual fleet in Route Map.',
             'regional_art_still_not_resident_and_no_regional_native_display_credit': True,
             'full_goal_complete': False, 'all18_original_plaques_incomplete_all22_historical_scopes_retained': True,
             'script_sha256': sha(Path(__file__).read_bytes())}
    save(ROOT / 'parent_proof.json', proof)
    print('Actual original Route Map parent/resource/Level crop verified; donor has only its main fleet. Regional display remains open; use original Shipyard/Dock creation next.')


if __name__ == '__main__':
    main()
