"""Grouped native prefix controls and complete original memory-stream operations."""

import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import check_file_requests_v681 as prefix
from scripts.observe_file_requests_v681 import assemble
from scripts.prepare_memory_streams_v682 import BUFFERS, ROM, ROOT
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_village_wrap_v608 import read, save


def main():
    source = read(ROOT / 'source_contract.json')
    old_root, old_assemble = prefix.ROOT, prefix.assemble

    def grouped(cpu, header, callback, original, targets, address):
        group = [t for t in source['targets'] if t['instruction_index'] == targets[0]['instruction_index']]
        return assemble(cpu, header, callback, original, group, address)

    prefix.ROOT, prefix.assemble = ROOT, grouped
    try:
        prefix.main()
    finally:
        prefix.ROOT, prefix.assemble = old_root, old_assemble
    controls = read(ROOT / 'native_prefix_controls.json')
    assert len(controls['native_host_cases']) == 20
    controls.update(current_observer_sha256=sha(Path('scripts/observe_memory_streams_v682.py').read_bytes()),
        reused_native_prefix_checker='scripts/check_file_requests_v681.py',
        reused_native_prefix_checker_sha256=sha(Path('scripts/check_file_requests_v681.py').read_bytes()),
        actual_shared_opcode_target_groups_tested=True)
    save(ROOT / 'native_prefix_controls.json', controls)
    cases = []
    obj, dest, src = 0x02460020, 0x02470020, 0x02471020
    seed = bytes((i * 37 + 11) & 255 for i in range(4096))
    replacement = bytes(range(19))
    for version, path in (('current', ROM), ('clean', Path('work/clean.nds'))):
        arm = NdsImage.open(path).read_file('/__arm9__.bin')
        u = machine(arm)
        for mode, provider in BUFFERS.items():
            u.mem_write(obj - 16, b'\xA5' * 72)
            u.mem_write(provider - 16, b'\x5A' * 16 + seed + b'\x5A' * 16)
            u.mem_write(dest - 16, b'\xC3' * 1056)
            u.mem_write(src - 16, b'\x96' * 16 + replacement + b'\x96' * 16)
            expected = bytearray(seed)
            calls = []

            def run(offset, args, result, u=u, calls=calls):
                executed = call(u, offset, args)
                assert u.reg_read(UC_ARM_REG_R0) == result
                assert not {0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08} & executed
                calls.append({'entry': 0x02000000 + offset, 'args': list(args), 'return': result,
                              'complete_native_return_ABI_no_SDK_file_calls': True})

            call(u, 0xD05D0, (obj,))
            run(0xD0398, (obj, 0, mode), 1)  # Unmapped filename proves it is not read here.
            assert struct.unpack('<I', u.mem_read(obj + 28, 4))[0] == provider
            run(0xD01AC, (obj, dest, 17), 17)
            assert bytes(u.mem_read(dest, 17)) == seed[:17]
            run(0xD01AC, (obj, dest, 0), 0)
            run(0xD010C, (obj, src, 19), 19)
            expected[17:36] = replacement
            assert bytes(u.mem_read(provider, 4096)) == bytes(expected)
            run(0xD0274, (obj, 7, 0), 7)
            run(0xD01AC, (obj, dest, 13), 13)
            assert bytes(u.mem_read(dest, 13)) == expected[7:20]
            run(0xD0274, (obj, 41, 1), 61)
            run(0xD01AC, (obj, dest, 32), 32)
            assert bytes(u.mem_read(dest, 32)) == expected[61:93]
            assert struct.unpack('<I', u.mem_read(obj + 8, 4))[0] == 93
            run(0xD0274, (obj, 5, 2), 93)  # Memory end-origin leaves the cursor unchanged.
            run(0xD0340, (obj,), 1)
            fields = struct.unpack('<10I', u.mem_read(obj, 40))
            assert fields[2] == fields[7] == 0 and fields[8] == 93 and fields[9] == 0xFFFFFFFF
            assert bytes(u.mem_read(provider, 4096)) == bytes(expected)
            assert bytes(u.mem_read(provider - 16, 16)) == bytes(u.mem_read(provider + 4096, 16)) == b'\x5A' * 16
            assert bytes(u.mem_read(obj - 16, 16)) == bytes(u.mem_read(obj + 40, 16)) == b'\xA5' * 16
            assert bytes(u.mem_read(dest - 16, 16)) == b'\xC3' * 16
            assert bytes(u.mem_read(dest + 32, 992)) == b'\xC3' * 992
            assert bytes(u.mem_read(src - 16, 51)) == b'\x96' * 16 + replacement + b'\x96' * 16
            cases.append({'version': version, 'mode': mode, 'provider': provider, 'calls': calls,
                'fixed_buffer_selection_filename_ignored_reads_writes_seeks_highwater_and_close_verified': True,
                'read_write_and_object_canaries_source_bytes_and_ABI_exact': True,
                'memory_mode_selects_buffer_not_read_write_permission': True,
                'source_buffer_bytes_explicit_isolated_probe_not_actual_saved_payload': True})
    save(ROOT / 'native_memory_operations.json', {'cases': cases,
        '40_complete_original_operation_calls_current_and_clean': True,
        'checker_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V68220 grouped native prefixes and40 complete original memory-stream operations pass.', flush=True)


if __name__ == '__main__':
    main()
