"""Prepare complete B177 content fixtures and ordinary-input paired cold boots."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B177_display_preparation_v4635')
assert not ROOT.exists()
tools=[derive('scripts/research_lil_B176_display_fixture_v4585.py','scripts/research_lil_B177_display_fixture_v4635.py',{
    'B176':'B177','lil_B176':'lil_B177','display_fixture_v4585':'display_fixture_v4635',
    'all_routes_combined_v4541':'all_routes_combined_v4595','relocation_v4575':'relocation_v4625',
    'editorial_manuscript_v3':'editorial_manuscript_v5','bank[176]':'bank[177]','source_block=176':'source_block=177',
    'display_v4585':'display_v4635','source_event176_not_selected':'source_event177_not_selected',
    'closing_notice_names_Seville':'closing_notice_names_Genoa',
})]
tools.append(derive('scripts/prepare_lil_B176_display_runner_v4586.py','scripts/prepare_lil_B177_display_runner_v4636.py',{
    'B176':'B177','lil_B176':'lil_B177','display_tools_v4586':'display_tools_v4636',
    "derive('scripts/run_lil_B175_display_fixture_v4533.py','scripts/run_lil_B176_display_fixture_v4587.py'":
        "derive('scripts/run_lil_B176_display_fixture_v4587.py','scripts/run_lil_B177_display_fixture_v4637.py'",
    "'B175':'B176','lil_B175':'lil_B176','display_fixture_v4531':'display_fixture_v4585'":
        "'B176':'B177','lil_B176':'lil_B177','display_fixture_v4585':'display_fixture_v4635'",
    "'display_run_v4533':'display_run_v4587','display_v4533':'display_v4587'":
        "'display_run_v4587':'display_run_v4637','display_v4587':'display_v4637'",
    "'source_event175_not_selected':'source_event176_not_selected'":
        "'source_event176_not_selected':'source_event177_not_selected'",
    '"\'displayed_original_source_block\':175":"\'displayed_original_source_block\':176"':
        '"\'displayed_original_source_block\':176":"\'displayed_original_source_block\':177"',
    "        'all_source39_commands_23_progressive9_FE_resource_three_presentations_C200_and_two_ends_retained':\n            'all_source13_commands_9_progressive1_impersonal_FE_A000_C200_and_single_end_retained',\n":'',
    "        'range(2600,15501,240)':'range(2600,8501,240)',\n":'',
    '        "\'requested_frames\':16001":"\'requested_frames\':9001",\n':'',
    '        "\'--frames\',\'16001\'":"\'--frames\',\'9001\'",\n':'',
    "        'range(2350,16001,60)':'range(2350,9001,60)',\n":'',
    'display_fixture_v4585/complete_B176_B22_fixtures':'display_fixture_v4635/complete_B177_B22_fixtures',
}))
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tools=tools,source_commands=13,fixture_commands=22,
    source_A000=1,original_prelude_A000=4,source_speeches=10,source_FE=1,
    four_row_R12_target_preserved=True,no_ROM_registry_ledger_orcredit_change_yet=True,full_goal_complete=False))
