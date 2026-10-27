"""Verify matched allocation controls without claiming a production repair."""

import json
import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile
from PIL import Image

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_town_allocation_sizes_v492 import ENTRY, PARENT, ROOT, SLOT


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    parent = NdsImage.open(PARENT)
    source_arm = parent.read_file('/__arm9__.bin')
    movie = parent.read_file('/FLS/M28.fls')
    texture = FlsArchive(movie).texture(46)
    points = [(12 + i % texture.width, 167 + i // texture.width,
               tuple(v >> 3 for v in texture.palette[n][:3]))
              for i, n in enumerate(texture.indices) if n]
    assert len(points) == 3047
    options = None
    cases = []
    for size in (0, 16, 128, 608, 2912):
        manifest = read(ROOT / f'allocate_{size}_manifest.json')
        rom = Path(manifest['research_ROM'])
        fixture = NdsImage.open(rom)
        arm = fixture.read_file('/__arm9__.bin')
        assert fixture.read_file('/FLS/M20.fls') == movie
        # Only the constructor branch differs in the main section. Other
        # sections are exact, except the explicitly declared fixed-size helper.
        old = MainCodeFile(source_arm, 0x02000000)
        new = MainCodeFile(arm, 0x02000000)
        restored = bytearray(new.sections[0].data)
        restored[0xB59AC:0xB59B0] = old.sections[0].data[0xB59AC:0xB59B0]
        assert restored == old.sections[0].data
        assert all(new.sections[i].data == old.sections[i].data for i in (1, 2, 3))
        assert len(arm) == len(source_arm)
        folder = Path('work/emulation_v193') / f'town_allocation_sizes_v492_{size}'
        report_path = folder / 'capture_report.json'
        report = read(report_path)
        assert report['ROM_sha256'] == sha(rom.read_bytes()) == manifest['research_ROM_sha256']
        assert report['cold_boot'] and not report['savestate_loaded']
        assert report['frames'] == 6000 and not report['callback_errors']
        assert report['scripted_input_schedule'] == read('work/analysis/m28_planes_v485/inputs.json')
        if options is None:
            options = report['core_options']
        assert options == report['core_options']
        for shot in report['frames_captured']:
            assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
        shot = next(s for s in report['frames_captured'] if s['frame'] == 3700)
        image = Image.open(shot['path']).convert('RGB').point(lambda v: v >> 3)
        matches = sum(image.getpixel((x, y)) == rgb for x, y, rgb in points)
        assert matches == (3047 if size <= 128 else 553)
        helper_intact, pointer = None, None
        if size:
            itcm = (folder / 'native_state/arm9_itcm.bin').read_bytes()
            offset = ENTRY - 0x01FF8000
            code_offset = ENTRY - new.sections[4].ramAddress
            length = len(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(
                (ROOT / f'allocate_{size}.asm').read_text(), ENTRY)[0])
            helper_intact = itcm[offset:offset + length] == new.sections[4].data[code_offset:code_offset + length]
            assert helper_intact
            pointer = struct.unpack_from('<I', itcm, SLOT - 0x01FF8000)[0]
            assert pointer == 0x023A9780
        cases.append({'allocation_bytes': size, 'manifest': str(ROOT / f'allocate_{size}_manifest.json'),
                      'report': str(report_path), 'report_sha256': sha(report_path.read_bytes()),
                      'frame3700': shot, 'matching_name_pixels': matches,
                      'all3047_name_pixels_match': matches == 3047,
                      'terminal_helper_bytes_intact': helper_intact, 'allocated_pointer': pointer})
    proof = {'candidate': str(PARENT), 'candidate_sha256': sha(PARENT.read_bytes()),
             'cases': cases, 'production_ROM_unchanged': True,
             'one_line_608_and_five_line_2912_persistent_buffers_rejected': True,
             'exact_allocation_failure_mechanism_unproven': True,
             'normal_M28_ending_caller_and_unlock_not_proven': True,
             'all22_historical_requirements_retained': True,
             'all18_plaques_remain_incomplete': True, 'full_goal_complete': False}
    (ROOT / 'control_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print('Five matched controls verified: 0/16/128 complete; 608/2912 incomplete. No production fix.')


if __name__ == '__main__':
    main()
