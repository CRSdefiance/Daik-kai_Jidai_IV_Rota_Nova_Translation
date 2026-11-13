"""Source-review native Online captions and prepare three faithful refinements."""
import hashlib
import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import REFERENCE_ASCII_FONT_SHA256, GameAsciiFont
from dk4tool.rom.nds import NdsImage
from scripts.materialize_extras_menu_v1 import ARM9_RECORDS

BASE = Path('out/raphael_natural_v2_accepted_base.nds')
BASE_SHA = '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
REFINEMENTS = {
    'DK4_EXTRAS_CHARACTER_DRAMA': ('A drama of diverse lives',
                                 'Human drama involving many different people; preserve diversity rather than implying only player choice.'),
    'DK4_EXTRAS_ORDERS': ('Royal orders, new horizons',
                         'Receive royal orders and embark on further adventures. New horizons conveys further adventures in natural promotional copy; royal authority restored.'),
    'DK4_EXTRAS_TRADE_FORTUNE': ('Trade varied goods for a profit!',
                               'Buy and sell a varied range of trade goods to make money; preserve variety and avoid overstating the profit as a fortune.'),
}


def main():
    if hashlib.sha256(BASE.read_bytes()).hexdigest() != BASE_SHA:
        raise ValueError('Canonical base changed')
    base = NdsImage.open(BASE)
    clean = NdsImage.open('work/clean.nds')
    arm9 = base.read_file('/__arm9__.bin')
    source = clean.read_file('/__arm9__.bin')
    candidate = NdsImage.open('out/all_routes_combined_v132_candidate.nds')
    current = candidate.read_file('/__arm9__.bin')
    code_ranges = [(0x10434C, 0x10435C), (0x104CD8, 0x104D30), (0x105694, 0x105704)]
    for lo, hi in code_ranges:
        if arm9[lo:hi] != source[lo:hi] or current[lo:hi] != source[lo:hi]:
            raise ValueError('Mapped caption consumer differs')
    font = GameAsciiFont.from_arm9(arm9)
    if hashlib.sha256(font.glyphs).hexdigest() != REFERENCE_ASCII_FONT_SHA256:
        raise ValueError('Reference ASCII font changed')
    records, audit = [], []
    descriptors = []
    for offset in (0x12F88C, 0x12F898, 0x12F8A4, 0x12F8B0):
        data, table, count = struct.unpack_from('<3I', source, offset)
        pointer_offsets = [struct.unpack_from('<I', source, table - 0x02000000 + n * 4)[0]
                           - 0x02000000 for n in range(count)]
        descriptors.append({'descriptor_offset': offset, 'data_pointer': data,
                            'caption_table_pointer': table, 'count': count,
                            'caption_offsets': pointer_offsets})
    if {offset for d in descriptors for offset in d['caption_offsets']} != {
            offset for _, offset, _, _, context in ARM9_RECORDS if context == 'Online overview caption'}:
        raise ValueError('Descriptor-selected caption set differs from the source review')
    out = Path('work/qa/online_caption_fidelity')
    out.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1040, 952), 'white')
    draw = ImageDraw.Draw(sheet)
    for name, offset, japanese, previous, context in ARM9_RECORDS:
        if context != 'Online overview caption':
            continue
        locked = japanese.encode('cp932') + b'\0'
        if source[offset:offset + len(locked)] != locked:
            raise ValueError(f'{name}: clean source differs')
        original = arm9[offset:offset + len(locked)]
        if original != current[offset:offset + len(locked)]:
            raise ValueError(f'{name}: V132 caption differs from canonical')
        if original.split(b'\0', 1)[0].decode('ascii') != previous:
            raise ValueError(f'{name}: accepted English differs')
        english, note = REFINEMENTS.get(name, (previous, 'Reviewed existing promotional adaptation against the clean Japanese source.'))
        raw = english.encode('ascii')
        if len(raw) >= len(locked):
            raise ValueError(f'{name}: in-place slot overflow')
        width = len(raw) * 6
        left = 128 - width // 2
        if not 0 <= left <= left + width <= 256:
            raise ValueError(f'{name}: centered panel overflow')
        index = len(audit)
        panel = Image.new('RGB', (256, 48), '#eff1f4')
        for n, char in enumerate(english):
            panel.paste('#15273d', (left + n * 6, 12), font.decode(char))
        panel.resize((512, 96), Image.Resampling.NEAREST).save(out / f'{name}.png')
        x, y = index % 2 * 520, index // 2 * 136
        draw.text((x + 4, y + 4), f'{offset:#x}: {english}', fill='black')
        sheet.paste(panel.resize((512, 96), Image.Resampling.NEAREST), (x + 4, y + 28))
        audit.append({'id': name, 'offset': offset, 'source_hex': locked.hex(),
                      'japanese': japanese, 'previous_english': previous, 'english': english,
                      'slot_bytes': len(locked), 'encoded_bytes_including_nul': len(raw) + 1,
                      'width_pixels': width, 'left': left, 'right_exclusive': left + width,
                      'source_review_note': note})
        if name in REFINEMENTS:
            records.append({'id': name + '_FIDELITY', 'offset': offset,
                            'source_hex': original.hex().upper(), 'english': english,
                            'clean_source_hex': locked.hex().upper(), 'japanese': japanese,
                            'context': context, 'source_meaning': note,
                            'notes': 'Source-reviewed single-line caption; preserves slot and NUL. Integration and runtime pending.'})
    assert len(audit) == 13 and len(records) == 3
    sheet.save(out / 'sheet.png')
    batch = {'format': 'dk4-arm9-fixed-text-batch-v1', 'file_path': '/__arm9__.bin',
             'source_file_sha256': hashlib.sha256(arm9).hexdigest(),
             'target_locale': 'en-US', 'scope': 'Three source-faithful native Online caption refinements',
             'fixed_text_policy': {'require_c_string_termination': True},
             'status': 'source-reviewed-preview-awaiting-integration', 'records': records}
    Path('translations/online_caption_fidelity_arm9_v2.json').write_text(
        json.dumps(batch, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    report = {'source_reviewed_captions': 13, 'proposed_refinements': 3,
              'native_descriptors': descriptors,
              'renderer_ranges_sha256': [{'start': lo, 'end': hi, 'sha256': hashlib.sha256(source[lo:hi]).hexdigest()}
                                         for lo, hi in code_ranges],
              'ascii_advance': 6, 'center_x': 128, 'screen_width': 256,
              'native_y': 12, 'entries': audit,
              'limitations': ['Diagnostic font panels are not gameplay screenshots.',
                              'This ARM9 caption path does not classify the long COMMON promotional copies.',
                              'Prepared batch is not yet integrated into a playable candidate.']}
    (out / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('13 source-reviewed captions; 3 refinements fit exact slots and centered native geometry')


if __name__ == '__main__':
    main()
