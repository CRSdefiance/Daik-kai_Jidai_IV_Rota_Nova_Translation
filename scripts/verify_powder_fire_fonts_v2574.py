"""Eight current direct gunner voice paths,six unique alerts,complete native fonts."""
from pathlib import Path
OLD=Path('scripts/verify_aftermath_city_fonts_v2566.py')
if __name__=='__main__':
 outer=OLD.read_text();needle="\n exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})";assert outer.count(needle)==1
 env={'__name__':'__main__','__file__':__file__};exec(compile(outer.replace(needle,'\n captured_effective_source=source'),__file__,'exec'),env);source=env['captured_effective_source']
 changes={
  'aftermath_city_fonts_v2566':'powder_fire_fonts_v2574','aftermath_city_contextual':'powder_fire_contextual',
  'out/all_routes_combined_v1224_candidate.nds':'out/all_routes_combined_v1316_candidate.nds','from scripts.battle_aftermath_native_plan_v1255 import compiled':'from scripts.powder_fire_native_plan_v1309 import compiled',
  "representatives.setdefault(row['message_ID'],row)":"representatives.setdefault(row['voice_class'],row)\n  if row['actor_ID']==16:representatives[row['voice_class']]=row",
  'set(representatives)==set(range(2038,2046))':'set(representatives)==set(range(8))',
  'work/analysis/battle_aftermath_fonts_v1260/native_font_proof.json':'work/analysis/powder_fire_fonts_v1310/native_font_proof.json',
  " for row in doc['records']:":" records_by_ID={r['message_id']:r for r in doc['records']}\n for source_voice,r in sorted(representatives.items()):\n  row=records_by_ID[r['message_ID']]",
  "r=representatives[n];actor=r['actor_object'];assigned,fixture=raw,None":"actor=r['actor_object'];assigned,fixture=raw,None",
  '0x021178C0':'0x02117980',
  'case=dict(message_ID=n,message_id=n,':'case=dict(source_voice=source_voice,message_ID=n,message_id=n,',
  'previews.append(dict(path=str(p),':'previews.append(dict(source_voice=source_voice,path=str(p),',
  "'ID'+str(item['message_ID'])+' current direct defender font'":"'Voice'+str(item['source_voice'])+' ID'+str(item['message_ID'])+' current gunner font'",
  'all8_current_direct_city_native_fonts':'all8_current_powder_fire_voice_native_fonts','for n in range(2038,2046)':'for n in range(2052,2058)',
  'len(cases)==8 and len(copies)==16':'len(cases)==8 and len(copies)==12',
  'all8_complete_native_cases=cases':'all6_complete_native_cases=[next(c for c in cases if c["message_ID"]==n)for n in sorted(records_by_ID)],all8_voice_pipeline_full_font_cases=cases',
  'all16_native_cold_warm_copies':'all12_native_cold_warm_copies',
  'all8_source_numeric_selection_complete_ABI_words_and_visible_ink_pass':'all6_source_numeric_selection_complete_ABI_words_and_visible_ink_pass',
  'all8_original_direct_defender_pipelines':'all8_original_direct_gunner_pipelines',
  'Current isolated CPU original53F0C direct defender selection':'Current isolated CPU original53F0C direct gunner selection for all eight voice classes including both first-valid2052 fallback voices',
  'Eight current direct-defender pipelines,full native fonts and16 cold/warm copies':'Eight current direct-gunner voice pipelines,six unique full native alerts and12 cold/warm copies',
 }
 for a,b in changes.items():
  assert a in source,a
  source=source.replace(a,b)
 needle=" save(ROOT/'native_font_proof.json',dict("
 extra=""" assert [c['source_voice']for c in cases]==list(range(8))
 assert [c['message_ID']for c in cases]==[2052,2053,2052,2052,2054,2055,2056,2057]
 assert next(c for c in cases if c['source_voice']==1)['native_pipeline']['source_actor_ID']==16
"""
 assert source.count(needle)==1;source=source.replace(needle,extra+needle)
 source=source.replace('complete_native_font_cases=8,findings=findings,','complete_native_font_cases=8,unique_native_alerts=6,all_eight_voices_and_both_fallbacks_current_native_verified=True,findings=findings,')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
