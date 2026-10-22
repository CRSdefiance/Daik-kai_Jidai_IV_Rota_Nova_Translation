"""Execute the caller-selected archive path with bounded native route contracts."""

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

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine

ROOT = Path('work/analysis/legacy_archive_access_v384')
ROM = Path('out/all_routes_combined_v383_candidate.nds')
OBJECT, CAPACITY = 0x02450020, 0x10000
OPEN, READ, SEEK, CLOSE = 0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08


def main():
    rom = NdsImage.open(ROM)
    paths = {name.casefold(): name for _, name, _ in rom.iter_files()}
    arm = rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x24134:0x241d0] == clean[0x24134:0x241d0]
    table = json.loads((ROOT / 'route_archive_table.json').read_text(encoding='utf-8'))
    u = machine(arm)
    handles, events = {}, []

    def bridge(uc, address, size, _):
        if address not in (OPEN, READ, SEEK, CLOSE):
            return
        obj = uc.reg_read(UC_ARM_REG_R0)
        if address == OPEN:
            pointer = uc.reg_read(UC_ARM_REG_R1)
            path = '/' + bytes(uc.mem_read(pointer, 128)).split(b'\0', 1)[0].decode('ascii').replace('\\', '/').lstrip('/')
            path = paths[path.casefold()]
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
        for entry in table['entries']:
            path = '/' + entry['path'].replace('\\', '/').lstrip('/')
            path = paths[path.casefold()]
            raw = rom.read_file(path)
            payload = IlnkContainer.parse(raw).blocks[0]
            assert len(payload) < CAPACITY - 8
            u.mem_write(int(table['selector_global_field'], 16), struct.pack('<I', entry['index']))
            u.mem_write(OBJECT - 16, b'\xA5' * (CAPACITY + 32))
            u.mem_write(OBJECT + 4, b'\xFF' * 4)
            start = len(events)
            call(u, 0x24134, (OBJECT, 0))
            assert u.reg_read(UC_ARM_REG_R0) == 1
            assert bytes(u.mem_read(OBJECT + 8, len(payload))) == payload
            assert bytes(u.mem_read(OBJECT + 4, 4)) == bytes(4)
            assert bytes(u.mem_read(OBJECT - 16, 20)) == b'\xA5' * 20
            assert bytes(u.mem_read(OBJECT + 8 + len(payload), CAPACITY + 8 - len(payload))) == b'\xA5' * (CAPACITY + 8 - len(payload))
            assert not handles
            assert [e['path'] for e in events[start:] if e['operation'] == 'open'] == [path]
            end = len(events)
            before = bytes(u.mem_read(OBJECT - 16, CAPACITY + 32))
            call(u, 0x24134, (OBJECT, 0))
            assert u.reg_read(UC_ARM_REG_R0) == 1 and len(events) == end
            assert bytes(u.mem_read(OBJECT - 16, CAPACITY + 32)) == before
            cases.append({'route_index': entry['index'], 'path': path, 'block': 0,
                          'complete_block_bytes': len(payload), 'block_sha256': sha(payload),
                          'native_IO': events[start:end], 'whole_cache_and_neighbor_guards_exact': True,
                          'same_block_cache_hit_no_IO_or_memory_change': True})
    finally:
        u.hook_del(handle)
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()), 'cases': cases,
             'original_dispatch_and_archive_reader_execute': True, 'SDK_IO_bridge_only': True,
             'valid_route_indices_and_block0_are_supplied_native_contracts': True,
             'dynamic_archive_path_at_02024170_selects_route_scripts': True,
             'other_generic_file_open_paths_and_indirect_consumers_unresolved': True,
             'legacy_graphics_unused_claim': False, 'ROM_changed': False, 'full_goal_complete': False}
    (ROOT / 'route_dispatch_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('4 native route archive loads and4 unchanged cache hits pass; this dynamic archive path selects SC0-SC3.')


if __name__ == '__main__':
    main()
