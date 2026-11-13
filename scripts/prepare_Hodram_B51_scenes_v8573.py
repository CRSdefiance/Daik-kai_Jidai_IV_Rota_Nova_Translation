"""Prepare full-source/full-revised B51 entry fixtures and read-only observers."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__ == '__main__':
    root = Path('work/analysis/Hodram_B51_scene_tools_v8573')
    assert not root.exists()
    fixtures = derive('scripts/create_Hodram_B50_fixtures_v8504.py', 'scripts/create_Hodram_B51_fixtures_v8573.py', {
        'Hodram_B50_fixtures_v8504': 'Hodram_B51_fixtures_v8573',
        'Hodram_B50_reference_v8502': 'Hodram_B51_reference_v8570b',
        'Hodram_B50_references_v8503': 'Hodram_B51_references_v8572',
        'Hodram_B50_current_v8488': 'Hodram_B51_current_v8559',
        'all12_commands3_full_preambles_source_FE_item_hide_effects_terminal_andtails_bound':
            'all20_commands5_full_preambles8_relatives2_queries4_opaque_controls_andterminal_bound',
        '_v8504_RESEARCH_ONLY.nds': '_v8573_RESEARCH_ONLY.nds',
        "sum(len(f['all_original_exchange_commands']) for f in fixtures)==24": "sum(len(f['all_original_exchange_commands']) for f in fixtures)==40",
        'all12_commands3_speeches_zero_relative_query_choice_sites_preserved_perversion': 'all20_commands5_speeches8_relative_sites2_queries_preserved_perversion',
        'registered_current_V8475_mainV4701_unchanged': 'registered_current_V8543_mainV4701_unchanged',
        'B50': 'B51',
        'all12commands3speeches0relatives perversion': 'all20commands5speeches8relatives2queries perversion',
    })
    runner = derive('scripts/run_Hodram_B49_v8407.py', 'scripts/run_Hodram_B51_v8574.py', {
        'Hodram_B49_scene_runs_v8407': 'Hodram_B51_scene_runs_v8574',
        'Hodram_B49_fixtures_v8406': 'Hodram_B51_fixtures_v8573',
        'choices=[49]': 'choices=[51]',
        'frames={49:10001}[block]': 'frames={51:10001}[block]',
        '_v8407': '_v8574',
    })
    root.mkdir(parents=True)
    save(root / 'derivations.json', dict(derivations=[fixtures, runner], all_native_high_constants_addresses_andmultiplicity_preserved=True,
        original_eight_opening_initializers_andall_twenty_B51_commands_preserved=True, original_nested_relative_operands_preserved_under_constant_shift=True,
        whole_source_andrevised_scripts_not_flattened_line_samplers=True, identical_ordinary_inputs_no_forced_runtime_conditions=True,
        disclosed_entry_fixture_not_original_location_ornatural_optional_event_activation=True, no_ROM_capture_orcredit_by_preparer=True))
