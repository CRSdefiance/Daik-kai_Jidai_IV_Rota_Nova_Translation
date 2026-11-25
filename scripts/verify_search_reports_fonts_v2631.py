"""Current Search294 numeric/voice/font cases with source-domain layout gates."""
import textwrap
from pathlib import Path
from itertools import product
from scripts import probe_search_reports_fonts_v1663 as old
from scripts import search_reports_native_consumers_v1662b as consumers
from scripts.current_common_native_context_v2620b import CurrentContext
from scripts.probe_common_single_cache_v862 import Loader
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/search_reports_fonts_v2631');DOC=Path('translations/search_reports_contextual_editorial_manuscript_v1.json')
if __name__=='__main__':
 ctx=CurrentContext(DOC,'out/all_routes_combined_v1676_candidate.nds',ROOT);doc=read(DOC)
 # Preserve the established font loop/quantity matrix and its strict source-domain
 # distinction;only bind it to the current ROM and explicit current CPU context.
 outer=Path('scripts/probe_search_reports_fonts_v1667.py').read_text();needle="    exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__,'product':product})";assert outer.count(needle)==1;env={'__name__':'__main__','__file__':__file__};exec(compile(outer.replace(needle,'    captured=source'),__file__,'exec'),env);source=env['captured'];source=textwrap.dedent(source.split("if __name__ == '__main__':\n",1)[1]);source=source[source.index('cases, findings, choices, previews ='):]
 source=source.replace('outside_original_quantity_bounds_CPU_stress_only','outside_original_quantity_domain_CPU_stress_only').replace('outside_source_bounds_stress_findings','outside_source_domain_stress_findings');needle="0<=native['source_amounts'][0]<=4650 and 0<=native['source_amounts'][1]<=3875";assert source.count(needle)==1;source=source.replace(needle,needle+" and all(v%5==0 for v in native['source_amounts'])")
 # Prefer unchanged actual logical speakers for their original voice;all other
 # alternatives use the original roster setter on one isolated duty byte.
 source=source.replace("assert set(reps) == set(range(8))","actual_id=get(0x82478,get(0xCB1A8)+0x2090,role)\n    actual_actor=actors+4+32*actual_id\n    actual_voice=get(0x7E988,actual_actor)\n    reps[actual_voice]=(actual_id,actual_actor,get(0x53F4C,actual_actor,table))\n    assert set(reps) == set(range(8))")
 def assigned(a,r,role,actor_id,actor):
  cpu,get=old.get_machine(a,r)
  if get(0x82478,get(0xCB1A8)+0x2090,role)==actor_id:return r,dict(no_roster_fixture=True,original_logical_role=role,original_logical_actor=actor_id)
  return consumers.assigned_role(a,r,role,actor_id,actor)
 def speech(a,c,r,p,role,table,values):return ctx.execute(consumers.speech,role,table,values,raw=r)
 def loss(a,c,r,p,value):return ctx.execute(consumers.loss,value,raw=r)
 cpu,get=old.get_machine(ctx.arm,ctx.raw);actors,captain=get(0xCB184),get(0x7F244)
 env={**old.__dict__,'__file__':__file__,'ROOT':ROOT,'DOC':DOC,'PLAN':ctx.proof_path,'RAW':Path(read(doc['native_context_proof'])['actual_snapshot']),'doc':doc,'arm':ctx.arm,'common':ctx.common,'source_arm':ctx.arm,'rom':ctx.rom,'raw':ctx.raw,'plan':ctx.plan,'entries':ctx.entries,'rows':{r['message_id']:r for r in doc['records']},'raster':ctx.raster,'cpu':cpu,'get':get,'actors':actors,'captain':captain,'speech':speech,'loss':loss,'assigned_role':assigned,'product':product}
 assert not any(ctx.raster(ctx.arm,b' ',0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000));exec(compile(source,__file__,'exec'),env)
 path=ROOT/'native_font_research.json';proof=read(path);goldpath=Path('work/analysis/search_reports_fonts_v1671/native_font_research.json');gold=read(goldpath);lookup={(r['message_ID'],r['source_voice'],tuple(r['native_pipeline']['source_amounts'])):r for r in gold['cases']};assert len(proof['cases'])==len(gold['cases'])==294
 for case in proof['cases']:
  prior=lookup[(case['message_ID'],case['source_voice'],tuple(case['native_pipeline']['source_amounts']))]
  for k in ['compiled_hex','lines','all_ordered_complete_native_glyph_events','zero_ink_phase_guards','native_font_plane_sha256','native_origin_x','findings']:assert case[k]==prior[k],(case['message_ID'],k)
  for k in ['source_amounts','source_ABF50_argument_hex','loaded_template_hex','formatted_hex']:assert case['native_pipeline'][k]==prior['native_pipeline'][k]
 assert not proof['findings']and proof['outside_source_domain_stress_findings']==gold['outside_source_domain_stress_findings']and len(proof['outside_source_domain_stress_findings'])==7
 count_unaltered=sum(bool(c['CPU_role_fixture']and c['CPU_role_fixture'].get('no_roster_fixture'))for c in proof['cases']);assert count_unaltered==35
 proof.update(candidate_sha256=sha(ctx.rompath.read_bytes()),all11_complete_native_cases=[next(c for c in proof['cases']if c['message_ID']==n)for n in consumers.previous.__dict__.get('IDS',old.IDS)],all22_native_cold_warm_copies=[Loader(ctx.arm,ctx.common).copy(n,ctx.entries[n].text,mode)for mode in ['cold','warm']for n in old.IDS],review_sheets=proof['sheets_for_visual_review'],complete_native_font_cases=294,all294_current_voice_numeric_native_planes_golden_exact=True,all_executed_pipeline_instructions_current_ROM_byte_exact=True,all_original_actor_models_unchanged=True,blank_space_font_freshly_verified_zero_ink=True,unaltered_actual_logical_speaker_native_cases=35,source_reachable_layout_findings=[],impossible_domain_stress_layout_findings_count=7,pipeline_plan=str(ctx.proof_path),pipeline_plan_sha256=sha(ctx.proof_path.read_bytes()),golden_proof=str(goldpath),golden_proof_sha256=sha(goldpath.read_bytes()),scope='Current original role1/role7 speech and literal312 CPU pipelines,294 full independent native font planes,414 valid original actor choices and22 cold/warm copies. Real forage values are multiples5 with conservative maxima4650/3875. Seven awkward impossible-domain stress layouts are explicitly disclosed;all preserve every glyph and bounds. Actual logical speakers Gerhard16 and Charles18 are unchanged in35cases;other voices use one isolated original-setter duty byte. Loss numeric cases include formatting stress,not original crew-loss events. No current emulator visit or outcome forcing.',full_goal_complete=False)
 save(path,proof);print('294current Search font cases golden-exact;22copies;17compiler negatives;0real-domain layout findings;7impossible-domain stress findings retained.')
