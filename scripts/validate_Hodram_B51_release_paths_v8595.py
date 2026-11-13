"""Validate completed production paths and measured scope; identify pending sealing work."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B51_release_paths_v8595 import PARENT, ROM, DOC, NAMES, SEAL, CONFIG, proofs, observed_scope
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B51_release_plan_v8595')

if __name__ == '__main__':
    assert not ROOT.exists()
    paths = proofs()
    future = {key: value for key, value in paths.items() if key in ['builder_support', 'builder_validation', 'predecessor_compatibility']}
    ready = {key: value for key, value in paths.items() if key not in future}
    assert all(Path(path).is_file() for path in ready.values())
    assert all(not Path(path).exists() for path in future.values()) and not SEAL.exists() and not CONFIG.exists()
    data = {key: read(path) for key, path in ready.items()}
    doc = read(DOC)
    assert sha(PARENT.read_bytes()) == doc['current_ROM_sha256'] == data['predecessor_release']['candidate_sha256']
    assert sha(ROM.read_bytes()) == doc['reference_ROM_sha256'] == data['reference']['research_ROM_sha256']
    assert doc['names_packet_sha256'] == sha(NAMES.read_bytes()) and data['reference']['only_changed_blocks'] == [51]
    scope = observed_scope(data)
    assert scope['complete_page_occurrences'] == 8 and scope['complete_body_name_holds'] == 56
    assert len(scope['actual_unique_speech_IDs']) == 4 and scope['unvisited_conditional_text_IDs'] == ['DK4_MES_B51_R0032']
    assert [g['native_result'] for g in scope['normal_returns']] == [[0, 0], [0, 0]]
    assert scope['measured_comparisons'][0]['later_RGB_pairs'] == 89 and scope['measured_comparisons'][0]['later_RGB_difference_count'] == 3
    assert data['independent_controls']['negative_count'] == 6 and data['independent_actual']['negative_count'] == 5
    assert data['builder_inspection']['no_suitable_existing_registered_hook_for_this_relocatable_late_B51_contract']
    ROOT.mkdir(parents=True)
    save(ROOT / 'release_path_plan.json', dict(ready_proofs=ready, pending_predecessor_andbuilder_proofs=future,
        pending_seal=str(SEAL), pending_config=str(CONFIG), observed_scope=scope,
        all_completed_production_native_controls_actual_references_loaders_andcomparisons_bound=True,
        builder_guard_compatibility_predecessor_equivalence_seal_atomic_stage_andregistered_release_still_pending=True,
        current_V8543_mainV4701_andall_prior_artifacts_unchanged=True, new_credit=0, new_ROMs=0, new_emulator_runs=0, full_goal_complete=False,
        evidence={str(path): sha(Path(path).read_bytes()) for path in [*ready.values(), Path(__file__), Path('scripts/Hodram_B51_release_paths_v8595.py')]}))
    print('B51 production path/scope plan validated: all completed readers bind, eight actual pages/56holds andoffline-only Charles retained. Three builder/predecessor proofs plusseal/config remain pending; no ROM/registry change.')
