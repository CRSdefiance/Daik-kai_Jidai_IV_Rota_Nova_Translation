"""Two current-bound NPC response holds and original declaration-to-battle return."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/rebind_retreat_transfer_history_v2603.py').read_text()
 changes={
 'retreat_transfer_history_v2603':'declaration_responses_history_v2609',
 'from dk4tool.patch.retreat_transfer_editorial import current_entries as old_entries':'from dk4tool.patch.declaration_responses_editorial import current_entries as old_entries',
 'out/all_routes_combined_v1520_candidate.nds':'out/all_routes_combined_v1542_candidate.nds','range(2683,2690)':'range(2201,2209)',
 'work/analysis/retreat_transfer_actual_fonts_v1526c/actual_retreat_font_and_transition_verification.json':'work/analysis/declaration_responses_actual_fonts_v1547b/actual_NPC_response_font_and_transition_verification.json',
 'work/analysis/retreat_transfer_context_v2600/source_context_packet.json':'work/analysis/declaration_responses_context_v2606/source_context_packet.json',
 'work/analysis/retreat_transfer_fonts_v2602/native_font_proof.json':'work/analysis/declaration_responses_fonts_v2608/native_font_proof.json',
 "case=next(c for c in fp['cases']if c['source_voice']==1 and c['variant']==0);assert case['message_ID']==2684 and case['name']=='Latina'":"case=next(c for c in fp['cases']if c['message_ID']==2205);assert case['source_voice']==4 and case['existing_actor_ID']==28",
 'prior[2684]':'prior[2205]','entries[2684]':'entries[2205]',
 'for n in(8750,8800,8850)':'for n in(6120,6150)',"==550 for h in holds":"==815 for h in holds",
 'work/analysis/retreat_transfer_replay_v1524/original_departure_inputs.json':'work/analysis/declaration_responses_replay_v1546/original_departure_inputs.json',
 'data=raw(8800);screen=picture(8800)':'data=raw(6150);screen=picture(6150)',
 "text.index(b'Our')":"text.index(b'What')","formatted_hex']).index(b'Our')":"formatted_hex']).index(b'What')",
 'resident-leading-O':'resident-leading-W','wrapped-leading-O':'wrapped-leading-W','verify(8800':'verify(6150',
 'three_historical_complete_retreat_holds':'two_historical_complete_NPC_response_holds',
 'Historical V1520 ID2684':'Historical V1542 ID2205','historical_defeat_retreat_transfer_and_sailing':'historical_declaration_NPC_response_battle_and_return',
 "(768,410)":"(512,410)",
 'historical_retreat_transfer_current_binding':'historical_declaration_responses_current_binding',
 'historical_IDs=[2684]':'historical_IDs=[2205]',
 'all7_current_historical_payloads_and_all8_voice_font_planes_equal':'all8_current_historical_payloads_and_font_planes_equal',
 'only2684_has_individual_historical_activation_other6_and_voice3_fallback_use_family_sample':'only2205_has_individual_historical_activation_other7_use_family_sample',
 }
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 a=source.index(' def verify(');b=source.index(' holds=',a)
 source=source[:a]+""" def verify(frame,data=None,screen=None):
  data=raw(frame)if data is None else data;screen=picture(frame)if screen is None else screen;cpu,get=get_machine(arm,data);actors,companies=get(0xCB184),get(0xCB160);actor=get(0x3CD2C,companies+4+4*76)
  assert actor==actors+4+28*32 and get(0x7EE08,actor)==28 and get(0x7E988,actor)==4 and get(0x53F4C,actor,0x021184E0)==2205
  assert data[owner-BASE+0x2030:owner-BASE+0x2230].split(b'\\0')[0]==entries[2205].text
  assert data[wrapped-BASE:wrapped-BASE+512].split(b'\\0')[0].hex()==case['native_pipeline']['formatted_hex']and data.count(block)==1
  expected={(16+x,296+y)for y in range(64)for x in range(228)if plane.getpixel((x,y))==0};actual={(x,y)for y in range(294,366)for x in range(16,244)if screen.getpixel((x,y))==(0,8,0)};assert actual==expected
  return dict(message_ID=2205,message_id=2205,frame=frame,source_company_ID=4,source_company_leader_getter=0x0203CD2C,source_actor_ID=28,source_voice=4,original_voice_table=0x021184E0,original_parent=0x02053F40,original_table_stack_offset=0x274,lines=case['lines'],current_template_wrapped_bytes_and_full228x64_native_RGB_ink_and_blank_mask_equal=True,matching_foreground_pixels=len(expected),missing_or_unexpected_foreground_pixels=0,RAM=snapshots[frame]['path'],RAM_sha256=sha(data),capture=images[frame]['path'],capture_sha256=images[frame]['PNG_sha256'],historical_only_not_current_emulator_visit=True)
