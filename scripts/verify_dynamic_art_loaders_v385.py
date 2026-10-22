"""Execute original event/town filename generation, cache and full image copying."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.research_online_loader_v190 import resource_call

ROOT = Path('work/analysis/image_registry_v385')
ROM = Path('out/all_routes_combined_v383_candidate.nds')
VIEW = 0x02470020
OPEN, READ, SEEK, CLOSE = 0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    ranges = [(0x5310, 0x5340), (0x12FB58, 0x12FC00), (0x28B74, 0x28BAC),
              (0xB7158, 0xB7294), (0xD3D30, 0xD42AC)]
    assert all(arm[lo:hi] == clean[lo:hi] for lo, hi in ranges)
    u = machine(arm)
    trace = resource_call(u, 0x5310, ())
    constructors = list(struct.unpack_from('<41I', arm, 0x12FB58))
    assert struct.unpack_from('<I', arm, 0x12FBFC)[0] == 0
    assert set(constructors) <= trace
    memory = bytes(u.mem_read(0x02000000, 0x400000))
    owners = []
    paths = {name.casefold(): name for _, name, _ in rom.iter_files()}
    for at in range(0, len(memory) - 20, 4):
        address = 0x02000000 + at
        fields = struct.unpack_from('<5I', memory, at)
        if fields[1:3] != (address + 4, address + 4) or fields[4] != 0xFFFFFFFF:
            continue
        pointer = fields[3]
        if not 0x02000000 <= pointer < 0x02400000:
            continue
        raw = memory[pointer - 0x02000000:].split(b'\0', 1)[0]
        if not raw.endswith(b'.pxl') or len(raw) > 128 or any(b < 32 or b >= 127 for b in raw):
            continue
        assert fields[0] == 0x02160538
        filename = '/' + raw.decode().replace('\\', '/').lstrip('/')
        owners.append({'owner': address, 'native_filename': filename, 'path': paths.get(filename.casefold())})
    assert len(owners) == 372
    matched = {r['path'] for r in owners if r['path'] is not None}
    assert len(matched) == 356
    owner_map = {r['owner']: r for r in owners}
    online_pages = []
    for category, (descriptor, count) in enumerate(zip(
            (0x12F88C, 0x12F898, 0x12F8A4, 0x12F8B0), (4, 4, 2, 3), strict=True)):
        table, captions, actual_count = struct.unpack_from('<3I', arm, descriptor)
        assert actual_count == count
        assert arm[descriptor:descriptor + 12] == clean[descriptor:descriptor + 12]
        for page in range(count):
            at = table - 0x02000000 + page * 16
            background, images, caption_art, image_count = struct.unpack_from('<4I', arm, at)
            assert arm[at:at + 16] == clean[at:at + 16]
            selected = [background, caption_art, *struct.unpack_from(
                f'<{image_count}I', arm, images - 0x02000000)]
            rows = [owner_map[p] for p in selected]
            assert all(r['path'] and r['path'].startswith('/_pxl/online/') for r in rows)
            online_pages.append({'category': category, 'page': page,
                                 'actual_owner_references': rows, 'caption_table': captions})
    assert len(online_pages) == 13
    manager = struct.unpack_from('<I', arm, 0x5D24)[0]
    call(u, 0xD6C0C, (manager,))
    pool_start, pool_end = struct.unpack('<2I', u.mem_read(manager, 8))
    handles, events = {}, []

    def bridge(uc, address, size, _):
        if address == 0x020E5650:
            raise ValueError('Native image loader reached fatal assertion')
        if address not in (OPEN, READ, SEEK, CLOSE):
            return
        obj = uc.reg_read(UC_ARM_REG_R0)
        if address == OPEN:
            pointer = uc.reg_read(UC_ARM_REG_R1)
            requested = '/' + bytes(uc.mem_read(pointer, 128)).split(b'\0', 1)[0].decode().replace('\\', '/').lstrip('/')
            path = paths[requested.casefold()]
            raw = rom.read_file(path)
            assert obj not in handles
            handles[obj] = [path, raw, 0]
            uc.mem_write(obj + 0x20, struct.pack('<2I', 0, len(raw)))
            events.append({'operation': 'open', 'path': path, 'sha256': sha(raw)})
            result = 1
        elif address == SEEK:
            state = handles[obj]
            offset = uc.reg_read(UC_ARM_REG_R1)
            assert uc.reg_read(UC_ARM_REG_R2) == 0 and 0 <= offset <= len(state[1])
            state[2] = offset
            result = 1
        elif address == READ:
            state = handles[obj]
            pointer, count = uc.reg_read(UC_ARM_REG_R1), uc.reg_read(UC_ARM_REG_R2)
            assert state[2] + count <= len(state[1])
            uc.mem_write(pointer, state[1][state[2]:state[2] + count])
            state[2] += count
            events.append({'operation': 'read', 'path': state[0], 'bytes': count})
            result = count
        else:
            events.append({'operation': 'close', 'path': handles.pop(obj)[0]})
            result = 1
        uc.reg_write(UC_ARM_REG_R0, result)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    handle = u.hook_add(UC_HOOK_CODE, bridge)
    cases = []
    try:
        owner = next(r['owner'] for r in owners if r['path'] == '/_pxl/common00bg.pxl')
        u.mem_write(VIEW - 16, b'\xA5' * 80)
        u.mem_write(VIEW, bytes(48))
        u.mem_write(STACK, struct.pack('<4I', 256, 192, 0, 0))
        call(u, 0xD3D30, (VIEW, owner, 0, 0))
        resource_call(u, 0xD4170, (VIEW,))
        pointer = u.reg_read(UC_ARM_REG_R0)
        original = rom.read_file('/_pxl/common00bg.pxl')
        assert bytes(u.mem_read(pointer, len(original))) == original
        assert pool_start <= pointer < pointer + len(original) <= pool_end
        files = sorted((name, raw) for _, name, raw in rom.iter_files()
                       if name.endswith('.pxl') and name.startswith(('/evstill/', '/towngrp/')))
        assert len(files) == 300
        for path, raw in files:
            assert len(raw) == len(original) == 49684
            assert raw[:20] == original[:20]
            index = int(Path(path).stem.removeprefix('evstill').removeprefix('towngrp'))
            entry = 0x28B74 if path.startswith('/evstill/') else 0xB7260
            before = bytes(u.mem_read(pool_start, pool_end - pool_start))
            old_view = bytes(u.mem_read(VIEW - 16, 80))
            start = len(events)
            call(u, entry, (VIEW if entry == 0x28B74 else pointer, index))
            assert bytes(u.mem_read(pointer, len(raw))) == raw, path
            after = bytes(u.mem_read(pool_start, pool_end - pool_start))
            offset = pointer - pool_start
            assert before[:offset] == after[:offset]
            assert before[offset + len(raw):] == after[offset + len(raw):]
            assert bytes(u.mem_read(VIEW - 16, 80)) == old_view
            assert not handles
            assert [e['path'] for e in events[start:] if e['operation'] == 'open'] == [path]
            cases.append({'path': path, 'index': index, 'native_entry': 0x02000000 + entry,
                          'whole_PXL_bytes': len(raw), 'whole_PXL_sha256': sha(raw),
                          'all_header_palette_pixels_exact': True,
                          'cache_pool_outside_target_and_view_guards_unchanged': True,
                          'native_IO': events[start:]})
            if len(cases) % 50 == 0:
                print('Verified dynamic art files:', len(cases), flush=True)
    finally:
        u.hook_del(handle)
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'all41_original_startup_constructors_executed': constructors,
             'initialized_PXL_owners': owners, 'distinct_exact_ROM_matches': len(matched),
             'all13_original_Online_pages': online_pages,
             'unmatched_bare_Online_owners_not_selected_by_these13_pages': True,
             'dynamic_event_and_town_files': cases,
             'SDK_filesystem_operations_only_bridge': True,
             'original_filename_formatter_cache_and_copy_execute': True,
             'supplied_view_on_real_common_canvas_and_valid_filename_indices': True,
             'actual_gameplay_trigger_GPU_crop_and_palette_application_not_proven': True,
             'ROM_changed': False, 'full_goal_complete': False}
    (ROOT / 'dynamic_loader_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('All300 dynamic event/town files load completely through original native code; no ROM changes.')


if __name__ == '__main__':
    main()
