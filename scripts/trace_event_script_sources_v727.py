"""Original EV action selector and complete SC-buffer loader with SDK I/O only.

Supplied source-backed selector registers are not ordinary event reachability.
This excludes generation inside this loader, not arbitrary post-load mutation,
other stream builders, indirect callers or global unused artwork.
"""

import struct
from collections import Counter
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R4,
    UC_ARM_REG_R9,
    UC_ARM_REG_R10,
    UC_ARM_REG_SP,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, STOP, call, machine
from scripts.trace_control_aliases_v688 import sections
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/event_script_sources_v727')
ROM = Path('out/all_routes_combined_v712_candidate.nds')
OWNER, BUFFER = 0x02410010, 0x02420010
CAPACITY = 0x2400
OPEN, READ, SEEK, CLOSE = 0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08
CARDS = {168, 169, 170, 171, 206, 207, 208, 209}


def run(rom, label):
    arm = rom.read_file('/__arm9__.bin')
    cpu = machine(arm)
    files = {f'/data/SC{i}.DK4': rom.read_file(f'/data/SC{i}.DK4') for i in range(4)}
    case_paths = {p.casefold(): p for p in files}
    parts = sections(rom)
    handles, events, executed = {}, [], set()
    phase = 'idle'
    stopped = []
    route_global = struct.unpack_from('<I', arm, 0x241C4)[0]
    assert route_global == 0x02279668
    vtable, empty_index = struct.unpack_from('<2I', arm, 0x24228)
    assert (vtable, empty_index) == (0x02134578, 0x00000FFF)

    def bridge(u, pc, size, unused):
        executed.add(pc)
        if phase == 'select' and pc in (0x02023F4C, 0x02023F84):
            stopped.append(pc)
            u.emu_stop()
            return
        if pc not in (OPEN, READ, SEEK, CLOSE):
            return
        obj, arg1, arg2 = [u.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2)]
        if pc == OPEN:
            requested = bytes(u.mem_read(arg1, 128)).split(b'\0')[0].decode('ascii')
            normalized = '/' + requested.replace('\\', '/').lstrip('/')
            # Explicit bridge mapping, not a host filesystem case-sensitivity claim.
            path = case_paths[normalized.casefold()]
            assert obj not in handles
            handles[obj] = [path, 0]
            u.mem_write(obj + 0x20, struct.pack('<2I', 0, len(files[path])))
            events.append({'operation': 'open', 'requested': requested, 'ROM_path': path})
            result = 1
        elif pc == SEEK:
            state = handles[obj]
            assert arg2 == 0 and 0 <= arg1 <= len(files[state[0]])
            state[1] = arg1
            events.append({'operation': 'seek', 'offset': arg1})
            result = 1
        elif pc == READ:
            state = handles[obj]
            raw = files[state[0]]
            assert state[1] + arg2 <= len(raw)
            payload = raw[state[1]:state[1] + arg2]
            u.mem_write(arg1, payload)
            events.append({'operation': 'read', 'offset': state[1], 'bytes': arg2})
            state[1] += arg2
            result = arg2
        else:
            handles.pop(obj)
            events.append({'operation': 'close'})
            result = 1
        u.reg_write(UC_ARM_REG_R0, result)
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    cpu.hook_add(UC_HOOK_CODE, bridge)
    routes, all_actions, loaded, hits = [], 0, 0, []
    for route in range(4):
        path = f'/data/SC{route}.DK4'
        scripts = IlnkContainer.parse(files[path]).blocks
        ev_path = f'/data/EV{route}.DK4'
        ev = rom.read_file(ev_path)
        assert ev[:2] == b'VE' and struct.unpack_from('<I', ev, 4)[0] == len(ev) - 96
        begin, end = struct.unpack_from('<2I', ev, 0x4C)
        inline = struct.unpack_from('<I', ev, 0x5C)[0]
        assert 0 <= begin <= end <= len(ev) - 96 and (end - begin) % 2 == 0
        assert inline + 96 == len(ev)
        words = struct.unpack_from(f'<{(end - begin) // 2}H', ev, 96 + begin)
        kinds = Counter((w >> 12) & 3 for w in words)
        assert not kinds[1] and not kinds[3]
        assert [w & 4095 for w in words if (w >> 12) & 3 == 2] == list(range(len(scripts)))
        cpu.mem_write(OWNER - 16, b'\xA5' * (0x34 + len(ev) + 32))
        cpu.mem_write(OWNER + 0x34, ev)
        cpu.mem_write(route_global + 0x48, struct.pack('<I', route))
        rows = []
        for action, word in enumerate(words):
            assert not handles
            events.clear()
            stopped.clear()
            cpu.mem_write(BUFFER - 16, b'\xA5' * (8 + CAPACITY + 32))
            for reg, value in ((UC_ARM_REG_R10, OWNER), (UC_ARM_REG_R0, OWNER + 0x34),
                               (UC_ARM_REG_R9, action), (UC_ARM_REG_R4, BUFFER),
                               (UC_ARM_REG_SP, STACK), (UC_ARM_REG_LR, STOP)):
                cpu.reg_write(reg, value)
            # Original pointer arithmetic, kind/index decode and child constructor.
            # Header/object inputs are supplied; the enclosing event is not run.
            phase = 'select'
            cpu.emu_start(0x02023EA4, STOP, count=1000)
            all_actions += 1
            if (word >> 12) & 3 == 0:
                assert stopped == [0x02023F84] and not events
                assert bytes(cpu.mem_read(BUFFER - 16, 8 + CAPACITY + 32)) == b'\xA5' * (8 + CAPACITY + 32)
                rows.append({'action': action, 'word': word, 'kind': 0, 'no_script_load_or_constructor': True})
                continue
            assert stopped == [0x02023F4C], (label, route, action, word, stopped)
            index = cpu.reg_read(UC_ARM_REG_R1)
            assert index == word & 4095 and cpu.reg_read(UC_ARM_REG_R0) == BUFFER
            assert struct.unpack('<2I', cpu.mem_read(BUFFER, 8)) == (vtable, empty_index)
            raw = scripts[index]
            assert len(raw) <= CAPACITY
            phase = 'load'
            call(cpu, 0x24134, (BUFFER, index), instruction_limit=500000)
            assert cpu.reg_read(UC_ARM_REG_R0) == 1 and not handles
            assert bytes(cpu.mem_read(BUFFER + 8, len(raw))) == raw
            assert struct.unpack('<2I', cpu.mem_read(BUFFER, 8)) == (vtable, index)
            assert bytes(cpu.mem_read(BUFFER - 16, 16)) == b'\xA5' * 16
            assert bytes(cpu.mem_read(BUFFER + 8 + len(raw), CAPACITY - len(raw) + 16)) == b'\xA5' * (CAPACITY - len(raw) + 16)
            assert bytes(cpu.mem_read(OWNER + 0x34, len(ev))) == ev
            assert len([e for e in events if e['operation'] == 'open']) == 1
            assert len([e for e in events if e['operation'] == 'close']) == 1
            assert next(e['ROM_path'] for e in events if e['operation'] == 'open') == path
            first_io = list(events)
            cached = bytes(cpu.mem_read(BUFFER - 16, 8 + CAPACITY + 32))
            events.clear()
            call(cpu, 0x24134, (BUFFER, index), instruction_limit=500000)
            assert cpu.reg_read(UC_ARM_REG_R0) == 1 and not events and not handles
            assert bytes(cpu.mem_read(BUFFER - 16, len(cached))) == cached
            for at in range(len(raw) - 3):
                command, operand = struct.unpack_from('<2H', raw, at)
                if command & 0xFF00 == 0x4600 and operand & 0x8000 and operand & 255 in CARDS:
                    hits.append({'route': route, 'block': index, 'offset': at,
                                 'word': command, 'operand': operand})
            rows.append({'action': action, 'word': word, 'kind': 2, 'native_selected_block': index,
                'complete_native_loaded_payload_bytes': len(raw), 'payload_sha256': sha(raw),
                'only_SDK_open_seek_read_close_bridged': first_io,
                'whole_native_loader_return_and_saved_register_SP_PC_ABI_pass': True,
                'cache_hit_no_IO_complete_object_and_neighbor_bytes_exact': True})
            loaded += 1
        routes.append({'route': route, 'SC_path': path, 'SC_sha256': sha(files[path]),
            'EV_path': ev_path, 'EV_sha256': sha(ev), 'EV_inline_offset_equals_body_end': inline,
            'bounded_action_table_body_span': [begin, end], 'action_kinds': dict(kinds),
            'all_archive_blocks_selected_once': len(scripts), 'maximum_source_block_bytes': max(map(len, scripts)),
            'actions': rows})
        print(f'{label} route{route}: {len(scripts)} complete native SC loads/cache hits; {kinds[0]} null actions.', flush=True)
    assert all_actions == 1312 and loaded == 1307
    assert not hits
    # All machine source code except bridge bodies is mapped from the registered ROM.
    for pc in executed - {OPEN, READ, SEEK, CLOSE}:
        matches = [data[pc - base:pc - base + 4] for _, base, data in parts if base <= pc and pc + 4 <= base + len(data)]
        assert matches and all(bytes(cpu.mem_read(pc, 4)) == value for value in matches)
    return {'ROM': label, 'ROM_sha256': sha(rom.source.read_bytes()), 'routes': routes,
        'native_selected_action_cases': all_actions, 'complete_SC_loads_and_cache_hits': loaded,
        'all_native_executed_code_source_exact': sorted(executed - {OPEN, READ, SEEK, CLOSE}),
        'no_village_card_event_opcode_byte_candidates_in_any_loaded_SC_payload': True,
        'source_selector_registers_and_VE_header_supplied_not_a_normal_event_trigger': True,
        'filename_case_bridge_maps_exact_original_request_to_explicit_ROM_path': True}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'proof.json').exists()
    release = {str(p): sha(p.read_bytes()) for p in (ROM, ROM.with_suffix('.manifest.json'),
        ROM.with_suffix('.xdelta'), Path('translations/release_stack.json'),
        Path('out/raphael_natural_v2_accepted_base.nds'))}
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    assert release[str(ROM)] == '6534e5619673ea6bdffa3a2342622b99ef393bef52ef58cac131ee94ae0f4030'
    ranges = [(0x23E94, 0x23F84), (0x24124, 0x24230), (0x134528, 0x1345A4), (0xD1EF0, 0xD2124)]
    a, b = [r.read_file('/__arm9__.bin') for r in (current, clean)]
    assert all(a[lo:hi] == b[lo:hi] for lo, hi in ranges)
    cases = [run(clean, 'clean'), run(current, 'current')]
    proof = {'candidate': str(ROM), 'candidate_sha256': release[str(ROM)],
        'source_exact_code_ranges': ranges, 'two_ROM_cases': cases,
        'all2624_action_fragments2614_whole_SC_loads_and2614_cache_hits_pass': True,
        'four_shipped_route_action_tables_select_SC_blocks_or_null_no_inline_scripts': True,
        'these_complete_SC_loaders_return_original_file_blocks_without_generating_commands': True,
        'arbitrary_other_stream_builders_post_load_mutation_indirect_consumers_not_excluded': True,
        'ordinary_village_triggers_original_comic_viewer_GPU_and_global_unused_claim': False,
        'prototype_case_sensitive_host_lookup_failure_not_game_or_ROM_failure': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'release_hashes_unchanged': release,
        'full_goal_complete': False}
    for path, digest in release.items():
        assert sha(Path(path).read_bytes()) == digest
    save(ROOT / 'proof.json', proof)
    print('V727: all original route script-buffer loads/cache hits source-exact; inline source path empty. No global non-use/ordinary trigger claim.')


if __name__ == '__main__':
    main()
