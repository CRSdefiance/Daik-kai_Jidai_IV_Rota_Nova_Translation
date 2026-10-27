"""Fresh historical2131 masks and complete capture/victory/reward/cargo/sailing flow."""
from pathlib import Path
if __name__=='__main__':
 outer=Path('scripts/rebind_flagship_capture_history_v2583b.py').read_text();needle="\n exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})";assert outer.count(needle)==1
 env={'__name__':'__main__','__file__':__file__};exec(compile(outer.replace(needle,'\n captured=source'),__file__,'exec'),env);source=env['captured']
 changes={
 'flagship_capture_history_v2583b':'battle_victory_history_v2591',
 'from dk4tool.patch.flagship_capture_precision import current_entries as old_entries':'from dk4tool.patch.battle_victory_editorial import current_entries as old_entries',
 'out/all_routes_combined_v1364_candidate.nds':'out/all_routes_combined_v1404_candidate.nds',
 'range(2011,2016)':'range(2130,2138)',
 'work/analysis/flagship_capture_verified_v1370/actual_flagship_capture_verification.json':'work/analysis/battle_victory_verified_v1410/actual_victory_and_return_verification.json',
 'all4MiB_fixture_input_schedule_primary_RAM_and_PNG_hash_audits_pass':'entire4MiB_fixture_input_primary_RAM_and_PNG_hash_audits_pass',
 "historical['sole_fixture']":"historical['sole_prebattle_fixture']",
 'original_duel_victory_capture_and_return_code_exact_clean':'original_victory_duel_capture_reward_and_logical_role_code_exact_clean',
 'work/analysis/flagship_capture_fonts_v2582/native_font_proof.json':'work/analysis/battle_victory_fonts_v2590/native_font_proof.json',
 '2011':'2131','0x02117740':'0x02117EE0','(10800,10850)':'(10950,11000)',
 'work/analysis/flagship_capture_replay_v1369/original_departure_inputs.json':'work/analysis/battle_victory_replay_v1409/original_departure_inputs.json',
 "entries[2131].text.index(b'We')":"entries[2131].text.index(b'Admiral')",
 "bytes.fromhex(case['native_formatted_hex']).index(b'We')":"bytes.fromhex(case['native_formatted_hex']).index(b'Admiral')",
 'corrupt-resident-leading-W':'corrupt-resident-leading-A','corrupt-wrapped-leading-W':'corrupt-wrapped-leading-A',
 'verify(10800':'verify(10950','source_raw(10800)':'source_raw(10950)',
 'len(controls)==7':'len(controls)==6','seven_negative_controls_current_binding_on_offline_clones':'six_negative_controls_current_binding_on_offline_clones',
 'historical_flagship_capture_current_binding':'historical_battle_victory_current_binding',
 'all5_current_historical_payloads_and_all8_voice_font_planes_equal':'all8_current_historical_payloads_and_voice_font_planes_equal',
 'only2131_has_individual_historical_activation_other4_use_family_sample':'only2131_has_individual_historical_activation_other7_use_family_sample',
 'two_historical_complete_capture_holds':'two_historical_complete_victory_holds',
 'historical_capture_rewards_cargo_and_sailing':'historical_capture_victory_rewards_cargo_and_sailing',
 }
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 a=source.index(" line=case['lines'][0]");b=source.index(' bad=image.copy();bad.putpixel',a)
 source=source[:a]+""" line=case['lines'][0]
 for column,label in((0,'erase-complete-leading-A'),(len(line)-1,'erase-final-exclamation'),(line.index('victory'),'erase-interior-victory-v')):
  bad=image.copy();x,y=22+column*6,296;bad.paste('white',(x,y,x+6,y+11));controls.append(dict(negative=label,rejected=rejected(lambda:verify(10950,image_override=bad))))
"""+source[b:]
 a=source.index(' states = []');b=source.index(' ROOT.mkdir(parents=True);',a)
 original=Path('scripts/verify_battle_victory_replay_v1410.py').read_text();c=original.index('    states = []');d=original.index('    ROOT.mkdir',c)
 block='\n'.join(line[3:]if line.startswith('   ')else line for line in original[c:d].splitlines()).replace('raw(frame)','source_raw(frame)')+'\n'
 block+=""" assert states==historical['original_result_reward_cargo_return_states']and historical['normal_victory_A_dismissal_rewards_X_cargo_finish_touch_Yes_and_return_to_sailing']and historical['untransferred_spoil_cargo_discarded_through_original_confirmation_not_silently_claimed_acquired']
 flow=[]
 for frame,label in((10800,'preceding flagship capture;context only'),(10950,'complete victory report before normal A dismissal'),(11100,'provisions reward;context only'),(11300,'captured coins;context only'),(11500,'national-coins reward;context only'),(12400,'actual cargo-transfer screen before normal X Finish'),(12700,'original confirmation before touch Yes discards untransferred spoil cargo'),(12900,'power reward;context only'),(13200,'ordinary sailing after rewards and cargo disposition;source mode0')):
  picture=Path(images[frame]['path']);assert sha(picture.read_bytes())==images[frame]['PNG_sha256'];flow.append(dict(frame=frame,visually_reviewed_state=label,RAM=str(snapshots[frame]['path']),RAM_sha256=sha(source_raw(frame)),capture=str(picture),capture_sha256=sha(picture.read_bytes()),historical_only_not_current_startup_or_whole_route_approval=True))
"""
 source=source[:a]+block+source[b:]
 source=source.replace("spans=[tuple(r)for r in historical['original_victory_duel_capture_reward_and_logical_role_code_exact_clean']];assert all(arm[a:b]==oldarm[a:b]for a,b in spans)","spans=[tuple(r)for r in historical['original_victory_duel_capture_reward_and_logical_role_code_exact_clean']];cleanarm=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');assert all(arm[a:b]==oldarm[a:b]==cleanarm[a:b]for a,b in spans)")
 a=source.index("  scope='");b=source.index('\n  producer_sha256',a)
 source=source[:a]+"  scope='Historical V1404 original battle victory2131 after capture,role1 logical82478 member16 Gerhard with physical First Mate empty. Sole frame4800 fixture owns40 live-position bytes for five existing own ships;completed whole4MiB/input audits and actual-loaded enemy-position reference hash bound. No health,crew,actor,role,RNG,result or later fixture change. Two full RGB ink/blank masks freshly bind current native text/font. Fourteen original states and nine preceding-capture/victory/reward/cargo/sailing transitions bind actual RAM/images;context strings add zero prose credit. Normal X Finish,touch Yes discards untransferred spoils,and reward dismissal returns to sailing. Only2131 individually activated;other seven use current offline/native tests and representative family coverage. No new current emulator run,startup approval,earned travel,sinking,permanent fleet addition or hardware proof.',"+source[b:]
 source=source.replace('Two complete historical capture holds,7 corruptions,15 original states and9 reward/cargo/sailing transitions pass.','Two complete historical victory holds,6 corruptions,14 original states and9 capture/reward/cargo/sailing transitions pass.')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
