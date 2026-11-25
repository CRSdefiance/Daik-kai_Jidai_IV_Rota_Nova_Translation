"""Bind one ordinary DOWN press inside both actually observed source/English menu holds."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B46_decline_input_v7947')
FIX=Path('work/analysis/Rafael_B46_scene_fixtures_v7944/two_complete_source_English_original_Rafael_prelude_fixtures.json')
FLOW=Path('work/analysis/Rafael_B46_menu_flow_v7925/two_choice_native_forwarding_four_relative_sites_accept22_decline7_source_scope.json')
if __name__=='__main__':
    assert not ROOT.exists();fixtures,flow=map(read,[FIX,FLOW]);groups=[]
    for version in ['clean_Japanese','English']:
        root=Path('work/analysis/Rafael_B46_scene_runs_v7945')/f'route0_{version}_accept'
        terminal,plan=map(read,[root/'terminal.json',root/'run_plan.json']);trace=read(terminal['observer']);owner=read(terminal['menu_observer'])
        assert terminal['terminal'] and terminal['all_callbacks_readonly_andhost_slots_restored']
        assert sha(Path(terminal['observer']).read_bytes())==terminal['observer_sha256']
        assert sha(Path(terminal['menu_observer']).read_bytes())==terminal['menu_observer_sha256']
        assert not trace['errors'] and not trace['mismatches'] and not owner['errors'] and not owner['mismatches']
        fixture=next(f for f in fixtures['fixtures'] if f['version']==version);texts={r['fixture_command_offset']:r['id'] for r in fixture['original_text_records']}
        pairs=[(trace['rows'][r['entry_row']],r) for r in trace['rows'] if r['kind']=='after_command' and r['source'].get('classification')=='original_SC_cache' and (r['source']['route'],r['source']['block'])==(0,44)]
        menus=[(a,b) for a,b in pairs if b['source']['first_word']==0x2100];assert len(menus)==1
        a,b=menus[0];assert a['frame']+20<4900<b['frame']-20 and b['result_words']==[2,0]
        speeches=[texts[b['source']['instruction_offset']] for a,b in pairs if b['source']['first_word']==0x4000]
        assert speeches==flow['source_paths'][0]['source_speech_IDs'] and len(speeches)==22
        ends=[b for a,b in pairs if b['source']['first_word']==0];assert len(ends)==1 and ends[0]['result_words']==[0,0]
        assert all(r['bitmap_header_words'][:3]==[4,64,36] and r['backing_bytes']==4608 and r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'] for r in owner['rows'])
        groups.append(dict(version=version,acceptance_terminal=str(root/'terminal.json'),acceptance_terminal_sha256=sha((root/'terminal.json').read_bytes()),
            menu_start=a['frame'] if False else menus[0][0]['frame'],menu_return=menus[0][1]['frame'],menu_selected_value=0,
            expected22_speeches_observed=True,normal_return_frame=ends[0]['frame'],normal_return=[0,0],
            observed_caption_width=84 if version=='clean_Japanese' else 66,actual_backing=[256,36],
            report=str(terminal['report']),report_sha256=terminal['report_sha256']))
    ROOT.mkdir(parents=True);save(ROOT/'one_DOWN4900_bound_to_both_actual_menu_intervals.json',dict(
        groups=groups,DOWN_start_frame=4900,DOWN_duration=5,ordinary_A_start_frames=list(range(4000,15501,240)),
        identical_source_English_inputs_except_language_ROM=True,no_result_condition_seed_orRAM_forcing=True,
        actual_decline_selection_native_path_body_menu_highlight_andnormal_return_pending=True,
        acceptance_body_name_FE_glyph_comparison_andlate_analysis_still_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [FIX,FLOW,Path(__file__)]},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('DOWN4900/duration5 lies inside both actual menu intervals; acceptance22 and[0,0] normalends observed. Decline path remains tobe captured.')
