"""Eight role1 voice paths;five reports with both registered prose owners."""
from pathlib import Path
OLD=Path('scripts/verify_aftermath_fled_fonts_v2542.py')
if __name__=='__main__':
 source=OLD.read_text().replace('else255','else 255')
 changes={
  'aftermath_fled_fonts_v2542':'flagship_capture_fonts_v2582','aftermath_fled_contextual':'flagship_capture_contextual',
  'out/all_routes_combined_v1224_candidate.nds':'out/all_routes_combined_v1364_candidate.nds',
  'from scripts.battle_aftermath_native_plan_v1255 import compiled':'from scripts.review_flagship_capture_context_v2581 import compiled',
  "if row['actor_ID']!=captain:representatives.setdefault(row['message_ID'],row)":"if row['actor_ID']!=captain:representatives.setdefault(row['voice_class'],row)\n  if row['actor_ID']==16:representatives[row['voice_class']]=row",
  'set(representatives)==set(range(2046,2052))':'set(representatives)==set(range(8))',
  'work/analysis/battle_aftermath_fonts_v1260/native_font_proof.json':'work/analysis/flagship_precision_fonts_v1357/native_font_proof.json',
  " for row in doc['records']:":" records_by_ID={r['message_id']:r for r in doc['records']}\n for source_voice,r in sorted(representatives.items()):\n  row=records_by_ID[r['message_ID']]",
  'if n==2046:assigned,fixture=raw,None':'if source_voice==1:assigned,fixture=raw,None',
  "r=representatives[n];assigned,fixture=assigned_role_raw":"assigned,fixture=assigned_role_raw",
  '0x02117900':'0x02117740',
  "old=next(c for c in prior['cases']if c['message_id']==n and c['name_case']is None)":"old=next(c for c in prior['cases']if c['source_voice']==source_voice)",
  "old['native_formatted_hex']":"old['native_pipeline']['formatted_hex']",
  'case=dict(message_ID=n,message_id=n,':'case=dict(source_voice=source_voice,message_ID=n,message_id=n,',
  'previews.append(dict(path=str(p),':'previews.append(dict(source_voice=source_voice,path=str(p),',
  "p=ROOT/f'ID{n}_complete_current_role1_font.png'":"p=ROOT/f'voice{source_voice}_ID{n}_complete_current_role1_font.png'",
  "'ID'+str(item['message_ID'])+' current role1 portrait font'":"'Voice'+str(item['source_voice'])+' ID'+str(item['message_ID'])+' current role1 font'",
  '(936,462)':'(936,616)',
  'all6_current_fled_victory_native_fonts':'all8_current_flagship_capture_native_fonts',
  'for n in range(2046,2052)':'for n in range(2011,2016)',
  'len(cases)==6 and len(copies)==12':'len(cases)==8 and len(copies)==10',
  'all6_complete_native_cases=cases':'all5_complete_native_cases=[next(c for c in cases if c["message_ID"]==n)for n in sorted(records_by_ID)],all8_voice_pipeline_full_font_cases=cases',
  'all12_native_cold_warm_copies':'all10_native_cold_warm_copies',
  'all6_source_numeric_selection_complete_ABI_words_and_visible_ink_pass':'all5_source_numeric_selection_complete_ABI_words_and_visible_ink_pass',
  'all6_original_role1_pipelines':'all8_original_role1_pipelines','all_five_CPU_original_single_roster_byte_fixtures':'all_seven_CPU_original_single_roster_byte_fixtures',
  'complete_native_font_cases=6':'complete_native_font_cases=8,unique_native_reports=5',
  'Five alternatives use original setter82BB8':'Seven voice alternatives use original setter82BB8',
  'Six current role1 pipelines,full native fonts and12 cold/warm copies':'Eight current role1 pipelines,five full native reports and10 cold/warm copies',
 }
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 needle='  result=run(arm,common,assigned,plan,0x53D44,1,0x02117740,None)'
 extra="""  check,logical_get,_=machine(arm,common,assigned,plan);fleet=logical_get(0xCB1A8)
  assert logical_get(0x82478,fleet+0x2090,1)==r['actor_ID']
  assert (logical_get(0x82428,fleet+0x2090,1)==0)if source_voice==1 else (logical_get(0x82428,fleet+0x2090,1)==r['actor_object'])
  models=bytes(check.mem_read(root,0x1A04))
"""
 assert needle in source;source=source.replace(needle,extra+needle)
 source=source.replace('result.update(message_ID=n,','result.update(source_actor_ID=r["actor_ID"],source_voice=source_voice,logical82478_selection_verified=True,actual_voice1_logical16_physical0_unchanged=source_voice==1,message_ID=n,')
 needle=" save(ROOT/'native_font_proof.json',dict("
 extra=""" assert [c['source_voice']for c in cases]==list(range(8)) and [c['message_ID']for c in cases]==[2011,2011,2012,2011,2011,2013,2014,2015]
 assert len(fixtures)==7 and cases[1]['native_pipeline']['source_actor_ID']==16 and cases[1]['role_fixture'] is None
"""
 assert needle in source;source=source.replace(needle,extra+needle)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
