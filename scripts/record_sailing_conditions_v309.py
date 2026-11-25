"""Verify actual English reef warning and preserve open graphics audit scope."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_sailing_conditions_v309 import ROOT
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_sailing_conditions_release_v309 import ROM, read


def main():
    proof = read(ROOT / 'release_proof.json')
    report_path = Path('work/emulation_v193/sailing_conditions_v309/capture_report.json')
    report = read(report_path)
    source = read('work/emulation_v193/weapon_acquisition_v309/capture_report.json')
    assert report['ROM_sha256'] == proof['candidate_sha256'] == sha(ROM.read_bytes())
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames'] == 30000 and report['scripted_input_schedule'] == read(ROOT / 'reef_replay_inputs.json')
    assert report['scripted_input_schedule'] == [r for r in source['scripted_input_schedule'] if r['start'] <= 28800]
    frames = {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        frames[row['frame']] = row
    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file('/__arm9__.bin'))
    shot = Image.open(frames[28800]['path']).convert('RGB')
    matches = []
    for color in ((0, 8, 0), (0, 0, 0), (8, 8, 8)):
        for y in range(293, 310):
            for x in range(8, 26):
                try:
                    count, bounds = complete_mask(font, 'Admiral! Reefs!', shot, x, y, color)
                    matches.append({'text': 'Admiral! Reefs!', 'complete_ink_pixels': count, 'bounds': bounds,
                                    'color': color, 'first_internal_and_final_glyph_and_blank_cells_exact': True})
                except ValueError:
                    pass
    assert len(matches) == 1, matches
    unchanged, changed = [], []
    seen = set()
    for row in source['frames_captured']:
        number = row['frame']
        if number > 28800 or number not in frames or number in seen:
            continue
        seen.add(number)
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        old = Image.open(row['path']).convert('RGB')
        new = Image.open(frames[number]['path']).convert('RGB')
        delta = [(x, y) for y in range(384) for x in range(256) if old.getpixel((x, y)) != new.getpixel((x, y))]
        if delta:
            assert number >= 28000 and all(8 <= x < 248 and 293 <= y < 368 for x, y in delta), (number, delta[:5])
            changed.append({'frame': number, 'changed_pixels_only_inside_warning_text': len(delta)})
        else:
            unchanged.append(number)
    assert changed and unchanged
    proof.update({'actual_English_reef_warning_pending': False, 'fresh_cold_boot_frames': 30000,
                  'capture_report': str(report_path), 'capture_report_sha256': sha(report_path.read_bytes()),
                  'actual_warning_font_case': matches[0], 'unchanged_comparable_whole_frames': unchanged,
                  'changed_comparable_frames': changed,
                  'actual_warning_visually_reviewed': True,
                  'all26_conditions_physical_gameplay_contexts_verified': False,
                  'weapon_armor_acquired_in_this_run': False,
                  'all18_plaque_entries_and_variants_remain_incomplete': True,
                  'experimental_user_acceptance_pending': True,
                  'documentation': 'docs/sailing_condition_names_v309.md'})
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for name in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        path = Path('translations') / name
        audit = read(path)
        assert not audit['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        group = audit['plaque_style_v247']
        assert len(group['ongoing_plaque_inventory']) == 18 and not group['full_plaque_audit_complete']
        assert all(not r['fully_completed'] for r in group['ongoing_plaque_inventory'])
        for row in group['ongoing_plaque_inventory']:
            assert all(not v['fully_completed'] for v in row.get('observed_variants', []))
        audit['sailing_condition_names_v309'] = {**proof, 'release_proof': str(ROOT / 'release_proof.json'),
                                                'native_proof': str(ROOT / 'native_proof.json')}
        audit['latest_candidate'], audit['latest_candidate_sha256'] = str(ROM), proof['candidate_sha256']
        path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    section = '''## V309: shared sailing condition names

Ordinary sailing exposed an untranslated Japanese reef warning. All26 original
condition names now have complete English in the existing owned staged pool.
All30 native valid/invalid selector cases,26 complete native font rasters and
startup/cache/arena checks pass. The same ordinary30,000-frame cold boot now
shows the complete Admiral! Reefs! warning; comparable changes remain within
the warning text. Every470 inherited batch, art asset, route/COMMON/HELP file,
ARM7 and overlay is retained. V307 reproduces before/after the builder change;
the clean-input patch reconstructs V309 exactly. Experimental; broader actual
conditions, occupied Weapon/Armor and all18 plaque entries remain open. Online
images exempt. See [V309 evidence](sailing_condition_names_v309.md).

'''
    for name in ('translation_progress.md', 'known_issues.md', 'todo.md'):
        path = Path('docs') / name
        content = path.read_text(encoding='utf-8')
        if '## V309:' not in content:
            title, rest = content.split('\n\n', 1)
            path.write_text(title + '\n\n' + section + rest, encoding='utf-8')
    print(json.dumps({'current_ROM': str(ROM), 'actual_warning': matches[0],
                      'unchanged_whole_frames': len(unchanged), 'changed_frames': changed}))


if __name__ == '__main__':
    main()
