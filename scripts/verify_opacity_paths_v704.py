"""Bind the portrait palette initializer and distinguish an in-place half blend.

Original routines execute in Unicorn with ROM-backed SDK file operations only.
These are supplied native contracts, not normal comic scene or GPU evidence.
"""

import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from ndspy.code import loadOverlayTable
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.run_room_gender_v694 import ROM
from scripts.scan_opacity_paths_v704 import immediate
from scripts.trace_control_aliases_v688 import sections
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/opacity_paths_v704')
SNAPSHOT = Path('E:/Rota Nova translations/Generated/work/emulation_v193/raw_caption_v703_baseline/frame_006080_arm9_ram.bin')
OPEN, READ, SEEK, CLOSE = 0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08
OBJECT, LENGTH = 0x02410020, 0x840C
FB, POINT, SIZE = 0x022E1794, 0x02430000, 0x02430010


def text(u, pointer):
    return bytes(u.mem_read(pointer, 128)).split(b'\0')[0].decode('ascii')


def literal_mask_users(parts):
    rows = []
    for name, base, data in parts:
        for at in range(0, len(data) - 3, 4):
            word = struct.unpack_from('<I', data, at)[0]
            # ARM LDR word, immediate, pre-index, PC base, no writeback.
            if word & 0x0F7F0000 != 0x051F0000:
                continue
            literal = base + at + 8 + (word & 4095) * (1 if word & (1 << 23) else -1)
            value = None
            for _, other_base, other in parts:
                if other_base <= literal <= other_base + len(other) - 4:
                    value = struct.unpack_from('<I', other, literal - other_base)[0]
                    break
            if value in (0x8000, 0x80008000):
                rows.append({'section': name, 'PC': base + at, 'literal': literal,
                    'destination_register': word >> 12 & 15, 'value': value})
    return rows


def byte_opacity_leads(parts):
    """Find ARM immediate ORR #80 near STRB; no Thumb/register dataflow claim."""
    decoder, rows, total = Cs(CS_ARCH_ARM, CS_MODE_ARM), [], 0
    for name, base, data in parts:
        for at in range(0, len(data) - 3, 4):
            word = struct.unpack_from('<I', data, at)[0]
            if word & 0x0E000000 != 0x02000000 or word >> 21 & 15 != 12 or immediate(word) != 0x80:
                continue
            total += 1
            start, end = max(0, at - 24), min(len(data), at + 40)
            window = list(decoder.disasm(data[start:end], base + start))
            if any(i.mnemonic.startswith('strb') for i in window):
                rows.append({'section': name, 'PC': base + at, 'window': [
                    {'PC': i.address, 'mnemonic': i.mnemonic, 'operands': i.op_str} for i in window]})
    return {'immediate_ORR_80_leads_including_inline_data': total,
        'nearby_STRB_leads': rows, 'Thumb_register_masks_and_cross_function_flows_not_excluded': True}


def initialized(arm, snapshot, rom):
    u = machine(arm)
    u.mem_write(BASE, snapshot)
    overlay = loadOverlayTable(rom.rom.arm9OverlayTable, lambda _, file_id: rom.rom.files[file_id])[0]
    u.mem_write(overlay.ramAddress, bytes(overlay.data))
    return u


