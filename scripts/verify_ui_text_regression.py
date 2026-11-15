"""Candidate-specific native ASCII regression suite; never builds a ROM.

The isolated CPU fixtures verify drawing/ABI/storage contracts, not GPU output,
natural screen reachability, earned progression or hardware compatibility.
"""
import argparse
import hashlib
import json
import struct
import sys
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO), str(REPO / '.deps'), str(REPO / '.runtime_deps')]

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.ascii_glyph_right_bounds import propose
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import machine, call, STACK
from scripts.verify_ascii_glyph_right_bounds import verify as existing_bounds
from scripts import verify_font_offset_one_native_20261027 as footer_checks
from scripts import verify_square_caption_cells_v483 as square_checks

BASE = 0x02000000
HEADER = 0x02450000
POINT, TEXT = 0x02460000, 0x02461000
TYPES = ['Square', 'Market', 'Yard', 'Port', 'Tavern', 'Guild', 'Palace', 'Govt',
         'Inn', 'Ruins', 'Church', 'Gate']


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def helper_bytes(arm):
    section = MainCodeFile(arm, BASE).sections[4]
    require(section.ramAddress == 0x01FFC000 and len(section.data) == 4096, 'Helper ownership differs')
    return bytes(section.data)


def expected_paint(font, initial, mode, width, height, draws, color):
    """Independent pixel oracle. Pitched widths use pixels, not packed bytes."""
    result = bytearray(initial)
    stride = width // 2 if mode == 4 else width * 2
    for text, origin_x, origin_y, style in draws:
        for index, character in enumerate(text):
            glyph = font.decode(character)
            for gy in range(11):
                py = origin_y + 1 + gy
                if py >= height:
                    continue
                for gx in range(6):
                    px = origin_x + index * 6 + gx
                    if px >= width:
                        continue
                    ink = bool(glyph.getpixel((gx, gy)))
                    if mode == 16:
                        if ink:
                            struct.pack_into('<H', result, py * stride + px * 2, color)
                    else:
                        at, shift = py * stride + px // 2, px % 2 * 4
                        result[at] = result[at] & ~(15 << shift) | ((style if ink else 0) << shift)
    return bytes(result)


def extended_bounds(arm):
    font, cpu = GameAsciiFont.from_arm9(arm), machine(arm)
    palette = struct.unpack_from('<I', arm, 0xD181C)[0] - BASE
    color = struct.unpack_from('<H', arm, palette + 2)[0]
    section = helper_bytes(arm)
    cases = []

    def case(mode, width, height, x, y, text, glyph=False, before=False):
        pitch = width // 4 if mode == 4 else width
        size = width * height // 2 if mode == 4 else width * height * 2
        pixel_at = HEADER - size if before else HEADER + 20
        low, high = min(pixel_at, HEADER), max(pixel_at + size, HEADER + 20)
        raw = struct.pack('<5I', mode, pitch, height, 0x2000, (pixel_at - HEADER) & 0xFFFFFFFF)
        cpu.mem_write(low - 32, b'\xA5' * (high - low + 64))
        cpu.mem_write(HEADER, raw)
        initial = b'\x99' * size
        cpu.mem_write(pixel_at, initial)
        cpu.mem_write(TEXT, text.encode('ascii') + b'\0')
        source_string = bytes(cpu.mem_read(TEXT, len(text) + 1))
        if glyph:
            cpu.mem_write(STACK, struct.pack('<2I', ord(text), 1))
            call(cpu, 0xD16B4, (0, HEADER, x, y))
        else:
            cpu.mem_write(POINT, struct.pack('<2I', x, y))
            cpu.mem_write(STACK, struct.pack('<I', 1))
            call(cpu, 0xD1604, (0, HEADER, POINT, TEXT))
        expected = expected_paint(font, initial, mode, width, height, [(text, x, y, 1)], color)
        label = (mode, width, height, x, y, text, glyph, before)
        require(bytes(cpu.mem_read(pixel_at, size)) == expected, ('Pixels differ', label))
        require(bytes(cpu.mem_read(HEADER, 20)) == raw, ('Header changed', label))
        require(bytes(cpu.mem_read(low - 32, 32)) == b'\xA5' * 32, ('Leading guard', label))
        require(bytes(cpu.mem_read(high, 32)) == b'\xA5' * 32, ('Trailing guard', label))
        require(bytes(cpu.mem_read(TEXT, len(text) + 1)) == source_string, ('Input changed', label))
        require(bytes(cpu.mem_read(0x01FFC000, 4096)) == section, ('Helper overwritten', label))
        cases.append(dict(mode=mode, width=width, height=height, x=x, y=y, text=text,
                          single_glyph=glyph, pixels_before_header=before,
                          complete_expected_pixels_and_metadata_and_canaries=True))

    # All printable ASCII in a full cell and at the partial right/bottom edge.
    for mode in [4, 16]:
        for code in range(32, 127):
            for x, y in [(0, 0), (33, 0), (35, 1), (0, 11)]:
                case(mode, 36, 12, x, y, chr(code), glyph=True)
        widths = [4, 8, 12, 32, 36, 64, 256] if mode == 4 else [1, 3, 6, 7, 12, 36, 64, 256]
        for width in widths:
            for height in [0, 1, 11, 12, 14]:
                for x in sorted(set([0, max(0, width - 6), max(0, width - 3), width - 1, width, width + 1])):
                    for y in [0, max(0, height - 2), height]:
                        for text in ['g', ' ']:
                            case(mode, width, height, x, y, text, glyph=True)
        # Full string entry point: odd/even lengths and full/partial/no capacity.
        for width in [12, 36, 64, 256]:
            capacity = width // 6
            lengths = sorted(set([0, 1, 2, 5, 6, 7, max(0, capacity - 1), capacity, capacity + 1]))
            for length in lengths:
                text = ('Ggyp []_9!?' * 30)[:length]
                for x in [0, 3, width]:
                    for height in [12, 14]:
                        case(mode, width, height, x, 0, text, before=True)
    return dict(count=len(cases), cases=cases, all_printable_ASCII=True,
                unsupported_negative_coordinates_not_claimed=True,
                isolated_low_level_clipping_does_not_certify_long_UI_labels_fit=True)


