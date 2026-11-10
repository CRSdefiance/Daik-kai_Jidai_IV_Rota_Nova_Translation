"""Seal the directly viewed Lil254 emulator sample and its native returns."""

from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(Path('scripts/approve_lil269_actual_v1.py').read_text(encoding='utf-8'), {
    'work/Lil269_B243_B282_clean_20261110': 'work/Lil254_B312_B319_clean_20261110',
    "['Lil269_expedition_figurehead', 'Lil269_ruins_riddle', 'Lil269_spy_capture_rewards']":
        "['Lil254_wolf_ruins_trade']",
    'range(2)': 'range(1)',
    'actual_menus{i}_v1': 'actual_menus_returns{i}_v1',
    'display_run{i}_v1': 'actual_run{i}_v1',
    'actual_sheets{i}_v1/receipt.json': 'actual_sheets{i}_v1/sheets.json',
    '{(250, 470): [0], (251, 270): [1, 2], (251, 1752): [1]}':
        '{(312, 754): [1, 2], (314, 684): [0, 1], (316, 812): [0, 1]}',
    "        assert digest(plan['fixture']) == plan['fixture_sha256'] and not plan['existing_system_only_unlock_not_earned']":
        "        assert digest(plan['fixture']) == plan['fixture_sha256']\n"
        "        assert plan['no_savestate_battery_or_emulated_memory_override']\n"
        "        assert not fixture['preexisting_system_only_unlock_required_not_earned']\n"
        "        assert digest(terminal['report']) == terminal['report_sha256']\n"
        "        report = load(terminal['report'])\n"
        "        assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded')",
    "receipt['actual_pixel_proof_sha256']": "receipt['actual_sha256']",
    "receipt['actual_dialogue_pages'] == pixel['selected_pages'] and not receipt['full_scene_sheets']":
        "receipt['pages'] == pixel['selected_pages'] and receipt['lower_screen_only']",
    "len(receipt['bottom_screen_sheets']) == [5, 3, 5][i]": "len(receipt['sheets']) == 5",
    "enumerate(receipt['bottom_screen_sheets'])": "enumerate(receipt['sheets'])",
    "sheet['full_original_capture_refs'] == [s['capture'] for s in part]":
        "sheet['pages'] == [{k: s[k] for k in ('id', 'page', 'capture')} for s in part]",
    'n // 3 * 410 + 25': 'n // 3 * 410 + 26',
    'if i < 2:': 'if i == 0:',
    '(139, 141, 141, 64563)': '(53, 58, 58, 25841)',
    '== 123 and len(styles) == 2 and len(captions) == 7': '== 193 and len(styles) == 4 and len(captions) == 8',
    'len(turns) == 2 and len(FE_returns) == 21 and len(sheets) == 18':
        'len(turns) == 5 and len(FE_returns) == 7 and len(sheets) == 7',
    "    assert 'DK4_MES_B251_R0009' in {r['id'] for r in FE_returns}":
        "    assert 'DK4_MES_B316_R0205' in {r['id'] for r in FE_returns}\n"
        "    assert {'DK4_MES_B317_R0030', 'DK4_MES_B317_R0043', 'DK4_MES_B319_R0008'} <= observed\n"
        "    assert any(h['source_selector'] == 0 and h['text'] == 'Rafael Castor' for h in headers)",
    'frames=64563, initialized_runs=3': 'frames=25841, initialized_runs=1',
    'distinct_source_body_objects=139': 'distinct_source_body_objects=53',
    'observed_pages_including_repeats=141, distinct_body_pages=141, offline_only_source_body_objects=123':
        'observed_pages_including_repeats=58, distinct_body_pages=58, offline_only_source_body_objects=193',
    'actual_caption_strings=7': 'actual_caption_strings=8',
    'repaired_riddle_complete_with_normal_A_return_observed=True':
        'repaired_B316_alert_and_B319_company_substitution_observed=True, both_B317_source_selector_00_headers_observed=True',
    'three_choice_Right_andtwo_choice_No_cursor_andfollowing_A_return_observed=True':
        'all_three_menus_and_following_A_returns_observed=True',
    'PASS139 bodies/141 pages,2 turns,21 FE returns,3 menus and18 directly viewed sheets;123 bodies offline-only.':
        'PASS 53 bodies, 58 pages, five turns, seven FE returns, three menus, and seven directly viewed sheets. 193 bodies remain offline-only.',
})


if __name__ == '__main__':
    exec(compile(source, __file__, 'exec'), globals())
