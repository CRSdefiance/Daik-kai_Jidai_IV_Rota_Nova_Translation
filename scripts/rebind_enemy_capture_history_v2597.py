"""Fresh two named-capture holds,negative glyph/name controls and original return."""
from pathlib import Path
if __name__=='__main__':
 outer=Path('scripts/rebind_battle_victory_history_v2591c.py').read_text();needle="\n exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})";assert outer.count(needle)==1
 env={'__name__':'__main__','__file__':__file__};exec(compile(outer.replace(needle,'\n captured=source'),__file__,'exec'),env);source=env['captured']
 changes={
 'battle_victory_history_v2591c':'enemy_capture_history_v2597',
 'from dk4tool.patch.battle_victory_editorial import current_entries as old_entries':'from dk4tool.patch.enemy_capture_editorial import current_entries as old_entries',
 'out/all_routes_combined_v1404_candidate.nds':'out/all_routes_combined_v1430_candidate.nds',
 'range(2130,2138)':'range(2082,2090)',
 'work/analysis/battle_victory_verified_v1410/actual_victory_and_return_verification.json':'work/analysis/enemy_capture_verified_v1435b/actual_capture_and_return_verification.json',
 'original_victory_duel_capture_reward_and_logical_role_code_exact_clean':'original_capture_duel_reward_and_actor_selection_code_exact_clean',
 'work/analysis/battle_victory_fonts_v2590/native_font_proof.json':'work/analysis/enemy_capture_fonts_v2596/native_font_proof.json',
 '2131':'2082','0x02117EE0':'0x02117B00','(10950,11000)':'(10750,10780)',
 'work/analysis/battle_victory_replay_v1409/original_departure_inputs.json':'work/analysis/enemy_capture_replay_v1434/original_departure_inputs.json',
 "entries[2082].text.index(b'Admiral')":"entries[2082].text.index(b'We')",
 "bytes.fromhex(case['native_formatted_hex']).index(b'Admiral')":"bytes.fromhex(case['native_formatted_hex']).index(b'We')",
 'corrupt-resident-leading-A':'corrupt-resident-leading-W','corrupt-wrapped-leading-A':'corrupt-wrapped-leading-W',
 'verify(10950':'verify(10750','source_raw(10950)':'source_raw(10750)',
 'len(controls)==6':'len(controls)==7','six_negative_controls_current_binding_on_offline_clones':'seven_negative_controls_current_binding_on_offline_clones',
 'historical_battle_victory_current_binding':'historical_enemy_capture_current_binding',
 'only2082_has_individual_historical_activation_other7_use_family_sample':'only2082_has_individual_historical_activation_other7_use_family_sample',
 'two_historical_complete_victory_holds':'two_historical_complete_named_capture_holds',
 'historical_capture_victory_rewards_cargo_and_sailing':'historical_named_capture_flagship_victory_rewards_cargo_and_sailing',
 'Historical V1404':'Historical V1430',
 }
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 a=source.index('  cpu,get=get_machine(arm,raw);fleet,actors=');b=source.index('  assert raw[owner-BASE+',a)
 source=source[:a]+"""  cpu,get=get_machine(arm,raw);fleet,actors=get(0xCB1A8),get(0xCB184)
  attacker=get(0x36C70,fleet+4+132+12);target=get(0x36C70,fleet+4+5*132+12);actor=get(0x55DC4,attacker,8)
  assert actor==actors+4+18*32 and get(0x7EE08,actor)==18 and get(0x7E988,actor)==0 and get(0x53F4C,actor,0x02117B00)==2082
  assert get(0x5543C,target)==30 and get(0x55444,target)==0
  vt=struct.unpack('<I',cpu.mem_read(target,4))[0];getter=struct.unpack('<I',cpu.mem_read(vt+4,4))[0];ptr=get(getter-BASE,target);name=bytes(cpu.mem_read(ptr,64)).split(b'\\0')[0];assert name==b'Hanse Cog'
"""+source[b:]
 source=source.replace("==entries[2082].text\n","==entries[2082].text.replace(b'%s',name)\n")
 source=source.replace('source_role_selector=1,source_actor_ID=16','source_attacker_selector_argument=8,source_actor_ID=18,target_name=name.decode("ascii"),target_Hull_Crew=[30,0]')
 a=source.index(" line=case['lines'][0]");b=source.index(' bad=image.copy();bad.putpixel',a)
 source=source[:a]+""" for rowindex,column,label in((0,0,'erase-complete-leading-W'),(1,len(case['lines'][1])-1,'erase-final-exclamation'),(1,0,'erase-runtime-name-leading-H'),(1,case['lines'][1].index('Cog'),'erase-runtime-name-Cog-C')):
  bad=image.copy();x,y=22+column*6,296+16*rowindex;bad.paste('white',(x,y,x+6,y+11));controls.append(dict(negative=label,rejected=rejected(lambda:verify(10750,image_override=bad))))
"""+source[b:]
 a=source.index(' states = []');b=source.index(' ROOT.mkdir(parents=True);',a)
 original=Path('scripts/verify_enemy_capture_replay_v1435.py').read_text();c=original.index('    states = []');d=original.index('    # Extra ordinary',c)
 block='\n'.join(line[3:]if line.startswith('   ')else line for line in original[c:d].splitlines()).replace('raw(frame)','source_raw(frame)')+'\n'
 block+=""" assert states==historical['original_result_reward_cargo_return_states']and historical['normal_capture_A_dismissal_flagship_victory_rewards_X_cargo_finish_touch_Yes_and_return_to_sailing']and historical['untransferred_spoil_cargo_discarded_through_original_confirmation_not_silently_claimed_acquired']
 flow=[]
 for frame,label in((10780,'complete individual named-enemy-ship capture before A'),(10850,'later flagship-capture report;context only,original A blink phase differs from V1404'),(11000,'later victory report;context only'),(11200,'provisions reward;context only'),(11400,'captured coins;context only'),(11600,'national-coins reward;context only'),(12400,'cargo-transfer screen before normal X Finish'),(12700,'original confirmation before touch Yes discards untransferred spoils'),(12900,'power reward;context only'),(13200,'ordinary sailing after cargo disposition and rewards;source mode0')):
  picture=Path(images[frame]['path']);assert sha(picture.read_bytes())==images[frame]['PNG_sha256'];flow.append(dict(frame=frame,visually_reviewed_state=label,RAM=str(snapshots[frame]['path']),RAM_sha256=sha(source_raw(frame)),capture=str(picture),capture_sha256=sha(picture.read_bytes()),historical_only_not_current_startup_or_whole_route_approval=True))
"""
 source=source[:a]+block+source[b:]
 source=source.replace("(768,1230)","(1024,1230)").replace('x,y=i%3*256,i//3*410','x,y=i%4*256,i//4*410')
 a=source.index("  scope='");b=source.index('\n  producer_sha256',a)
 source=source[:a]+"  scope='Historical V1430 named enemy-vessel capture2082,original55DC4(attacker,8) officerCharles18 and target virtual name Hanse Cog,Hull30/Crew0,direct53F0C/table02117B00. Two full RGB ink/blank masks freshly bind current expanded payload and native font. Sole frame4800 fixture owns40 live-position bytes for five existing own ships;completed whole4MiB/input and actual enemy-position audits are hash-bound without unnecessary replay. No health,crew,actor,role,RNG,result or later fixture change. Fifteen original states and ten individual-capture/flagship/victory/reward/cargo/sailing transitions bind RAM/images;context strings add zero prose credit. Original later10850 differs from V1404 only inside16x16 blinking A prompt per preserved1435b audit;no text or portrait waiver. Normal X Finish/touch Yes discard untransferred spoils before return to sailing. Only2082 individually activated;other seven use current offline/native name tests and representative family coverage. No new current emulator run,startup approval,earned travel,sinking,permanent fleet addition or hardware proof.',"+source[b:]
 source=source.replace('Two complete historical victory holds,6 corruptions,14 original states and9 capture/reward/cargo/sailing transitions pass.','Two complete historical named-capture holds,7 corruptions,15 original states and10 capture/reward/cargo/sailing transitions pass.')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
