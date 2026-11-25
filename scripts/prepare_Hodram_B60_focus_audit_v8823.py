"""Audit existing focused captures and compare the bounded post-exchange interval."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B60_focus_audit_tools_v8823');assert not root.exists()
    audit=derive('scripts/audit_Hodram_B54_B60_actual_v8820.py','scripts/audit_Hodram_B60_focus_v8823.py',{
        'Hodram_B54_B60_actual_v8820':'Hodram_B60_focus_actual_v8823',
        'Hodram_B54_B60_scene_runs_v8816':'Hodram_B60_boundary_focus_runs_v8822',
        'choices=[54,57,58,59,60]':'choices=[60]',
        '{54:6001,57:9001,58:16001,59:10001,60:10001}':'{60:7001}',
    })
    compare=derive('scripts/compare_Hodram_B54_B60_actual_v8821.py','scripts/compare_Hodram_B60_focus_v8824.py',{
        'Hodram_B54_B60_comparison_v8821':'Hodram_B60_focus_comparison_v8824',
        'for number in [54,56,57,58,59,60]:':'for number in [60]:',
        "proofpath='work/analysis/Hodram_B56_actual_v8818/B56/paired_actual_dialogue_headers_flow_returns.json' if number==56 else f'work/analysis/Hodram_B54_B60_actual_v8820/B{number}/paired_actual_dialogue_headers_flow_returns.json'":
        "proofpath='work/analysis/Hodram_B60_focus_actual_v8823/B60/paired_actual_dialogue_headers_flow_returns.json'",
        'total_actual_frames=116012':'total_actual_frames=14002',
    })
    root.mkdir(parents=True);save(root/'source_locked_focus_audit_andcomparison.json',dict(audit=audit,comparison=compare,
        existing7001frame_runs_only_no_recapture=True,original_input_prefix_through_A6400_not_retimed=True,
        comparison_uses_saved_final_WRAM_at7001_not_unsaved_mainRAM_at_6176_or6415=True,
        captured_native_boundary_exports_have_CPU_TCM_VRAM_butdo_not_save_mainWRAM=True,
        long_10001frame_divergence_remains_preserved_not_overridden=True,
        all_native_glyph_flow_snapshot_state_andABI_guards_preserved=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
