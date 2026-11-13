"""Fresh current binding of historical capture2011 and reward/cargo/sailing flow."""
from pathlib import Path
OLD=Path('scripts/rebind_aftermath_fled_history_v2543.py')
if __name__=='__main__':
 source=OLD.read_text()
 changes={
 'aftermath_fled_history_v2543':'flagship_capture_history_v2583',
 'from dk4tool.patch.battle_aftermath_editorial import current_entries as old_entries':'from dk4tool.patch.flagship_capture_precision import current_entries as old_entries',
 'out/all_routes_combined_v1266_candidate.nds':'out/all_routes_combined_v1364_candidate.nds',
 'range(2046,2052)':'range(2011,2016)',
 'work/analysis/aftermath_victory_verified_v1271/actual_fled_victory_verification.json':'work/analysis/flagship_capture_verified_v1370/actual_flagship_capture_verification.json',
 "report['frames']==11782":"report['frames']==13200",
 "assert historical['source_and_disposable_saves_unchanged']and len(historical['all31_fixture_replays'])==31 and historical['all_fixtures_before_duel5772_last5770']and historical['no_during_or_post_duel_fixtures']":"assert historical['source_and_disposable_saves_unchanged']and historical['all4MiB_fixture_input_schedule_primary_RAM_and_PNG_hash_audits_pass']\n assert historical['sole_fixture']['all_actors_IDs_roles_crew_health_stored_fleets_towns_companies_RNG_and_results_unchanged']\n reference=Path(historical['sole_fixture']['actual_position_reference']);assert sha(reference.read_bytes())==historical['sole_fixture']['actual_position_reference_sha256']",
 " assert historical['no_actor_ID_numeric_message_RNG_eligibility_flag_or_result_injection']\n":"",
 'source_fled_result_code_matches_clean_Japanese_ARM9':'original_duel_victory_capture_and_return_code_exact_clean',
 'work/analysis/aftermath_fled_fonts_v2542b/native_font_proof.json':'work/analysis/flagship_capture_fonts_v2582/native_font_proof.json',
 '2046':'2011','0x02117900':'0x02117740',
 "assert identity==18 and get(0x7EE08,actor)==18":"assert identity==16 and get(0x82428,fleet+0x2090,1)==0 and get(0x7EE08,actor)==16",
 'source_actor_ID=18':'source_actor_ID=16',
 '(10942,10982)':'(10800,10850)','10942':'10800',
 'work/analysis/aftermath_victory_v1270/original_load_inputs.json':'work/analysis/flagship_capture_replay_v1369/original_departure_inputs.json',
 "row['frame']>=5772":"row['frame']>4800",
 "and not any(5773<=e['start']<=10982 for e in schedule)":"",
 "entries[2011].text.index(b'The')":"entries[2011].text.index(b'We')",
 "bytes.fromhex(case['native_formatted_hex']).index(b'The')":"bytes.fromhex(case['native_formatted_hex']).index(b'We')",
 'corrupt-resident-leading-T':'corrupt-resident-leading-W','corrupt-wrapped-leading-T':'corrupt-wrapped-leading-W',
 "((0,'erase-complete-leading-T'),(len(line)-1,'erase-final-exclamation'),(line.index('won')+1,'erase-interior-victory-word-letter'))":"((0,0,'erase-complete-leading-W'),(1,len(case['lines'][1])-1,'erase-final-exclamation'),(1,0,'erase-entire-crew-continuation-e'),(1,case['lines'][1].index('ship'),'erase-captured-ship-word-s'))",
 'for column,label in':'for rowindex,column,label in',
 'x,y=22+column*6,296':'x,y=22+column*6,296+16*rowindex',
 'len(controls)==6':'len(controls)==7',
 'historical_aftermath_fled_current_binding':'historical_flagship_capture_current_binding',
 'six_negative_controls_current_binding_on_offline_clones':'seven_negative_controls_current_binding_on_offline_clones',
 'no_inputs5773_through10982=True':'no_fixtures_after4800=True',
 'original31_pre_duel_fixture_audits_hash_bound_not_needlessly_repeated=True':'original_sole40_position_byte_fixture_audit_hash_bound_not_needlessly_repeated=True,sole_fixture=historical["sole_fixture"]',
 'all6_current_historical_payloads_and_font_planes_equal':'all5_current_historical_payloads_and_all8_voice_font_planes_equal',
 'only2011_has_individual_historical_activation_other5_use_family_sample':'only2011_has_individual_historical_activation_other4_use_family_sample',
 'Historical V1266':'Historical V1364',
 }
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 start=source.index(' states=[]\n');end=source.index(' ROOT.mkdir(parents=True);',start)
 original=Path('scripts/verify_flagship_capture_v1354.py').read_text();a=original.index('    states = []');b=original.index('    ROOT.mkdir',a)
 block=original[a:b];block='\n'.join(line[3:]if line.startswith('   ')else line for line in block.splitlines()).replace('raw(frame)','source_raw(frame)')+'\n'
 block+=""" assert states==historical['original_encounter_duel_capture_reward_and_return_states']
 assert historical['normal_A_dialogue_X_cargo_finish_touch_Yes_and_reward_dismissal_return_to_sailing']
 flow=[]
 for frame,label in((10850,'complete capture report after original duel victory'),(10950,'subsequent original victory dialogue;context only'),(11100,'original provisions reward;context only'),(11300,'original captured-coins reward;context only'),(11500,'cargo handling;no retained untransferred spoils claim'),(12900,'original power reward;context only'),(13200,'ordinary sailing after X Finish,touch Yes discards untransferred cargo,and reward dismissal')):
  picture=Path(images[frame]['path']);assert sha(picture.read_bytes())==images[frame]['PNG_sha256'];flow.append(dict(frame=frame,visually_reviewed_state=label,RAM=str(snapshots[frame]['path']),RAM_sha256=sha(source_raw(frame)),capture=str(picture),capture_sha256=sha(picture.read_bytes()),historical_only_not_current_startup_or_whole_route_approval=True))
"""
 source=source[:start]+block+source[end:]
 source=source.replace("sheet=Image.new('RGB',(512,410),'#263238');draw=ImageDraw.Draw(sheet)\n for i,r in enumerate(flow):draw.text((i*256+4,3),str(r['frame'])+' historical return',fill='white');sheet.paste(Image.open(r['capture']),(i*256,24))","sheet=Image.new('RGB',(1024,820),'#263238');draw=ImageDraw.Draw(sheet)\n for i,r in enumerate(flow):\n  x,y=i%4*256,i//4*410;draw.text((x+4,y+3),str(r['frame'])+' historical context',fill='white');sheet.paste(Image.open(r['capture']),(x,y+24))")
 source=source.replace('two_historical_complete_flight_victory_holds','two_historical_complete_capture_holds').replace('historical_report_to_ordinary_sailing_return','historical_capture_rewards_cargo_and_sailing')
 a=source.index("  scope='");b=source.index("\n  producer_sha256",a)
 source=source[:a]+"  scope='Historical V1364 capture report2011 via original role1 logical82478 member16 Gerhard with empty physical First Mate,voice1 fallback. Sole frame4800 fixture owns40 live-position bytes for five existing own ships;health,crew,roles,IDs,stored fleets,towns,companies,RNG and results unchanged. Actual-loaded enemy-position reference hash bound;enemy not relocated. Completed whole4MiB/input audits reused. Two whole RGB ink/blank masks bind current text/fonts. Later victory,rewards,cargo handling and sailing are transition context only with no duplicate prose credit. X Finish and touch Yes discard untransferred spoil cargo. Only2011 individually activated;other four are current offline/font and family sampling. No new current emulator run,startup approval,earned travel,permanent fleet addition,sinking or hardware proof.',"+source[b:]
 source=source.replace('Two complete historical flight/victory holds,6 corruptions,exact inputs and original A return to mode0/sailing pass.','Two complete historical capture holds,7 corruptions,15 original states and7 reward/cargo/sailing transitions pass.')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
