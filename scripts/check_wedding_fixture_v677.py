"""Scratch-only fixture policy and native callback ABI/selection controls."""

import ctypes as ct
import struct
from pathlib import Path

from keystone import KS_ARCH_X86, KS_MODE_64, Ks

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_wedding_fixture_v677 import PC, ROOT, WORD, assemble, plan
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre = read(ROOT / 'preflight.json')
    arm = NdsImage.open(pre['candidate']).read_file('/__arm9__.bin')
    raw = bytearray((CAP / 'wedding_source_v676_observed/frame_002300_arm9_ram.bin').read_bytes())
    obj = 0x0218F2A8
    struct.pack_into('<I', raw, obj - 0x02000000 + 4, struct.unpack_from('<I', arm, 0x2422C)[0])
    values = [0x10000000 + i for i in range(32)]
    values[1], values[2], values[4], values[5] = WORD, PC, obj, 22
    policy = []
    for case in ('selected', 'disabled', 'already_applied', 'another_block', 'wrong_captain',
                 'wrong_object', 'nonempty_reader', 'wrong_PC', 'wrong_word', 'wrong_version', 'short_RAM'):
        cpu, data, version = bytearray(struct.pack('<32I', *values)), bytearray(raw), arm
        if case == 'another_block':
            struct.pack_into('<I', cpu, 20, 23)
        if case == 'wrong_captain':
            struct.pack_into('<I', data, 0x022796B0 - 0x02000000, 1)
        if case == 'wrong_object':
            struct.pack_into('<I', cpu, 16, 0x02500000)
        if case == 'nonempty_reader':
            struct.pack_into('<I', data, obj - 0x02000000 + 4, 22)
        if case == 'wrong_PC':
            struct.pack_into('<I', cpu, 8, PC + 4)
        if case == 'wrong_word':
            struct.pack_into('<I', cpu, 4, WORD ^ 1)
        if case == 'wrong_version':
            version = bytes([arm[0] ^ 1]) + arm[1:]
        if case == 'short_RAM':
            data = data[:-1]
        before = bytes(cpu), bytes(data)
        rejected = None
        try:
            after, receipt = plan(version, before[0], before[1],
                enabled=case != 'disabled', already=case == 'already_applied')
        except ValueError as exc:
            rejected = str(exc)
        assert (bytes(cpu), bytes(data)) == before
        if case == 'selected':
            assert rejected is None and receipt['applied'] and after[20:24] == struct.pack('<I', 70)
            assert after[:20] == before[0][:20] and after[24:] == before[0][24:]
        elif case in ('disabled', 'already_applied', 'another_block'):
            assert rejected is None and not receipt['applied'] and after == before[0]
        else:
            assert rejected
        policy.append({'case': case, 'rejected': rejected, 'input_CPU_RAM_unchanged': True,
                       'only_selected_case_changes_expected_R1_to70': True})
    native, seen, errors = NativeMemory(), [], []
    cpu, source, result = ct.create_string_buffer(128), ct.create_string_buffer(1024), ct.create_string_buffer(144)
    header, arguments = (ct.c_uint32 * 4)(0, 1, 0, 0), (ct.c_uint32 * 5)()

    def callback(frame):
        try:
            seen.append(frame)
            struct.pack_into('<I', cpu, 20, 70)
        except BaseException as exc:  # noqa: BLE001 - never throw across C.
            errors.append(repr(exc))

    cb = ct.WINFUNCTYPE(None, ct.c_uint32)(callback)
    leaf_asm = ';'.join([
        *[f'mov qword ptr [r12+{i * 8}],{reg}' for i, reg in enumerate(('rax', 'rcx', 'rdx', 'r8', 'r9', 'r10', 'r11', 'rsi', 'rdi', 'rsp'))],
        'pushfq', 'pop rax', 'mov qword ptr [r12+80],rax',
        'inc qword ptr [r12+120]', 'mov eax,ecx', 'ret'])
    leaf = native.executable(bytes(Ks(KS_ARCH_X86, KS_MODE_64).asm(leaf_asm)[0]))
    ptr = native.alloc(None, 4096, 0x3000, 0x04)
    code, assembly = assemble(ct.addressof(cpu), ct.addressof(header), ct.cast(cb, ct.c_void_p).value, leaf, ptr)
    ct.memmove(ptr, code, len(code))
    old = ct.c_uint32()
    assert native.protect(ptr, 4096, 0x20, ct.byref(old))
    assert native.flush(native.process, ptr, len(code))
    driver_asm = ';'.join([
        'push r12', 'push rsi', 'push rdi', 'sub rsp,32', 'mov r12,rcx', 'mov qword ptr [r12+88],rsp',
        'mov rdx,0x1122334455667788', 'mov r8,0x2233445566778899', 'mov r9,0x33445566778899aa',
        'mov r10,0x445566778899aabb', 'mov r11,0x5566778899aabbcc',
        'mov rsi,0x66778899aabbccdd', 'mov rdi,0x778899aabbccddee',
        'xor eax,eax', 'cmp eax,1', 'pushfq', 'pop rax', 'mov qword ptr [r12+96],rax',
        f'mov rcx,{ct.addressof(arguments)}', 'mov ecx,dword ptr [rcx+16]',
        f'mov rax,{ptr}', 'call rax', 'mov dword ptr [r12+104],eax', 'mov qword ptr [r12+112],rsp',
        'add rsp,32', 'pop rdi', 'pop rsi', 'pop r12', 'ret'])
    driver = native.executable(bytes(Ks(KS_ARCH_X86, KS_MODE_64).asm(driver_asm)[0]))
    run, rows = ct.WINFUNCTYPE(None, ct.c_void_p)(driver), []
    try:
        for case in ('selected', 'disabled', 'wrong_PC', 'wrong_word', 'wrong_argument'):
            words = list(values)
            if case == 'wrong_PC':
                words[2] += 4
            if case == 'wrong_word':
                words[1] ^= 1
            before = struct.pack('<32I', *words)
            ct.memmove(cpu, before, 128)
            arguments[4] = WORD ^ int(case == 'wrong_argument')
            header[0], header[1], header[2], header[3] = 2222, int(case != 'disabled'), 0, 0
            seen.clear()
            ct.memset(ct.addressof(result), 0, 144)
            run(ct.addressof(result))
            registers = struct.unpack_from('<11Q', result)
            assert registers[:9] == (ptr, arguments[4], 0x1122334455667788, 0x2233445566778899,
                0x33445566778899AA, 0x445566778899AABB, 0x5566778899AABBCC,
                0x66778899AABBCCDD, 0x778899AABBCCDDEE)
            before_sp, before_flags, returned, after_sp = struct.unpack_from('<QQI4xQ', result, 88)
            assert registers[9] == before_sp - 8 and registers[10] == before_flags
            assert before_sp == after_sp and returned == arguments[4]
            assert struct.unpack_from('<Q', result, 120)[0] == 1 and bytes(source) == bytes(1024)
            expected = bytearray(before)
            if case == 'selected':
                struct.pack_into('<I', expected, 20, 70)
            assert bytes(cpu)[:128] == bytes(expected)
            assert header[2] == len(seen) == int(case == 'selected')
            assert header[3] == int(case in ('wrong_word', 'wrong_argument')) and not errors
            rows.append({'case': case, 'all_host_GPR_flags_stack_and_original_handler_once_exact': True,
                         'only_selected_expected_emulated_R1_change': True})
    finally:
        for address in (leaf, ptr, driver):
            assert native.free(address, 0, 0x8000)
    save(ROOT / 'fixture_controls.json', {'policy_cases': policy, 'native_prefix_cases': rows,
        'assembly': assembly, 'host_only_scratch_not_gameplay': True,
        'script_sha256': sha(Path(__file__).read_bytes())})
    print('V67711 fixture policy and5 native ABI/selection controls passed.', flush=True)


if __name__ == '__main__':
    main()
