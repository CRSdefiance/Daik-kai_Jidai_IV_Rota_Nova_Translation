"""Research scoped market word wrapping in an explicitly declared ITCM section."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_hook import branch_link

BASE, ENTRY = 0x02000000, 0x01FFC000
ROOT = Path('work/analysis/commodity_market_v352')


def helper(source):
    words, labels, branches = [], {}, []

    def emit(word):
        words.append(word)

    def mark(label):
        labels[label] = len(words)

    def branch(label, condition=14):
        branches.append((len(words), label, condition))
        emit(0)

    emit(0xE92D4070)  # Preserve r4-r6/lr, aligned stack.
    emit(0xE1A04000)
    emit(0xE1A05001)
    emit(0xE1A06001)
    emit(0xE3A02000)
    emit(0xE3A03000)
    mark('scan')
    emit(0xE4D6C001)
    emit(0xE35C000A)
    branch('finish', 0)
    emit(0xE35C0000)
    branch('finish', 0)
    emit(0xE35C0020)
    emit(0x0352000E)  # Only spaces at/before character14 are candidates.
    emit(0x92463001)
    emit(0xE2822001)
    branch('scan')
    mark('finish')
    emit(0xE352000E)
    emit(0xE3A0000C)
    emit(0x83A00018)
    emit(0x83530000)
    emit(0x83A0C00A)
    emit(0x85C3C000)
    # The Local mirror is the adjacent, source-locked72-pixel bitmap/view.
    # Short names keep the original12-pixel view; longer names use24 pixels.
    emit(0xE594102C)
    emit(0xE2811074)
    emit(0xE581002C)
    emit(0xE5810040)
    emit(0xE5912068)
    emit(0xE0822000)
    emit(0xE5812070)
    # Compact text leaves narrower cells than the original six-pixel painter.
    # Clear this owned source view before repainting to remove old wider glyphs.
    emit(0xE594002C)
    emit(branch_link(ENTRY + len(words) * 4, BASE + 0xD393C))
    emit(0xE5946000)
    font_load = len(words)
    emit(0)
    emit(0xE5842000)
    emit(0xE1A00004)
    emit(0xE1A01005)
    emit(branch_link(ENTRY + len(words) * 4, BASE + 0x15BB40))
    emit(0xE5846000)
    emit(0xE8BD8070)
    literal_at = len(words)
    emit(ENTRY + 0xB0)
    words[font_load] = 0xE59F2000 | (literal_at - font_load - 2) * 4
    for at, label, condition in branches:
        words[at] = condition << 28 | 0x0A000000 | ((labels[label] - at - 2) & 0xFFFFFF)
    payload = bytearray(struct.pack('<' + 'I' * len(words), *words))
    assert len(payload) <= 0xB0
    payload.extend(bytes(0xB0 - len(payload)))
    callbacks = list(struct.unpack_from('<9I', source, 0x1603E4))
    assert callbacks[7] == BASE + 0xD501C
    # The native compact dispatch identifies this callback by its low byte1C.
    single = ENTRY + 0x11C
    callbacks[7] = single
    payload.extend(struct.pack('<9I', *callbacks))
    payload.extend(bytes(0x11C - len(payload)))
    wrapper = [0xE92D4070, 0xE24DD010, 0xE1A04000, 0xE1A05001, 0xE1A06002,
               0xE594102C, 0xE5913000, 0xE5933008, 0xE1A0000D, 0xE12FFF33,
               0xE59D0000, 0xE5951000, 0xE0800001, 0xE58D0008,
               0xE59D0004, 0xE5951004, 0xE0800001, 0xE58D000C,
               0xE1A00004, 0xE28D1008, 0xE1A02006,
               branch_link(single + 84, BASE + 0xD501C),
               0xE28DD010, 0xE8BD8070]
    payload.extend(struct.pack('<24I', *wrapper))
    return bytes(payload)


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    source = Path('work/analysis/commodity_lazy_canvas_v349/research_arm9.bin').read_bytes()
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    rom = NdsImage.open('out/all_routes_combined_v342_candidate.nds')
    overlays = loadOverlayTable(rom.rom.arm9OverlayTable, lambda oid, fid: rom.files[fid])
    payload = helper(source)
    assert len(payload) <= 512 and ENTRY % 32 == 0
    for s in code.sections:
        assert ENTRY + len(payload) <= s.ramAddress or s.ramAddress + len(s.data) + s.bssSize <= ENTRY
    for s in overlays.values():
        assert ENTRY + len(payload) <= s.ramAddress or s.ramAddress + len(s.data) + s.bssSize <= ENTRY
    # Explicit SDK autoload allocation: no zero-filled ROM bytes are repurposed.
    # The original ITCM section and overlay0 stay byte-exact.
    code.sections.append(MainCodeFile.Section(payload, ENTRY, 0))
    fields = [0xC3E1C, 0xC3F98]
    for field in fields:
        assert struct.unpack_from('<I', before[0], field)[0] == branch_link(BASE + field, BASE + 0xD5404)
        struct.pack_into('<I', code.sections[0].data, field, branch_link(BASE + field, ENTRY))
    target = bytes(code.save())
    loaded = MainCodeFile(target, BASE)
    assert len(loaded.sections) == 5 and bytes(loaded.sections[4].data) == payload
    for i in (1, 2, 3):
        assert bytes(loaded.sections[i].data) == before[i]
    restored = bytearray(loaded.sections[0].data)
    for field in fields:
        restored[field:field + 4] = before[0][field:field + 4]
    restored[code.codeSettingsOffs:code.codeSettingsOffs + 12] = before[0][code.codeSettingsOffs:code.codeSettingsOffs + 12]
    assert bytes(restored) == before[0]
    assert target[0xE45DC:0xE45E0] == source[0xE45DC:0xE45E0]
    (ROOT / 'research_arm9.bin').write_bytes(target)
    for variant in ['normal', 'long']:
        original_fixture = NdsImage.open('work/analysis/commodity_lazy_canvas_v349/research_only_' + variant + '_Maria.nds')
        original_arm = original_fixture.read_file('/__arm9__.bin')
        fixture = bytearray(target)
        fixture[0x9F068] = original_arm[0x9F068]
        for index in (42, 51, 62):
            field = 0x15EF18 + index * 12
            fixture[field:field + 4] = original_arm[field:field + 4]
        original_fixture.replace_file('/__arm9__.bin', bytes(fixture))
        original_fixture.save(ROOT / ('research_only_' + variant + '_Maria.nds'))
    plan = {'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(target),
            'helper': ENTRY, 'helper_size': len(payload), 'helper_bytes': payload.hex(),
            'scoped_calls': fields, 'old_sections_and_overlay_bytes_preserved': True,
            'arena_and_heap_bounds_unchanged': True, 'name_and_trade_metadata_unchanged': True,
            'new_ITCM_allocation': [ENTRY, ENTRY + len(payload)],
            'declared_native_overlay_spans': [[s.ramAddress, s.ramAddress + len(s.data) + s.bssSize] for s in overlays.values()],
            'native_and_actual_allocation_verification_pending': True, 'not_for_handoff': True}
    (ROOT / 'plan.json').write_text(json.dumps(plan, indent=2) + '\n')
    print('Prepared scoped market formatter; explicit new ITCM autoload section requires native/cold-boot verification.')


if __name__ == '__main__':
    main()
