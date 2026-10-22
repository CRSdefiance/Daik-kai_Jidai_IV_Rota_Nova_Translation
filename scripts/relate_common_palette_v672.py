"""Exact observed palette correspondence, not an invented runtime converter."""

import struct
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_embedded_paints_v672 import ROOT, preflight, sources
from scripts.verify_village_wrap_v608 import read, save


def words(blob):
    return struct.unpack(f'<{len(blob) // 2}H', blob)


def main():
    pre = preflight()
    clean, current = NdsImage.open('work/clean.nds'), NdsImage.open(pre['candidate'])
    source, _, _ = sources(clean, clean)
    reference = clean.read_file('/_pxl/__frame.pxl')[20:2676]
    pairs = list(zip(words(source), words(reference), strict=True))
    lookup = defaultdict(set)
    for old, new in pairs[:41 * 16]:
        for shift in (0, 5, 10):
            lookup[old >> shift & 31].add(new >> shift & 31)
    assert set(lookup) == set(range(32)) and all(len(v) == 1 for v in lookup.values())
    lut = [next(iter(lookup[i])) for i in range(32)]

    def converted(word):
        color = sum(lut[word >> shift & 31] << shift for shift in (0, 5, 10))
        return color | (0x8000 if word else 0)

    assert all(converted(old) == new for old, new in pairs)
    counterpart_rows = []
    for label, image in (('clean_Japanese', clean), ('current_English', current)):
        legacy_palette, _, indices = sources(image, clean)
        converted_words = [converted(w) for w in words(legacy_palette)]
        for path in ('/_pxl/__frame.pxl', '/_pxl/__marker.pxl'):
            modern = image.read_file(path)
            assert tuple(converted_words) == words(modern[20:2676])
            counterpart_rows.append({'version': label, 'path': path,
                'all1328_palette_words_equal_under_explicit_observed_mapping': True,
                'palette_sha256': sha(modern[20:2676]),
                'held_out_palette_banks41_to82': 42, 'held_out_words': 672})
        # Full index halves were separately compared in sources(). Together with
        # complete palette correspondence this proves the declared storage-color
        # relation for every index of every bank; no original conversion is run.
        assert len(indices) == 131072
    naive_all_opaque = sum((old | 0x8000) != new for old, new in pairs)
    naive_preserve_zero = sum((old | (0x8000 if old else 0)) != new for old, new in pairs)
    assert naive_all_opaque and naive_preserve_zero
    # This atlas relationship must not be generalized to the portrait store.
    old_face = IlnkContainer.parse(clean.read_file('/GRP/CMMNIMG.DK4')).blocks[0]
    face = clean.read_file('/GRP/CMMNIMG.000')
    a, b = [converted(w) & 32767 for w in words(old_face[:512])], [w & 32767 for w in words(face[:512])]
    matched = sum(a[x] == b[y] for x, y in zip(old_face[512:], face[512:], strict=True))
    assert matched != len(old_face) - 512
    proof = read(ROOT / 'native_embedded_paint_proof.json')
    rows = []
    title = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 20)
    font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 16)
    for flags, bank in ((f, b) for f in (4, 260) for b in (0, 9, 74, 82)):
        for version in ('original_Japanese', 'current_English'):
            row = next(p for p in proof['previews'] if Path(p['path']).name == f'{version}_flags{flags}_bank{bank}_CONTROLLED_NATIVE.png')
            path = Path(row['path'])
            assert sha(path.read_bytes()) == row['sha256']
            rows.append(row)
    sheet = Image.new('RGB', (820, 80 + 8 * 160), '#263238')
    draw = ImageDraw.Draw(sheet)
    draw.text((12, 8), 'Controlled native paints; supplied descriptors, not gameplay captures', font=title, fill='white')
    draw.text((12, 40), 'Original Japanese                              Current English — unchanged legacy palette', font=font, fill='#d6d6d6')
    for i, (flags, bank) in enumerate((f, b) for f in (4, 260) for b in (0, 9, 74, 82)):
        y = 80 + i * 160
        draw.text((12, y), f'Flags {flags}, bank {bank}; actual descriptor mode is still unknown', font=font, fill='#e7d9aa')
        for x, version in ((12, 'original_Japanese'), (422, 'current_English')):
            path = ROOT / f'{version}_flags{flags}_bank{bank}_CONTROLLED_NATIVE.png'
            crop = Image.open(path).crop((12, 36, 92, 68))
            sheet.paste(crop.resize((320, 128), Image.Resampling.NEAREST), (x, y + 24))
    review_path = ROOT / 'original_current_CONTROLLED_NATIVE_REVIEW_4x.png'
    sheet.save(review_path)
    save(ROOT / 'palette_correspondence.json', {'candidate_sha256': pre['candidate_sha256'],
        'source_banks0_to40_derive_all32_channel_values': True, 'one_shared_RGB5_lookup': lut,
        'observed_alpha_rule': 'Bit15 set iff original complete16-bit legacy word is nonzero.',
        'counterparts': counterpart_rows, 'all83_banks_complete_palette_correspondence': True,
        'full512x256_current_and_clean_atlas_index_halves_exact': True,
        'all10878976_declared_mapped_storage_words_per_version_correspond': True,
        'naive_set_high_bit_mismatched_palette_words': naive_all_opaque,
        'naive_set_high_bit_except_zero_mismatched_palette_words': naive_preserve_zero,
        'mapping_not_applied_to_ROM_or_palette_bytes': True,
        'no_original_runtime_conversion_or_legacy_consumer_inferred': True,
        'portrait_control_same_mapping_only_matches_pixels': matched,
        'portrait_control_total_pixels': len(old_face) - 512,
        'same_mapping_is_not_a_global_legacy_graphics_converter': True,
        'review_sheet': str(review_path), 'review_sheet_sha256': sha(review_path.read_bytes()),
        'verified_native_preview_inputs': rows, 'script_sha256': sha(Path(__file__).read_bytes()),
        'full_goal_complete': False})
    print('V672 atlas palettes: all1328 words/four counterparts, held-out banks and rejected naive conversions; no runtime conversion inferred.')


if __name__ == '__main__':
    main()
