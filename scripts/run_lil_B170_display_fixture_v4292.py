"""Cold boot complete retained B170 content with ordinary input and read-only observation."""
import argparse
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', choices=['clean_Japanese', 'reviewed_English'], required=True)
    case = parser.parse_args().case
    fixture_path = Path('work/analysis/lil_B170_display_fixture_v4291/complete_effect_preserving_B22_fixtures.json')
    fixture = read(fixture_path)
    selected = next(row for row in fixture['fixtures'] if row['case'] == case)
    source = Path('scripts/run_lil_opening_trace_v1706.py')
    text = source.read_text(encoding='utf-8')
    root = f'work/analysis/lil_B170_display_run_v4292_{case}'
    capture = f'E:/Rota Nova translations/Generated/work/emulation_v193/lil_B170_display_v4292_{case}'
    changes = [
        ('from scripts.prepare_lil_opening_research_v1704 import ROM', "ROM=Path(SELECTED['research_ROM'])"),
        ("ROOT=Path('work/analysis/lil_opening_trace_v1706')", 'ROOT=Path(' + repr(root) + ')'),
        ("CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_opening_trace_v1706_RESEARCH_ONLY')", 'CAP=Path(' + repr(capture) + ')'),
        ("receipt=read('work/analysis/lil_opening_research_v1704/research_image_receipt.json')", 'receipt=SELECTED'),
        ("inputs=Path('work/analysis/movie_viewport_v303/lil_start_inputs.json')", "base_inputs=Path('work/analysis/movie_viewport_v303/lil_start_inputs.json');inputs=ROOT/'inputs.json'"),
        ("assert sha(inputs.read_bytes())=='097df0c69d30d00532373b2b8b7fe2f5969ba581a0bd35e27074c22749631541'", "assert sha(base_inputs.read_bytes())=='097df0c69d30d00532373b2b8b7fe2f5969ba581a0bd35e27074c22749631541'"),
        ("ROOT.mkdir(parents=True);(ROOT/'source_contract.json')", "ROOT.mkdir(parents=True);save(inputs,read(base_inputs)+[dict(start=f,duration=5,buttons=['A']) for f in range(2600,19501,240)]);(ROOT/'source_contract.json')"),
        ('no_save_savestate_or_gameplay_fixtures', 'no_save_or_savestate_or_RAM_fixtures'),
        ("'only_ROM_ROOT_globals_rebound_for_current_source':True", "'only_observer_ROM_ROOT_globals_rebound':True,'explicit_B22_entry_ROM_fixture':True,'source_event170_not_selected':True,'displayed_original_source_block':170,'all_source_commands_and_later_A000_retained':True,'fixture_manifest':str(FIXTUREPATH),'fixture_manifest_sha256':sha(FIXTUREPATH.read_bytes())"),
        ("'--frames','100000'", "'--frames','20001'"),
        ("'--capture-at','4000','6000','--pause-at','6000'", "'--capture-at',*map(str,range(2350,20001,60))"),
        ("'--dump-capture-ram','--dump-pause-ram','--dump-ram'", "'--dump-ram'"),
        ('no_gameplay_fixture_save_or_ROM_runtime_edit', 'no_savestate_or_emulated_RAM_runtime_fixture'),
    ]
    for old, new in changes:
        assert old in text, old
        text = text.replace(old, new)
    exec(compile(text, str(source) + '::B170-complete-retained-content-fixture', 'exec'),
         dict(__name__='__main__', __file__=__file__, SELECTED=selected, FIXTUREPATH=fixture_path))
