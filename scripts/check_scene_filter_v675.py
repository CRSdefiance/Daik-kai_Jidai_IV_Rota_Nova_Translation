"""Native host ABI/control checks for the read-only scene-entry callback filter."""

import ctypes as ct
import struct
from pathlib import Path

from keystone import KS_ARCH_X86, KS_MODE_64, Ks

from dk4tool.patch.grand_race_menu_release import sha
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.observe_scene_entry_v675 import CONTEXT, PC, WORD, assemble
from scripts.research_still_reveal_v675 import ROOT
from scripts.verify_village_wrap_v608 import save


def main():
    native, rows, seen, errors = NativeMemory(), [], [], []
    cpu, source, result = ct.create_string_buffer(128), ct.create_string_buffer(b'unchanged emulated source' * 32), ct.create_string_buffer(144)
    header, selection = (ct.c_uint32 * 4)(0, 1, 0, 0), (ct.c_ubyte * 4001)()
    selection[3800] = 1

    def callback(frame):
        try:
            seen.append((frame, sha(bytes(cpu)), sha(bytes(source))))
        except (ValueError, OSError) as exc:
            errors.append(repr(exc))

    cb = ct.WINFUNCTYPE(None, ct.c_uint32)(callback)
    leaf_asm = ';'.join([
        *[f'mov qword ptr [r12+{i * 8}],{reg}' for i, reg in enumerate(('rax', 'rcx', 'rdx', 'r8', 'r9', 'r10', 'r11', 'rsi', 'rdi', 'rsp'))],
        'pushfq', 'pop rax', 'mov qword ptr [r12+80],rax',
        'inc qword ptr [r12+120]', 'mov eax,ecx', 'ret'])
    leaf = native.executable(bytes(Ks(KS_ARCH_X86, KS_MODE_64).asm(leaf_asm)[0]))
    ptr = native.alloc(None, 4096, 0x3000, 0x04)
    code, assembly = assemble(ct.addressof(cpu), ct.addressof(header), ct.addressof(selection),
        ct.cast(cb, ct.c_void_p).value, leaf, ptr)
    assert len(code) < 4096
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
        f'mov rcx,{ct.addressof(header)}', 'mov ecx,dword ptr [rcx+16]',
        f'mov rax,{ptr}', 'call rax', 'mov dword ptr [r12+104],eax', 'mov qword ptr [r12+112],rsp',
        'add rsp,32', 'pop rdi', 'pop rsi', 'pop r12', 'ret'])
    # Separate argument slot avoids aliasing the four filter counter words.
    arguments = (ct.c_uint32 * 5)()
    driver_asm = driver_asm.replace(f'mov rcx,{ct.addressof(header)}', f'mov rcx,{ct.addressof(arguments)}')
    driver = native.executable(bytes(Ks(KS_ARCH_X86, KS_MODE_64).asm(driver_asm)[0]))
    run = ct.WINFUNCTYPE(None, ct.c_void_p)(driver)
    try:
        for case in ('selected', 'disabled', 'wrong_PC', 'wrong_word', 'wrong_argument',
                     'lower_context', 'later_list_link', 'unselected_frame', 'beyond_selection_bound'):
            values = [0x10000000 + i for i in range(32)]
            values[1], values[2], values[8] = WORD, PC, CONTEXT
            values[9] = CONTEXT + 12
            if case == 'wrong_PC':
                values[2] += 4
            if case == 'wrong_word':
                values[1] ^= 1
            raw = struct.pack('<32I', *values)
            ct.memmove(ct.addressof(cpu), raw, 128)
            if case == 'lower_context':
                struct.pack_into('<I', cpu, 32, CONTEXT - 24)
            elif case == 'later_list_link':
                struct.pack_into('<I', cpu, 36, CONTEXT + 16)
            arguments[4] = WORD ^ int(case == 'wrong_argument')
            header[0], header[1], header[2], header[3] = 3800, int(case != 'disabled'), 0, 0
            if case == 'unselected_frame':
                header[0] = 3801
            elif case == 'beyond_selection_bound':
                header[0] = 4001
            seen.clear()
            before = bytes(cpu), bytes(source)
            ct.memset(ct.addressof(result), 0, 144)
            run(ct.addressof(result))
            registers = struct.unpack_from('<11Q', result)
            assert registers[:9] == (ptr, arguments[4], 0x1122334455667788, 0x2233445566778899,
                0x33445566778899AA, 0x445566778899AABB, 0x5566778899AABBCC,
                0x66778899AABBCCDD, 0x778899AABBCCDDEE)
            before_sp, before_flags, returned, after_sp = struct.unpack_from('<QQI4xQ', result, 88)
            assert registers[9] == before_sp - 8 and registers[10] == before_flags
            assert before_sp == after_sp and returned == arguments[4]
            assert struct.unpack_from('<Q', result, 120)[0] == 1
            assert (bytes(cpu), bytes(source)) == before
            assert header[2] == len(seen) == int(case == 'selected')
            assert header[3] == int(case in ('wrong_word', 'wrong_argument'))
            assert not errors
            rows.append({'case': case, 'callback_count': len(seen), 'mismatch_count': header[3],
                'all_host_registers_flags_stack_exact_original_handler_once_and_emulated_bytes_unchanged': True})
    finally:
        for address in (leaf, ptr, driver):
            assert native.free(address, 0, 0x8000)
    save(ROOT / 'host_snapshot_controls.json', {'cases': rows, 'native_filter_assembly': assembly,
        'host_only_scratch_not_gameplay': True, 'script_sha256': sha(Path(__file__).read_bytes())})
    print('V675 nine native snapshot-filter ABI/selection guards pass, including first-list-link selection.')


if __name__ == '__main__':
    main()
