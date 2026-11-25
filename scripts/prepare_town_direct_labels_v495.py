"""Research stack bitmap composition; preserves the V484 production ROM."""

import json
import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_hook import branch_link

ROOT = Path('work/analysis/town_direct_labels_v495')
PARENT = Path('out/all_routes_combined_v484_candidate.nds')
BASE, ENTRY, CAPTURE, CACHE = 0x02000000, 0x01FFC504, 0x01FFC6AC, 0x0215DC24
TRAMPOLINE = 0x0215BB60


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


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    parent = NdsImage.open(PARENT)
    source = parent.read_file('/__arm9__.bin')
    assert sha(source) == 'b03327187284a6ac560bf76ff442d75f9caa34c6b130438b582a44f2baf37c5b'
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    tails = json.loads(Path('work/analysis/commodity_lazy_canvas_v349/plan.json').read_text())['owned_tail_blocks']
    name_blocks = [(BASE + lo, BASE + hi) for lo, hi, count in tails if hi - lo == 16]
    init = name_blocks.pop(0)[0]
    assembly = Path('work/town_direct_labels_v495.asm').read_text()
    blob = bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(assembly, ENTRY)[0])
    patches, mapping = scatter(blob, len(blob) - 16, ENTRY,
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
    assert struct.unpack_from('<I', source, 0xD470C)[0] == 0xE92D40F0
    patches.append((TRAMPOLINE, struct.pack('<2I', 0xE92D40F0,
                                          0xEA000000 | (branch_link(TRAMPOLINE + 4, 0x020D4710) & 0xFFFFFF))))
    changed = []
    for address, data in patches:
        if address < BASE:
            section, offset = code.sections[4], address - 0x01FFC000
            assert section.data[offset:offset + len(data)] == bytes(len(data))
        else:
            section, offset = code.sections[0], address - BASE
            assert any(BASE + lo <= address < address + len(data) <= BASE + hi
                       for lo, hi, count in tails)
        changed.append({'address': address, 'bytes': len(data),
                        'before_hex': bytes(section.data[offset:offset + len(data)]).hex(),
                        'after_hex': data.hex()})
        section.data[offset:offset + len(data)] = data
    main_section = code.sections[0].data
    for offset, value in ((0xD470C, 0xEA000000 | (branch_link(BASE + 0xD470C, ENTRY) & 0xFFFFFF)),
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
    (ROOT / 'research_arm9.bin').write_bytes(arm)
    (ROOT / 'draw.asm').write_text(assembly)
    plan = {'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(arm),
            'entry': ENTRY, 'capture': CAPTURE, 'initialize': init, 'cache': CACHE, 'trampoline': TRAMPOLINE,
            'changed_ranges': changed, 'instruction_map': mapping,
            'stack_bitmap_size': [96, 12], 'stack_bytes': 832,
            'no_added_allocation_or_free': True, 'not_for_handoff': True}
    (ROOT / 'runtime_plan.json').write_text(json.dumps(plan, indent=2) + '\n')
    for variant in ('normal', 'm28'):
        rom = NdsImage.open(PARENT)
        rom.replace_file('/__arm9__.bin', arm)
        if variant == 'm28':
            rom.replace_file('/FLS/M20.fls', parent.read_file('/FLS/M28.fls'))
        path = ROOT / f'research_only_direct_{variant}.nds'
        rom.save(path)
        manifest = {'research_only': True, 'parent': str(PARENT),
                    'parent_sha256': sha(PARENT.read_bytes()), 'research_ROM': str(path),
                    'research_ROM_sha256': sha(path.read_bytes()),
                    'no_added_allocation_or_free': True,
                    'M20_replaced_with_M28': variant == 'm28', 'not_for_handoff': True}
        (ROOT / f'{variant}_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Prepared stack-based direct town labels in unchanged section extents.')


if __name__ == '__main__':
    main()
