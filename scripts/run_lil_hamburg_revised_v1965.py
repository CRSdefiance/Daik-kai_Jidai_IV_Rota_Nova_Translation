"""Cold boot revised B74 using the disclosed original Hamburg access replay."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read

SOURCE = Path('scripts/run_lil_speyer_context_v1920.py')
SOURCE_SHA = '266f4661bda3aae83ddd5a8aba080998239c3a243b0f4f70dae428c799d4ea10'

if __name__ == '__main__':
    assert sha(SOURCE.read_bytes()) == SOURCE_SHA
    assert read('work/analysis/lil_Speyer_access_run_v1924/terminal.json')['terminal']
    assert read('work/analysis/lil_Hamburg_loader_v1962/whole_SC2_and_B74_initial_entry_proof.json')['all336_whole_blocks_and672_modes_each_pass']
    assert read('work/analysis/lil_Hamburg_font_approval_v1959/approval_receipt.json')['original79_speeches_observed_new79_planes632_macro_cases']
    assert read('work/analysis/lil_Hamburg_reference_census_v1963/all123_commands20_relative_sites_and_shipped_entry_census.json')['all123_clean_current_target_commands_and20_relative_sites_reexecuted']
    text = SOURCE.read_text(encoding='utf-8')
    changes = {
        "ROM = Path('out/all_routes_combined_v1909_candidate.nds')":"ROM = Path('work/analysis/lil_Hamburg_research_v1961/lil_Hamburg_V1945_derived_RESEARCH_ONLY.nds')",
        'from scripts.native_lil_london_location_v1883 import apply_fixture':'from scripts.native_lil_speyer_access_v1923 import apply_fixture',
        "ROOT = Path('work/analysis/lil_Speyer_context_run_v1920')":"ROOT = Path('work/analysis/lil_Hamburg_revised_run_v1965')",
        'lil_Speyer_context_run_v1920_RESEARCH_ONLY':'lil_Hamburg_revised_run_v1965_RESEARCH_ONLY',
        "source_run = Path('work/analysis/lil_London_revised_run_v1903')":"source_run = Path('work/analysis/lil_Speyer_access_run_v1924')",
        "read(source_run/'terminal.json')['frame'] == 86310":"read(source_run/'terminal.json')['frame'] == 93780",
        "assert digest == plan['research_ROM_sha256'] == read('work/analysis/lil_London_release_v1908b/registered_release_verification.json')['candidate_sha256']":
            "assert digest == read('work/analysis/lil_Hamburg_research_v1961/research_image_receipt.json')['research_ROM_sha256']\n    assert plan['research_ROM_sha256'] == read('work/analysis/lil_Speyer_original_audit_v1935b/original_Hamburg79_Speyer51_and_three_access_fixture_audit.json')['candidate_sha256']",
        "r.get('until',999999) <= 86310":"r.get('until',999999) <= 49440",
        "assert commands[-1]['until'] == 86310":"assert commands[-1]['until'] == 49440",
        "registered_profile='all-routes-unified-v1909'":"registered_profile=None,parent_registered_profile='all-routes-unified-v1945',unregistered_research_only=True",
        'replay_target_frame=86310':'replay_target_frame=49440',
        "inherited_three_coordinate_only_fixture_paths=plan['declared_each16_byte_location_only_fixtures']":
            "inherited_two_coordinate_only_fixture_paths=plan['inherited_two_coordinate_only_fixture_paths']",
        'future_Speyer_access_fixtures_must_be_separately_source_bound_and_disclosed=True':
            "declared_Speyer_access_fixture='scripts/native_lil_speyer_access_v1923.py',synthetic_funds=60000,Speyer_fixture_owned_bytes=20",
    }
    for old,new in changes.items():
        assert text.count(old) == 1,(old,text.count(old))
        text = text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
