"""Complete actual Sailor Info condition masks on captain and ordinary crew."""

import json
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_condition_fixture_v520 import set_condition
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask

ROM = Path('out/all_routes_combined_v518_candidate.nds')
CAPTURE = Path('work/emulation_v193/conditions_live_v520')
OUT = Path('work/analysis/conditions_v520')
HEALTH = ['Healthy', 'Tired', 'Hurt', 'Wounded', 'Dying', 'Sick', 'Dead']
MOOD = ['Excited', 'Good', 'Relaxed', 'Normal', 'Upset', 'Confused']


def main():
    digest = sha(ROM.read_bytes())
    assert digest == 'c451a11bb696c71970d7224a5194e28ec57fa406995862f9cc8e0b67711173b7'
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x7E070:0x7E108] == clean[0x7E070:0x7E108]
    assert arm[0x80A84:0x80AD0] == clean[0x80A84:0x80AD0]
    report_path = CAPTURE / 'capture_report.json'
    report = json.loads(report_path.read_text())
    assert report['ROM_sha256'] == digest and report['cold_boot']
    assert not report['savestate_loaded'] and not report['callback_errors']
    assert not report['natural_condition_event_verified']
    donor = report['battery_save_preloaded']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    assert donor['source_sha256'] == 'fbae21aa2c5a695bde0eddfc10a3bbeb80d01478bd6a9ed743d824595dc3096e'
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    fixtures = report['synthetic_condition_fixtures']
    assert len(fixtures) == 16
    for row in fixtures:
        raw = (CAPTURE / f"frame_{row['frame']:06d}_arm9_ram.bin").read_bytes()
        after, replay = set_condition(arm, raw, {
            'actor': row['actor_id'], 'health': row['health'], 'mood': row['mood']})
        assert row == dict(replay, frame=row['frame'])
        offset = row['actor_address'] + 6 - 0x02000000
        assert raw[:offset] == after[:offset] and raw[offset + 2:] == after[offset + 2:]
    font = GameAsciiFont.from_arm9(arm)
    baseline = Image.open(CAPTURE / 'frame_004400_navigation.png').convert('RGB')
    cases = []
    for actor_id, first_frame, name in [(3, 4800, 'Maria Huamei Li'), (10, 7800, 'Xien Yan')]:
        for health in range(7):
            mood = health if health < 6 else 3
            frame = first_frame + health * 400
            path = CAPTURE / f'frame_{frame:06d}_navigation.png'
            image = Image.open(path).convert('RGB')
            raw = (CAPTURE / f'frame_{frame:06d}_arm9_ram.bin').read_bytes()
            u = machine(arm)
            u.mem_write(0x02000000, raw)
            fixture = next(r for r in fixtures if r['actor_id'] == actor_id and r['health'] == health
                           and r['mood'] == mood)
            actor = fixture['actor_address']
            assert raw[actor + 6 - 0x02000000:actor + 8 - 0x02000000] == bytes((health, mood))
            labels = []
            for group, state, text, selector, table, y in [
                ('Health', health, HEALTH[health], 0x7E0BC, 0x1483C8, 108),
                ('Mood', mood, MOOD[mood], 0x7E070, 0x1483B0, 128),
            ]:
                call(u, selector, (actor,))
                pointer = u.reg_read(UC_ARM_REG_R0)
                actual = bytes(u.mem_read(pointer, 32)).split(b'\0')[0].decode('ascii')
                assert actual == text
                source_pointer = struct.unpack_from('<I', clean, table + state * 4)[0]
                japanese = clean[source_pointer - 0x02000000:].split(b'\0')[0].decode('cp932')
                ink, bounds = complete_mask(font, text, image, 56, y, (230, 230, 230))
                # Check unused cells through the entire original 48x16 field.
                for dy in range(16):
                    for dx in range(48):
                        char = dx // 6
                        expected = (dy < 11 and char < len(text)
                                    and bool(font.decode(text[char]).getpixel((dx % 6, dy))))
                        assert (image.getpixel((56 + dx, y + dy)) == (230, 230, 230)) == expected
                labels.append({'group': group, 'state': state, 'Japanese': japanese,
                               'English': text, 'native_pointer': pointer, 'complete_ink_pixels': ink,
                               'bounds': bounds, 'all48x16_field_pixels_and_first_final_glyph_cells_exact': True})
            complete_mask(font, name, image, 84, 30, (230, 230, 230))
            for rect in ((0, 104, 50, 120), (0, 124, 50, 140)):
                assert image.crop(rect).tobytes() == baseline.crop(rect).tobytes()
            cases.append({'actor': name, 'actor_id': actor_id, 'frame': frame, 'image': str(path),
                          'labels': labels, 'Health_and_Mood_plaque_pixels_unchanged': True})
    campaign = json.loads(Path('translations/graphics_completion_campaign_v1.json').read_text())
    plaques = campaign['plaque_style_v247']['ongoing_plaque_inventory']
    assert len(plaques) == 18 and all(not row['fully_completed'] for row in plaques)
    proof = {'candidate': str(ROM), 'candidate_sha256': digest,
             'report': str(report_path), 'report_sha256': sha(report_path.read_bytes()),
             'all13_labels_on_both_captain_and_ordinary_crew_actual_GPU_verified': True,
             'complete_field_masks': cases, 'user_authorized_synthetic_conditions': True,
             'natural_hazard_injury_death_or_recovery_events_not_claimed': True,
             'only_two_condition_bytes_per_fixture_permitted': True,
             'original_captain_binding_and_condition_getter_code_exact_to_source': True,
             'donor_save_and_production_ROM_unchanged': True,
             'initial_wrong_ordinary_reference_attempt_excluded': str(OUT / 'initial_attempt.json'),
             'all18_plaques_remain_incomplete': True, 'full_goal_complete': False,
             'hardware_device_verification': False}
    (OUT / 'condition_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('All13 labels on Maria and Xien: 28 complete48x16 GPU masks; original binding, only condition bytes, plaques and donor preservation pass.')


if __name__ == '__main__':
    main()
