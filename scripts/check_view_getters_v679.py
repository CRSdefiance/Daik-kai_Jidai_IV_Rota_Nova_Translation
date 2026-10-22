"""Native scratch controls for the read-only view-input filter and its ABI."""

import ctypes as ct
import struct
from pathlib import Path

from keystone import KS_ARCH_X86, KS_MODE_64, Ks

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.observe_view_getters_v679 import HEADER, STRIDE, assemble
from scripts.prepare_view_getters_v679 import ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    source, rom, native = read(ROOT / 'source_contract.json'), NdsImage.open(ROM), NativeMemory()
    cpu, wram = ct.create_string_buffer(128), ct.create_string_buffer(0x400000)
    buffer, result = ct.create_string_buffer(HEADER + STRIDE * 2), ct.create_string_buffer(144)
    blobs = [rom.read_file(row['path']) for row in source['source_assets']]
    assets = [ct.create_string_buffer(blob) for blob in blobs]
    args = [(ct.addressof(a), len(blob)) for a, blob in zip(assets, blobs, strict=True)]
    leaf = native.executable(bytes(Ks(KS_ARCH_X86, KS_MODE_64).asm(';'.join([  # noqa: FLY002 - separate native instructions
        'mov qword ptr [r12],rax', 'mov qword ptr [r12+8],rcx', 'mov qword ptr [r12+16],rdx',
        'mov qword ptr [r12+24],r8', 'mov qword ptr [r12+32],r9', 'mov qword ptr [r12+40],r10',
        'mov qword ptr [r12+48],r11', 'mov qword ptr [r12+56],rsi', 'mov qword ptr [r12+64],rdi',
        'mov qword ptr [r12+72],rsp', 'pushfq', 'pop rax', 'mov qword ptr [r12+80],rax',
        'mov eax,ecx', 'ret']))[0]))
    address = native.alloc(None, 4096, 0x3000, 0x04)
    code, assembly = assemble(ct.addressof(cpu), ct.addressof(wram), ct.addressof(buffer), leaf,
        2, args, source['target'], address)
    assert len(code) < 4096
    ct.memmove(address, code, len(code))
    protection = ct.c_uint32()
    assert native.protect(address, 4096, 0x20, ct.byref(protection))
    assert native.flush(native.process, address, len(code))
    driver = native.executable(bytes(Ks(KS_ARCH_X86, KS_MODE_64).asm(';'.join([
        'push r12', 'push rsi', 'push rdi', 'sub rsp,32', 'mov r12,rcx', 'mov qword ptr [r12+88],rsp',
        'mov rdx,0x1122334455667788', 'mov r8,0x2233445566778899', 'mov r9,0x33445566778899aa',
        'mov r10,0x445566778899aabb', 'mov r11,0x5566778899aabbcc',
        'mov rsi,0x66778899aabbccdd', 'mov rdi,0x778899aabbccddee',
        'xor eax,eax', 'cmp eax,1', 'pushfq', 'pop rax', 'mov qword ptr [r12+96],rax',
        f'mov rcx,{ct.addressof(cpu)}', 'mov ecx,dword ptr [rcx+4]', f'mov rax,{address}', 'call rax',
        'mov dword ptr [r12+104],eax', 'mov qword ptr [r12+112],rsp',
        'add rsp,32', 'pop rdi', 'pop rsi', 'pop r12', 'ret']))[0]))
    run = ct.WINFUNCTYPE(None, ct.c_void_p)(driver)
    cases = []
    names = ['cached_Frame', 'cached_Confirm', 'cached_Marker', 'cached_Frame_final_byte_corrupt',
        'cached_Confirm_final_byte_corrupt', 'cached_Marker_final_byte_corrupt', 'resource_Frame',
        'resource_Confirm', 'bad_cached_pointer', 'bad_view_pointer', 'bad_owner_pointer',
        'bad_filename_pointer', 'disabled', 'overflow', 'wrong_PC', 'wrong_instruction']
    try:
        for name in names:
            ct.memset(ct.addressof(wram), 0, ct.sizeof(wram))
            asset = 1 if 'Confirm' in name else 2 if 'Marker' in name else 0
            blob = blobs[asset]
            ct.memmove(ct.addressof(wram) + 0x4000, blob, len(blob))
            if name.endswith('corrupt'):
                ct.c_ubyte.from_address(ct.addressof(wram) + 0x4000 + len(blob) - 1).value ^= 1
            view = [0x0216567C, 1, 2, 0x02002000, 0x02004000,
                    4 if name.startswith(('resource', 'bad_owner', 'bad_filename')) else 0,
                    6, 208, 32, 9, 48, 8]
            if name == 'bad_cached_pointer':
                view[4] = 0x01000000
            if name == 'bad_owner_pointer':
                view[3] = 0x01000000
            struct.pack_into('<12I', wram, 0x1000, *view)
            owner = [0x02160538, 0x02002004, 0x02002004,
                     0x01000000 if name == 'bad_filename_pointer' else 0x02003000, 0xFFFFFFFF]
            struct.pack_into('<5I', wram, 0x2000, *owner)
            filename = source['source_assets'][asset]['path'].lstrip('/').encode() + b'\0'
            ct.memmove(ct.addressof(wram) + 0x3000, filename, len(filename))
            stack = tuple(0x12340000 + i for i in range(8))
            struct.pack_into('<8I', wram, 0x800, *stack)
            values = [0x10000000 + i for i in range(32)]
            values[1], values[2] = source['target']['original_instruction'], source['target']['PC']
            values[4:8] = [0x01000000 if name == 'bad_view_pointer' else 0x02001000, 11, 22, 33]
            values[17], values[18], values[19] = 0x02000800, 0x02045678, values[2] + 8
            if name == 'wrong_PC':
                values[2] += 4
            if name == 'wrong_instruction':
                values[1] ^= 1
            raw = struct.pack('<32I', *values)
            ct.memmove(ct.addressof(cpu), raw, len(raw))
            ct.memset(ct.addressof(buffer), 0, ct.sizeof(buffer))
            count, enabled = (2 if name == 'overflow' else 0), int(name != 'disabled')
            struct.pack_into('<QII', buffer, 0, count, 321, enabled)
            before = bytes(wram)
            run(ct.addressof(result))
            registers = struct.unpack_from('<11Q', result)
            assert registers[:9] == (address, values[1], 0x1122334455667788, 0x2233445566778899,
                0x33445566778899AA, 0x445566778899AABB, 0x5566778899AABBCC,
                0x66778899AABBCCDD, 0x778899AABBCCDDEE)
            before_sp, before_flags, returned, after_sp = struct.unpack_from('<QQI4xQ', result, 88)
            assert registers[9] == before_sp - 8 and registers[10] == before_flags
            assert before_sp == after_sp and returned == values[1]
            assert bytes(cpu)[:128] == raw and bytes(wram) == before
            actual_count, _, _, overflow, mismatch = struct.unpack_from('<Q4I', buffer)
            selected = name not in ('disabled', 'overflow', 'wrong_PC', 'wrong_instruction')
            assert actual_count == count + int(selected) and overflow == int(name == 'overflow')
            assert mismatch == int(name == 'wrong_instruction')
            if selected:
                row = struct.unpack_from('<48I', buffer, HEADER)
                assert row[:12] == (321, values[2], values[1], *values[4:8], values[17], values[18], values[19], values[20], values[1])
                assert row[12:20] == stack
                if name != 'bad_view_pointer':
                    assert row[20:32] == tuple(view)
                expected_flag = {'bad_cached_pointer': 16, 'bad_view_pointer': 2,
                                 'bad_owner_pointer': 4, 'bad_filename_pointer': 8}.get(name, 0)
                assert row[38] == expected_flag, (name, row[38])
                expected_binding = (1, 2, 6)[asset] if name.startswith('cached_') and not name.endswith('corrupt') else 0
                assert row[37] == expected_binding, (name, row[37], expected_binding)
                if name.startswith('cached_'):
                    assert row[32:37] == struct.unpack_from('<5I', blob)
                if name.startswith('resource'):
                    assert row[32:37] == tuple(owner) and bytes(buffer)[HEADER + 160:HEADER + 192] == filename.ljust(32, b'\0')
            cases.append({'case': name, 'input_CPU_all4MiB_RAM_and_host_ABI_return_exact': True,
                          'expected_binding_and_bounded_read_guards_verified': True})
    finally:
        for p in (leaf, address, driver):
            assert native.free(p, 0, 0x8000)
    save(ROOT / 'native_filter_controls.json', {'cases': cases, 'filter_hex': code.hex(),
        'filter_assembly': assembly, 'observer_sha256': sha(Path('scripts/observe_view_getters_v679.py').read_bytes()),
        'checker_sha256': sha(Path(__file__).read_bytes()), 'scratch_native_controls_not_actual_gameplay': True})
    print('V679 sixteen original-input/native host ABI controls pass.', flush=True)


if __name__ == '__main__':
    main()