"""+source[b:]
 a=source.index(" for row,col,label in(");b=source.index(' bad=screen.copy();bad.putpixel',a)
 source=source[:a]+""" for row,col,label in((0,0,'erase-leading-W'),(2,len(case['lines'][2])-1,'erase-final-question-mark'),(1,0,'erase-contemptuous-Ha-H'),(2,case['lines'][2].index('beat'),'erase-full-personal-boast-beat-b')):
  bad=screen.copy();x,y=22+col*6,296+row*16;bad.paste('white',(x,y,x+6,y+11));controls.append(dict(negative=label,rejected=reject(lambda:verify(6150,screen=bad))))
"""+source[b:]
 a=source.index(' for frame,label in((');b=source.index('  picture(frame);flow.append',a)
 source=source[:a]+" for frame,label in((6020,'preceding original declaration setup;context only'),(6150,'complete target-company-leader response before A'),(6300,'original battle after normal response dismissal'),(8800,'later replacement-ship retreat;context only'),(9000,'ordinary sailing after original defeat/transfer'),(9200,'continued sailing with four surviving ships;source mode0')):\n"+source[b:]
 a=source.index(' pixelpath=Path(');b=source.index(' ROOT.mkdir(parents=True);',a)
 source=source[:a]+""" pixelpath=hp;pixelproof=h
 assert len(h['complete_actual2205_holds'])==2 and all(r['whole256x384_changed_pixels']==907 and r['every_changed_pixel_exact_old_new_native_glyph_symmetric_difference']and r['all_other_portrait_scenery_border_and_paper_pixels_unchanged']for r in h['complete_actual2205_holds'])and len(h['all_other_sampled_whole_frames_exact_to_V1520'])==43
"""+source[b:]
 source=source.replace('old_new_three_screen278_glyph_differences_and42_other_whole_frames_proof','old_new_two_screen907_glyph_differences_and43_other_whole_frames_proof')
 a=source.index("scope='Historical V1520");b=source.index("',producer_sha256=",a)
 scope='Historical V1542 target-company leaderJames Clifford28/company4/voice4 response2205 after ordinary Yes declaration,original3CD2C/direct53F0C/table021184E0. Two full RGB ink/blank masks freshly bind current complete paragraph and font. Sole40-owned-byte prebattle own-position fixture,whole4MiB/input audit and907-pixel/43-whole-frame controls remain hash-bound without unnecessary replay. No later actor,health,crew,ability,RNG,result,hostility or membership edits. Fourteen original states and six declaration/response/battle/retreat/sailing transitions are freshly checked;surrounding strings add zero prose credit. Only2205 individually activated;other seven use current native/offline tests and representative-family coverage. No new current startup/emulator run,earned travel,full-route,guaranteed boast/threat result or hardware proof.'
 source=source[:a]+'scope='+repr(scope)+source[b+1:]
 source=source.replace('Three complete historical2684 holds,7 corruptions,14 original states and6 defeat/transfer/sailing transitions pass.','Two complete historical2205 holds,7 corruptions,14 original states and6 declaration/battle/return transitions pass.')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
