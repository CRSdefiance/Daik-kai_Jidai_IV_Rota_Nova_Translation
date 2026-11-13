"""All16 current original voice selections and13 distinct native paragraphs."""
import textwrap
from pathlib import Path
from scripts import probe_hot_spring_fonts_v1617 as old
from scripts.current_common_native_context_v2620 import CurrentContext
from scripts.probe_common_single_cache_v862 import Loader
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/hot_spring_fonts_v2624')
DOC=Path('translations/hot_spring_contextual_editorial_manuscript_v1.json')
if __name__=='__main__':
 ctx=CurrentContext(DOC,'out/all_routes_combined_v1676_candidate.nds',ROOT);doc=read(DOC);context=read(doc['native_context_proof'])
 for table in context['voice_tables']:
  table['all207_existing_actor_choices']=[dict(existing_actor_ID=c['actor_ID'],source_voice=c['voice_class'],resolved_message_ID=c['message_ID'],uses_original_minus1_fallback_to_voice0=c['uses_original_minus1_fallback'])for c in table['all207_original_actor_choices']]
 def assigned(a,r,actor_id,actor):
  if actor_id==16:return r,dict(no_roster_fixture=True,original_logical_role1_actor=16)
  return old.assigned_role_raw(a,r,actor_id,actor)
 def consumer(a,c,r,p,entry,role,table):return ctx.speak(entry,role,table,raw=r)
 source=textwrap.dedent(Path(old.__file__).read_text().split("if __name__=='__main__':\n",1)[1]);end=source.index('for table in context')
 source="assert not any(raster(arm,b' ',0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000))\ncpu,get=get_machine(source_arm,raw);actors,captain=get(0xCB184),get(0x7F244);cases=[];findings=[]\n"+source[end:]
 source=source.replace("if choice['existing_actor_ID']!=captain:reps.setdefault(choice['source_voice'],choice)","if choice['existing_actor_ID']!=captain:reps.setdefault(choice['source_voice'],choice)\n    reps[1]=next(c for c in table['all207_existing_actor_choices']if c['existing_actor_ID']==16)")
 source=source.replace("assert query(0x82478,query(0xCB1A8)+0x2090,1)==actor_id","assert query(0x82478,query(0xCB1A8)+0x2090,1)==actor_id")
 env={**old.__dict__,'__file__':__file__,'ROOT':ROOT,'DOC':DOC,'PLAN':ctx.proof_path,'doc':doc,'context':context,'arm':ctx.arm,'source_arm':ctx.arm,'common':ctx.common,'raw':ctx.raw,'plan':ctx.plan,'entries':ctx.entries,'current':ctx.rom,'rows':{r['message_id']:r for r in doc['records']},'raster':ctx.raster,'consumer':consumer,'assigned_role_raw':assigned}
 exec(compile(source,__file__,'exec'),env)
 path=ROOT/'native_font_research.json';proof=read(path);gold=read('work/analysis/hot_spring_fonts_v1617/native_font_research.json');lookup={(c['source_table'],c['source_voice']):c for c in gold['cases']}
 for case in proof['cases']:
  before=lookup[(case['source_table'],case['source_voice'])]
  for k in ['message_ID','compiled_hex','lines','complete_ordered_glyph_events','native_zero_ink_continuation_guards','whole_native_font_plane_sha256']:assert case[k]==before[k],(case['message_ID'],k)
  assert case['native_pipeline']['formatted_hex']==before['native_pipeline']['formatted_hex']
 assert len(proof['cases'])==16 and not proof['findings'];assert sum(c['CPU_only_role_fixture'].get('no_roster_fixture',False)for c in proof['cases'])==2
 proof.update(candidate_sha256=sha(ctx.rompath.read_bytes()),all13_complete_native_cases=[next(c for c in proof['cases']if c['message_ID']==n)for n in range(2275,2288)],all26_native_cold_warm_copies=[Loader(ctx.arm,ctx.common).copy(n,ctx.entries[n].text,mode)for mode in ['cold','warm']for n in range(2275,2288)],review_sheets=proof['sheets_for_visual_review'],complete_native_font_cases=16,all16_current_voice_native_planes_golden_exact=True,all_executed_pipeline_instructions_current_ROM_byte_exact=True,all_original_actor_models_unchanged=True,blank_space_font_freshly_verified_zero_ink=True,pipeline_plan=str(ctx.proof_path),pipeline_plan_sha256=sha(ctx.proof_path.read_bytes()),unaltered_original_role1_Gerhard_cases=2,alternative_voice_single_byte_CPU_fixture_cases=14,scope='Current native CPU source selection, macro/wrapping and independent228x64 glyph planes. Two voice1 cases keep original Gerhard16 raw unchanged. Fourteen alternatives use isolated original-setter duty-byte fixtures. No new gameplay or forced optional branch.',full_goal_complete=False)
 save(path,proof);print('16 current voice/table pipelines,13 paragraphs,26 cold/warm copies golden-exact;no findings.')
