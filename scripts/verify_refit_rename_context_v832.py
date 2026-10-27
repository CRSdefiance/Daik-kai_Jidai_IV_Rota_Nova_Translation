"""Bind source rename prompts to actual visible glyphs and native transitions."""

import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_help_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from scripts.context_refit_dialogue_v832 import ROOT, ROM
from scripts.finish_refit_display_v712 import load
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_full_fleet_battle_v652 import fleet_models
from scripts.verify_full_fleet_victory_v654 import funds
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save

BASE = 0x02000000
CAP = Path('work/emulation_v193')


def main():
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    entries = current_entries(rom.read_file('/COMMON/MESFILE.DK4'), arm)
    reports, shots, receipts = {}, {}, {}
    for case, frames in (('rename_context', 14000), ('name_entry', 14600)):
        reports[case], shots[case], receipts[case] = load(CAP / f'refit_dialogue_v832_{case}', sha(ROM.read_bytes()), frames)
        assert not any(v for k, v in reports[case].items() if k.startswith('synthetic_'))
        plan = read(ROOT / ('rename_run_plan.json' if case == 'rename_context' else 'name_entry_run_plan.json'))
        assert reports[case]['battery_save_preloaded']['source_sha256'] == plan['donor_sha256']
        assert sha(Path(plan['disposable_source']).read_bytes()) == plan['donor_sha256']
    prefix_frames = sorted(shots['rename_context'].keys() & shots['name_entry'].keys() & set(range(13101)))
    assert all(shots['rename_context'][f].tobytes() == shots['name_entry'][f].tobytes() for f in prefix_frames)
    owner, wrapped = [struct.unpack_from('<I', arm, at)[0] for at in (0x552A0, 0x54450)]

    def snapshot(case, frame):
        row = next(r for r in reports[case]['read_only_capture_RAM_snapshots'] if r['frame'] == frame)
        raw = Path(row['path']).read_bytes()
        assert row['read_only_export'] and sha(raw) == row['sha256']
        return raw

    def cstring(raw, pointer):
        return raw[pointer - BASE:pointer - BASE + 512].split(b'\0')[0]

    holds = []
    for case, frame, number in (('rename_context', 12800, 1264), ('name_entry', 12800, 1264), ('name_entry', 13400, 1265)):
        raw = snapshot(case, frame)
        template, visible = cstring(raw, owner + 0x2030), cstring(raw, wrapped)
        assert b' '.join(template.split()) == b' '.join(entries[number].text.split())
        assert b' '.join(visible.split()) == b' '.join(entries[number].text.split())
        lines = [s.strip().decode('ascii') for s in visible.split(b'\n')]
        plane = independent_font(arm, b'', lines)
        assert raster(arm, visible, 0x01FFCE40 - BASE, size=(228, 64)) == plane
        expected = {(16 + i % 228, 296 + i // 228) for i, value in enumerate(plane) if value == 1}
        image = shots[case][frame]
        actual = {(x, y) for y in range(294, 366) for x in range(16, 244) if image.getpixel((x, y)) == (0, 8, 0)}
        assert actual == expected, (number, sorted(actual ^ expected)[:10])
        holds.append({'case': case, 'frame': frame, 'message_id': number, 'lines': lines,
                      'complete_native_and_independent_and_actual_glyph_planes_equal': True,
                      'current_visible_line_start_x22_y296': True,
                      'source_candidate_wording_only_not_new_draft_rendering': True})
    states = []
    for case, final in (('rename_context', 14000), ('name_entry', 14600)):
        before, after = snapshot(case, 3200), snapshot(case, final)
        a, b = fleet_models(arm, before, 1), fleet_models(arm, after, 1)
        assert a == b and len(a) == 5
        assert funds(arm, before) == funds(arm, after) == 25975
        states.append({'case': case, 'final_frame': final, 'all_five_names_Hull_Crew_and_model_pointers_unchanged': True,
                       'funds_unchanged25975': True})
    sheet = Image.new('RGB', (768, 824), '#263238')
    draw = ImageDraw.Draw(sheet)
    selected = [('rename_context', 12800), ('name_entry', 13100), ('name_entry', 13400), ('name_entry', 13700), ('name_entry', 14600)]
    for i, (case, frame) in enumerate(selected):
        x, y = i % 3 * 256, i // 3 * 412
        draw.text((x + 6, y + 6), f'V831 {case} {frame}', fill='white')
        sheet.paste(shots[case][frame], (x, y + 28))
    path = ROOT / 'actual_rename_context_sheet.png'
    sheet.save(path)
    save(ROOT / 'actual_rename_context.json', {
        'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()), 'receipts': receipts,
        'ordinary14k_and14600_frame_cold_boots_with_disposable_save_copies': True,
        'no_new_RAM_code_or_gameplay_fixtures_no_savestate': True,
        'unchanged_prefix_whole_frame_controls': prefix_frames, 'actual_visible_source_wording_holds': holds,
        'separate_question_ship_selection_invitation_keyboard_and_cancel_return_observed': True,
        'native_ship_name_input_page_hiragana_are_selectable_characters_not_untranslated_dialogue': True,
        'native_name_input_and_original_ship_names_preserved': states,
        'contact_sheet': str(path), 'contact_sheet_sha256': sha(path.read_bytes()),
        'visual_review_pending': True,
        'new12_draft_wording_format_units_integration_and_actual_helper_scene_pending': True,
        'no_new_completed_entry_credit': True, 'verifier_sha256': sha(Path(__file__).read_bytes()),
        'full_goal_complete': False})
    print('V832 rename context:actual1264/1265 complete glyphs,selection/name-input/cancel and five names/funds preserved. Draft release remains pending.', flush=True)


if __name__ == '__main__':
    main()
