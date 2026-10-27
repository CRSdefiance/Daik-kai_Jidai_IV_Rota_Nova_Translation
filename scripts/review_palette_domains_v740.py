"""Locate stored PXL shapes concealed by equal bank-zero RGB colors.

This is a source-content check, not a runtime palette/alpha or scene test.
"""

import itertools
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.pxl import PxlImage, bgr555
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/palette_domains_v740')
ROMS = {
    'clean': Path('work/clean.nds'),
    'current': Path('out/all_routes_combined_v712_candidate.nds'),
}


def inspect(raw):
    parsed = PxlImage.from_bytes(raw)
    assert parsed.to_bytes() == raw
    offset, end = struct.unpack_from('<2I', raw, 12)
    size = 1 << parsed.bits_per_pixel
    assert end == parsed.pixels_offset and (end - offset) % (size * 2) == 0
    words = [v for v, in struct.iter_unpack('<H', raw[offset:end])]
    banks = [words[i:i + size] for i in range(0, len(words), size)]
    assert banks and all(len(bank) == size for bank in banks)
    used = sorted(set(parsed.indices))
    # Any pair distinguishable in another bank but equal in bank zero is a
    # potentially concealed shape. No arbitrary contrast threshold is implied.
    hidden = []
    for a, b in itertools.combinations(used, 2):
        if (banks[0][a] & 0x7FFF) != (banks[0][b] & 0x7FFF):
            continue
        other = [i for i, bank in enumerate(banks[1:], 1)
                 if (bank[a] & 0x7FFF) != (bank[b] & 0x7FFF)]
        if other:
            hidden.append({'indices': [a, b], 'distinguishing_banks': other})
    return parsed, banks, {
        'file_sha256': sha(raw), 'palette_sha256': sha(raw[offset:end]),
        'packed_indices_sha256': sha(raw[end:]),
        'dimensions': [parsed.width, parsed.height],
        'bits_per_pixel': parsed.bits_per_pixel, 'banks': len(banks),
        'used_indices': used, 'bank_zero_RGB_hidden_pairs': hidden,
    }


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    release = read('work/analysis/display_context_packet_v739/proof.json')['release_hashes_unchanged']
    for path, digest in release.items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(ROMS['clean'].read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    all_rows, previews, stats = {}, {}, {}
    sheet = Image.new('RGB', (750, 310), '#30343c')
    draw = ImageDraw.Draw(sheet)
    for label, path in ROMS.items():
        rows, counters = {}, {'PXL_files': 0, 'single_bank': 0, 'direct_color': 0}
        for _, name, raw in NdsImage.open(path).iter_files():
            if not name.lower().endswith('.pxl'):
                continue
            counters['PXL_files'] += 1
            depth = struct.unpack_from('<I', raw)[0] & 255
            if depth == 16:
                counters['direct_color'] += 1
                continue
            parsed, banks, row = inspect(raw)
            if len(banks) == 1:
                counters['single_bank'] += 1
                continue
            rows[name] = row
            if row['bank_zero_RGB_hidden_pairs']:
                assert name == '/_pxl/fontpanel.pxl' and len(banks) == 2
                for index, bank in enumerate(banks):
                    im = Image.new('RGB', (parsed.width, parsed.height))
                    im.putdata([bgr555(bank[i])[:3] for i in parsed.indices])
                    target = ROOT / f'fontpanel_{label}_bank{index}.png'
                    im.save(target)
                    decoded = Image.open(target).convert('RGB')
                    assert decoded.size == im.size and decoded.tobytes() == im.tobytes()
                    previews[str(target)] = {'file_sha256': sha(target.read_bytes()),
                                            'RGB_sha256': sha(im.tobytes()),
                                            'dimensions': list(im.size)}
                    if label == 'clean':
                        sheet.paste(im.resize((352, 256), Image.Resampling.NEAREST),
                                    (10 + index * 380, 40))
                        draw.text((10 + index * 380, 10),
                                  f'fontpanel source stored bank {index}', fill='white')
        counters['multi_bank'] = len(rows)
        counters['hidden_domain_files'] = sum(bool(x['bank_zero_RGB_hidden_pairs']) for x in rows.values())
        assert counters['PXL_files'] == counters['single_bank'] + counters['direct_color'] + counters['multi_bank']
        all_rows[label], stats[label] = rows, counters
    assert set(all_rows['clean']) == set(all_rows['current'])
    assert all(all_rows['clean'][p]['palette_sha256'] == all_rows['current'][p]['palette_sha256']
               for p in all_rows['clean'])
    assert all_rows['clean']['/_pxl/fontpanel.pxl'] == all_rows['current']['/_pxl/fontpanel.pxl']
    sheet_path = ROOT / 'fontpanel_banks_8x.png'
    sheet.save(sheet_path)
    save(ROOT / 'proof.json', {
        'format': 'dk4-stored-PXL-RGB-palette-domain-review-v740',
        'statistics': stats, 'all_multi_bank_rows': all_rows,
        'previews': previews, 'sheet': str(sheet_path),
        'sheet_sha256': sha(sheet_path.read_bytes()),
        'all16_source_current_multi_bank_palettes_exact': len(all_rows['clean']) == 16,
        'only_fontpanel_has_bank_zero_RGB_collisions_refined_elsewhere': True,
        'producer_sha256': sha(Path(__file__).read_bytes()),
        'release_hashes_unchanged': release,
        'previous_goal_turn_classification': 'no-progress: existing queue restated; new source palette-domain check executed now',
        'scope': 'Stored RGB equality partitions over used indices of every 4/8-bit PXL in clean/current. Bit15 opacity, low-contrast legibility, external palettes, FLS and native consumers are not established by this check.',
        'ROM_modified': False, 'full_goal_complete': False,
    })
    print(stats, flush=True)


if __name__ == '__main__':
    main()
