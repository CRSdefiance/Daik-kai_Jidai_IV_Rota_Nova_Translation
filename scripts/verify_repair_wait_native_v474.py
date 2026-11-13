"""Exhaustive dispatch scope and complete native repair-message word rendering."""

import json
import struct
from pathlib import Path

from PIL import Image
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R3, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.repair_wait_wrap import ACTIVE, transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_button_prompt_native import STACK, machine
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_tavern_addresses_v413 import wrap

ROOT = Path('work/analysis/repair_wait_v474')
PARENT = Path('out/all_routes_combined_v468_candidate.nds')


def scope(arm, parent, number):
    u = machine(arm)
    u.mem_write(STACK + 0x264, struct.pack('<I', parent))
    u.mem_write(STACK + 0x274, struct.pack('<I', number))
    u.reg_write(UC_ARM_REG_SP, STACK)

    def stop(uc, address, size, data):
        if address in (ACTIVE, 0x01FF9EDC):
            uc.emu_stop()

    handle = u.hook_add(UC_HOOK_CODE, stop)
    try:
        u.emu_start(0x01FFCF3C, 0x01FFD000, count=100)
    finally:
        u.hook_del(handle)
    assert u.reg_read(UC_ARM_REG_SP) == STACK
    return u.reg_read(UC_ARM_REG_PC), u.reg_read(UC_ARM_REG_R3)


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open(PARENT)
    old = rom.read_file('/__arm9__.bin')
    arm, change = transform(old)
    entries = common_message_entries(rom.read_file('/COMMON/MESFILE.DK4'), arm, clean=False)
    text = entries[801].text
    clean = NdsImage.open('work/clean.nds')
    source = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))[801]
    assert source.text.decode('cp932') == '修理が終わるまで\n１日待ってくんな'
    assert text == b"Repairs will take one day. Please wait until they're finished."
    scope_cases = []
    # Execute the dispatch in both binaries for every real native message ID.
    for parent in (0x02054014, 0x02054044):
        for number in range(3668):
            a, b = scope(old, parent, number), scope(arm, parent, number)
            if parent == 0x02054014 and number == 801:
                assert a[0] == 0x01FF9EDC and b[0] == ACTIVE
            else:
                assert a == b, (parent, number, a, b)
        scope_cases.append({'parent': parent, 'all3668_dispatches_executed': True})
    formatted = wrap(arm, text, 0x02054014, 801)
    assert b' '.join(formatted.split()) == text
    events = []
    pixels = raster(arm, formatted, 0x01FFCE40 - 0x02000000,
                    size=(228, 80), instruction_limit=400000, glyph_events=events)
    visible = [e for e in events if e['code'] != 32]
    assert [e['code'] for e in visible] == [ord(c) for c in text.decode() if c != ' ']
    offset = 0
    for word in text.decode().split():
        group = visible[offset:offset + len(word)]
        assert len({e['y'] for e in group}) == 1, word
        offset += len(word)
    picture = Image.frombytes('L', (228, 80), bytes(0 if p else 255 for p in pixels))
    picture.save(ROOT / 'repair_native_preview.png')
    raw = b'A complete sentence with enough words to exercise the previous rumor, clue, equipment and Guild wrapping.'
    cases = []
    for parent in (0x02054014, 0x02054044, 0x020546E8):
        for number in (800, 802, 803, 820, 821, 870, 871, 872, 873, 321, 327, 3648, 3665, 3667):
            assert wrap(old, raw, parent, number) == wrap(arm, raw, parent, number)
            cases.append({'parent': parent, 'message_id': number, 'complete_old_wrap_behavior_exact': True})
    proof = {'parent_candidate_sha256': sha(PARENT.read_bytes()), 'target_arm9_sha256': sha(arm),
             'change': change, 'all7336_native_dispatch_comparisons': scope_cases,
             'only801_in_original_portrait_parent_added': True,
             'source_Japanese': source.text.decode('cp932'), 'English_unchanged': text.decode(),
             'native_lines': [s.decode() for s in formatted.split(b'\n')],
             'all_glyph_order_and_every_word_on_single_row': True,
             'complete_native_ink_pixels': sum(bool(p) for p in pixels),
             '42_old_full_wrapper_cases_exact': cases,
             'actual_registered_ROM_playback_pending': True, 'full_goal_complete': False}
    (ROOT / 'native_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('7336 native dispatch comparisons;all repair words/glyphs;42 old complete wrapper cases pass.')


if __name__ == '__main__':
    main()
