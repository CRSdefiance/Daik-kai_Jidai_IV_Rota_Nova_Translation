"""Search saved registered-candidate captures for complete miniature atlas masks.

Matches are leads, not native resource provenance. The scan covers actual saved
frames and original bank colors; it does not prove global absence or non-use.
"""

import json
import struct
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from PIL import Image, ImageChops

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/miniature_consumers_v577')
ROM = Path('out/all_routes_combined_v573_candidate.nds')
REPORT_ROOT = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
TEMPLATES = {}
COLORS = set()


def template(image, box):
    left, top, right, bottom = box
    width, height = right - left, bottom - top
    rows = [''.join('1' if image.indices[y * image.width + x] == 9 else '0'
                    for x in range(left, right)) for y in range(top, bottom)]
    assert {image.indices[y * image.width + x] for y in range(top, bottom)
            for x in range(left, right)} == {0, 9}
    anchor = max(range(height), key=lambda row: sum(a != b for a, b in zip(rows[row], rows[row][1:])))
    return {'box': box, 'width': width, 'height': height, 'rows': rows,
            'row_bits': [int(row, 2) for row in rows], 'anchor': anchor,
            'ink_pixels': sum(row.count('1') for row in rows)}


def setup(templates, colors):
    global TEMPLATES, COLORS
    TEMPLATES = templates
    COLORS = set(map(tuple, colors))


def scan_image(path, templates, colors):
    with Image.open(path) as source:
        assert source.size in ((256, 192), (256, 384)), (path, source.size)
        native = source.convert('RGB').point(lambda value: value >> 3)
    width, height = native.size
    present = {rgb for _, rgb in native.getcolors(maxcolors=32768)}
    channels = native.split()
    matches = []
    for color in sorted(colors & present):
        masks = [channel.point([255 if v == target else 0 for v in range(256)], '1')
                 for channel, target in zip(channels, color, strict=True)]
        binary = ImageChops.logical_and(ImageChops.logical_and(masks[0], masks[1]), masks[2])
        packed = binary.tobytes()
        stride = width // 8
        row_bits = [int.from_bytes(packed[y * stride:(y + 1) * stride], 'big') for y in range(height)]
        row_text = [format(row, f'0{width}b') for row in row_bits]
        for name, t in templates.items():
            anchor = t['anchor']
            pattern = t['rows'][anchor]
            mask = (1 << t['width']) - 1
            for row in range(anchor, height - t['height'] + anchor + 1):
                x = -1
                while (x := row_text[row].find(pattern, x + 1)) >= 0:
                    y = row - anchor
                    shift = width - x - t['width']
                    if all((row_bits[y + dy] >> shift) & mask == expected
                           for dy, expected in enumerate(t['row_bits'])):
                        matches.append({'caption': name, 'origin': [x, y],
                                        'bounds': [x, y, x + t['width'], y + t['height']],
                                        'native_color_5bit': list(color),
                                        'complete_ink_pixels': t['ink_pixels'],
                                        'all_ink_and_blank_cells_exact': True})
    return matches


