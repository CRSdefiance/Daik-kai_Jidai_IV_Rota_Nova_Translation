"""Exercise original header owners with a one-word, research-only selection cheat."""
import argparse
import json
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import rom_files
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_source_plaque_grain_v542 import capture_report

ROOT = Path('work/analysis/header_consumers_v567')
CAPTURE = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROM = Path('out/all_routes_combined_v566_candidate.nds')
PARENT = Path('out/all_routes_combined_v564_candidate.nds')
CHOICE = 0x0208529C
CASES = (('haifuhin', 2, 0x023139E8), ('senrihin', 3, 0x02313A4C))


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def prepare():
    ROOT.mkdir(parents=True, exist_ok=True)
    cases = []
    for stem, mode, owner in CASES:
        for kind, parent in (('control', PARENT), ('actual', ROM)):
            image = NdsImage.open(parent)
            before = rom_files(image)
            arm = image.read_file('/__arm9__.bin')
            u = machine(arm)
            pattern = bytes(u.mem_read(CHOICE-4, 16))
            assert pattern[4:8] == bytes.fromhex('100099e5')  # LDR r0,[sb,#0x10].
            offset = arm.find(pattern)
            assert offset >= 0 and arm.count(pattern) == 1
            offset += 4
            modified = arm[:offset] + struct.pack('<I', 0xE3A00000 | mode) + arm[offset+4:]
            image.replace_file('/__arm9__.bin', modified)
            target = ROOT/f'{stem}_{kind}_NATIVE_MODE_FIXTURE.nds'
            image.save(target)
            after = rom_files(NdsImage.open(target))
            assert [p for p in before if before[p] != after[p]] == ['/__arm9__.bin']
            assert all(a == b for n, (a, b) in enumerate(zip(arm, modified, strict=True))
                       if not offset <= n < offset+4)
            cases.append({'stem': stem, 'mode': mode, 'owner': owner, 'kind': kind,
                          'parent': str(parent), 'parent_sha256': sha(parent.read_bytes()),
                          'ROM': str(target), 'ROM_sha256': sha(target.read_bytes()),
                          'mapped_instruction': CHOICE, 'ARM9_file_offset': offset,
                          'original_word': arm[offset:offset+4].hex(),
                          'fixture_word': modified[offset:offset+4].hex(),
                          'source_file_substituted': False, 'original_event_earned': False})
    (ROOT/'fixtures.json').write_text(json.dumps(cases, indent=2)+'\n', encoding='utf-8')
    print('Four research-only original-owner mode fixtures; only one ARM instruction changes, no artwork/file substitution.')


def main():
    fixtures = read(ROOT/'fixtures.json')
    cases = []
    for fixture in fixtures:
        stem, kind, owner = fixture['stem'], fixture['kind'], fixture['owner']
        image = NdsImage.open(fixture['ROM'])
        parent = NdsImage.open(fixture['parent'])
        original_files, files = rom_files(parent), rom_files(image)
        assert [p for p in original_files if original_files[p] != files[p]] == ['/__arm9__.bin']
        a, b = original_files['/__arm9__.bin'], files['/__arm9__.bin']
        offset = fixture['ARM9_file_offset']
        assert a[:offset] == b[:offset] and a[offset+4:] == b[offset+4:]
        assert b[offset:offset+4].hex() == fixture['fixture_word']
        assert sha(Path(fixture['ROM']).read_bytes()) == fixture['ROM_sha256']
        report = capture_report(CAPTURE/f'header_consumers_v567_{stem}_{kind}', fixture['ROM_sha256'])
        alias_report = capture_report(CAPTURE/f'header_wood_v566_{stem}_{kind}',
                                      next(f for f in read('work/analysis/header_materials_v565/render_fixtures.json')
                                           if f['stem'] == stem and f['kind'] == kind)['sha256'])
        assert report['frames'] == 4600 and not report['savestate_loaded']
        assert report['scripted_input_schedule'] == alias_report['scripted_input_schedule']
        assert report['core_options'] == alias_report['core_options']
        source_save = Path(report['battery_save_preloaded']['source'])
        assert sha(source_save.read_bytes()) == report['battery_save_preloaded']['source_sha256']
        frames = {s['frame']: s for s in report['frames_captured']}
        aliases = {s['frame']: s for s in alias_report['frames_captured']}
        data = image.read_file(f'/_pxl/{stem}.pxl')
        atlas = PxlImage.from_bytes(data)
        for frame in (4300, 4600):
            raw_path = CAPTURE/f'header_consumers_v567_{stem}_{kind}'/f'frame_{frame:06d}_arm9_ram.bin'
            raw = raw_path.read_bytes()
            matches = []
            for pos in range(0, len(raw)-48, 4):
                words = struct.unpack_from('<12I', raw, pos)
                if words[3] == owner and words[7:9] == (0, 0) and words[10:12] == (256, 16):
                    matches.append((pos+0x02000000, words))
            assert len(matches) == 1, (stem, kind, frame, matches)
            view, words = matches[0]
            u = machine(image.read_file('/__arm9__.bin'))
            u.mem_write(0x02000000, raw)
            executed = call(u, 0xD4170, (view,))
            pointer = u.reg_read(UC_ARM_REG_R0)
            assert bytes(u.mem_read(pointer, len(data))) == data
            assert 0x020DED50 not in executed and 0x020DEBDC not in executed
            shot = Image.open(frames[frame]['path']).convert('RGB')
            expected = Image.open(aliases[frame]['path']).convert('RGB')
            assert shot.tobytes() == expected.tobytes()
            assert all(native5(shot.getpixel((x, y+261))) == native5(atlas.palette[atlas.indices[y*256+x]])
                       for y in range(16) for x in range(256))
            cases.append({'stem': stem, 'kind': kind, 'frame': frame, 'fixture_mode': fixture['mode'],
                          'actual_original_owner': owner, 'actual_original_view': view,
                          'actual_resident_PXL_pointer': pointer, 'resident_file_byte_exact': True,
                          'complete_source_crop': [0, 0, 256, 16], 'palette_parameter_low_byte': words[9] & 255,
                          'complete_98304_pixel_screen_exact_to_independent_alias_control': True,
                          'all4096_banner_pixels_exact': True, 'original_event_earned': False,
                          'RAM_sha256': sha(raw), 'PNG_sha256': frames[frame]['PNG_sha256']})
    proof = {'candidate_unchanged': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'cases': cases, 'actual_original_owner_loading_and_full_crop_cases': len(cases),
             'total_banner_pixels_exact': len(cases)*4096, 'total_complete_screen_pixels_exact': len(cases)*98304,
             'one_word_header_choice_cheat_in_research_ROMs_only': True,
             'no_artwork_or_resource_file_substitution': True,
             'original_resource_and_PXL_getter_binding_verified_from_actual_core_state': True,
             'original_reward_battle_event_reachability_or_earned_items_verified': False,
             'production_ROM_changed': False, 'hardware_or_full_route_verified': False,
             'all18_plaques_remain_incomplete': True, 'full_goal_complete': False}
    (ROOT/'native_consumer_proof.json').write_text(json.dumps(proof, indent=2)+'\n', encoding='utf-8')
    print('8 actual original-owner bindings/full crops,32768 banner pixels and786432 whole-screen pixels pass. One-word test selection cheats; no production changes or earned-event claims.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare-fixtures', action='store_true')
    if parser.parse_args().prepare_fixtures:
        prepare()
    else:
        main()
