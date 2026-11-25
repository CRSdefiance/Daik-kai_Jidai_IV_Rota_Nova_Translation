"""Verify actual current Sailor Info fields, plaques and bounded fixtures."""

import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_condition_fixture_v637 import BASE, set_condition
from scripts.prepare_condition_matrix_v637 import CAP, DONOR, ROM, ROOT
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_condition_fixtures_v520 import HEALTH, MOOD
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_village_wrap_v608 import read, save

COLOR = (230, 230, 230)
FIELDS = ((56, 108, 104, 124), (56, 128, 104, 144))
AUDIT_KEY = 'current84_condition_combinations_and_source_reviewed_Sailor_Info_plaques_v637'


def field(font, text, image, y, x=56, width=48, height=16):
    ink, bounds = complete_mask(font, text, image, x, y, COLOR)
    expected = Image.new('1', (width, height))
    for n, char in enumerate(text):
        expected.paste(font.decode(char), (n * 6, 0))
    actual = Image.new('1', (width, height))
    for dy in range(height):
        for dx in range(width):
            actual.putpixel((dx, dy), image.getpixel((x + dx, y + dy)) == COLOR)
    assert actual.tobytes() == expected.tobytes(), text
    # These two controls remove real pixels in the first and final glyph cells.
    visible_characters = [i for i, char in enumerate(text) if char != ' ']
    for char_index in (visible_characters[0], visible_characters[-1]):
        damaged = actual.copy()
        hit = next((x, y) for y in range(11) for x in range(char_index * 6, char_index * 6 + 6)
                   if damaged.getpixel((x, y)))
        damaged.putpixel(hit, 0)
        assert damaged.tobytes() != expected.tobytes()
    return {'text': text, 'ink_pixels': ink, 'glyph_bounds': bounds,
            'field_bounds': [x, y, x + width, y + height],
            'whole_field_foreground_and_blank_cells_exact': True,
            'dropped_first_and_final_glyph_pixel_controls_rejected': True}


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['ROM_patch_registry_and_canonical_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest, path
    for path, digest in pre['scripts'].items():
        assert sha(Path(path).read_bytes()) == digest, path
    assert sha(DONOR.read_bytes()) == pre['donor_sha256']
    report_path = CAP / 'capture_report.json'
    report = read(report_path)
    assert report['ROM_sha256'] == pre['candidate_sha256'] and report['frames'] == pre['last_pause_frame']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report['natural_condition_event_verified'] and not report['hardware_device_verification']
    donor = report['battery_save_preloaded']
    assert donor['source_sha256'] == pre['donor_sha256'] and donor['copied_byte_exact_before_cold_boot']
    assert sha(Path(donor['source']).read_bytes()) == pre['donor_sha256']
    assert not any(v for k, v in report.items() if k.startswith('synthetic_') and k != 'synthetic_condition_fixtures')
    snapshots = {r['frame']: r for r in report['read_only_pause_RAM_snapshots']}
    shots = {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        shots[row['frame']] = row
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x7D000:0x7EF00] == clean[0x7D000:0x7EF00]
    assert arm[0x8091C:0x80988] == clean[0x8091C:0x80988]
    skill_table = struct.unpack_from('<I', arm, 0x80A74)[0] - BASE
    assert arm[skill_table:skill_table + 23 * 28] == clean[skill_table:skill_table + 23 * 28]
    format_pointer = struct.unpack_from('<I', arm, 0x80A78)[0]
    assert arm[format_pointer - BASE:].split(b'\0')[0] == b'%7s%3d'
    font = GameAsciiFont.from_arm9(arm)
    fixtures = report['synthetic_condition_fixtures']
    assert len(fixtures) == 86
    replays = []
    for fixture in fixtures:
        snap = snapshots[fixture['frame']]
        raw = Path(snap['path']).read_bytes()
        assert sha(raw) == snap['sha256']
        after, replay = set_condition(arm, raw, {'actor': fixture['actor_id'],
                                              'health': fixture['health'], 'mood': fixture['mood']})
        assert fixture == dict(replay, frame=fixture['frame'])
        offset = fixture['actor_address'] + 6 - BASE
        assert raw[:offset] == after[:offset] and raw[offset + 2:] == after[offset + 2:]
        replays.append({'frame': fixture['frame'], 'before_RAM_sha256': sha(raw),
                        'after_RAM_sha256': sha(after), 'changed_bytes': len(fixture['changes'])})
    old = read('work/analysis/plaque_review_v632/current_plaque_review_proof.json')
    plaque_rows = old['all18_current_native_review_entries'][7:]
    assert len(plaque_rows) == 11
    current = NdsImage.open(ROM)
    earlier = NdsImage.open(old['candidate'])
    for path in ('/_pxl/personinfo.pxl', '/_pxl/dividecrewinfo.pxl'):
        assert current.read_file(path) == earlier.read_file(path)
    cases, backgrounds, first_images = [], [], {}
    pixels_outside_fields = 0
    cursor_difference_frames = []
    for case in read(ROOT / 'cases.json'):
        frame, actor_id = case['frame'], case['actor']
        fixture = next(f for f in fixtures if f['frame'] == case['fixture_frame'])
        assert all(fixture[k] == case[v] for k, v in [('actor_id', 'actor'), ('health', 'health'), ('mood', 'mood')])
        snap = snapshots[frame]
        raw = Path(snap['path']).read_bytes()
        assert sha(raw) == snap['sha256']
        actor = fixture['actor_address']
        assert raw[actor + 6 - BASE:actor + 8 - BASE] == bytes((case['health'], case['mood']))
        u = machine(arm)
        u.mem_write(BASE, raw)
        image = Image.open(shots[frame]['path']).convert('RGB')
        assert image.size == (256, 384)
        labels = []
        for group, state, text, selector, table, y in [
            ('Health', case['health'], HEALTH[case['health']], 0x7E0BC, 0x1483C8, 108),
            ('Mood', case['mood'], MOOD[case['mood']], 0x7E070, 0x1483B0, 128),
        ]:
            call(u, selector, (actor,))
            ptr = u.reg_read(UC_ARM_REG_R0)
            actual = bytes(u.mem_read(ptr, 32)).split(b'\0')[0].decode('ascii')
            assert actual == text
            source_ptr = struct.unpack_from('<I', clean, table + state * 4)[0]
            japanese = clean[source_ptr - BASE:].split(b'\0')[0].decode('cp932')
            labels.append(dict(field(font, text, image, y), group=group, state=state,
                               original_Japanese=japanese, original_selector_pointer=ptr))
        full_name = {3: 'Maria Huamei Li', 10: 'Xien Yan'}[actor_id]
        complete_mask(font, full_name, image, 84, 30, COLOR)
        skills = []
        for i in range(10):
            descriptor = struct.unpack_from('<7I', arm, skill_table + (13 + i) * 28)
            assert descriptor[5:] == (60, 12)
            call(u, 0x7EEB0, (i,))
            name_pointer = u.reg_read(UC_ARM_REG_R0)
            name = bytes(u.mem_read(name_pointer, 40)).split(b'\0')[0].decode('ascii')
            call(u, 0x7DCC8, (actor, i))
            value = u.reg_read(UC_ARM_REG_R0)
            text = f'{name:>7}{value:3d}'
            assert len(text) == 10
            checked = field(font, text, image, 192 + descriptor[2], descriptor[1], 60, 12)
            skills.append(dict(checked, index=i, original_skill_getter=BASE + 0x7DCC8,
                               original_label_getter=BASE + 0x7EEB0, value=value))
        for row in plaque_rows:
            reference = Path(row['current_crop'])
            assert sha(reference.read_bytes()) == row['current_crop_sha256']
            assert image.crop(row['bounds']).tobytes() == Image.open(reference).convert('RGB').tobytes(), (case, row['id'])
        # Condition changes also affect original derived skills. Verify those complete
        # fields above. Account separately for the two-pixel ring around slot4: its
        # time-varying selection effect is not a condition-label test or a whole-frame
        # equality claim. The icon/interior is retained in the exact comparison.
        outside = image.copy()
        checked_fields = list(FIELDS) + [r['field_bounds'] for r in skills]
        for bounds in checked_fields:
            outside.paste((0, 0, 0), bounds)
        ring = {(x, y) for y in range(222, 258) for x in range(206, 242)
                if x < 208 or x >= 240 or y < 224 or y >= 256}
        ring_values = {p: outside.getpixel(p) for p in ring}
        for p in ring:
            outside.putpixel(p, (0, 0, 0))
        if actor_id not in first_images:
            first_images[actor_id] = (outside.tobytes(), ring_values)
        else:
            assert outside.tobytes() == first_images[actor_id][0], ('outside independently checked fields/ring', case)
            pixels_outside_fields += 256 * 384 - 2 * 48 * 16 - 10 * 60 * 12 - len(ring)
            changed_ring = [p for p in ring if ring_values[p] != first_images[actor_id][1][p]]
            if changed_ring:
                cursor_difference_frames.append({'frame': frame, 'pixels': len(changed_ring),
                    'bounds': [min(p[0] for p in changed_ring), min(p[1] for p in changed_ring),
                               max(p[0] for p in changed_ring) + 1, max(p[1] for p in changed_ring) + 1]})
        backgrounds.append((case, image))
        cases.append({**case, 'actor_name': full_name, 'image': shots[frame]['path'],
                      'PNG_sha256': shots[frame]['PNG_sha256'], 'labels': labels, 'derived_skills': skills,
                      'all11_Sailor_Info_plaque_crops_exact_to_source_reviewed_V632_packet': True})
    assert len(cases) == 84
    for actor_id in (3, 10):
        assert {(r['health'], r['mood']) for r in cases if r['actor'] == actor_id} == {
            (h, m) for h in range(7) for m in range(6)}
    # In every field pixel where the labels leave background visible, all such
    # observations must agree. This catches stale non-font pixels across redraws.
    background_pixels = 0
    for actor_id in (3, 10):
        images = [im for c, im in backgrounds if c['actor'] == actor_id]
        for bounds in FIELDS:
            for y in range(bounds[1], bounds[3]):
                for x in range(bounds[0], bounds[2]):
                    colors = {im.getpixel((x, y)) for im in images if im.getpixel((x, y)) != COLOR}
                    assert len(colors) <= 1, (actor_id, x, y, colors)
                    background_pixels += bool(colors)
    before = read(ROOT / 'audit_before.json')
    for name, value in before.items():
        current_audit = read(Path('translations') / name)
        assert all(current_audit[k] == v for k, v in value.items()
                   if k not in (AUDIT_KEY, 'current_goal_turn_classification')), name
        assert set(current_audit) - set(value) <= {AUDIT_KEY}, name
        if AUDIT_KEY in current_audit:
            assert current_audit[AUDIT_KEY]['candidate_sha256'] == pre['candidate_sha256']
            assert current_audit[AUDIT_KEY]['full_goal_complete'] is False
    proof = {
        'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'], 'profile': pre['profile'],
        'report': str(report_path), 'report_sha256': sha(report_path.read_bytes()),
        'all84_actual_health_mood_combinations': cases,
        'both_captain_and_ordinary_crew_all42_combinations': True,
        'complete48x16_fields': len(cases) * 2, 'field_foreground_blank_cell_pixels': len(cases) * 2 * 48 * 16,
        'full11_plaque_crop_comparisons': len(cases) * len(plaque_rows),
        'plaque_crop_pixels': len(cases) * sum((r['bounds'][2] - r['bounds'][0]) *
                                             (r['bounds'][3] - r['bounds'][1]) for r in plaque_rows),
        'outside_independently_verified_fields_and_declared_cursor_ring_exact_pixels': pixels_outside_fields,
        'all840_complete60x12_derived_skill_fields_and_original_getter_values_verified': True,
        'original_skill_getters_and_caller_and_layout_table_exact': True,
        'selection_ring_excluded_from_equality_not_a_full_frame_pass': {
            'outer_bounds': [206, 222, 242, 258], 'unchanged_interior_bounds': [208, 224, 240, 256],
            'ring_pixels_per_frame': 272, 'frames_with_ring_differences': cursor_difference_frames,
            'time_varying_selection_effect_not_newly_verified': True},
        'visible_field_background_pixels_consistent_across_redraws': background_pixels,
        'all86_fixture_replays': replays,
        'fixture_only_two_actor_condition_bytes_permitted': True,
        'full_actual_names_and_original_Japanese_selector_bindings_verified': True,
        'ROM_patch_registry_canonical_and_source_donor_unchanged': True,
        'all18_plaque_entries_remain_incomplete': True, 'all22_historical_scopes_retained': True,
        'natural_injury_recovery_death_or_acquisition_not_claimed': True,
        'other_owners_equipment_variants_and_visual_texture_approval_remain_open': True,
        'fixture_negative_controls': pre['fixture_negative_controls_rejected'],
        'scripts': {str(p): sha(p.read_bytes()) for p in [Path(__file__),
            Path('scripts/native_condition_fixture_v637.py'), Path('scripts/headless_desmume_v193.py'),
            Path('scripts/prepare_condition_matrix_v637.py')]},
        'hardware_device_verification': False, 'full_goal_complete': False, 'canonical_promoted': False,
    }
    save(ROOT / 'current_condition_matrix_proof.json', proof)
    print(f'84 combinations,168 condition fields,840 skill fields,924 plaque crops; {pixels_outside_fields} context pixels exact excluding declared cursor ring;86 fixture replays pass.')


if __name__ == '__main__':
    main()