def scan_file(row):
    path, expected_sha = row
    assert sha(Path(path).read_bytes()) == expected_sha
    return {'path': path, 'PNG_sha256': expected_sha,
            'matches': scan_image(path, TEMPLATES, COLORS)}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    production = NdsImage.open(ROM)
    resource = '/_pxl/__frame.pxl'
    pxl = PxlImage.from_bytes(production.read_file(resource))
    batch = json.loads(Path('translations/frame_action_buttons_graphics_v7.json').read_text(encoding='utf-8'))
    all_templates = {row['text']: template(pxl, row['box']) for row in batch['records'][15:]}
    templates = {name: t for name, t in all_templates.items() if name not in ('M', 'D')}
    banks = []
    for bank in range((pxl.pixels_offset - 20) // 32):
        word = struct.unpack_from('<H', pxl.source, 20 + bank * 32 + 9 * 2)[0]
        banks.append((word & 31, word >> 5 & 31, word >> 10 & 31))
    colors = set(banks)
    assert len(banks) == 83 and len(templates) == 5

    calibration = []
    for frame in (3200, 3500, 4300):
        path = REPORT_ROOT / 'action_consumers_v562_navigation' / f'frame_{frame:06d}_navigation.png'
        matches = scan_image(path, {name: all_templates[name] for name in ('M', 'D')}, {(31, 31, 31)})
        for name, origin in (('M', [122, 333]), ('D', [146, 333])):
            assert any(row['caption'] == name and row['origin'] == origin for row in matches), (frame, name, matches)
        calibration.append({'frame': frame, 'path': str(path), 'PNG_sha256': sha(path.read_bytes()),
                            'expected_native_M_and_D_complete_cells_found': True})

    reports = []
    frames = {}
    identities = {}
    for path in sorted(REPORT_ROOT.rglob('capture_report.json')):
        report = json.loads(path.read_text(encoding='utf-8'))
        candidate = Path(report.get('ROM', ''))
        if not (candidate.name.startswith('all_routes_combined_v') and candidate.name.endswith('_candidate.nds')):
            continue
        identities.setdefault(report['ROM_sha256'], candidate)
        context = {'report': str(path), 'report_sha256': sha(path.read_bytes()),
                   'candidate': str(candidate), 'candidate_sha256': report['ROM_sha256'],
                   'frames_run': report['frames'], 'cold_boot': report['cold_boot'],
                   'savestate_loaded': report['savestate_loaded'],
                   'fixture_report_keys': [key for key in report if key.startswith('synthetic_')],
                   'input_schedule': report['scripted_input_schedule']}
        reports.append(context)
        for row in report['frames_captured']:
            item = frames.setdefault(row['PNG_sha256'], {'path': row['path'], 'PNG_sha256': row['PNG_sha256'], 'occurrences': []})
            item['occurrences'].append({'report': str(path), 'frame': row['frame'], 'path': row['path'],
                                        'candidate_sha256': report['ROM_sha256']})

    bindings = []
    registry = json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'))
    for expected, candidate in identities.items():
        assert sha(candidate.read_bytes()) == expected
        manifest_path = candidate.with_suffix('.manifest.json')
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        assert manifest['format'] == 'dk4-integrated-release-v1'
        assert manifest['candidate_sha256'] == expected
        assert manifest['profile'] in registry['profiles']
        assert manifest['base_sha256'] == registry['canonical_baseline']['sha256']
        previous = PxlImage.from_bytes(NdsImage.open(candidate).read_file(resource))
        assert previous.source[:previous.pixels_offset] == pxl.source[:pxl.pixels_offset]
        for t in all_templates.values():
            left, top, right, bottom = t['box']
            assert all(previous.indices[y * 256 + left:y * 256 + right] == pxl.indices[y * 256 + left:y * 256 + right]
                       for y in range(top, bottom))
        bindings.append({'candidate': str(candidate), 'sha256': expected,
                         'manifest': str(manifest_path), 'manifest_sha256': sha(manifest_path.read_bytes()),
                         'registered_profile': manifest['profile'], 'base_sha256': manifest['base_sha256'],
                         'all_seven_current_cell_masks_and_all_83_banks_exact': True})
    print(f'Bound {len(reports)} reports / {len(bindings)} ROMs / {len(frames)} unique PNGs; calibration passes.', flush=True)

    found = []
    processed = 0
    with ProcessPoolExecutor(max_workers=4, initializer=setup,
                             initargs=(templates, sorted(colors))) as pool:
        jobs = [(row['path'], key) for key, row in frames.items()]
        for result in pool.map(scan_file, jobs, chunksize=8):
            processed += 1
            if result['matches']:
                result['occurrences'] = frames[result['PNG_sha256']]['occurrences']
                found.append(result)
                print(f'MATCH {result["path"]}: {result["matches"]}', flush=True)
            if processed % 200 == 0:
                print(f'Searched {processed}/{len(frames)} unique PNGs', flush=True)

    proof = {'format': 'dk4-miniature-caption-capture-corpus-search-v577',
             'current_candidate': str(ROM), 'current_candidate_sha256': sha(ROM.read_bytes()),
             'resource': resource, 'resource_sha256': sha(pxl.source),
             'templates': templates, 'original_palette_bank_count': len(banks),
             'distinct_foreground_colors': sorted(colors), 'native_calibration': calibration,
             'registered_candidate_bindings': bindings, 'reports': reports,
             'unique_PNG_count': len(frames), 'captured_occurrence_count': sum(len(r['occurrences']) for r in frames.values()),
             'searched_images': [{'path': row['path'], 'PNG_sha256': key,
                                  'captured_occurrences': len(row['occurrences'])} for key, row in frames.items()],
             'matches': found, 'complete_mask_matches_are_only_context_leads': True,
             'frame_resource_owner_and_actual_crops_not_inferred_from_pixels_alone': True,
             'absence_is_not_global_nonuse_or_unsampled_frame_coverage': True,
             'arbitrary_fade_or_modulation_colors_not_covered': True,
             'production_ROM_changed': False, 'all18_plaques_remain_incomplete': True,
             'full_goal_complete': False}
    (ROOT / 'capture_corpus_search_proof.json').write_text(
        json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Complete: {processed} unique PNGs; {len(found)} positive images; no production changes.', flush=True)


if __name__ == '__main__':
    main()
