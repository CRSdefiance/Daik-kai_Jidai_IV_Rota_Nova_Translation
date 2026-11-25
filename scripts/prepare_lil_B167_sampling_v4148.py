"""Derive bounded cold boots of both sail-lesson choices using ordinary input."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B167_sampling_tools_v4148')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/run_lil_B166_display_fixture_v4103.py','scripts/run_lil_B167_display_fixture_v4149.py',{
        'B166':'B167','lil_B166_display_fixture_v4101':'lil_B167_display_fixture_v4147',
        'lil_B166_display_run_v4103':'lil_B167_display_run_v4149',
        'lil_B166_display_v4103':'lil_B167_display_v4149',
        'source_event166':'source_event167',"'displayed_original_source_block':166":"'displayed_original_source_block':167",
        'requested_advice_option':'requested_sail_lesson_option','19501':'13901','20001':'14401'
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tools=[tool],frames_per_cold_boot=14401,source_blocks=[167],original_menu_indices=[0,1],source_complete_no_flattening_or_effect_omission=True,option1_DOWN_scheduled_from_its_own_terminal_option0_observation=True,no_gameplay_coverage_added_by_tool_creation=True))
