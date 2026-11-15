"""Bind B50 original FE paint and three same-run held VRAM/CPU snapshots per language."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B50_FE_tools_v8508');assert not root.exists()
    proof=derive('scripts/bind_Hodram_B49_FE_v8420.py','scripts/bind_Hodram_B50_FE_v8508.py',{
        'Hodram_B49_FE_binding_v8420':'Hodram_B50_FE_binding_v8508',
        'Hodram_B49_FE_runs_v8419':'Hodram_B50_scene_runs_v8505',
        'Hodram_B49_models_v8408':'Hodram_B50_models_v8506',
        "folder=RUNS/version;terminal=read(folder/'terminal.json');plan=read(folder/'run_plan.json');rp,op=Path(terminal['report']),Path(terminal['observer']);report,observer=map(read,[rp,op])":"folder=RUNS/f'route1_B50_{version}';terminal=read(folder/'terminal.json');plan=read(folder/'run_plan.json');rp,op=Path(terminal['report']),Path(terminal['modal_observer']);report,observer=map(read,[rp,op])\n        combinedpath=Path(terminal['combined_FE_evidence']);assert sha(combinedpath.read_bytes())==terminal['combined_FE_evidence_sha256'];combined=read(combinedpath)\n        plan={**plan,'exact_expanded_FE_body_hex':combined['modal_observers'][0]['exact_FE_body_hex']}\n        assert combined['both_observers_disjoint_readonly'] and combined['modal_observers'][0]['command_andFE_host_slots_disjoint']",
        "terminal['frames']==4931 and terminal['exactly_one_complete_original_FE_paint_CPU_WRAM_DTCM_ITCM_snapshot']":"terminal['frames']==10001",
        "sha(op.read_bytes())==terminal['observer_sha256']":"sha(op.read_bytes())==terminal['modal_observer_sha256']",
        "full=Path('work/analysis/Hodram_B49_tail_runs_v8416')/f'route1_{version}_accept'":"full=folder",
        "assert report['scripted_input_schedule']==[e for e in fullreport['scripted_input_schedule'] if e['start']<=4930]":"assert report['scripted_input_schedule']==fullreport['scripted_input_schedule']\n        actual=read('work/analysis/Hodram_B50_actual_v8507/B50/paired_actual_dialogue_headers_flow_returns.json');ag=next(g for g in actual['groups'] if g['version']==version)\n        FE=next(s for s in ag['speeches'] if s['source_selector']==254);held={h['frame'] for h in FE['complete_holds']}\n        selected=[s for s in combined['held_snapshots'] if s['frame'] in held]\n        assert {s['frame'] for s in selected}==held=={4330,4390,4450}\n        for s in selected:\n            assert s['all_CPU_WRAM_DTCM_ITCM_andconfiguration_exact_before_after_readonly_export']\n            for f in s['files'].values():\n                v=Path(f['path']).read_bytes();assert len(v)==f['bytes'] and sha(v)==f['sha256']\n        RAM_snapshots=[dict(frame=s['frame'],**s['files']['WRAM'],read_only_export=True) for s in selected]",
        "for snap in report['read_only_capture_RAM_snapshots']:":"for snap in RAM_snapshots:",
        'frame in [4870,4930]':'frame in held',
        'whole_PNG_equal_to_completed_original_command_trace_run=True':'same_run_original_command_trace_andnative_export_PNG=True',
        'assert len(holds)==2':'assert len(holds)==3',
        'focused_actual_frames=9862,whole_scene_tests_not_repeated=True':'actual_frames=20002,whole_scene_tests_not_repeated=True',
        'full_native_scene_runs_40004_frames_referenced_separately=True':'same_whole_native_scene_runs_20002_frames=True',
        'two_original_FE_paint_snapshots_four_exact_bitmap_palette_RGB_holds.json':'two_original_FE_paint_snapshots_six_exact_bitmap_palette_RGB_holds.json',
        'Actual FE:two originalpaint snapshots/four complete held nativebitmaps/palettes/RGB;228x48/288stride/6x12/16pitch andcurrent vtables exact;9862focusedframes/no repeatedwholeflow tests.':'B50 actual FE:two originalpaint snapshots/six same-run held nativebitmaps/palettes/RGB;228x48/288stride/6x12/16pitch andcurrent vtables exact;no repeatedwholeflow tests.',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=proof,all_native_high_integer_constants_andmultiplicity_preserved=True,same_run_complete_FE_holds_no_reexecution=True,new_credit=0,full_goal_complete=False))
