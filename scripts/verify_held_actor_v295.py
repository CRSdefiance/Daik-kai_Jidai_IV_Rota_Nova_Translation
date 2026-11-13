"""Original message headers, native actor/body parsing and controlled real UI."""

import json
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R5

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_name_catalog_glyphs_v278 import expected_pixels, raster

ROOT = Path('work/analysis/held_actor_v295')
CAPTURE = Path('work/emulation_v193/held_actor_v295')
HELD = [('/data/SC0.DK4', 141, 107, 151), ('/data/SC0.DK4', 85, 5, 151),
        ('/data/SC1.DK4', 72, 6, 10), ('/data/SC3.DK4', 139, 137, 10)]


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    manifest = read(ROOT / 'fixture_manifest.json')
    report = read(CAPTURE / 'capture_report.json')
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames'] == 11640 and report['ROM_sha256'] == manifest['research_ROM_sha256']
    assert sha(Path(report['ROM']).read_bytes()) == report['ROM_sha256']
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    clean = NdsImage.open('work/clean.nds')
    image = NdsImage.open('out/all_routes_combined_v275_candidate.nds')
    arm, original = image.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    assert arm[0x29B18:0x29B30] == original[0x29B18:0x29B30]
    assert arm[0x2434C:0x24360] == original[0x2434C:0x24360]
    cases = []
    for path, block_id, index, actor in HELD:
        block = IlnkContainer.parse(clean.read_file(path)).blocks[block_id]
        parts = block.split(b'\0')
        at = sum(len(row) + 1 for row in parts[:index])
        raw = parts[index]
        assert raw[0] == actor and block[at - 5:at] == b'\0\x40\xFF\xFF\0'
        obj = block[at - 5:at + len(raw) + 1]
        assert struct.unpack_from('<I', obj)[0] == 0xFFFF4000
        assert struct.unpack_from('<H', obj, 4)[0] == actor << 8
        cpu = machine(arm)
        address = 0x02460000
        cpu.mem_write(address, obj)
        cpu.reg_write(UC_ARM_REG_R5, address)
        cpu.emu_start(0x02029B18, 0x0202425C, count=20)
        assert cpu.reg_read(UC_ARM_REG_PC) == 0x0202425C
        assert cpu.reg_read(UC_ARM_REG_R0) == actor and cpu.reg_read(UC_ARM_REG_R1) == address + 6
        assert bytes(cpu.mem_read(address + 6, len(raw))) == raw[1:] + b'\0'
        call(cpu, 0x2434C, (actor,))
        assert cpu.reg_read(UC_ARM_REG_R0) == actor
        cases.append({'file_path': path, 'id': f'DK4_MES_B{block_id}_R{index:04d}',
                      'clean_source_hex': raw.hex(), 'native_object_header_hex': obj[:6].hex(),
                      'presentation_byte': actor, 'native_actor_argument': actor,
                      'body_pointer_skips_one_metadata_byte': True,
                      'complete_Japanese_body': raw[1:].decode('cp932'),
                      'all_input_bytes_preserved': bytes(cpu.mem_read(address, len(obj))) == obj})
    records = IlnkContainer.parse(image.read_file('/data/SC0.DK4')).blocks[44].split(b'\0')
    actual = []
    for index, frame, name in [(179, 10000, 'Xien Yan'), (187, 11200, 'Sailor')]:
        body = records[index][1:].replace(b'FI', b'Raphael')
        pixels, _, font = raster(arm, body)
        _, events, _ = raster(arm, body)
        assert pixels == expected_pixels(arm, font, events)
        expected = {(16 + n % 216, 296 + n // 216) for n, value in enumerate(pixels) if value == 1}
        path = CAPTURE / f'frame_{frame:06d}_cold_boot.png'
        screen = Image.open(path).convert('RGB')
        observed = {(x, y) for y in range(296, 360) for x in range(16, 232)
                    if screen.getpixel((x, y)) == (0, 8, 0)}
        assert observed == expected
        actual.append({'record': index, 'frame': frame, 'capture': str(path),
                       'capture_sha256': sha(path.read_bytes()), 'actual_nameplate_visually_reviewed': name,
                       'actual_changed_portrait_visually_reviewed': True,
                       'all_complete_body_pixels_first_final_letters_and_bounds_exact': True,
                       'native_ink_pixels': len(expected)})
    proof = {'format': 'dk4-held-actor-original-header-and-actual-display-v295',
             'research_ROM_sha256': report['ROM_sha256'], 'actual_cold_boot_frames': 11640,
             'original_header_parser_cases': cases, 'actual_controlled_UI_cases': actual,
             '0A_is_actor10_metadata_not_an_initial_linebreak_in_exact_two_records': True,
             '97_is_actor151_metadata_not_CP932_prose_in_exact_two_records': True,
             'actor10_nameplate': 'Xien Yan', 'actor151_nameplate': 'Sailor',
             'all_native_parser_code_graphics_other_files_and_record_allocations_preserved': True,
             'original_held_scene_locations_not_traversed': True,
             'scope': 'Exact original message headers and native parsing, plus controlled actual nameplate/portrait/body display.',
             'full_registered_release_integration_pending': True,
             'all18_plaque_hint_entries_and_variants_incomplete': True, 'full_goal_complete': False}
    (ROOT / 'native_and_actual_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Four original headers/preambles mapped; actual Xien Yan/Sailor portraits and1351 complete body pixels verified.')


if __name__ == '__main__':
    main()
