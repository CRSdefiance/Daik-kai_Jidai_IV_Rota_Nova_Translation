"""Inspect mixed-width story Latin; prepare Julio's correction without altering a ROM.

Historical catalogue entries are candidates until current native lookup confirms
selection. No global Unicode normalization or historical compiler edits occur.
"""
import argparse
import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R1, UC_ARM_REG_SP

from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.profiles import DialogueProfile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.confirmed_name_message_catalog import CALLS, MACRO
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.patch.message_actor_integrity import HEADER
from dk4tool.patch.reviewed_name_catalog import ROUTE
from dk4tool.rom.nds import NdsImage
from scripts.verify_fixed_name_glyphs_v279 import expand
from scripts.verify_name_catalog_glyphs_v278 import raster
from scripts.verify_ordinary_name_fidelity_research import initialized


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def wide_letters(text):
    return [dict(index=i, character=c, codepoint=f'U+{ord(c):04X}')
            for i, c in enumerate(text)
            if '\uff21' <= c <= '\uff3a' or '\uff41' <= c <= '\uff5a']


def independent_pixels(arm, font, events):
    """Current native ASCII ink has the validated Y+1 offset; CP932 stays 11x11."""
    ascii_font = GameAsciiFont.from_arm9(arm)
    mapping = struct.unpack_from('<3340H', arm, 0x125EC4)
    pixels = bytearray(216 * 64)
    occupied = set()
    for e in events:
        x, y, code, style = [e[k] for k in ('x', 'y', 'code', 'style')]
        if e['kind'] == 'ascii':
            bitmap = ascii_font.decode(chr(code))
            width = 6
            ink = [(xx, yy + 1) for yy in range(11) for xx in range(6)
                   if bitmap.getpixel((xx, yy))]
        else:
            assert code in mapping
            at = mapping.index(code) * 22
            cell = font[at:at + 22]
            width = 12
            ink = [(xx, yy) for yy in range(11) for xx in range(11)
                   if cell[yy * 2 + xx // 8] & (0x80 >> (xx % 8))]
        if ink:
            assert 0 <= x <= 216 - width and y in (0, 16, 32, 48)
            cells = {(x + xx, y + yy) for yy in range(12) for xx in range(width)}
            assert not occupied.intersection(cells)
            occupied.update(cells)
        for yy in range(12):
            for xx in range(width):
                if 0 <= x + xx < 216 and 0 <= y + yy < 64:
                    pixels[(y + yy) * 216 + x + xx] = 0
        for xx, yy in ink:
            pixels[(y + yy) * 216 + x + xx] = style
        if e['kind'] == 'cp932':
            shadow = 14 if style == 15 else 0 if 7 <= style <= 14 else 15
            for yy in range(11, 0, -1):
                for xx in range(11):
                    if pixels[(y + yy - 1) * 216 + x + xx] and not pixels[(y + yy) * 216 + x + xx + 1]:
                        pixels[(y + yy) * 216 + x + xx + 1] = shadow
    return bytes(pixels)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists(), 'Use a fresh evidence directory.'
    manifest_path = args.rom.with_suffix('.manifest.json')
    manifest = load(manifest_path)
    assert sha(args.rom.read_bytes()) == manifest['candidate_sha256']
    assert all(manifest['checks'].values())
    image = NdsImage.open(args.rom)
    arm = image.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds')
    assert image.read_file('/GRP/KANJI.FNT') == clean.read_file('/GRP/KANJI.FNT')
    packet_path = Path('translations/reviewed_name_packet_v299.json')
    packet = load(packet_path)
    row = next(r for r in packet['records']
               if r['file_path'] == '/data/SC0.DK4' and r['id'] == 'DK4_MES_B43_R0017')
    current_blocks = IlnkContainer.parse(image.read_file(row['file_path'])).blocks
    source_blocks = IlnkContainer.parse(clean.read_file(row['file_path'])).blocks
    current = current_blocks[43].split(b'\0')[17]
    source = source_blocks[43].split(b'\0')[17]
    assert source.hex() == row['clean_source_hex'] and current == bytes.fromhex(row['current_key_hex'])
    legacy = bytes.fromhex(row['target_hex'])
    args.out.mkdir(parents=True)

    # Follow the current original call site, including later catalogue wrappers.
    instruction = struct.unpack_from('<I', arm, CALLS[0])[0]
    assert instruction >> 24 == 0xEB
    delta = (instruction & 0xFFFFFF) << 2
    if delta & 0x2000000:
        delta -= 0x4000000
    entry = BASE + CALLS[0] + 8 + delta
    cpu = initialized(arm)
    lookups = []
    for form, raw, expected in [('whole', current, legacy), ('body', current[1:], legacy[1:])]:
        for alignment in range(4):
            pointer = 0x02468020 + alignment
            cpu.mem_write(pointer - 16, b'\xa5' * (len(raw) + 33))
            cpu.mem_write(pointer, raw + b'\0')
            before = bytes(cpu.mem_read(pointer - 16, len(raw) + 33))
            cpu.mem_write(ROUTE, struct.pack('<I', 0))
            cpu.reg_write(UC_ARM_REG_R1, pointer)
            cpu.reg_write(UC_ARM_REG_LR, BASE + CALLS[0] + 4)
            cpu.reg_write(UC_ARM_REG_SP, 0x027F0000)
            cpu.emu_start(entry, MACRO, count=1000000)
            assert cpu.reg_read(UC_ARM_REG_PC) == MACRO
            selected = cpu.reg_read(UC_ARM_REG_R1)
            assert bytes(cpu.mem_read(selected, len(expected) + 1)) == expected + b'\0'
            assert bytes(cpu.mem_read(pointer - 16, len(raw) + 33)) == before
            lookups.append(dict(form=form, alignment=alignment, selected_pointer=selected,
                                exact_current_legacy_target=True))

    profile_data = dict(row['profile'])
    profile_data.update(name='julio-deck-glyph-review-20261101',
                        literal_prefix_policy='native-guard-v255')
    profile_data['leading_speaker_bytes'] = frozenset(profile_data['leading_speaker_bytes'])
    english = row['english'].removesuffix('{PAD}')
    encoded = encode_relocatable_dialogue(current, english, DialogueProfile(**profile_data))
    assert encoded.encoded[0] == source[0] == 6
    assert not wide_letters(encoded.formatted_markup)
    assert encoded.encoded.count(b'FI') == legacy.count(b'FI') == source.count(b'FI') == 1
    assert not any(d.severity == 'error' for d in encoded.diagnostics)
    # Literal-only tests exercise the real native F/I parser without constructing
    # a synthetic captain/name object. Actual FI substitution remains pending.
    literal_tests = [b'First, It cannot sail.', b'I agree. First.', b'First, a captain. It can sail.']
    for text in literal_tests:
        assert expand(cpu, text) == text

    pictures = []
    native = []
    for label, raw in [('current', legacy), ('proposed', encoded.encoded)]:
        body = raw[1:].replace(b'FI', b'Rafael')
        pixels, events, font = raster(arm, body)
        assert pixels == independent_pixels(arm, font, events)
        visible = [e for e in events if e['code'] != 32]
        expected = [('ascii', ord(c)) if ord(c) < 128 else
                    ('cp932', int.from_bytes(c.encode('cp932'), 'big'))
                    for c in body.decode('cp932') if c not in ' \n']
        assert [(e['kind'], e['code']) for e in visible] == expected
        assert [visible[0]['x'], visible[0]['y']] == [0, 0]
        pic = Image.new('RGB', (216, 64))
        colors = {0: (239, 232, 201), 1: (0, 8, 0), 15: (98, 97, 98)}
        pic.putdata([colors[p] for p in pixels])
        path = args.out / (label + '.png')
        pic.save(path)
        pictures.append((label, pic))
        native.append(dict(label=label, body_hex=body.hex(), events=events,
                           preview=str(path), preview_sha256=sha(path.read_bytes()),
                           complete_glyphs_independent_pixels_bounds_input_canaries=True,
                           default_name_expansion_host_supplied_not_native_name_test=True))
    sheet = Image.new('RGB', (648, 440), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, (label, pic) in enumerate(pictures):
        draw.text((8, i * 220 + 5), label + ' - offline native renderer', fill='white')
        sheet.paste(pic.resize((648, 192), Image.Resampling.NEAREST), (0, i * 220 + 24))
    sheet_path = args.out / 'comparison.png'
    sheet.save(sheet_path)

    # Broad candidates are intentionally not blanket approvals or repairs.
    stored = []
    for route in range(4):
        path = f'/data/SC{route}.DK4'
        for block, raw_block in enumerate(IlnkContainer.parse(image.read_file(path)).blocks):
            offset = 0
            for index, raw in enumerate(raw_block.split(b'\0')):
                body = raw[1:] if offset >= 5 and raw_block[offset - 5:offset] == HEADER else raw
                try:
                    text = body.decode('cp932')
                except UnicodeDecodeError:
                    offset += len(raw) + 1
                    continue
                found = wide_letters(text)
                if found:
                    stored.append(dict(file_path=path, block=block, record_index=index,
                                       block_offset=offset, raw_hex=raw.hex(), text=text,
                                       wide_letters=found, classification='candidate-not-editorial-defect-proof'))
                offset += len(raw) + 1
    payload = bytes(MainCodeFile(arm, BASE).sections[3].data)
    catalogue = []
    for r in packet['records']:
        if r['storage'] != 'catalog':
            continue
        target = bytes.fromhex(r['target_hex'])
        body = target[1:] if r['native_actor'] is not None else target
        found = wide_letters(body.decode('cp932'))
        if found and target + b'\0' in payload:
            catalogue.append(dict(file_path=r['file_path'], id=r['id'], target_hex=target.hex(),
                                  wide_letters=found, source_packet=str(packet_path),
                                  historical_target_resident=True, current_native_selection_unverified=True))
    report = dict(format='dk4-story-glyph-consistency-review-v1', ROM=str(args.rom),
                  ROM_sha256=manifest['candidate_sha256'], ARM9_sha256=sha(arm),
                  manifest=str(manifest_path), manifest_sha256=sha(manifest_path.read_bytes()),
                  id=row['id'], file_path=row['file_path'], source_hex=source.hex(), current_storage_hex=current.hex(),
                  current_effective_hex=legacy.hex(), original_current_native_lookups=lookups,
                  proposed_english=english, proposed_profile=profile_data | {'leading_speaker_bytes': sorted(profile_data['leading_speaker_bytes'])},
                  proposed_formatted_markup=encoded.formatted_markup, proposed_hex=encoded.encoded.hex(),
                  diagnostics=[dict(severity=d.severity, code=d.code, message=d.message) for d in encoded.diagnostics],
                  line_break_count_warning_reason='Four native rows retain the established paragraph; clean Japanese has four rows. No authored break or extra page.',
                  native_literal_F_I_parser_cases=[t.decode() for t in literal_tests], native_previews=native,
                  review_sheet=str(sheet_path), review_sheet_sha256=sha(sheet_path.read_bytes()),
                  direct_visual_review_pending=True, stored_mixed_width_candidates=stored,
                  resident_historical_catalogue_candidates=catalogue,
                  safe_literal_helper='scripts/revalidate_name_migration_v276.py::safe_literal_markup',
                  finding='Historical helper converts literal capital F/I to full-width glyphs. Current Julio target is confirmed by original native lookup.',
                  current_prose_retained=True, new_editorial_credit=0, ROM_modified=False,
                  actual_substitution_gameplay_and_registered_integration_pending=True,
                  source_packet_sha256=sha(packet_path.read_bytes()), producer_sha256=sha(Path(__file__).read_bytes()))
    save(args.out / 'report.json', report)
    print(json.dumps(dict(confirmed_current_Julio_wide_F_and_I=True, native_lookups=len(lookups),
                          stored_candidates=len(stored), resident_catalogue_candidates=len(catalogue),
                          native_literal_cases=len(literal_tests), native_pages=len(native),
                          report=str(args.out / 'report.json'), ROM_modified=False)))


if __name__ == '__main__':
    main()
