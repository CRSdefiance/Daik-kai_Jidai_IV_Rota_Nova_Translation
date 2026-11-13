"""Find source-bound leads for the actual World Map's two overlay regions."""

import struct
from pathlib import Path

from PIL import Image

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/worldmap_composition_v638')
CAP = Path('work/emulation_v193/worldmap_composition_v638')
ROM = Path('out/all_routes_combined_v636_candidate.nds')


def color5(rgb):
    r, g, b = rgb[:3]
    return (r >> 3) | ((g >> 3) << 5) | ((b >> 3) << 10)


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    report_path = CAP / 'capture_report.json'
    report = read(report_path)
    assert report['ROM_sha256'] == sha(ROM.read_bytes()) == 'c4ff537ddcd4da5eb1743fb28cd0eb160492e9b660af080ddae44e94a9f4d95d'
    assert report['frames'] == 36000 and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report.get('battery_save_preloaded')
    assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
    raw = (CAP / 'frame_036000_arm9_ram.bin').read_bytes()
    shot = next(r for r in report['frames_captured'] if r['frame'] == 36000 and 'final' in r['path'])
    assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
    image = Image.open(shot['path']).convert('RGB')
    header = 0x279B38
    assert struct.unpack_from('<5I', raw, header) == (4, 61, 160, 20, 52)
    palette = [v & 32767 for v in struct.unpack_from('<16H', raw, header + 20)]
    indices = [n for b in raw[header + 52:header + 52 + 19520] for n in (b & 15, b >> 4)]
    base = [palette[n] for n in indices]
    shown = [color5(image.getpixel((x + 6, y + 208))) for y in range(160) for x in range(244)]
    different = [(x, y) for y in range(160) for x in range(244) if base[y * 244 + x] != shown[y * 244 + x]]
    assert len(different) == 281
    rom = NdsImage.open(ROM)
    leads, scopes = [], []
    paths = ('/_pxl/__marker.pxl', '/_pxl/__frame.pxl', '/_pxl/ship.pxl', '/_pxl/ship16.pxl')
    for label, box in [('large', (122, 80, 146, 104)), ('small', (120, 26, 132, 38))]:
        x0, y0, x1, y1 = box
        points = [(x - x0, y - y0, shown[y * 244 + x]) for x, y in different
                  if x0 <= x < x1 and y0 <= y < y1]
        assert len(points) == (176 if label == 'large' else 105)
        for path in paths:
            data = rom.read_file(path)
            asset = PxlImage.from_bytes(data)
            count = 1 << asset.bits_per_pixel
            banks = (asset.pixels_offset - 20) // (count * 2)
            scopes.append({'overlay': label, 'path': path, 'sha256': sha(data), 'banks': banks})
            for bank in range(banks):
                palette = [v & 32767 for v in struct.unpack_from(f'<{count}H', data, 20 + bank * count * 2)]
                pixels = [palette[n] for n in asset.indices]
                # Prefer the rarest required colour in this exact source bank.
                colors = set(palette)
                if any(v not in colors for _, _, v in points):
                    continue
                anchor = min(points, key=lambda p: pixels.count(p[2]))
                rest = [p for p in points if p != anchor]
                for at, value in enumerate(pixels):
                    if value != anchor[2]:
                        continue
                    sx, sy = at % asset.width - anchor[0], at // asset.width - anchor[1]
                    if not (0 <= sx <= asset.width - (x1 - x0) and 0 <= sy <= asset.height - (y1 - y0)):
                        continue
                    if not all(pixels[(sy + y) * asset.width + sx + x] == color for x, y, color in rest):
                        continue
                    composites = []
                    for transparency in ('index0', 'black_color'):
                        errors = 0
                        for y in range(y1 - y0):
                            for x in range(x1 - x0):
                                p = (sy + y) * asset.width + sx + x
                                transparent = asset.indices[p] == 0 if transparency == 'index0' else pixels[p] == 0
                                expected = base[(y0 + y) * 244 + x0 + x] if transparent else pixels[p]
                                errors += expected != shown[(y0 + y) * 244 + x0 + x]
                        composites.append({'assumed_transparency': transparency, 'different_pixels': errors})
                    leads.append({'overlay': label, 'map_bounds': list(box), 'resource': path,
                                  'palette_bank': bank, 'source_origin': [sx, sy],
                                  'all_overlay_difference_points_match': len(points),
                                  'complete_composite_hypotheses': composites,
                                  'native_parent_binding_not_yet_proven': True})
    save(ROOT / 'overlay_source_leads.json', {
        'candidate': str(ROM), 'candidate_sha256': report['ROM_sha256'],
        'report': str(report_path), 'report_sha256': sha(report_path.read_bytes()),
        'raw_sha256': sha(raw), 'PNG_sha256': shot['PNG_sha256'],
        'actual_overlay_difference_points': len(different), 'scopes': scopes, 'leads': leads,
        'script_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Overlay source leads:', leads)


if __name__ == '__main__':
    main()