def portrait_initializer(rom, clean, snapshot):
    arm = rom.read_file('/__arm9__.bin')
    u = initialized(arm, snapshot, rom)
    original = machine(clean.read_file('/__arm9__.bin'))
    paths = {p.casefold(): p for p in rom.path_map()}
    handles, io, writes, executed = {}, [], [], set()
    for path in ('/GRP/CMMNIMG.000', '/_pxl/item.pxl'):
        assert rom.read_file(path) == clean.read_file(path)
    palette = rom.read_file('/GRP/CMMNIMG.000')[:512]
    expected = struct.pack('<256H', *(v | 0x8000 for v, in struct.iter_unpack('<H', palette)))
    target_header = 0x02279894
    target = target_header + struct.unpack('<I', u.mem_read(target_header + 12, 4))[0]
    assert target == 0x02279938
    owner = 0x02313F38
    filename = struct.unpack('<I', u.mem_read(owner + 12, 4))[0]
    assert text(u, filename).replace('\\', '/').lower().lstrip('/') == '_pxl/item.pxl'
    u.mem_write(OBJECT - 16, b'\xA5' * (LENGTH + 32))
    before = bytes(u.mem_read(BASE, 0x400000))

    def bridge(cpu, address, size, _):
        executed.add(address)
        if address not in (OPEN, READ, SEEK, CLOSE):
            return
        obj = cpu.reg_read(UC_ARM_REG_R0)
        if address == OPEN:
            name = text(cpu, cpu.reg_read(UC_ARM_REG_R1))
            canonical = '/' + name.replace('\\', '/').lstrip('/')
            assert canonical.casefold() in paths and obj not in handles
            path = paths[canonical.casefold()]
            assert path in ('/GRP/CMMNIMG.000', '/_pxl/item.pxl')
            raw = rom.read_file(path)
            handles[obj] = [path, raw, 0]
            cpu.mem_write(obj + 0x20, struct.pack('<2I', 0, len(raw)))
            io.append({'operation': 'open', 'requested_name': name, 'path': path,
                'file_sha256': sha(raw), 'file_id': rom.path_map()[path], 'object': obj})
            result = 1
        elif address == SEEK:
            state = handles[obj]
            offset = cpu.reg_read(UC_ARM_REG_R1)
            assert cpu.reg_read(UC_ARM_REG_R2) == 0 and 0 <= offset <= len(state[1])
            state[2] = offset
            io.append({'operation': 'seek', 'path': state[0], 'offset': offset})
            result = 1
        elif address == READ:
            state = handles[obj]
            dest, count = cpu.reg_read(UC_ARM_REG_R1), cpu.reg_read(UC_ARM_REG_R2)
            offset = state[2]
            assert count == 512 and offset + count <= len(state[1])
            assert (state[0], offset, dest) in (
                ('/GRP/CMMNIMG.000', 0, 0x02233040), ('/_pxl/item.pxl', 20, OBJECT + 0xCC))
            cpu.mem_write(dest, state[1][offset:offset + count])
            state[2] += count
            io.append({'operation': 'read', 'path': state[0], 'offset': offset, 'bytes': count,
                'destination': dest, 'payload_sha256': sha(state[1][offset:offset + count])})
            result = count
        else:
            io.append({'operation': 'close', 'path': handles.pop(obj)[0]})
            result = 1
        cpu.reg_write(UC_ARM_REG_R0, result)
        cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))

    hook = u.hook_add(UC_HOOK_CODE, bridge)
    write_hook = u.hook_add(UC_HOOK_MEM_WRITE, lambda cpu, access, a, size, value, _: writes.append((a, size)))
    try:
        trace = call(u, 0x47B18, (OBJECT,), instruction_limit=100000)
    finally:
        u.hook_del(hook)
        u.hook_del(write_hook)
    assert not handles and u.reg_read(UC_ARM_REG_R0) == 1
    assert bytes(u.mem_read(0x02233040, 512)) == expected
    assert bytes(u.mem_read(target, 512)) == expected
    assert bytes(u.mem_read(OBJECT + 0xCC, 512)) == rom.read_file('/_pxl/item.pxl')[20:532]
    assert bytes(u.mem_read(OBJECT - 16, 16)) == bytes(u.mem_read(OBJECT + LENGTH, 16)) == b'\xA5' * 16
    after = bytes(u.mem_read(BASE, 0x400000))
    allowed = [(0x02233040, 0x02233240), (target, target + 512),
        (0x02311874, 0x02311874 + 30), (0x02311894, 0x02311894 + 30 * 68)]
    differences = [BASE + i for i, (a, b) in enumerate(zip(before, after)) if a != b]
    assert all(any(lo <= a < hi for lo, hi in allowed) for a in differences)
    # Every actual executed native instruction must be clean-original. SDK entry
    # points are bridged before their original instruction executes.
    for address in trace:
        assert bytes(u.mem_read(address, 4)) == bytes(original.mem_read(address, 4)), hex(address)
    descriptors = []
    for index in range(16):
        address = OBJECT + 0x82CC + index * 20
        fields = struct.unpack('<5I', u.mem_read(address, 20))
        assert fields[:3] == (0xA5A5A408, 16, 32)
        assert (address + fields[3]) & 0xFFFFFFFF == OBJECT + 0xCC
        assert (address + fields[4]) & 0xFFFFFFFF == OBJECT + 0x2CC + index * 0x800
        descriptors.append({'address': address, 'words': list(fields)})
    # Only source-defined object fields may change, even though descriptor
    # construction intentionally leaves unrelated initial flag bits in place.
    obj = bytes(u.mem_read(OBJECT, LENGTH))
    obj_ranges = [(0xCC, 0x2CC), (0x82CC, 0x840C)]
    assert all(v == 0xA5 or any(lo <= i < hi for lo, hi in obj_ranges) for i, v in enumerate(obj))
    conversions = [a for a in trace if 0x02047B58 <= a <= 0x02047B74]
    assert len(conversions) == 8
    assert sum(a == 0x02233040 + i * 2 and size == 2 for a, size in writes for i in range(256)) == 256
    return {'entry': 0x02047B18, 'full_original_return_stack_and_saved_register_ABI': True,
        'supplied_output_object': OBJECT, 'real_initialized_snapshot_header': target_header,
        'palette_target': target, 'actual_owner_filename': text(u, filename), 'IO': io,
        'all256_palette_words_source_low15_RGB_exact_highbit_set': True,
        'actual_changed_highbits': sum(not v & 0x8000 for v, in struct.iter_unpack('<H', palette)),
        'runtime_palette_sha256': sha(expected), 'source_palette_sha256': sha(palette),
        'complete_item_palette_source_bytes_and16_descriptors_exact': descriptors,
        'whole_main_RAM_differences_confined_to_declared_palette_and_original_file_globals': allowed,
        'main_RAM_changed_bytes': len(differences), 'all_executed_native_words_clean_original': len(trace),
        'not_legacy_ILNK_CMMNIMG_DK4_or_SLACKIMG_raw19_import': True,
        'normal_initialization_call_or_GPU_not_newly_observed': True}