def facilities(arm, source, root, out):
    ram_path = root / 'observed_hover2/observer/Guild_before_ram.bin'
    native = root / 'native_trace/capture_native_state_004700'
    ram, itcm = ram_path.read_bytes(), (native / 'arm9_itcm.bin').read_bytes()
    dtcm = (native / 'arm9_dtcm.bin').read_bytes()
    state = json.loads((native / 'native_state.json').read_text())
    section, font = helper_bytes(arm), GameAsciiFont.from_arm9(arm)
    fixed_itcm = bytearray(itcm)
    fixed_itcm[0x4000:0x5000] = section
    fixed_itcm[0x42D8:0x42DC] = itcm[0x42D8:0x42DC]
    ui, caption = 0x021922A4, 0x02192AC0
    rows, reuse, negatives = [], [], []

    def initialized(image, fixed):
        cpu = machine(image)
        cpu.mem_write(BASE, ram)
        cpu.mem_write(0x01FF8000, bytes(fixed_itcm) if fixed else itcm)
        cpu.mem_write(state['DTCM_region'], dtcm)
        if fixed:
            # Captured mutable UI stays intact; only the two main-RAM runtime
            # instruction replacements are installed from the candidate itself.
            for at in [0xD1738, 0xD17F4]:
                cpu.mem_write(BASE + at, image[at:at + 4])
        return cpu

    for variant in [0, 1]:
        cpu = initialized(arm, True)
        cpu.mem_write(ui + 0x894, struct.pack('<I', variant))
        events = []

        def glyph(u, address, size, _):
            code, style = struct.unpack('<2I', u.mem_read(u.reg_read(UC_ARM_REG_SP), 8))
            events.append((chr(code), u.reg_read(UC_ARM_REG_R2), u.reg_read(UC_ARM_REG_R3), style))

        cpu.hook_add(UC_HOOK_CODE, glyph, begin=BASE + 0xD16B4, end=BASE + 0xD16B4)
        # One initialized owner is reused without restoring its RAM between calls.
        selections = list(range(12)) + [5, 1, 0, 8, 2, 5] * 20
        for step, index in enumerate(selections):
            header = struct.unpack('<I', cpu.mem_read(caption + 16, 4))[0]
            raw = bytes(cpu.mem_read(header, 20))
            mode, pitch, height, _, displacement = struct.unpack('<5I', raw)
            require((mode, pitch, height) == (4, 9, 12), 'Facility geometry changed')
            pixels = (header + displacement) & 0xFFFFFFFF
            events.clear()
            call(cpu, 0xB8014, (ui, index), instruction_limit=500000)
            pointer = struct.unpack('<I', cpu.mem_read(caption + 48, 4))[0]
            actual = bytes(cpu.mem_read(pointer, 32)).split(b'\0')[0].decode('ascii')
            require(actual == TYPES[index], ('Wrong facility', index, actual))
            require(''.join(e[0] for e in events).rstrip(' ') == actual, 'Lost facility character')
            expected = bytearray(216)
            for character, x0, y0, style in events:
                glyph_pixels = font.decode(character)
                require(style == 15 and y0 == 0, 'Unexpected facility font placement')
                # All actual letters must fit. Only synthetic blank cells may clip.
                if character != ' ':
                    require(x0 + 6 <= 36, ('Visible facility cell clipped', actual))
                for y in range(11):
                    for x in range(max(0, min(6, 36 - x0))):
                        px, py = x0 + x, y + 1
                        if glyph_pixels.getpixel((x, y)):
                            at, shift = py * 18 + px // 2, px % 2 * 4
                            expected[at] |= style << shift
            require(bytes(cpu.mem_read(pixels, 216)) == expected, ('Stale/incorrect facility pixels', actual, step))
            require(bytes(cpu.mem_read(header, 20)) == raw, ('Facility header overwritten', actual))
            helper = bytearray(cpu.mem_read(0x01FFC000, 4096))
            helper[0x2D8:0x2DC] = section[0x2D8:0x2DC]
            require(helper == section, 'Facility overwrote immutable helpers')
            record = dict(variant=variant, step=step, label=actual, complete_pixels=True,
                          header_and_helpers_intact=True)
            (rows if step < 12 else reuse).append(record)
        for index in [5, 9]:
            old = initialized(source, False)
            old.mem_write(ui + 0x894, struct.pack('<I', variant))
            header = struct.unpack('<I', old.mem_read(caption + 16, 4))[0]
            before = bytes(old.mem_read(header, 20))
            call(old, 0xB8014, (ui, index), instruction_limit=500000)
            after = bytes(old.mem_read(header, 20))
            require(after != before and struct.unpack_from('<I', after)[0] == 0, 'Negative control failed to fail')
            negatives.append(dict(variant=variant, label=TYPES[index], detected_header_corruption=True))
    return dict(all_types=rows, reuse_calls=reuse, reuse_cycles_per_layout=20,
                negative_controls=negatives, fixture_RAM_sha256=sha(ram), fixture_ITCM_sha256=sha(itcm),
                fixture_DTCM_sha256=sha(dtcm), fixture_root=str(root.resolve()),
                native_initialized_UI_only=True, actual_screen_transitions_tested=False)


