"""Bind directly viewed Lil361 body/menu pages without claiming the unresolved host exit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/approve_lil269_actual_v1.py').read_text(encoding='utf-8'), {
    'work/Lil269_B243_B282_clean_20261110': 'work/Lil361_B283_B298_clean_20261110',
    "['Lil269_expedition_figurehead', 'Lil269_ruins_riddle', 'Lil269_spy_capture_rewards']":
        "['Lil361_forest_London', 'Lil361_cave_Angkor', 'Lil361_fog_wristband']",
    "ROOT / 'gameplay_review_v1.json'": "ROOT / 'gameplay_pages_review_v1.json'",
    'formatting_v2/formatting_input.json': 'formatting_v1/formatting_input.json',
    "    transitionspath = ROOT / 'transition_review_v1/receipt.json'\n    transitions = load(transitionspath)\n    assert transitions['initialized_QA_hosts_reach_resupply_andfollowing_native_tutorial']\n    assert transitions['free_sailing_not_claimed']\n": '',
    '[nativepath, sourcepath, transitionspath, Path(__file__)]': '[nativepath, sourcepath, Path(__file__)]',
    'for i in range(2)': 'for i in range(3)',
    '{(250, 470): [0], (251, 270): [1, 2], (251, 1752): [1]}':
        '{(283, 884): [1, 2], (283, 1938): [0, 1], (288, 2436): [0, 1], (293, 1620): [0]}',
    'display_run{i}_v1': 'actual_run{i}_v1',
    '[5, 3, 5][i]': '[4, 7, 7][i]',
    "        for sheet in [transitions['runs'][i]['review_sheet']]:\n            assert digest(sheet['path']) == sheet['sha256']\n            sheets.append({**sheet, 'directly_viewed': True})\n": '',
    'if i < 2:': 'if i < 3:',
    '(139, 141, 141, 64563)': '(199, 200, 200, 64563)',
    '== 123 and len(styles) == 2 and len(captions) == 7': '== 153 and len(styles) == 24 and len(captions) == 9',
    'len(turns) == 2 and len(FE_returns) == 21 and len(sheets) == 18':
        'len(turns) == 1 and len(FE_returns) == 15 and len(sheets) == 21',
    "'DK4_MES_B251_R0009'": "'DK4_MES_B292_R0050'",
    'distinct_source_body_objects=139': 'distinct_source_body_objects=199',
    'observed_pages_including_repeats=141, distinct_body_pages=141, offline_only_source_body_objects=123':
        'observed_pages_including_repeats=200, distinct_body_pages=200, offline_only_source_body_objects=153',
    'actual_caption_strings=7': 'actual_caption_strings=9',
    'actual_menus=3': 'actual_menus=4',
    'all_actual_body_menu_andtransition_sheets_directly_viewed=True':
        'all_actual_body_andmenu_sheets_directly_viewed=True, host_exit_transition_approval_pending=True',
    'repaired_riddle_complete_with_normal_A_return_observed=True':
        'repaired_R50_FE_no_blank_row_andnormal_A_return_observed=True',
    'three_choice_Right_andtwo_choice_No_cursor_andfollowing_A_return_observed=True':
        'three_choice_Other_andtwo_choice_Run_andWait_cursors_andfollowing_A_returns_observed=True',
    'complete_QA_host_nonspeech_setup_cleanup_andfollowing_tutorial_observed=True':
        'complete_QA_host_nonspeech_setup_cleanup_andfollowing_tutorial_observed=False',
    "PASS139 bodies/141 pages,2 turns,21 FE returns,3 menus and18 directly viewed sheets;123 bodies offline-only.":
        'PASS199 bodies/200 pages,1 turn,15 FE returns,4 menus and21 directly viewed sheets;153 bodies offline-only. Host exit remains pending.',
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-pixel-tile-input-andmenu-guards-with-explicit-host-exit-exclusion', 'exec'), globals())
