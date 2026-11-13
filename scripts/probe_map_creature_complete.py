"""Replay all class substitutions and inherited Golden Route consumers."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_golden_route_empty_copy import execute as empty_copy
from scripts.execute_golden_route_heading import execute as heading
from scripts.execute_map_entity_tooltip_copy import format_copy, select
from scripts.execute_scene_caption_raster import execute as raster
from scripts.inventory_common_scene_caption_duplicates import captions
from scripts.inventory_map_tooltip_classes import execute_class
from scripts.probe_golden_route_footer import TABLES
from scripts.probe_map_entity_tooltip_raster import verify_raster


def probe(current, proposed, allocation, clean):
    if sha(current) != allocation['source_arm9_sha256'] or sha(proposed) != allocation['target_arm9_sha256']:
        raise ValueError('Complete allocation source/target differs')
    selections = [select(proposed, case) for case in ('pirates', 'monster', 'unknown', 'named')]
    classes = [execute_class(proposed, i) for i in range(39)]
    tooltip_cases = []
    for row in classes:
        ship_class = row['text'].encode('ascii')
        for name in (b'Pirates', b'Monster', b'???', b'FleetX'):
            expected = name + b'\n  ' + ship_class + b' class'
            copied = format_copy(proposed, 0x705F0, [name, ship_class], expected)
            text = bytes.fromhex(copied['full_text_hex'])[:-1].decode('ascii')
            for mode in (4, 16):
                tooltip_cases.append({'class_index': row['index'], 'name': name.decode('ascii'),
                                      **verify_raster(proposed, text, mode)})
    inherited = []
    for selection in (0, 1):
        for y in (0, 12):
            before, after = heading(current, selection, y=y), heading(proposed, selection, y=y)
            for field in ('full_text_hex', 'x', 'y', 'style'):
                if before[field] != after[field]:
                    raise ValueError('Relocated title table changes heading output')
            text = bytes.fromhex(after['full_text_hex'])[:-1].decode('ascii')
            for mode in (4, 16):
                old = raster(current, text, tracking=0, x=after['x'], y=y, mode=mode)
                new = raster(proposed, text, tracking=0, x=after['x'], y=y, mode=mode)
                if any(old[field] != new[field] for field in ('glyphs', 'pixels', 'final_x')):
                    raise ValueError('Inherited heading glyphs/pixels differ')
                inherited.append({'kind': 'heading', 'selection': selection, 'y': y,
                                  'mode': mode, 'pixels_sha256': sha(new['pixels'])})
    for table in TABLES:
        for mode in (4, 16):
            before = raster(current, 'unused', footer_table=table, mode=mode)
            after = raster(proposed, 'unused', footer_table=table, mode=mode)
            if any(before[field] != after[field] for field in ('glyphs', 'pixels', 'footer_metadata')):
                raise ValueError('Repacked footer placement/glyphs/pixels differ')
            if [r['text'] for r in before['footer_draws']] != [r['text'] for r in after['footer_draws']]:
                raise ValueError('Repacked footer loses complete English')
            inherited.append({'kind': 'footer', 'table': table, 'mode': mode,
                              'pixels_sha256': sha(after['pixels'])})
    for count in (0, 1, 2, 255):
        before, after = empty_copy(current, count=count), empty_copy(proposed, count=count)
        if before['empty_dialog_selected'] != after['empty_dialog_selected']:
            raise ValueError('Repacking changes zero-record dispatch')
        if not count:
            if before['complete_text_hex'] != after['complete_text_hex']:
                raise ValueError('Repacked empty-message native copy differs')
            text = bytes.fromhex(after['complete_text_hex'])[:-1].decode('ascii')
            for mode in (4, 16):
                old = raster(current, text, modal=True, mode=mode)
                new = raster(proposed, text, modal=True, mode=mode)
                if any(old[field] != new[field] for field in ('glyphs', 'pixels', 'final_x')):
                    raise ValueError('Inherited modal glyphs/pixels differ')
                inherited.append({'kind': 'empty-modal', 'mode': mode,
                                  'pixels_sha256': sha(new['pixels'])})
    caption_rows = captions(clean)
    for row in caption_rows:
        field = row['pointer_field']
        pointer = struct.unpack_from('<I', current, field)[0] - 0x02000000
        if struct.unpack_from('<I', proposed, field)[0] != pointer + 0x02000000:
            raise ValueError('Inherited caption pointer changes')
        if current[pointer:current.index(0, pointer) + 1] != proposed[pointer:proposed.index(0, pointer) + 1]:
            raise ValueError('Inherited full caption text/NUL changes')
    return {'status': 'pass-all-39-class-tooltip-substitutions-and-inherited-golden-consumers',
            'target_arm9_sha256': sha(proposed), 'native_selections': selections,
            'class_count': len(classes), 'tooltip_cases': tooltip_cases,
            'inherited_golden_raster_cases': inherited, 'empty_dispatch_counts': [0, 1, 2, 255],
            'inherited_caption_count': len(caption_rows),
            'limitations': ['All static classes are covered; dynamic faction/user names and numeric bounds remain pending.',
                           'Physical routing/composition and existing bounded bitmap/font contracts remain pending.',
                           'No ROM integration or formatting approval.']}


def main():
    root = Path('work/analysis/map_creature_complete_v139')
    proposed = (root / 'proposed_arm9.bin').read_bytes()
    allocation = json.loads((root / 'report.json').read_text(encoding='utf-8'))
    current = NdsImage.open('out/all_routes_combined_v139_candidate.nds').read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    report = probe(current, proposed, allocation, clean)
    (root / 'native_complete_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f"{len(report['tooltip_cases'])} full native class-tooltip rasters; 16 inherited Golden rasters and 164 unchanged captions pass.")


if __name__ == '__main__':
    main()