def square(arm):
    font, section, cases = GameAsciiFont.from_arm9(arm), helper_bytes(arm), []
    for index, name in enumerate(square_checks.names(arm)):
        text = name + ' Shop'
        pixels, context, cpu = square_checks.native(arm, text)
        expected = bytearray(64 * 12)
        for i, character in enumerate(text):
            g = font.decode(character)
            for y in range(11):
                for x in range(6):
                    if g.getpixel((x, y)):
                        require(i * 5 + x < 64, ('Shop clipped', text))
                        expected[(y + 1) * 64 + i * 5 + x] = 1
        require(pixels == expected, ('Shop pixels differ', text))
        require(bytes(cpu.mem_read(0x01FFC000, 4096)) == section, 'Shop overwrote helper')
        cases.append(dict(category=index, text=text, complete_pixels_and_helpers=True))
    return cases


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rom', type=Path, required=True)
    p.add_argument('--expect-sha256', required=True)
    p.add_argument('--reference', type=Path, default=Path('out/all_routes_combined_v8865_candidate.nds'))
    p.add_argument('--fixture-root', type=Path, default=Path('../tmp/lisbon_office_fix'))
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    if args.out.exists():
        p.error('Use a fresh output folder')
    args.out.mkdir(parents=True)
    digest = sha(args.rom.read_bytes())
    require(digest == args.expect_sha256, 'Candidate ROM hash differs')
    arm = NdsImage.open(args.rom).read_file('/__arm9__.bin')
    source = NdsImage.open(args.reference).read_file('/__arm9__.bin')
    compiled, _ = propose(source)
    # This suite currently binds its captured initialized UI to the exact repaired
    # V8865 runtime. A future candidate must explicitly requalify that fixture.
    require(compiled == arm, 'Candidate ARM9 differs from qualified runtime; requalify captured fixtures')
    identity = dict(ROM=str(args.rom.resolve()), ROM_sha256=digest, ARM9_sha256=sha(arm),
                    reference=str(args.reference.resolve()), reference_sha256=sha(args.reference.read_bytes()),
                    native_CPU_tests=True, hardware_verification=False,
                    script_sha256=sha(Path(__file__).read_bytes()))
    write(args.out / 'identity.json', identity)
    result = dict(identity=identity, groups={}, status='running')
    for name, run in [
        ('existing_1728_bounds', lambda: existing_bounds(source, arm)),
        ('extended_bounds_and_strings', lambda: extended_bounds(arm)),
        ('all_facilities_and_reuse', lambda: facilities(arm, source, args.fixture_root, args.out)),
        ('square_captions', lambda: square(arm)),
        ('existing_128_vertical_bounds', lambda: footer_checks.glyph_bounds(arm)),
    ]:
        print('Running', name, flush=True)
        try:
            data = run()
            write(args.out / (name + '.json'), data)
            result['groups'][name] = dict(status='passed', proof=name + '.json')
        except Exception as error:
            result['status'] = 'failed'
            result['groups'][name] = dict(status='failed', error=repr(error))
            write(args.out / 'summary.json', result)
            raise
        write(args.out / 'summary.json', result)
    footer_checks.ROOT = args.out
    footer = footer_checks.footer(arm)
    write(args.out / 'footer.json', footer)
    result['groups']['footer'] = dict(status='passed', proof='footer.json')
    result['status'] = 'passed'
    write(args.out / 'summary.json', result)
    print('All candidate-specific native UI text groups passed.', flush=True)


if __name__ == '__main__':
    main()
