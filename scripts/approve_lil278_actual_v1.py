"""Bind the directly viewed Lil278 gameplay sample to its native and input evidence."""

from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(Path('scripts/approve_lil269_actual_v1.py').read_text(encoding='utf-8'), {
    'work/Lil269_B243_B282_clean_20261110': 'work/Lil278_B299_B311_clean_20261110',
    "['Lil269_expedition_figurehead', 'Lil269_ruins_riddle', 'Lil269_spy_capture_rewards']":
        "['Lil278_expedition_spices_temple']",
    'formatting_v2/formatting_input.json': 'formatting_v1/formatting_input.json',
    'for i in range(2)': 'for i in range(1)',
    'actual_menus{i}_v1': 'actual_menus_returns{i}_v1',
    '{(250, 470): [0], (251, 270): [1, 2], (251, 1752): [1]}':
        '{(299, 908): [0, 1], (301, 918): [1], (306, 706): [0, 1]}',
    'display_run{i}_v1': 'actual_run{i}_v1',
    "        assert digest(plan['fixture']) == plan['fixture_sha256'] and not plan['existing_system_only_unlock_not_earned']":
        """        assert digest(plan['fixture']) == plan['fixture_sha256']
        assert plan['no_savestate_battery_or_emulated_memory_override']
        assert not fixture['preexisting_system_only_unlock_required_not_earned']
        assert digest(terminal['report']) == terminal['report_sha256']
        report = load(terminal['report'])
        assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded')""",
    '[5, 3, 5][i]': '5',
    'if i < 2:': 'if i == 0:',
    '(139, 141, 141, 64563)': '(52, 55, 55, 25121)',
    '== 123 and len(styles) == 2 and len(captions) == 7': '== 220 and len(styles) == 5 and len(captions) == 6',
    'len(turns) == 2 and len(FE_returns) == 21 and len(sheets) == 18':
        'len(turns) == 3 and len(FE_returns) == 8 and len(sheets) == 7',
    "'DK4_MES_B251_R0009' in {r['id'] for r in FE_returns}":
        "'DK4_MES_B304_R0051' in {r['id'] for r in turns}",
    'frames=64563, initialized_runs=3': 'frames=25121, initialized_runs=1',
    'distinct_source_body_objects=139': 'distinct_source_body_objects=52',
    'observed_pages_including_repeats=141, distinct_body_pages=141, offline_only_source_body_objects=123':
        'observed_pages_including_repeats=55, distinct_body_pages=55, offline_only_source_body_objects=220',
    'actual_caption_strings=7': 'actual_caption_strings=6',
    'repaired_riddle_complete_with_normal_A_return_observed=True':
        'revised_Basra_Market_Info_page_turn_observed=True',
    'three_choice_Right_andtwo_choice_No_cursor_andfollowing_A_return_observed=True':
        'all_three_two_choice_menus_and_following_A_returns_observed=True',
    'PASS139 bodies/141 pages,2 turns,21 FE returns,3 menus and18 directly viewed sheets;123 bodies offline-only.':
        'PASS 52 bodies/55 pages, three page turns, eight FE returns, three menus and seven directly viewed sheets. 220 bodies remain offline-only.',
})


if __name__ == '__main__':
    exec(compile(source, __file__, 'exec'), globals())
