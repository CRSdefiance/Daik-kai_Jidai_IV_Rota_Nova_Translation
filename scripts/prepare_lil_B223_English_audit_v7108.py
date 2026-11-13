"""Freeze the complete English audit, preserving cross-route and two-page scope."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B223_English_audit_tools_v7108')
if __name__=='__main__':
    assert not ROOT.exists()
    a='scripts/audit_lil_B214_English_v6724.py';b='scripts/audit_lil_B223_English_v7108.py'
    boundary="    assert predicate_values==[0,0];expected=next(r['offsets'] for r in control['four_structural_route_models'] if r['predicate_Boolean_values']==predicate_values);assert [p['source_offset'] for p in pairs if p['source_offset'] is not None]==expected and len(pairs)==30 and len(panels)==9 and not failures and pairs[-1]['source_offset']==1310 and pairs[-1]['native_result']==[0,0];signature=next(p for p in panels if p['source_record_index']==68);assert signature['native_pages']==1;"
    reviewed="""    transitions=[];schedule=read(plan['original_inputs'])
    for panel in panels:
        for left,right in zip(panel['pages'],panel['pages'][1:]):
            lo=left['complete_body_holds'][-1]['frame'];hi=right['complete_body_holds'][0]['frame'];inputs=[v for v in schedule if lo<v['start']<=hi and v['buttons']==['A']]
            assert lo<hi and inputs
            transitions.append(dict(id=panel['id'],from_page=left['page'],to_page=right['page'],last_complete_previous_frame=lo,first_complete_next_frame=hi,original_A_inputs_in_interval=inputs,capture_bracket_not_exact_transition_frame=True))
    assert len(transitions)==2 and {t['id'] for t in transitions}=={'DK4_MES_B223_R0031','DK4_MES_B223_R0040'}
    assert sum(p['native_pages'] for p in panels)==11
    assert predicate_values==[0];expected=next(r['offsets'] for r in control['two_structural_route_models'] if r['predicate_Boolean_value']==0);assert [p['source_offset'] for p in pairs if p['source_offset'] is not None]==expected and len(pairs)==27 and len(panels)==9 and not failures and pairs[-1]['source_offset']==1312 and pairs[-1]['native_result']==[0,0];signature=next(p for p in panels if p['source_record_index']==48);assert signature['native_pages']==1;"""
    oldsheet="""    post=min(f for f in photos if f>threshold);sheet=Image.new('RGB',(1024,410),'#263238');draw=ImageDraw.Draw(sheet);transition_frames=[panels[0]['selected_complete_capture']['frame'],signature['selected_complete_capture']['frame'],post,16001]
    for i,frame in enumerate(transition_frames):draw.text((i*256+3,3),'English frame'+str(frame),fill='white');sheet.paste(photos[frame][1],(i*256,24))"""
    newsheet="""    post=min(f for f in photos if f>threshold);sheet=Image.new('RGB',(768,1230),'#263238');draw=ImageDraw.Draw(sheet)
    transition_frames=[panels[0]['selected_complete_capture']['frame'],panels[1]['selected_complete_capture']['frame'],*[page['selected_complete_capture']['frame'] for panel in panels if panel['source_record_index'] in [31,40] for page in panel['pages']],signature['selected_complete_capture']['frame'],post,16001];assert len(transition_frames)==9
    for i,frame in enumerate(transition_frames):
        x,y=i%3*256,i//3*410;draw.text((x+3,y+3),'English frame'+str(frame),fill='white');sheet.paste(photos[frame][1],(x,y+24))"""
    changes={
      'B214':'B223','English_actual_v6724':'English_actual_v7108','English_run_v6723':'English_run_v7107','English_fixture_v6722':'English_fixture_v7106',
      'source_actual_v6709b/eight_speeches_one_selected_style_complete_source_masks30_commands_and_return':'source_actual_v7088c/eight_speeches_one_style_ten_complete_pages27_commands_and_source_return',
      'stored_v6717/all17_stored_targets68_alignments_seventeen_complete_pages':'stored_v7098/all17_stored_targets68_alignments_nineteen_complete_pages',
      'name_planes_v6710':'name_planes_v7084',
      'controls_v6708/four_unforced_predicates_ten_structural_cases50_seeded_ends_four_route_models':'controls_v7082/two_unforced_predicate_cases_ten_structural_cases50_seeded_ends_two_route_models',
      "not trace['unreturned_at_capture_end']":"all((trace['rows'][p['entry_row']]['source']['route'],trace['rows'][p['entry_row']]['source']['block'])!=(2,22) for p in trace['unreturned_at_capture_end'])",
      "plan['all27_source_commands_retained']":"plan['all22_source_commands_retained']",
      'panels=[];pairs=[];following=[];failures=[];last=0;predicate_values=[]':"banks={i:IlnkContainer.parse(image.read_file(f'/data/SC{i}.DK4')).blocks for i in range(4)};panels=[];pairs=[];following=[];failures=[];last=0;predicate_values=[]",
      "s['route']==2":"s['route'] in banks", "sha(after[s['block']])":"sha(banks[s['route']][s['block']])",
      "if s['block']!=22:following.append(dict(frame=row['frame'],block=s['block']":"if (s['route'],s['block'])!=(2,22):following.append(dict(frame=row['frame'],route=s['route'],block=s['block']",
      'DK4_VOICE_B214_C8_T170':'DK4_VOICE_B223_C8_T176',
      boundary:reviewed,oldsheet:newsheet,
      'all36_commands_stored_not_all_executed':'all31_commands_stored_not_all_executed',
      'all_nine_actual_objects_original_single_pages_with_ordinary_A_input=True':'all_eleven_actual_pages_two_continuations_with_ordinary_A_input=True,page_transitions=transitions',
      'Janus_Pasar_signature_complete_native_black_gray_and_name_masks_match':'Ian_Dukov_signature_complete_native_black_gray_and_name_masks_match',
      'natural_event214_original_location':'natural_event223_original_location',
      "capture_report=str(rp),observer_report=str(tp)":"capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),observer_report=str(tp),observer_report_sha256=sha(tp.read_bytes()),unreturned_following_dialogues_at_capture_end=trace['unreturned_at_capture_end'],all_following_resident_payloads_verified_against_actual_SC0_to_SC3_bank=True,later_scene_not_claimed_complete=True",
    }
    assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),changes)
    row=derive(a,b,changes);ROOT.mkdir(parents=True);save(ROOT/'source_locked_actual_audit.json',dict(tool=row,original_native_addresses_getters_and_pixel_origins_unchanged=True,two_page_transitions_and_actual_cross_route_banks_checked=True,later_open_non_B22_dialogue_disclosed=True,new_credit=0,full_goal_complete=False))
