"""Source-bound Refit crop diagnosis, owned layout and bounded native lifetimes."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
)

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.refit_help import compile_paragraph
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_help_layout import BASE, CLEANUP, INIT_END, INIT_START, transform
from dk4tool.rom.nds import NdsImage
from scripts.finish_refit_display_v708 import load
from scripts.probe_button_prompt_native import STOP, call, machine
from scripts.run_room_gender_v694 import CAP
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/refit_help_v710')
ROM = Path('out/all_routes_combined_v708_candidate.nds')
PIXELS, TEXT = 0x02450020, 0x02440020


def make(raw, target, proof):
    u = machine(target)
    u.mem_write(BASE, raw)
    for lo, hi in proof['owned_spans']:
        u.mem_write(BASE + lo, target[lo:hi])
    return u


def main():
    ROOT.mkdir(exist_ok=True)
    assert not (ROOT / 'native_layout_proof.json').exists()
    source = NdsImage.open(ROM).read_file('/__arm9__.bin')
    target, layout = transform(source)
    (ROOT / 'target_ARM9.bin').write_bytes(target)
    save(ROOT / 'layout_plan.json', layout)
    events = read(CAP / 'refit_help_v709_all_consumers/observer/events.json')
    assert not events['errors'] and not events['mismatches'] and events['all_host_slots_restored']
    row = events['rows'][0]
    raw = Path(row['RAM']).read_bytes()
    assert sha(raw) == row['RAM_sha256']
    # This supplied allocator is an isolated native instruction/lifetime test.
    # Actual allocation and full constructor entry are verified separately in ROM.
    u = make(raw, target, layout)
    requests = []
    def bridge(uc, pc, size, data):
        if pc == 0x02005148:
            requests.append(('allocate', uc.reg_read(UC_ARM_REG_R0)))
            assert requests[-1][1] == 9072
            uc.reg_write(UC_ARM_REG_R0, PIXELS)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif pc == BASE + INIT_END:
            uc.reg_write(UC_ARM_REG_PC, STOP)
        elif pc == 0x02005180:
            requests.append(('free', uc.reg_read(UC_ARM_REG_R0)))
            assert requests[-1][1] == PIXELS
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
    u.hook_add(UC_HOOK_CODE, bridge)
    parent, surface = 0x0218F790, 0x0218F7A0
    u.reg_write(UC_ARM_REG_R4, 1)
    u.reg_write(UC_ARM_REG_R5, parent)
    u.emu_start(BASE + INIT_START, STOP, count=10000)
    assert u.reg_read(UC_ARM_REG_PC) == STOP
    header = parent + 0x1C38
    assert struct.unpack('<3I', u.mem_read(header, 12)) == (4, 42, 108)
    assert (header + struct.unpack('<I', u.mem_read(header + 16, 4))[0]) & 0xFFFFFFFF == PIXELS
    assert struct.unpack('<2I', u.mem_read(surface + 40, 8)) == (168, 108)
    palette = (header + struct.unpack('<I', u.mem_read(header + 12, 4))[0]) & 0xFFFFFFFF
    assert palette == struct.unpack_from('<I', source, 0x19FFC)[0]
    context = row['R0_context']
    u.mem_write(context + 16, struct.pack('<I', 108))
    prepared = bytes(u.mem_read(BASE, 0x400000))
    font = GameAsciiFont.from_arm9(target)
    records = read('translations/refit_help_manuscript_v2.json')['records']
    results = []
    for record in records:
        u.mem_write(BASE, prepared)
        u.mem_write(PIXELS - 16, b'\xA5' * (9072 + 32))
        u.mem_write(PIXELS, bytes(9072))
        text, lines = compile_paragraph(record['english'])
        u.mem_write(TEXT - 16, b'\x5A' * (len(text) + 32))
        u.mem_write(TEXT, text)
        before = bytes(u.mem_read(BASE, 0x400000))
        call(u, 0xD5404, (context, TEXT), instruction_limit=1000000)
        after = bytes(u.mem_read(BASE, 0x400000))
        changed = [BASE + i for i, (a, b) in enumerate(zip(before, after)) if a != b]
        assert all(context <= a < context + 72 for a in changed)
        pixels = bytes(u.mem_read(PIXELS, 9072))
        actual = bytes(n for value in pixels for n in (value & 15, value >> 4))
        expected = bytearray(168 * 108)
        for line_index, line in enumerate(lines):
            for i, char in enumerate(line):
                for y in range(11):
                    for x in range(6):
                        if font.decode(char).getpixel((x, y)):
                            expected[(line_index * 12 + y) * 168 + i * 6 + x] = 1
        assert actual == expected and all(v == 0 for v in actual[60 * 168:])
        assert bytes(u.mem_read(PIXELS - 16, 16)) == bytes(u.mem_read(PIXELS + 9072, 16)) == b'\xA5' * 16
        assert bytes(u.mem_read(TEXT - 16, 16)) == bytes(u.mem_read(TEXT + len(text), 16)) == b'\x5A' * 16
        assert bytes(u.mem_read(TEXT, len(text))) == text
        results.append({'message_id': record['message_id'], 'English': record['english'],
            'lines': lines, 'full168x108_indices_sha256': sha(actual),
            'all_body_glyphs_fit_first60_rows_heading_and_three_detail_rows_unmodified': True,
            'full_RAM_changes_only_context_pixel_and_text_guards_exact': True})
    u.mem_write(BASE, prepared)
    call(u, CLEANUP - BASE, (surface,))
    assert struct.unpack('<I', u.mem_read(surface + 16, 4))[0] == 0
    call(u, CLEANUP - BASE, (surface,))
    assert requests == [('allocate', 9072), ('free', PIXELS)]
    # Independently finish the already-terminal ordinary New Game comparison.
    pre = read('work/analysis/refit_help_v708/preflight.json')
    _, shots, receipt = load(CAP / 'refit_help_v708_newgame', sha(ROM.read_bytes()), 31000)
    _, old, old_receipt = load(CAP / 'refit_help_v706_newgame_control', pre['candidate_sha256'], 31000)
    assert shots.keys() == old.keys() and len(shots) == 49
    assert all(shots[f].tobytes() == old[f].tobytes() for f in shots)
    save(ROOT / 'native_layout_proof.json', {'layout': layout, 'actual_V709_consumer_events':
        str(CAP / 'refit_help_v709_all_consumers/observer/events.json'),
        '31_complete168x108_native_fonts': results, 'native_pixels_compared': 31 * 168 * 108,
        'isolated_allocator_bridge_requests': requests,
        'native_initializer_header_palette_dimensions_and_both_cleanup_calls_pass': True,
        'heap_bridge_is_not_actual_allocator_or_whole_constructor_proof': True,
        'previous_V708_all49_New_Game_full_RGB_pairs_pass': [receipt, old_receipt],
        'previous_goal_turn_classification': 'no progress: user status answer only; resumed safe crop/lifetime investigation',
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    config = {'format': 'dk4-refit-help-layout-v1', 'proof': layout, 'dependencies': {
        str(ROOT / 'native_layout_proof.json'): sha((ROOT / 'native_layout_proof.json').read_bytes()),
        'dk4tool/patch/refit_help_layout.py': sha(Path('dk4tool/patch/refit_help_layout.py').read_bytes())}}
    save('translations/refit_help_layout_v1.json', config)
    print('V710 crop cause pinned;31 native full expanded bitmaps and bounded init/free pass;V708 all49 New Game RGB pairs exact.', flush=True)


if __name__ == '__main__':
    main()
