"""Bounded metadata/geometry follow-up, never a filename or non-use classifier."""

import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_plaque_review_v671 import ROOT
from scripts.run_village_visits_v664 import CAP
from scripts.verify_graphic_paints_v669 import source_rect
from scripts.verify_village_wrap_v608 import read, save


def main():
    rows = []
    for label, folder in (
        ('newgame', 'graphic_paints_v669_newgame_observed_marker'),
        ('equipment', 'graphic_paints_v669_equipment_observed_marker'),
        ('crew', 'graphic_contexts_v670_crew_observed'),
        ('race', 'graphic_contexts_v670_race_observed'),
    ):
        path = CAP / folder / 'observer/paint_entries.bin'
        meta = read(path.parent / 'paint_observer.json')
        data = path.read_bytes()
        assert sha(data) == meta['sha256'] and len(data) == meta['records'] * 160
        beyond, count, candidates = [], 0, 0
        for r in struct.iter_unpack('<40I', data):
            assert r[38] == 0
            rect = source_rect(r)
            flags, stride, _height, _, _ = r[32:37]
            candidates += int(flags & 255 == 4 and stride == 128)
            if rect[0] + max(1, rect[2]) > 440:
                count += 1
                if len(beyond) < 30:
                    beyond.append({'frame': r[0], 'PC': r[1], 'LR': r[8], 'header': r[4],
                        'header_words': list(r[32:37]), 'binding': r[37], 'source_XYWH': list(rect)})
        rows.append({'case': label, 'trace': str(path), 'trace_sha256': meta['sha256'],
            'records': meta['records'], 'source_beyond_x440': beyond, 'source_beyond_x440_count': count,
            'flags4_stride128_count': candidates,
            'no_complete_embedded_source_binding_or_global_nonuse_inferred': True})
    assert sum(r['records'] for r in rows) == 745022
    save(ROOT / 'embedded_geometry_followup.json', {'cases': rows,
        'actual_primitive_source_geometry_only': True, 'global_nonuse_proved': False,
        'script_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V671 embedded metadata follow-up retained; no source identity or unused-art claim.')


if __name__ == '__main__':
    main()
