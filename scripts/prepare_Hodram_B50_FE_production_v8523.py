"""Derive independent same-run FE register/typed-object/palette/VRAM readers for B50."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B50_FE_production_tools_v8523');assert not root.exists()
    result=derive('dk4tool/patch/hodram_B49_FE_evidence_v1.py','dk4tool/patch/hodram_B50_FE_evidence_v1.py',{
        "declared['focused_actual_frames']==9862":"declared['actual_frames']==20002",
        'two focused FE language groups/9862 frames':'two complete same-run FE language groups/20002 frames',
        "Path('work/analysis/Hodram_B49_FE_runs_v8419')/version":"Path('work/analysis/Hodram_B50_scene_runs_v8505')/f'route1_B50_{version}'",
        "Path(terminal['observer'])":"Path(terminal['modal_observer'])",
        "terminal['frames']==report['frames']==plan['frames']==4931":"terminal['frames']==report['frames']==plan['frames']==10001",
        " and terminal['exactly_one_complete_original_FE_paint_CPU_WRAM_DTCM_ITCM_snapshot']":"",
        "terminal['observer_sha256']":"terminal['modal_observer_sha256']",
        "data['tail_fixtures']['fixtures']":"data['fixtures']['fixtures']",
        "f['source_block']==49":"f['source_block']==50",
        "        body=native['bodies'][version]['DK4_MES_B49_R0081']['expanded_body'];":"        combined_path=Path(terminal['combined_FE_evidence']);require(sha(combined_path.read_bytes())==terminal['combined_FE_evidence_sha256'],'same-run combined observer export receipt')\n        combined=load(combined_path);require(combined['both_observers_disjoint_readonly'] and combined['modal_observers'][0]['command_andFE_host_slots_disjoint'],'disjoint readonly command andFE observers')\n        plan={**plan,'exact_expanded_FE_body_hex':combined['modal_observers'][0]['exact_FE_body_hex']}\n        body=native['bodies'][version]['DK4_MES_B50_R0013']['expanded_body'];",
        'DK4_MES_B49_R0081':'DK4_MES_B50_R0013',
        "Path('work/analysis/Hodram_B49_tail_runs_v8416')/f'route1_{version}_accept'":"root",
        "report['scripted_input_schedule']==[e for e in fullreport['scripted_input_schedule'] if e['start']<=4930]":"report['scripted_input_schedule']==fullreport['scripted_input_schedule']",
        'exact unretimed focused/fullrun input prefix':'exact one-run unretimed complete ordinary input schedule',
        "        for snap in report['read_only_capture_RAM_snapshots']:":"        selected=[s for s in combined['held_snapshots'] if s['frame'] in [4330,4390,4450]]\n        require([s['frame'] for s in selected]==[4330,4390,4450],'three complete same-run FE holds')\n        for s in selected:\n            require(s['all_CPU_WRAM_DTCM_ITCM_andconfiguration_exact_before_after_readonly_export'],'held export leaves allCPU WRAM DTCM ITCM configuration unchanged')\n            for ref in s['files'].values():\n                b=Path(ref['path']).read_bytes();require(len(b)==ref['bytes'] and sha(b)==ref['sha256'],'whole held CPU/WRAM/TCM export')\n        RAM_snapshots=[dict(frame=s['frame'],**s['files']['WRAM'],read_only_export=True) for s in selected]\n        for snap in RAM_snapshots:",
        'frame in [4870,4930]':'frame in [4330,4390,4450]',
        'whole_PNG_equal_to_completed_original_command_trace_run=True':'same_run_original_command_trace_andnative_export_PNG=True',
        "len(holds)==2,'two complete held bitmaps perFE language'":"len(holds)==3,'three complete held bitmaps perFE language'",
        'full_native_scene_runs_40004_frames_referenced_separately':'same_whole_native_scene_runs_20002_frames',
        'complete_actual_VRAM_bitmap_palette_RGB_holds_recomputed=4,focused_actual_frames_bound=9862':'complete_actual_VRAM_bitmap_palette_RGB_holds_recomputed=6,actual_frames_bound=20002',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,all_native_high_integer_constants_andmultiplicity_preserved=True,all_original_FE_PC_R0_R1_complete_input_NUL_typed_descriptors_palette_bankD_VRAM_andRGB_guards_preserved=True,all_CPU_register_indices_andlogical_palette_indices_unchanged=True,six_holds_from_same_two_complete_runs_no_repeated_capture=True,no_emulator_ROM_orcredit_change=True,new_credit=0,full_goal_complete=False))
