"""Native host prefix and bounded DS main-RAM mirror controls."""

import ctypes as ct
import struct
from pathlib import Path

from keystone import KS_ARCH_X86, KS_MODE_64, Ks

from dk4tool.patch.grand_race_menu_release import sha
from scripts.observe_file_requests_v681 import assemble, main_read
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.prepare_file_requests_v681 import ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    source = read(ROOT / 'source_contract.json')
    native, seen, errors = NativeMemory(), [], []
    cpu, result, arguments = ct.create_string_buffer(128), ct.create_string_buffer(144), (ct.c_uint32 * 5)()
    header = (ct.c_uint32 * 4)(0, 1, 0, 0)

    def callback(frame):
        try:
            seen.append((frame, bytes(cpu)[:128]))
        except BaseException as exc:  # noqa: BLE001 - never throw across native ABI.
            errors.append(repr(exc))

    cb = ct.WINFUNCTYPE(None, ct.c_uint32)(callback)
    assembly = ';'.join([
        *[f'mov qword ptr [r12+{i * 8}],{r}' for i, r in enumerate(('rax', 'rcx', 'rdx', 'r8', 'r9', 'r10', 'r11', 'rsi', 'rdi', 'rsp'))],
        'pushfq', 'pop rax', 'mov qword ptr [r12+80],rax', 'inc qword ptr [r12+120]', 'mov eax,ecx', 'ret'])
    leaf = native.executable(bytes(Ks(KS_ARCH_X86, KS_MODE_64).asm(assembly)[0]))
    address = native.alloc(None, 4096, 0x3000, 0x04)
    driver_asm = ';'.join([
        'push r12', 'push rsi', 'push rdi', 'sub rsp,32', 'mov r12,rcx', 'mov qword ptr [r12+88],rsp',
        'mov rdx,0x1122334455667788', 'mov r8,0x2233445566778899', 'mov r9,0x33445566778899aa',
        'mov r10,0x445566778899aabb', 'mov r11,0x5566778899aabbcc',
        'mov rsi,0x66778899aabbccdd', 'mov rdi,0x778899aabbccddee',
        'xor eax,eax', 'cmp eax,1', 'pushfq', 'pop rax', 'mov qword ptr [r12+96],rax',
        f'mov rcx,{ct.addressof(arguments)}', 'mov ecx,dword ptr [rcx+16]', f'mov rax,{address}',
        'call rax', 'mov dword ptr [r12+104],eax', 'mov qword ptr [r12+112],rsp',
        'add rsp,32', 'pop rdi', 'pop rsi', 'pop r12', 'ret'])
    driver = native.executable(bytes(Ks(KS_ARCH_X86, KS_MODE_64).asm(driver_asm)[0]))
    run = ct.WINFUNCTYPE(None, ct.c_void_p)(driver)
    cases, sources = [], []
    try:
        for target in source['targets']:
            code, asm = assemble(ct.addressof(cpu), ct.addressof(header), ct.cast(cb, ct.c_void_p).value,
                                  leaf, [target], address)
            assert len(code) < 4096
            old = ct.c_uint32()
            assert native.protect(address, 4096, 0x04, ct.byref(old))
            ct.memmove(address, code, len(code))
            assert native.protect(address, 4096, 0x20, ct.byref(old))
            assert native.flush(native.process, address, len(code))
            sources.append({'target': target, 'code_hex': code.hex(), 'assembly': asm})
            for name in ('selected', 'disabled', 'wrong_PC', 'wrong_word', 'wrong_argument'):
                values = [0x10000000 + i for i in range(32)]
                values[1], values[2] = target['word'], target['PC']
                if name == 'wrong_PC':
                    values[2] += 4
                if name == 'wrong_word':
                    values[1] ^= 1
                before = struct.pack('<32I', *values)
                ct.memmove(cpu, before, len(before))
                arguments[4] = target['word'] ^ int(name == 'wrong_argument')
                header[0], header[1], header[2], header[3] = 1234, int(name != 'disabled'), 0, 0
                seen.clear()
                ct.memset(ct.addressof(result), 0, 144)
                run(ct.addressof(result))
                regs = struct.unpack_from('<11Q', result)
                assert regs[:9] == (address, arguments[4], 0x1122334455667788, 0x2233445566778899,
                    0x33445566778899AA, 0x445566778899AABB, 0x5566778899AABBCC,
                    0x66778899AABBCCDD, 0x778899AABBCCDDEE)
                sp, flags, returned, after_sp = struct.unpack_from('<QQI4xQ', result, 88)
                assert regs[9] == sp - 8 and regs[10] == flags and sp == after_sp
                assert returned == arguments[4] and struct.unpack_from('<Q', result, 120)[0] == 1
                assert bytes(cpu)[:128] == before and not errors
                assert seen == ([(1234, before)] if name == 'selected' else [])
                assert header[2] == int(name == 'selected') and header[3] == int(name in ('wrong_word', 'wrong_argument'))
                cases.append({'target': target['name'], 'case': name,
                    'host_registers_flags_stack_CPU_prefix_original_return_and_one_original_call_exact': True})
    finally:
        for pointer in (leaf, address, driver):
            assert native.free(pointer, 0, 0x8000)
    raw = bytes(range(256)) * 16384
    memory = []
    for address, length, valid in ((0x02001000, 128, True), (0x02401000, 128, True),
        (0x02801000, 128, True), (0x02C01000, 128, True), (0x023FFFF0, 16, True),
        (0x023FFFF0, 17, False), (0x01000000, 16, False), (0x03000000, 16, False)):
        try:
            result = main_read(raw, address, length)
        except ValueError:
            assert not valid
        else:
            assert valid and result == raw[(address - 0x02000000) & 0x3FFFFF:((address - 0x02000000) & 0x3FFFFF) + length]
        memory.append({'address': address, 'length': length, 'accepted': valid})
    save(ROOT / 'native_prefix_controls.json', {'native_host_cases': cases, 'read_policy_cases': memory,
        'native_prefix_sources': sources, 'observer_sha256': sha(Path('scripts/observe_file_requests_v681.py').read_bytes()),
        'checker_sha256': sha(Path(__file__).read_bytes()), 'scratch_controls_not_gameplay': True})
    print('V68115 native prefix/ABI and8 bounded mirror-read controls pass.', flush=True)


if __name__ == '__main__':
    main()
