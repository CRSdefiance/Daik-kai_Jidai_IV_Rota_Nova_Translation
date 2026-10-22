"""Original FLS stream constructor/parser with captured globals and SDK I/O only.

Caller-supplied filenames and isolated scratch object are explicit contracts.
No GPU, runtime trigger or root-FLS gameplay usage is inferred.
"""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE, UcError
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, SAVED, STACK, STOP, machine
from scripts.research_archive_callers_v264 import CLOSE, OPEN, READ, SEEK
from scripts.research_graphics_file_open_v301 import resolve, scan

ROOT = Path('work/analysis/fls_stream_v310')
ROM = Path('out/all_routes_combined_v309_candidate.nds')
SNAPSHOT = Path('work/emulation_v193/sailing_conditions_v309/final_arm9_ram.bin')
OBJECT, NAME = 0x02460000, 0x02464000
SIZE = 0x1B18


def case(rom, arm, ram, path, *, inspect=None):
    u = machine(arm)
    u.mem_write(BASE, ram)
    u.mem_write(OBJECT - 32, b'\xA5' * (SIZE + 64))
    u.mem_write(OBJECT, bytes(SIZE))
    u.mem_write(NAME, path.encode('ascii') + b'\0')
    u.mem_write(STACK - 8192, b'\xA5' * 8224)
    saved = {register: 0xA5000000 + number for number, register in enumerate(SAVED)}
    for register, value in saved.items():
        u.reg_write(register, value)
    handles, events, executed = {}, [], set()

    def observe(uc, address, size, _):
        executed.add(address)
        if address not in (OPEN, READ, SEEK, CLOSE):
            return
        owner = uc.reg_read(UC_ARM_REG_R0)
        if address == OPEN:
            p = uc.reg_read(UC_ARM_REG_R1)
            requested = bytes(uc.mem_read(p, 128)).split(b'\0')[0].decode('ascii')
            resolved = resolve(rom, requested)
            assert resolved == path
            raw = rom.read_file(resolved)
            handles[owner] = [raw, 0]
            uc.mem_write(owner + 0x20, struct.pack('<2I', 0, len(raw)))
            events.append({'operation': 'open', 'path': resolved, 'sha256': sha(raw), 'bytes': len(raw)})
            result = 1
        elif address == READ:
            raw, at = handles[owner]
            destination, count = uc.reg_read(UC_ARM_REG_R1), uc.reg_read(UC_ARM_REG_R2)
            assert 0 <= at <= len(raw)
            returned = min(count, len(raw) - at)
            uc.mem_write(destination, raw[at:at + returned])
            handles[owner][1] += returned
            event = {'operation': 'read', 'offset': at, 'bytes': returned, 'destination': destination}
            if returned != count:
                event['requested_bytes'] = count
            events.append(event)
            result = returned
        elif address == SEEK:
            at, origin = uc.reg_read(UC_ARM_REG_R1), uc.reg_read(UC_ARM_REG_R2)
            assert origin == 0 and at <= len(handles[owner][0])
            handles[owner][1] = at
            events.append({'operation': 'seek', 'offset': at})
            result = 1
        else:
            handles.pop(owner)
            events.append({'operation': 'close'})
            result = 1
        uc.reg_write(UC_ARM_REG_R0, result)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    u.hook_add(UC_HOOK_CODE, observe)
    u.reg_write(UC_ARM_REG_SP, STACK)
    u.reg_write(UC_ARM_REG_LR, STOP)
    u.reg_write(UC_ARM_REG_R0, OBJECT)
    u.emu_start(BASE + 0xFE050, STOP, count=500000)
    assert u.reg_read(UC_ARM_REG_PC) == STOP and u.reg_read(UC_ARM_REG_SP) == STACK
    assert all(u.reg_read(register) == value for register, value in saved.items())
    u.reg_write(UC_ARM_REG_LR, STOP)
    u.reg_write(UC_ARM_REG_R0, OBJECT)
    u.reg_write(UC_ARM_REG_R1, NAME)
    try:
        u.emu_start(BASE + 0xFDED0, STOP, count=1000000)
        assert u.reg_read(UC_ARM_REG_PC) == STOP and u.reg_read(UC_ARM_REG_SP) == STACK
        result = u.reg_read(UC_ARM_REG_R0)
        assert result == 1
        assert all(u.reg_read(register) == value for register, value in saved.items())
        assert bytes(u.mem_read(STACK - 8192, 32)) == b'\xA5' * 32
        assert bytes(u.mem_read(STACK, 32)) == b'\xA5' * 32
        assert bytes(u.mem_read(OBJECT - 32, 32)) == b'\xA5' * 32
        assert bytes(u.mem_read(OBJECT + SIZE, 32)) == b'\xA5' * 32
        allocation = struct.unpack('<I', u.mem_read(OBJECT + 0x1F8, 4))[0]
        raw = rom.read_file(path)
        command_offset, table_offset, texture_count, prefix_bytes = struct.unpack_from('<4I', raw)
        assert bytes(u.mem_read(allocation, prefix_bytes)) == raw[:prefix_bytes]
        assert struct.unpack('<I', u.mem_read(OBJECT + 4, 4))[0] == allocation
        assert struct.unpack('<I', u.mem_read(OBJECT + 8, 4))[0] == allocation + table_offset
        assert struct.unpack('<I', u.mem_read(OBJECT + 0x1A0C, 4))[0] == allocation + command_offset, 'Command pointer differs'
        assert raw[128:132] == b'FINF'
        assert struct.unpack('<I', u.mem_read(OBJECT + 0x1AA8, 4))[0] == allocation + 144
        canvas = struct.unpack_from('<2h', raw, 152)
        assert struct.unpack('<2h', u.mem_read(OBJECT + 0x1AA2, 4)) == canvas
        assert struct.unpack('<I', u.mem_read(OBJECT + 0x200, 4))[0] == 0
        result = {'path': path, 'native_constructor_and_full_stream_parser_return_pass': True,
                'allocated_prefix_pointer': allocation, 'all_declared_prefix_bytes_exact': prefix_bytes,
                'native_FINF_canvas': list(canvas), 'texture_record_count': texture_count,
                'native_table_command_and_FINF_pointers_match_original_header': True,
                'constructor_parser_saved_register_stack_return_and_outer_guards_pass': True,
                'events': events, 'object_hex': bytes(u.mem_read(OBJECT, SIZE)).hex(),
                'executed_native_addresses': sorted(executed), 'SDK_io_is_only_instruction_bridge': True,
                'controlled_filename_scratch_object_and_captured_global_state_are_contracts': True,
                'actual_trigger_texture_decode_GPU_and_screen_crops_verified': False}
        if inspect is not None:
            result['additional_scoped_inspection'] = inspect(u, OBJECT)
        return result
    except (AssertionError, UcError, ValueError) as error:
        return {'path': path, 'native_constructor_pass': True, 'native_stream_parser_pass': False,
                'error': str(error), 'stop_PC': u.reg_read(UC_ARM_REG_PC), 'events': events,
                'executed_native_addresses': sorted(executed), 'no_failed_case_clearance': True}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open(ROM)
    arm, ram = rom.read_file('/__arm9__.bin'), SNAPSHOT.read_bytes()
    capture = json.loads(Path('work/emulation_v193/sailing_conditions_v309/capture_report.json').read_text(encoding='utf-8'))
    assert capture['ROM_sha256'] == sha(ROM.read_bytes()) and capture['read_only_RAM_snapshot']['sha256'] == sha(ram)
    assert len(ram) == 0x400000 and capture['cold_boot'] and not capture['savestate_loaded']
    paths = sorted(p for _, p, _ in rom.iter_files() if p.casefold().endswith('.fls'))
    assert len(paths) == 15
    cases = [case(rom, arm, ram, path) for path in paths]
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'capture_report': 'work/emulation_v193/sailing_conditions_v309/capture_report.json',
             'captured_RAM_sha256': sha(ram), 'native_stream_parent_callers': scan(rom, arm, (BASE + 0xFDED0,)),
             'cases': cases, 'ROM_modified': False, 'full_goal_complete': False}
    (ROOT / 'proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps([{k: v for k, v in row.items() if k not in ('object_hex', 'executed_native_addresses')}
                      for row in cases], indent=2))


if __name__ == '__main__':
    main()
