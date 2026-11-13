"""Research equipment327 word wrapping after expansion; no prose mutation."""

import json
import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_hook import branch_link
from scripts.probe_common_native_word_wrap import helper_bytes

ROOT = Path('work/analysis/equipment_wrap_v363')
ENTRY, WORDS = 0x01FFC900, 0x01FFCA00


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    image = NdsImage.open('out/all_routes_combined_v360_candidate.nds')
    source = image.read_file('/__arm9__.bin')
    code = MainCodeFile(source, 0x02000000)
    before = [bytes(s.data) for s in code.sections]
    assert code.sections[4].ramAddress == 0x01FFC000
    payload = bytearray(code.sections[4].data)
    assert len(payload) <= 0x900
    payload.extend(bytes(0x900 - len(payload)))
    assembly = """
        ldr r3,[sp,#0xc4]
        ldr r12,=0x020546e8
        cmp r3,r12
        bne original
        ldr r3,[sp,#0xd0]
        ldr r12,=327
        cmp r3,r12
        bne original
        push {r4-r6,lr}
        sub sp,sp,#240
        mov r4,r0
        bl 0x02053914
        mov r0,r4
        mov r1,sp
        bl 0x01ffca00
        cmp r0,#0
        beq done
        add r2,r0,#1
        mov r0,r4
        mov r1,sp
        bl 0x020cec74
    done:
        mov r0,#0
        add sp,sp,#240
        pop {r4-r6,pc}
    original:
        b 0x01ff9ce4
    """
    raw, _ = Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(assembly, ENTRY)
    assert len(raw) <= 0x100
    payload.extend(bytes(raw))
    payload.extend(bytes(0xA00 - len(payload)))
    wrap = bytearray(helper_bytes())
    # Full38-cell source width; continuation guards consume their normal cells.
    replacements = {0xE3A07027: 0xE3A07026, 0xE3A07026: 0xE3A07025,
                    0xE35B0026: 0xE35B0025, 0xE3520026: 0xE3520025}
    changed = []
    for off in range(0, len(wrap), 4):
        old = struct.unpack_from('<I', wrap, off)[0]
        if old in replacements:
            struct.pack_into('<I', wrap, off, replacements[old])
            changed.append({'offset': off, 'before': old, 'after': replacements[old]})
    assert len(changed) == 4
    payload.extend(wrap)
    assert len(payload) <= 0x1000
    field = 0x54798
    assert struct.unpack_from('<I', source, field)[0] == branch_link(0x02000000 + field, 0x01FF9CE4)
    struct.pack_into('<I', code.sections[0].data, field, branch_link(0x02000000 + field, ENTRY))
    code.sections[4].data = payload
    target = bytes(code.save())
    loaded = MainCodeFile(target, 0x02000000)
    assert all(bytes(loaded.sections[i].data) == before[i] for i in (1, 2, 3))
    assert bytes(loaded.sections[4].data[:len(before[4])]) == before[4]
    restored = bytearray(loaded.sections[0].data)
    restored[field:field + 4] = before[0][field:field + 4]
    restored[code.codeSettingsOffs:code.codeSettingsOffs + 12] = before[0][code.codeSettingsOffs:code.codeSettingsOffs + 12]
    assert bytes(restored) == before[0]
    (ROOT / 'research_arm9.bin').write_bytes(target)
    image.replace_file('/__arm9__.bin', target)
    image.save(ROOT / 'research_only_equipment_wrap.nds')
    plan = {'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(target),
            'scope': {'native_parent_return': 0x020546E8, 'native_message_id': 327},
            'macro_call': field, 'wrapper': ENTRY, 'word_helper': WORDS,
            'first_line_cells': 38, 'continuation_cells': 37, 'helper_limit_changes': changed,
            'all_prose_names_controls_metadata_and_previous_payload_bytes_preserved': True,
            'all_other_messages_tail_call_original_scoped_wrapper': True,
            'native_and_actual_verification_pending': True, 'not_for_handoff': True}
    (ROOT / 'plan.json').write_text(json.dumps(plan, indent=2) + '\n')
    print('Prepared scoped equipment327 wrapper; unrelated messages retain the original wrapper/frame.')


if __name__ == '__main__':
    main()
