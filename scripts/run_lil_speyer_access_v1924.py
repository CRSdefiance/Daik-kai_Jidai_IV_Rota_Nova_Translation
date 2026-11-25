"""Shorter cold-boot Speyer sample: two prior coordinates, then disclosed20-byte access."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read

SOURCE = Path('scripts/run_lil_speyer_context_v1920.py')
SOURCE_SHA = '266f4661bda3aae83ddd5a8aba080998239c3a243b0f4f70dae428c799d4ea10'

if __name__ == '__main__':
    assert sha(SOURCE.read_bytes()) == SOURCE_SHA
    assert read('work/analysis/lil_Speyer_context_run_v1920/terminal.json')['terminal']
    preflight = read('work/analysis/lil_Speyer_access_v1923/twenty_byte_access_preflight.json')
    assert preflight['only16_coordinates_and4_company_funds_bytes_owned']
    assert len(preflight['negative_controls']) == 3
    text = SOURCE.read_text(encoding='utf-8')
    changes = {
        'from scripts.native_lil_london_location_v1883 import apply_fixture':
            'from scripts.native_lil_speyer_access_v1923 import apply_fixture, REQUEST',
        "ROOT = Path('work/analysis/lil_Speyer_context_run_v1920')":"ROOT = Path('work/analysis/lil_Speyer_access_run_v1924')",
        'lil_Speyer_context_run_v1920_RESEARCH_ONLY':'lil_Speyer_access_run_v1924_RESEARCH_ONLY',
        "r.get('until',999999) <= 86310":"r.get('until',999999) <= 48810",
        "assert commands[-1]['until'] == 86310":"assert commands[-1]['until'] == 48810\n    commands.append(dict(until=48840,battle_fixture=REQUEST,duration=1))",
        'replay_target_frame=86310':'replay_target_frame=48840',
        "inherited_three_coordinate_only_fixture_paths=plan['declared_each16_byte_location_only_fixtures']":
            "inherited_two_coordinate_only_fixture_paths=plan['declared_each16_byte_location_only_fixtures'][:2]",
        'future_Speyer_access_fixtures_must_be_separately_source_bound_and_disclosed=True':
            "declared_Speyer_access_fixture='scripts/native_lil_speyer_access_v1923.py',declared_Speyer_access_preflight='work/analysis/lil_Speyer_access_v1923/twenty_byte_access_preflight.json',synthetic_funds=60000,Speyer_fixture_owned_bytes=20",
    }
    for old,new in changes.items():
        assert text.count(old) == 1,old
        text = text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
