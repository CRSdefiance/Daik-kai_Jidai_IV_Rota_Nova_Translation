"""Scope the completed letter separately from the later original B44 dialogue open at capture end."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B223_source_scope_v7088b')
if __name__=='__main__':
    assert not ROOT.exists();plan=read('work/analysis/lil_B223_source_run_v7086/run_plan.json');tp=Path(plan['capture_folder'])/'observer/commands.json';trace=read(tp);pending=[]
    assert not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact']
    for item in trace['unreturned_at_capture_end']:
        row=trace['rows'][item['entry_row']];assert row['kind']=='before_command' and row['source']['block']==44 and row['source']['first_word']==0x4000 and row['source']['classification']=='original_SC_cache' and row['source']['whole_resident_payload_exact_ROM']
        pending.append(dict(entry_row=item['entry_row'],frame=row['frame'],source=row['source'],original_dialogue_still_open_not_returned_or_future_verified=True))
    assert len(pending)==1 and any(r['kind']=='after_command' and r['source']['block']==22 and r['source']['first_word']==0 and r['result_words']==[0,0] and r['frame']==5253 for r in trace['rows'])
    changes={'source_actual_v7088':'source_actual_v7088b',"and not trace['unreturned_at_capture_end'] and trace['all_host_slots_restored_and_core_file_exact']":"and all(trace['rows'][p['entry_row']]['source']['block']!=22 for p in trace['unreturned_at_capture_end']) and trace['all_host_slots_restored_and_core_file_exact']",'all_jobs_terminal_and_reaped=True,visual_review_pending=True':"all_jobs_terminal_and_reaped=True,following_open_dialogue_scope='work/analysis/lil_B223_source_scope_v7088b/completed_letter_and_preserved_later_open_dialogue.json',unreturned_following_dialogues_at_capture_end=trace['unreturned_at_capture_end'],later_scene_not_claimed_complete=True,visual_review_pending=True"}
    checked_text(Path('scripts/audit_lil_B223_source_v7088.py').read_text('utf8'),changes);tool=derive('scripts/audit_lil_B223_source_v7088.py','scripts/audit_lil_B223_source_v7088b.py',changes)
    ROOT.mkdir(parents=True);save(ROOT/'completed_letter_and_preserved_later_open_dialogue.json',dict(failed_producer='scripts/audit_lil_B223_source_v7088.py',failed_before_output_directory_or_ROM_mutation=True,failure='Initial assertion required no outstanding command in any later scene;one original B44 progressive dialogue remains open at frame16001.',original_letter_B22_normal_result=[0,0],original_letter_normal_return_frame=5253,pending_later_dialogues=pending,all_original_trace_records_and_capture_bytes_preserved=True,no_EMU_replay_input_retiming_RNG_state_code_or_scope_manufacture=True,successor=tool,trace=str(tp),trace_sha256=sha(tp.read_bytes()),source_letter_native_masks_headers_branches_and_commands_still_required=True,new_credit=0,full_goal_complete=False))
