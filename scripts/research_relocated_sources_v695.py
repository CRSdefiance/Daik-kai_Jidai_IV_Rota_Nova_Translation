"""Inspect complete relocated source planes during an original captured UI paint.

These are isolated native replays of retained V653 captures, not new current-ROM
gameplay captures. No resource is identified from its header alone.
"""

import argparse
import struct
from collections import Counter, defaultdict
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable
from unicorn import UC_HOOK_CODE, UcError, arm_const

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.rom.nds import NdsImage
from scripts import research_equipment_cursor_v663 as painter
from scripts.probe_button_prompt_native import machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/relocated_sources_v695')
CURRENT = Path('out/all_routes_combined_v692_candidate.nds')
TARGETS = (0x01FF8E4C, 0x01FF92D8, 0x01FFAE70)


def main(frame):
    ROOT.mkdir(exist_ok=True)
    folder = ROOT / (str(frame) + '_complete_planes')
    assert not folder.exists() or not any(folder.iterdir())
    folder.mkdir(exist_ok=True)
    old_root, original_setup = painter.ROOT, painter.setup
    old_rom = NdsImage.open(read(old_root / 'preflight.json')['candidate'])
    (folder / 'preflight.json').write_bytes((old_root / 'preflight.json').read_bytes())
    current = NdsImage.open(CURRENT)
    table = defaultdict(list)
    source_bytes = {}
    for _, path, data in current.iter_files():
        if not path.lower().endswith('.pxl'):
            continue
        assert data == old_rom.read_file(path), path
        flags, width_words, height, _, pixels = struct.unpack('<5I', data[:20])
        depth = flags & 255
        assert depth in (4, 8, 16)
        width = width_words * (16 // depth)
        assert len(data) - pixels == width * height * depth // 8
        key = (depth, width, height, sha(data[pixels:]))
        table[key].append(path)
        source_bytes[path] = data
    arm = current.read_file('/__arm9__.bin')
    expected = machine(arm)
    expected.mem_write(POOL, bytes(MainCodeFile(arm, 0x02000000).sections[3].data[:-48]))
    overlay = loadOverlayTable(current.rom.arm9OverlayTable, lambda _, f: current.rom.files[f])[0]
    expected.mem_write(overlay.ramAddress, bytes(overlay.data))
    calls, headers, seen_code, divergent_code = [], {}, {}, {}
    hook_handles, models = [], []

    def setup(*args, **kwargs):
        u, mapping = original_setup(*args, **kwargs)
        models.append(mapping)

        def code(cpu, pc, size, unused):
            if pc not in seen_code:
                actual = bytes(cpu.mem_read(pc, size))
                registered = bytes(expected.mem_read(pc, size))
                seen_code[pc] = actual.hex()
                if actual != registered:
                    divergent_code[pc] = {'captured': actual.hex(), 'current': registered.hex()}
            if pc not in TARGETS:
                return
            values = [cpu.reg_read(getattr(arm_const, 'UC_ARM_REG_R' + str(i))) for i in range(4)]
            sp = cpu.reg_read(arm_const.UC_ARM_REG_SP)
            screen, pointer, bank, source = values
            h = struct.unpack('<5I', cpu.mem_read(pointer, 20))
            key = (pointer, bank, h)
            if key not in headers:
                record = {'header': pointer, 'bank': bank, 'words': list(h)}
                depth = h[0] & 255
                width = h[1] * (16 // depth) if depth in (4, 8, 16) else 0
                pixel_pointer, palette_pointer = [(pointer + h[n]) & 0xFFFFFFFF for n in (4, 3)]
                length = width * h[2] * depth // 8
                record.update({'depth': depth, 'width': width, 'height': h[2],
                    'pixels_pointer': pixel_pointer, 'palette_pointer': palette_pointer, 'packed_bytes': length})
                if not (width and 0 < h[2] <= 4096 and 0 < length <= 262144):
                    record['unsupported_extent'] = True
                else:
                    try:
                        packed = bytes(cpu.mem_read(pixel_pointer, length))
                        indices = bytes(v for b in packed for v in (b & 15, b >> 4)) if depth == 4 else packed
                        pp = folder / f'source_{len(headers):02d}_pixels.bin'
                        pp.write_bytes(packed)
                        record.update({'packed_path': str(pp), 'packed_sha256': sha(packed),
                            'indices_sha256': sha(indices),
                            'whole_index_plane_matching_current_PXL_paths': table.get((depth, width, h[2], sha(packed)), [])})
                        if depth != 16:
                            palette = bytes(cpu.mem_read(palette_pointer + bank * (1 << depth) * 2, (1 << depth) * 2))
                            pal = folder / f'source_{len(headers):02d}_palette.bin'
                            pal.write_bytes(palette)
                            record.update({'selected_palette_path': str(pal), 'selected_palette_sha256': sha(palette)})
                    except UcError as exc:
                        record['whole_declared_plane_not_readable'] = repr(exc)
                headers[key] = record
            if pc == 0x01FFAE70:
                rect = struct.unpack('<4I', cpu.mem_read(source, 16))
                destination = struct.unpack('<4I', cpu.mem_read(struct.unpack('<I', cpu.mem_read(sp, 4))[0], 16))
            else:
                x, y = struct.unpack('<2I', cpu.mem_read(source, 8))
                size_pointer, dest_pointer = struct.unpack('<2I', cpu.mem_read(sp, 8))
                w, hgt = struct.unpack('<2I', cpu.mem_read(size_pointer, 8))
                rect = (x, y, w, hgt)
                destination = struct.unpack('<' + ('4I' if pc == 0x01FF8E4C else '2I'),
                    cpu.mem_read(dest_pointer, 16 if pc == 0x01FF8E4C else 8))
            calls.append({'primitive': pc, 'screen': screen, 'header_index': list(headers).index(key),
                'source_XYWH': list(rect), 'destination': list(destination),
                'original_return': cpu.reg_read(arm_const.UC_ARM_REG_LR)})
        hook_handles.append((u, u.hook_add(UC_HOOK_CODE, code)))
        return u, mapping

    painter.ROOT, painter.setup = folder, setup
    try:
        result = painter.paint(frame, False)
    finally:
        painter.ROOT, painter.setup = old_root, original_setup
        for u, handle in hook_handles:
            u.hook_del(handle)
    save(folder / 'research.json', {'captured_ROM': str(read(old_root / 'preflight.json')['candidate']),
        'current_ROM': str(CURRENT), 'all660_current_PXL_files_exact_captured_ROM': len(source_bytes) == 660,
        'calls': calls, 'headers': list(headers.values()), 'source_mapping': models,
        'current_registered_code_differences': divergent_code, 'native_paint_result': result,
        'source_calls_by_primitive': dict(Counter(r['primitive'] for r in calls)),
        'all_executed_current_code_matches': not divergent_code,
        'isolated_original_paint_with_explicit_SDK_blink_input_not_new_gameplay': True,
        'script_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V695 source planes', frame, len(calls), len(headers),
          [(r['width'], r['height'], r.get('whole_index_plane_matching_current_PXL_paths', [])) for r in headers.values()],
          'current code differences', len(divergent_code), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('frame', type=int)
    main(parser.parse_args().frame)
