"""Regress the reported code overwrite and exercise all eighteen native captions."""

import json
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UcError
from unicorn.arm_const import UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.square_font_scratch_20261027 import propose
from dk4tool.rom.nds import NdsImage
from scripts import verify_square_caption_cells_v483 as caption

ROOT = Path('work/lisbon_square_freeze_20261027')
ROM = Path('out/font_v2_all_punctuation_one_pixel_20261027_test.nds')


def main():
    source = NdsImage.open(ROM).read_file('/__arm9__.bin')
    target, transform = propose(source)
    section = bytes(MainCodeFile(target, 0x02000000).sections[4].data)
    assert GameAsciiFont.from_arm9(source).glyphs == GameAsciiFont.from_arm9(target).glyphs
    failed = None
    try:
        caption.native(source, 'Food Shop')
    except (ValueError, UcError) as error:
        # The exact frozen-state evidence independently establishes the write.
        # Retain the old native failure rather than accepting an arbitrary error.
        failed = str(error)
    assert failed and ('native prompt routine' in failed or 'Invalid memory' in failed), failed

    original_machine = caption.machine
    traces = []

    def observed_machine(arm):
        u = original_machine(arm)
        trace = dict(min_sp=caption.STACK, writes_to_former_static_scratch=[])
        u.mem_write(caption.STACK - 0x10000, b'\xA5' * 64)

        def instruction(uc, address, size, data):
            sp = uc.reg_read(UC_ARM_REG_SP)
            if sp:
                trace['min_sp'] = min(trace['min_sp'], sp)

        def write(uc, access, address, size, value, data):
            if address < 0x01FFC360 and address + size > 0x01FFC1A0:
                trace['writes_to_former_static_scratch'].append([address, size])

        u.hook_add(UC_HOOK_CODE, instruction)
        u.hook_add(UC_HOOK_MEM_WRITE, write)
        traces.append(trace)
        return u

    caption.machine = observed_machine
    font = GameAsciiFont.from_arm9(target)
    cases = []
    try:
        for category, name in enumerate(caption.names(target)):
            text = name + ' Shop'
            pixels, context, u = caption.native(target, text)
            expected = bytearray(64 * 12)
            for index, char in enumerate(text):
                glyph = font.decode(char)
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x, y)):
                            assert index * 5 + x < 64
                            expected[(y + 1) * 64 + index * 5 + x] = 1
            assert pixels == bytes(expected), text
            assert bytes(u.mem_read(0x01FFC000, 4096)) == section
            assert bytes(u.mem_read(caption.STACK - 0x10000, 64)) == b'\xA5' * 64
            assert not traces[-1]['writes_to_former_static_scratch']
            cases.append(dict(category=category, text=text, all768_pixels_exact=True,
                complete_ITCM_unchanged=True, original_view_header_context_and_ABI_pass=True,
                min_stack_pointer=traces[-1]['min_sp'], stack_high_water=caption.STACK - traces[-1]['min_sp']))
        fallbacks = []
        for width, origin in ((48, (0, 0)), (64, (1, 0)), (64, (0, 1)), (80, (0, 0))):
            old_pixels, old_context, _ = caption.native(source, 'Food Shop', width, origin)
            new_pixels, new_context, _ = caption.native(target, 'Food Shop', width, origin)
            assert old_pixels == new_pixels and old_context == new_context
            fallbacks.append(dict(width=width, origin=origin, exact_predecessor_output_and_context=True))
    finally:
        caption.machine = original_machine

    proof = dict(source_ROM_sha256=sha(ROM.read_bytes()), transform=transform,
        reported_predecessor_native_failure=failed, all18_caption_cases=cases,
        original_fallbacks=fallbacks, no_font_or_glyph_stubs=True,
        native_controlled_views_not_actual_GPU_or_earned_gameplay=True)
    (ROOT / 'native_repair_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print('Old Square painter fails; all18 repaired caption masks/ABI/code guards and four fallbacks pass.')


if __name__ == '__main__':
    main()
