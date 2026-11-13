"""Verify the Ancient Map painter's pre-LF flush against every stored field."""

from hashlib import sha256
from inspect import getsource
from types import FunctionType, SimpleNamespace

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import stage_ancient_map_text_v1 as prior
from scripts.source_locked_derivation_v5118 import checked_text
from scripts import verify_common_alignment_native_v257 as raster_tools


base, parent = prior.base, prior.parent
ARM, COMMON = prior.ARM, prior.COMMON
ROOT = prior.ROOT.with_name('ancient_map_text_staged_20261111_v2')
ROM, PROOF = ROOT / prior.ROM.name, ROOT / prior.PROOF.name
FORMAT = 'static-map-pre-LF-empty-cell-v2'
CANVAS = (256, 64)


def build_stage():
    source = checked_text(getsource(prior.stage), {
        "value = '\\n'.join(lines)": """encoded_lines = [line + (' ' if i < len(lines) - 1 and len(line) % 2 else '')
                             for i, line in enumerate(lines)]
            assert all(len(line) * 6 <= RIGHT - X for line in encoded_lines)
            assert all(len(line) % 2 == 0 for line in encoded_lines[:-1])
            value = '\\n'.join(encoded_lines)""",
    })
    environment = vars(prior).copy()
    exec(compile(source, __file__ + '::pre-LF-empty-cell', 'exec'), environment)
    return environment['stage']


stage = build_stage()


def native_raster(image):
    source = checked_text(getsource(raster_tools.raster), {
        'struct.pack("<2I", 6, 16)': 'struct.pack("<2I", 6, 12)',
    })
    environment = vars(raster_tools).copy()
    environment['NdsImage'] = SimpleNamespace(open=lambda _: image)
    exec(compile(source, __file__ + '::map-row-pitch', 'exec'), environment)
    return environment['raster']


def expected_pixels(font, lines):
    width, height = CANVAS
    canvas = bytearray(width * height)
    for y, line in enumerate(lines):
        assert len(line) * 6 <= prior.RIGHT - prior.X
        for x, char in enumerate(line):
            glyph = font.decode(char)
            for gy in range(11):
                for gx in range(6):
                    if glyph.getpixel((gx, gy)):
                        canvas[(y * prior.ROW + gy + 1) * width + x * 6 + gx] = 1
    return bytes(canvas)


def verify_native_fields():
    proof = base.load(PROOF)
    image = base.NdsImage.open(ROM)
    arm = image.read_file(ARM)
    font = GameAsciiFont.from_arm9(arm)
    raster = native_raster(image)
    cases = []
    for record in proof['records'][:51]:
        raw = bytes.fromhex(record['staged_hex'])
        padded = raw.decode('ascii').split('\n')
        lines = record['visible_lines']
        events = []
        pixels = raster(arm, raw, 0xD5404, size=CANVAS, instruction_limit=2000000, glyph_events=events)
        expected = expected_pixels(font, lines)
        assert pixels == expected, (record['message_ID'], padded, lines, events)
        visible = [dict(code=ord(char), style=1, x=x * 6, y=y * prior.ROW)
                   for y, line in enumerate(lines) for x, char in enumerate(line) if char != ' ']
        assert [event for event in events if event['code'] != 32] == visible
        cases.append(dict(message_ID=record['message_ID'], full_native_mask_sha256=sha256(pixels).hexdigest(),
            glyphs=len(visible), inserted_pre_LF_empty_cells=sum(len(p) - len(l) for p, l in zip(padded, lines, strict=True))))
    assert [case['message_ID'] for case in cases] == list(range(3607, 3658))

    # Reintroduce the exact previous storage to catch the observed migration.
    negative = next(row for row in base.load(prior.PROOF)['records'] if row['message_ID'] == 3649)
    events = []
    pixels = raster(arm, bytes.fromhex(negative['staged_hex']), 0xD5404, size=CANVAS,
                    instruction_limit=2000000, glyph_events=events)
    assert pixels != expected_pixels(font, negative['visible_lines'])
    assert dict(code=ord('o'), style=1, x=210, y=12) in events
    assert dict(code=ord('u'), style=1, x=6, y=24) in events
    base.save(ROOT / 'native_document_fields.json', dict(candidate_sha256=base.digest(ROM), formatting_profile=FORMAT,
        original_painter=prior.RENDERER, view_width=prior.RIGHT-prior.X, row_pitch=prior.ROW,
        all_masks_and_complete_ordered_glyph_positions_exact=cases,
        old_odd_row_observed_o_on_previous_row_and_next_line_indented=True,
        offline_scope='Native painter on a controlled surface with the original 6x12 metrics.'))
    print(f'{len(cases)} exact native map fields; odd-line failure reproduced and rejected.')


def main():
    source = checked_text(getsource(prior.main), {
        "visible_lines=display.decode('ascii').split('\\n')":
            "visible_lines=[line.rstrip(' ') for line in display.decode('ascii').split('\\n')]",
    })
    environment = vars(prior) | dict(ROOT=ROOT, ROM=ROM, PROOF=PROOF, stage=stage)
    environment['document_sheets'] = FunctionType(prior.document_sheets.__code__, environment)
    exec(compile(source, __file__ + '::staged-document-and-rumors', 'exec'), environment)
    environment['main']()
    verify_native_fields()


if __name__ == '__main__':
    main()
