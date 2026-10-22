"""Controlled native sepia atlas loading/painting, not an identified gameplay parent."""

import struct
from pathlib import Path

from ndspy.code import loadOverlayTable
from PIL import Image
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
)

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, call, machine
from scripts.research_online_loader_v190 import resource_call
from scripts.verify_movie_transition_bitmaps_v648 import rgb
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/sepia_consumers_v662')
VIEW, DEST, POINT, SIZE, POSITION = 0x02470020, 0x022E1794, 0x024A0000, 0x024A0010, 0x024A0020
PATH = '/_pxl/seamap.pxl'


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    rom = NdsImage.open(pre['candidate'])
    clean = NdsImage.open('work/clean.nds')
    arm = rom.read_file('/__arm9__.bin')
    blob = rom.read_file(PATH)
    assert blob == clean.read_file(PATH)
    asset = PxlImage.from_bytes(blob)
    assert (asset.width, asset.height, asset.bits_per_pixel) == (244, 1280, 4)
    u, original = machine(arm), machine(clean.read_file('/__arm9__.bin'))
    for image, cpu in ((rom, u), (clean, original)):
        overlay = loadOverlayTable(image.rom.arm9OverlayTable, lambda i, f, image=image: image.files[f])[0]
        cpu.mem_write(overlay.ramAddress, bytes(overlay.data))
    executed = set()
    h = u.hook_add(UC_HOOK_CODE, lambda cpu, a, size, data: executed.add(a))
    resource_call(u, 0x10E190, ())
    manager = struct.unpack_from('<I', arm, 0x5D24)[0]
    resource_call(u, 0xD6C0C, (manager,))
    owner = struct.unpack_from('<I', arm, 0x10F328)[0]
    assert owner == 0x02313B8C
    handles, events = {}, []

    def bridge(cpu, address, size, data):
        if address == 0x020E5650:
            raise AssertionError('Original fatal assertion')
        if address not in (0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08):
            return
        obj = cpu.reg_read(UC_ARM_REG_R0)
        if address == 0x020DED50:
            p = cpu.reg_read(UC_ARM_REG_R1)
            name = bytes(cpu.mem_read(p, 96)).split(b'\0')[0].decode('ascii')
            assert '/' + name == PATH and obj not in handles
            handles[obj] = 0
            cpu.mem_write(obj + 0x20, struct.pack('<2I', 0, len(blob)))
            events.append({'open': PATH, 'source_sha256': sha(blob)})
            result = 1
        elif address == 0x020DEB70:
            offset = cpu.reg_read(UC_ARM_REG_R1)
            assert cpu.reg_read(UC_ARM_REG_R2) == 0 and 0 <= offset <= len(blob)
            handles[obj] = offset
            events.append({'seek': offset})
            result = 1
        elif address == 0x020DEBDC:
            target, count = cpu.reg_read(UC_ARM_REG_R1), cpu.reg_read(UC_ARM_REG_R2)
            start = handles[obj]
            assert start + count <= len(blob)
            cpu.mem_write(target, blob[start:start + count])
            handles[obj] += count
            events.append({'read': count, 'offset': start, 'destination': target})
            result = count
        else:
            del handles[obj]
            events.append({'close': True})
            result = 1
        cpu.reg_write(UC_ARM_REG_R0, result)
        cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))

    io_hook = u.hook_add(UC_HOOK_CODE, bridge)
    cases = []
    painting, written = False, set()

    def write(cpu, kind, address, size, value, data):
        if painting and DEST <= address < DEST + 98304:
            for p in range(address, address + size):
                y, x = divmod((p - DEST) // 2, 256)
                assert 6 <= x < 250 and 16 <= y < 176
                written.add(p)

    def memory_read(cpu, kind, address, size, value, data):
        if painting:
            assert not (DEST <= address < DEST + 98304), 'Painter reads completed output as input'

    write_hook = u.hook_add(UC_HOOK_MEM_WRITE, write)
    read_hook = u.hook_add(UC_HOOK_MEM_READ, memory_read)
    try:
        u.mem_write(POINT, struct.pack('<2I', 0, 0))
        u.mem_write(SIZE, struct.pack('<2I', 244, 160))
        u.mem_write(POSITION, struct.pack('<2I', 6, 16))
        for bank in range(8):
            palette = struct.unpack_from('<16H', blob, 20 + bank * 32)
            for page in range(8):
                u.mem_write(VIEW - 16, b'\xA5' * 80)
                u.mem_write(STACK, struct.pack('<4I', 244, 160, bank, 0))
                resource_call(u, 0xD3D30, (VIEW, owner, 0, page * 160))
                resource_call(u, 0xD4170, (VIEW,))
                header = u.reg_read(UC_ARM_REG_R0)
                fields = struct.unpack('<12I', u.mem_read(VIEW, 48))
                assert fields[3] == owner and fields[7:9] == (0, page * 160)
                assert fields[9] & 65535 == bank and fields[10:12] == (244, 160)
                assert bytes(u.mem_read(header, len(blob))) == blob and not handles
                assert bytes(u.mem_read(VIEW - 16, 16)) == bytes(u.mem_read(VIEW + 48, 16)) == b'\xA5' * 16
                u.mem_write(POINT, struct.pack('<2I', 0, page * 160))
                # 1FF92D8 accepts a screen selector, not a destination header.
                # Its original literal selects 022E1794 + screen*98304.
                u.mem_write(DEST - 16, b'\xA5' * (98304 + 32))
                background = 0x4210
                u.mem_write(DEST, struct.pack('<H', background) * 49152)
                u.mem_write(STACK, struct.pack('<2I', SIZE, POSITION))
                painting, written = True, set()
                call(u, 0x01FF92D8 - BASE, (0, header, bank, POINT), instruction_limit=3000000)
                painting = False
                actual = bytes(u.mem_read(DEST, 98304))
                expected = [background] * 49152
                opaque, opaque_zero = 0, 0
                for y in range(160):
                    for x in range(244):
                        index = asset.indices[(page * 160 + y) * 244 + x]
                        # Source flag4 selects the original palette-bit15 alpha
                        # branch at 1FF948C/1FF9498, including palette entry0.
                        if palette[index] & 32768:
                            expected[(y + 16) * 256 + x + 6] = palette[index]
                            opaque += 1
                            opaque_zero += index == 0
                target = struct.pack('<49152H', *expected)
                if actual != target:
                    diffs = [(i, hex(a), hex(b)) for i, (a, b) in enumerate(zip(struct.unpack('<49152H', actual), expected, strict=True)) if a != b]
                    save(ROOT / 'first_paint_difference.json', {'page': page, 'bank': bank,
                        'palette': list(palette), 'differences': diffs[:30], 'count': len(diffs)})
                    raise AssertionError(f'Full native words differ: {page=} {bank=} {diffs[:3]}')
                assert bytes(u.mem_read(DEST - 16, 16)) == bytes(u.mem_read(DEST + 98304, 16)) == b'\xA5' * 16
                assert len(written) == opaque * 2
                assert palette[0] != background
                # A common but invalid index-zero transparency model loses these
                # exact source pixels on pages that actually contain index0.
                cases.append({'page': page, 'bank': bank, 'whole49152_words_sha256': sha(actual),
                              'source_opaque_pixels': opaque, 'opaque_index0_pixels': opaque_zero,
                              'wrong_index0_transparency_model_rejected': opaque_zero > 0,
                              'all_source_opaque_bytes_written_no_output_reads_or_outside_crop_writes': True})
                if bank == 0:
                    image = Image.new('RGB', (256, 192))
                    image.putdata(rgb(expected))
                    image.save(ROOT / f'controlled_native_sepia_page_{page}.png')
            print('Complete native sepia bank', bank, flush=True)
        # One isolated alpha control changes only bit15 of copied palette0,
        # then restores the entire loaded file exactly. This is not shipped art.
        control_page = next(r['page'] for r in cases if r['bank'] == 0 and r['opaque_index0_pixels'])
        palette = list(struct.unpack_from('<16H', blob, 20))
        u.mem_write(header + 20, struct.pack('<H', palette[0] & 32767))
        u.mem_write(POINT, struct.pack('<2I', 0, control_page * 160))
        u.mem_write(DEST, struct.pack('<H', background) * 49152)
        u.mem_write(STACK, struct.pack('<2I', SIZE, POSITION))
        painting, written = True, set()
        call(u, 0x01FF92D8 - BASE, (0, header, 0, POINT), instruction_limit=3000000)
        painting = False
        expected = [background] * 49152
        transparent_count = 0
        for y in range(160):
            for x in range(244):
                index = asset.indices[(control_page * 160 + y) * 244 + x]
                if index:
                    expected[(y + 16) * 256 + x + 6] = palette[index]
                else:
                    transparent_count += 1
        assert bytes(u.mem_read(DEST, 98304)) == struct.pack('<49152H', *expected)
        assert len(written) == (39040 - transparent_count) * 2
        u.mem_write(header + 20, blob[20:22])
        assert bytes(u.mem_read(header, len(blob))) == blob
        alpha_control = {'page': control_page, 'bank': 0, 'temporary_one_palette_bit_cleared': 15,
                         'transparent_source_cells_retained_background': transparent_count,
                         'all49152_expected_words_and_write_coverage_exact': True,
                         'complete_loaded_source_restored_exact': True}
    finally:
        u.hook_del(io_hook)
        u.hook_del(h)
        u.hook_del(write_hook)
        u.hook_del(read_hook)
        save(ROOT / 'paint_research.json', {'completed_cases': cases, 'SDK_file_bridge_events': events,
            'executed_instruction_addresses': sorted(executed), 'no_actual_gameplay_parent_claim': True})
    for address in executed:
        assert bytes(u.mem_read(address, 4)) == bytes(original.mem_read(address, 4)), hex(address)
    assert sum(r['opaque_index0_pixels'] for r in cases) == 30200
    save(ROOT / 'native_paint_proof.json', {'candidate_sha256': pre['candidate_sha256'],
        'source_path': PATH, 'source_sha256': sha(blob), 'native_owner': owner,
        'source_palette_banks8_pages8': True, 'cases': cases,
        'unique_complete_paintings': len({r['whole49152_words_sha256'] for r in cases}),
        'isolated_native_palette_alpha_control': alpha_control,
        'all3145728_destination_words_exact_including_borders_and_transparent_cells': True,
        'all_executed_code_exact_clean': True, 'SDK_file_bridge_events': events,
        'original_loader_cache_view_and_blitter_ABI_guards_pass': True,
        'source_getter_and_painter_not_substituted': True,
        'no_actual_gameplay_parent_GPU_hardware_or_legacy_CMMN_display_claim': True,
        'no_ROM_or_registered_release_change': True, 'full_goal_complete': False,
        'script_sha256': sha(Path(__file__).read_bytes())})
    print('V662: all64 controlled native page/bank paints pass; gameplay/legacy consumer still open.')


if __name__ == '__main__':
    main()
