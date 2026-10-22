"""Compose complete town commodity labels without persistent bitmap allocation."""

import json
import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_common_display_name_hook import branch_link

BASE, ENTRY, CAPTURE, CACHE = 0x02000000, 0x01FFC504, 0x01FFC6AC, 0x0215DC24
TRAMPOLINE = 0x0215BB60
SOURCE = 'b03327187284a6ac560bf76ff442d75f9caa34c6b130438b582a44f2baf37c5b'
TAILS = ((0x15DC24, 0x15DC44), (0x15DB24, 0x15DB34),
         (0x15DB44, 0x15DB54), (0x15DC54, 0x15DC64),
         (0x15DC74, 0x15DC84), (0x15DD44, 0x15DD54),
         (0x15DD74, 0x15DD84), (0x15DE14, 0x15DE24),
         (0x15BB60, 0x15BB68))


def scatter(blob, code_bytes, origin, blocks):
    """Relocate ARM branches and duplicate PC-relative literals within each block."""
    words = list(struct.unpack(f'<{code_bytes // 4}I', blob[:code_bytes]))
    layout, mapped, left, offset = [], {}, len(words), 0
    for lo, hi in blocks:
        count = min(left, (hi - lo) // 4)
        while count:
            literals = {}
            for index, word in enumerate(words[offset:offset + count], offset):
                if word & 0x0F7F0000 == 0x051F0000:
                    displacement = word & 4095
                    target = index * 4 + 8 + (displacement if word & (1 << 23) else -displacement)
                    assert code_bytes <= target <= len(blob) - 4
                    literals[word] = struct.unpack_from('<I', blob, target)[0]
            jump = int(count < left)
            if (count + jump + len(literals)) * 4 <= hi - lo:
                break
            count -= 1
        if not count:
            continue
        literal_addresses = {word: lo + (count + jump + i) * 4 for i, word in enumerate(literals)}
        for i in range(count):
            mapped[origin + (offset + i) * 4] = lo + i * 4
        layout.append((lo, hi, offset, count, jump, literals, literal_addresses))
        offset += count
        left -= count
        if not left:
            break
    assert not left, ('Insufficient owned storage', left)
    patches = []
    for lo, hi, offset, count, jump, literals, literal_addresses in layout:
        data = bytearray()
        for i, word in enumerate(words[offset:offset + count]):
            old, new = origin + (offset + i) * 4, lo + i * 4
            if word & 0x0E000000 == 0x0A000000:
                delta = word & 0xFFFFFF
                if delta & 0x800000:
                    delta -= 1 << 24
                target = old + 8 + delta * 4
                target = mapped.get(target, target)
                word = (word & 0xFF000000) | (branch_link(new, target) & 0xFFFFFF)
            elif word & 0x0F7F0000 == 0x051F0000:
                delta = literal_addresses[word] - new - 8
                assert -4095 <= delta <= 4095
                word = (word & ~((1 << 23) | 4095)) | ((1 << 23) if delta >= 0 else 0) | abs(delta)
            data.extend(struct.pack('<I', word))
        if jump:
            target = mapped[origin + (offset + count) * 4]
            data.extend(struct.pack('<I', 0xEA000000 | (branch_link(lo + count * 4, target) & 0xFFFFFF)))
        for value in literals.values():
            data.extend(struct.pack('<I', value))
        patches.append((lo, bytes(data)))
    return patches, mapped


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError('Town stock renderer requires exact V484 ARM9')
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    name_blocks = [(BASE + lo, BASE + hi) for lo, hi in TAILS if hi - lo == 16]
    init = name_blocks.pop(0)[0]
    assembly = Path(__file__).with_suffix('.asm').read_text(encoding='utf-8')
    blob = bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(assembly, ENTRY)[0])
    patches, mapping = scatter(blob, len(blob) - 12, ENTRY,
                               [(ENTRY, 0x01FFC600), (CAPTURE + 24, 0x01FFC71C)] + name_blocks)
    patches += [(CAPTURE, bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(f'''
ldr r2,cache
str r1,[r2,sl,lsl #2]
add r3,sl,#1
str r3,[r2,#20]
bx lr
cache: .word {CACHE}
''', CAPTURE)[0])), (init, bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(f'''
mov sl,#0
ldr r2,[pc,#{CACHE + 24 - init - 12}]
str sl,[r2,#20]
bx lr
''', init)[0]))]
    patches.append((CACHE, bytes(24) + struct.pack('<I', CACHE)))
    assert struct.unpack_from('<I', source, 0xD437C)[0] == 0xE92D4000
    patches.append((TRAMPOLINE, struct.pack('<2I', 0xE92D4000,
                                          0xEA000000 | (branch_link(TRAMPOLINE + 4, 0x020D4380) & 0xFFFFFF))))
    changed = []
    for address, data in patches:
        if address < BASE:
            section, offset = code.sections[4], address - 0x01FFC000
            assert section.data[offset:offset + len(data)] == bytes(len(data))
        else:
            section, offset = code.sections[0], address - BASE
            assert any(BASE + lo <= address < address + len(data) <= BASE + hi
                       for lo, hi in TAILS)
        changed.append({'address': address, 'bytes': len(data),
                        'before_hex': bytes(section.data[offset:offset + len(data)]).hex(),
                        'after_hex': data.hex()})
        section.data[offset:offset + len(data)] = data
    main_section = code.sections[0].data
    for offset, value in ((0xD437C, 0xEA000000 | (branch_link(BASE + 0xD437C, ENTRY) & 0xFFFFFF)),
                          (0xB59AC, branch_link(BASE + 0xB59AC, BASE + 0xD3E44)),
                          (0xB63D4, branch_link(BASE + 0xB63D4, CAPTURE)),
                          (0xB6364, branch_link(BASE + 0xB6364, init)),
                          (0x11A650, 72)):
        changed.append({'address': BASE + offset, 'bytes': 4,
                        'before_hex': bytes(main_section[offset:offset + 4]).hex(),
                        'after_hex': struct.pack('<I', value).hex()})
        struct.pack_into('<I', main_section, offset, value)
    for i in range(5):
        offset = 0x11A73C + i * 28 + 12
        data = bytes(16)
        changed.append({'address': BASE + offset, 'bytes': 16,
                        'before_hex': bytes(main_section[offset:offset + 16]).hex(),
                        'after_hex': data.hex()})
        main_section[offset:offset + 16] = data
    arm = bytes(code.save())
    assert len(arm) == len(source)
    assert all(bytes(code.sections[i].data) == before[i] for i in (1, 2, 3))
    # Byte restoration identifies every change, including reclaimed lazy code.
    restored = [bytearray(s.data) for s in code.sections]
    for row in changed:
        address = row['address']
        section, offset = (4, address - 0x01FFC000) if address < BASE else (0, address - BASE)
        restored[section][offset:offset + row['bytes']] = bytes.fromhex(row['before_hex'])
    assert all(bytes(s) == old for s, old in zip(restored, before))
    # Reclaim only abandoned lazy-allocation instructions, not any current name.
    table = 0x15EF18
    assert bytes(main_section[table:table + 124 * 12]) == before[0][table:table + 124 * 12]
    for index in range(124):
        pointer = struct.unpack_from('<I', before[0], table + index * 12)[0] - BASE
        end = before[0].index(0, pointer) + 1
        assert bytes(main_section[pointer:end]) == before[0][pointer:end]
    plan = {'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(arm),
            'entry': ENTRY, 'capture': CAPTURE, 'initialize': init, 'cache': CACHE, 'trampoline': TRAMPOLINE,
            'changed_ranges': changed, 'instruction_map': mapping,
            'stack_bitmap_size': [96, 16], 'visible_crop_size': [96, 12], 'stack_bytes': 960,
            'no_added_allocation_or_free': True,
            'all124_names_and_metadata_preserved': True,
            'all_autoload_extents_and_other_sections_exact': True,
            'original_screen_selector_field': 100,
            'original_viewport_origin_field': 108,
            'original_destination_origin_field': 60,
            'original_numeric_VRAM_binding_restored': True,
            'changed_records': ['COMMODITY_TOWN_STOCK_RENDERER_WITHOUT_PERSISTENT_HEAP'],
            'full_goal_complete': False}
    return arm, plan


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-town-stock-rows-v1':
        raise ValueError('Unknown town stock renderer configuration')
    if sha(source) != config['source_arm9_sha256']:
        raise ValueError('Town stock renderer source differs')
    assembly = Path(__file__).with_suffix('.asm')
    if sha(assembly.read_bytes()) != config['assembly_sha256']:
        raise ValueError('Town stock renderer assembly differs')
    target, plan = transform(source)
    if sha(target) != config['target_arm9_sha256']:
        raise ValueError('Town stock renderer target differs')
    return target, plan