def half_blend(rom, clean, snapshot):
    u = initialized(rom.read_file('/__arm9__.bin'), snapshot, rom)
    original = initialized(clean.read_file('/__arm9__.bin'), snapshot, clean)
    assert bytes(u.mem_read(0x01FFAB74, 0x228)) == bytes(original.mem_read(0x01FFAB74, 0x228))
    # Original clip origins are supplied here; both entire software screens and
    # guards are checked, not just the changed rectangle.
    u.mem_write(0x022E176C, bytes(8))
    source = struct.pack('<98304H', *((i * 197 + 123) & 65535 for i in range(98304)))
    cases = []
    for screen, colour, xy, wh in ((0, 0x7FFF, (3, 4), (11, 7)),
            (1, 0x0000, (-4, -3), (12, 8)), (0, 0x95A7, (249, 188), (18, 12)),
            (1, 0x0000, (256, 192), (3, 4)), (0, 0x0000, (0, 0), (256, 192))):
        u.mem_write(FB - 16, b'\xA5' * 16 + source + b'\xA5' * 16)
        u.mem_write(POINT, struct.pack('<2i', *xy))
        u.mem_write(SIZE, struct.pack('<2i', *wh))
        before = bytes(u.mem_read(BASE, 0x400000))
        trace = call(u, 0x01FFAB74 - BASE, (screen, colour, POINT, SIZE), instruction_limit=1500000)
        expected = bytearray(source)
        x0, y0 = max(0, min(256, xy[0])), max(0, min(192, xy[1]))
        x1, y1 = max(0, min(256, xy[0] + wh[0])), max(0, min(192, xy[1] + wh[1]))
        differing_from_opacity_only = 0
        for y in range(y0, y1):
            for x in range(x0, x1):
                at = screen * 0x18000 + y * 512 + x * 2
                value = struct.unpack_from('<H', source, at)[0]
                result = (((value & 0x7BDE) + (colour & 0x7BDE)) >> 1) | 0x8000
                struct.pack_into('<H', expected, at, result)
                differing_from_opacity_only += result != value | 0x8000
        actual = bytes(u.mem_read(FB, len(source)))
        assert actual == bytes(expected)
        assert bytes(u.mem_read(FB - 16, 16)) == bytes(u.mem_read(FB + len(source), 16)) == b'\xA5' * 16
        after = bytes(u.mem_read(BASE, 0x400000))
        assert before[:FB - BASE] == after[:FB - BASE] and before[FB - BASE + len(source):] == after[FB - BASE + len(source):]
        assert bytes(u.mem_read(POINT, 8)) == struct.pack('<2i', *xy)
        assert bytes(u.mem_read(SIZE, 8)) == struct.pack('<2i', *wh)
        for address in trace:
            assert bytes(u.mem_read(address, 4)) == bytes(original.mem_read(address, 4))
        cases.append({'screen': screen, 'fill_colour': colour, 'XYWH': [*xy, *wh],
            'clipped_pixels': max(0, x1 - x0) * max(0, y1 - y0),
            'complete_two_screen_bytes_compared': len(actual), 'output_sha256': sha(actual),
            'original_return_ABI_source_guards_and_whole_outside_RAM_unchanged': True,
            'pixels_rejecting_an_opacity_only_import_model': differing_from_opacity_only})
    return {'entry': 0x01FFAB74, 'mask': 0x7BDE, 'cases': cases,
        'reads_existing_destination_halfwords_and_supplied_scalar_fill_not_external_image_stream': True,
        'is_in_place_half_blend_not_RGB_preserving_raw_import': True,
        'source_defined_clipping_and_complete_original_native_routine_executed': True,
        'normal_caller_or_GPU_not_observed': True}


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    snapshot = SNAPSHOT.read_bytes()
    assert len(snapshot) == 0x400000
    portrait = portrait_initializer(rom, clean, snapshot)
    blend = half_blend(rom, clean, snapshot)
    users = literal_mask_users(sections(rom))
    byte_leads = byte_opacity_leads(sections(rom))
    assert users == [{'section': 'main0', 'PC': 0x020F412C, 'literal': 0x020F424C,
        'destination_register': 4, 'value': 0x80008000}]
    save(ROOT / 'native_proof.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'snapshot': str(SNAPSHOT), 'snapshot_sha256': sha(snapshot), 'portrait_palette_initializer': portrait,
        'original_in_place_half_blend': blend, 'bounded_ARM_word_literal_mask_users': users,
        'byte_opacity_leads': byte_leads,
        'literal_user_20F412C_is_a_lead_not_a_proven_raw_import': True,
        'TITLEMAP_20_4BB3C_already_bound_by_V221_not_new_coverage': True,
        'previous_goal_turn_classification': 'no progress: status-only answer; new native verification resumes here',
        'raw_comic_original_import_viewer_and_normal_display_still_open': True,
        'production_ROM_archive_palette_and_source_highbits_unchanged': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V704 complete original portrait palette initializer and five whole-frame half blends verified; no raw-comic import established.', flush=True)


if __name__ == '__main__':
    main()
