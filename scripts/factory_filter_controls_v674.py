"""Host-only FLS-entry matching/ABI witness using the verified filter implementation."""

import ctypes as ct
import struct

from keystone import KS_ARCH_X86, KS_MODE_64, Ks

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_graphic_paints_v669 import ROM
from scripts.observe_graphic_paints_v669 import HEADER, STRIDE, NativeMemory, assemble
from scripts.prepare_maria_opening_v674 import ROOT
from scripts.verify_village_wrap_v608 import read, save


def factory_controls():
    """Original ROM bytes are inputs to isolated host-only scratch tests."""
    native, rom = NativeMemory(), NdsImage.open(ROM)
    source = read(ROOT / 'source_contract.json')
    assets = [ct.create_string_buffer(rom.read_file(r['path'])) for r in source['source_assets']]
    asset_args = [(ct.addressof(a), r['bytes']) for a, r in zip(assets, source['source_assets'], strict=True)]
    cpu, wram = ct.create_string_buffer(128), ct.create_string_buffer(0x400000)
    buffer, result = ct.create_string_buffer(HEADER + STRIDE * 2), ct.create_string_buffer(144)
    leaf_assembly = ';'.join([  # noqa: FLY002 - separate native instructions
        'mov qword ptr [r12],rax', 'mov qword ptr [r12+8],rcx', 'mov qword ptr [r12+16],rdx',
        'mov qword ptr [r12+24],r8', 'mov qword ptr [r12+32],r9', 'mov qword ptr [r12+40],r10',
        'mov qword ptr [r12+48],r11', 'mov qword ptr [r12+56],rsi', 'mov qword ptr [r12+64],rdi',
        'mov qword ptr [r12+72],rsp', 'pushfq', 'pop rax', 'mov qword ptr [r12+80],rax', 'mov eax,ecx', 'ret'])
    leaf = native.executable(bytes(Ks(KS_ARCH_X86, KS_MODE_64).asm(leaf_assembly)[0]))
    code_address = native.alloc(None, 4096, 0x3000, 0x04)
    assert code_address
    code, assembly = assemble(ct.addressof(cpu), ct.addressof(wram), ct.addressof(buffer), leaf,
                              2, asset_args, source['targets'], code_address)
    assert len(code) < 4096
    ct.memmove(code_address, code, len(code))
    old = ct.c_uint32()
    assert native.protect(code_address, 4096, 0x20, ct.byref(old))
    assert native.flush(native.process, code_address, len(code))
    driver_assembly = ';'.join([
        'push r12', 'push rsi', 'push rdi', 'sub rsp,32', 'mov r12,rcx', 'mov qword ptr [r12+88],rsp',
        'mov rdx,0x1122334455667788', 'mov r8,0x2233445566778899', 'mov r9,0x33445566778899aa',
        'mov r10,0x445566778899aabb', 'mov r11,0x5566778899aabbcc',
        'mov rsi,0x66778899aabbccdd', 'mov rdi,0x778899aabbccddee',
        'xor eax,eax', 'cmp eax,1', 'pushfq', 'pop rax', 'mov qword ptr [r12+96],rax',
        f'mov rcx,{ct.addressof(cpu)}', 'mov ecx,dword ptr [rcx+4]',
        f'mov rax,{code_address}', 'call rax', 'mov dword ptr [r12+104],eax', 'mov qword ptr [r12+112],rsp',
        'add rsp,32', 'pop rdi', 'pop rsi', 'pop r12', 'ret'])
    driver = native.executable(bytes(Ks(KS_ARCH_X86, KS_MODE_64).asm(driver_assembly)[0]))
    run = ct.WINFUNCTYPE(None, ct.c_void_p)(driver)
    rows = []
    try:
        for name, target_index, asset_index, enabled, count, mutate, invalid in (
            ('Frame_corner', 3, 0, 1, 0, False, False), ('Frame_tiled', 2, 0, 1, 0, False, False),
            ('Frame_scaled', 0, 0, 1, 0, False, False), ('Confirm_corner', 1, 1, 1, 0, False, False),
            ('Marker_corner_shared_header', 1, 2, 1, 0, False, False),
            ('Frame_last_byte_differs', 1, 0, 1, 0, True, False),
            ('Confirm_last_byte_differs', 1, 1, 1, 0, True, False),
            ('Marker_last_byte_differs', 1, 2, 1, 0, True, False),
            ('disabled_retains_original', 1, 0, 0, 0, False, False),
            ('overflow_retains_original', 1, 0, 1, 2, False, False),
            ('unsupported_source_pointer_retains_original', 1, 0, 1, 0, False, True),
            ('wrong_PC_retains_original', 1, 0, 1, 0, False, False),
            ('wrong_instruction_retains_original', 1, 0, 1, 0, False, False),
        ):
            target = source['targets'][target_index]
            ct.memset(ct.addressof(wram), 0, ct.sizeof(wram))
            blob = rom.read_file(source['source_assets'][asset_index]['path'])
            ct.memmove(ct.addressof(wram) + 0x4000, blob, len(blob))
            if mutate:
                ct.c_ubyte.from_address(ct.addressof(wram) + 0x4000 + len(blob) - 1).value ^= 1
            struct.pack_into('<4I', wram, 0x1000, 208, 32, 48, 8)
            struct.pack_into('<8I', wram, 0x2000, 0x02002100, 0x02002200, 3, 4, 5, 6, 7, 8)
            struct.pack_into('<4I', wram, 0x2100, *([10, 20, 58, 28] if target_index == 2 else [48, 8, 0, 0]))
            struct.pack_into('<4I', wram, 0x2200, 10, 20, 58, 28)
            values = [0x10000000 + i for i in range(32)]
            values[1], values[2], values[19] = target['original_instruction'], target['PC'], target['PC'] + 8
            if name.startswith('wrong_PC'):
                values[2] += 4
                values[19] += 4
            if name.startswith('wrong_instruction'):
                values[1] ^= 1
            values[4:8] = [0, 0x01000000 if invalid else 0x02004000, 9, 0x02001000]
            values[17] = 0x02002000
            raw = struct.pack('<32I', *values)
            ct.memmove(ct.addressof(cpu), raw, len(raw))
            before_ram = sha(bytes(wram))
            ct.memset(ct.addressof(buffer), 0, ct.sizeof(buffer))
            struct.pack_into('<QII', buffer, 0, count, 321, enabled)
            run(ct.addressof(result))
            registers = struct.unpack_from('<11Q', result)
            assert registers[:9] == (code_address, values[1], 0x1122334455667788, 0x2233445566778899,
                0x33445566778899AA, 0x445566778899AABB, 0x5566778899AABBCC,
                0x66778899AABBCCDD, 0x778899AABBCCDDEE)
            before_sp, before_flags, returned, after_sp = struct.unpack_from('<QQI4xQ', result, 88)
            assert registers[9] == before_sp - 8 and registers[10] == before_flags
            assert before_sp == after_sp and returned == values[1]
            assert bytes(cpu)[:128] == raw and sha(bytes(wram)) == before_ram
            actual_count, _, _, overflow, mismatch = struct.unpack_from('<Q4I', buffer)
            matched = enabled == 1 and count < 2 and not name.startswith(('wrong_PC', 'wrong_instruction'))
            assert actual_count == count + int(matched) and mismatch == int(name.startswith('wrong_instruction'))
            assert overflow == int(name.startswith('overflow'))
            binding, flags = struct.unpack_from('<2I', buffer, HEADER + count * STRIDE + 148) if matched else (None, None)
            if matched:
                expected_binding = ((1, 3), (2, 4), (6, 7))[asset_index][int(mutate)]
                if mutate and asset_index == 0:
                    expected_binding = 7  # Shared metadata matches neither complete atlas.
                assert binding == (0 if invalid else expected_binding), (name, binding, expected_binding)
                assert bool(flags & 4) == invalid
                record = struct.unpack_from('<40I', buffer, HEADER + count * STRIDE)
                assert record[:12] == (321, values[2], values[1], *values[4:8], values[17], values[18], values[19], values[20], values[1])
                assert record[20:24] == ((208, 32, 48, 8) if target_index == 2 else (208, 32, 0, 0))
                assert record[24:28] == ((10, 20, 58, 28) if target_index == 2 else (48, 8, 0, 0))
                assert record[28:32] == ((0, 0, 0, 0) if target_index == 2 else
                                         (10, 20, 58, 28) if target_index == 0 else (10, 20, 0, 0))
            rows.append({'case': name, 'binding_ID': binding, 'guard_flags': flags,
                         'host_registers_flags_stack_original_return_and_entire_source_RAM_exact': True})
    finally:
        for address in (leaf, code_address, driver):
            assert native.free(address, 0, 0x8000)
    return {'cases': rows, 'native_filter_hex': code.hex(), 'native_filter_assembly': assembly,
            'whole_expected_files_compared_including_last_byte_controls': True,
            'host_only_scratch_witnesses_not_gameplay': True}

if __name__ == '__main__':
    save(ROOT / 'factory_host_controls.json', factory_controls())
    print('V674 thirteen host controls pass; first corner case selects actual FLS factory PC with source exact push instruction.')
