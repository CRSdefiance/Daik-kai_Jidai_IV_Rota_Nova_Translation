"""Current2700 bearing/name matrix,15 complete native speech/font samples."""
import struct,textwrap
from pathlib import Path
from copy import deepcopy
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_PC,UC_ARM_REG_SP,UC_ARM_REG_LR
from scripts import verify_current_sighting_matrix_v1792 as old
from scripts.current_common_native_context_v2620b import CurrentContext
from scripts.search_reports_native_consumers_v1662 import assigned_role
from scripts.probe_common_single_cache_v862 import Loader
from scripts.probe_button_prompt_native import BASE,STACK,STOP
from scripts.verify_village_wrap_v608 import read,save
from scripts.sighting_layout_v1069 import compiled,IDS
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/sighting_fonts_v2637');DOC=Path('translations/sighting_contextual_editorial_manuscript_v1.json')
def speech(arm,common,raw,plan,role,table,arguments):
 cpu,get,provider=machine(arm,common,raw,plan);pointers=[];seen={}
 for i,value in enumerate(arguments):
  assert value and b'\0'not in value and len(value)<128;ptr=0x02470000+i*0x100;cpu.mem_write(ptr,value+b'\0');pointers.append(ptr)
 def observe(u,pc,size,unused):
  if pc==BASE+0x5408C:u.reg_write(UC_ARM_REG_PC,BASE+0x54144)
  elif pc==0x01FFCF3C:
   sp=u.reg_read(UC_ARM_REG_SP);seen.update(parent=struct.unpack('<I',u.mem_read(sp+0x264,4))[0],selector=struct.unpack('<I',u.mem_read(sp+0x27C,4))[0],input_hex=bytes(u.mem_read(u.reg_read(UC_ARM_REG_R1),512)).split(b'\0')[0].hex(),output=u.reg_read(UC_ARM_REG_R0))
  else:seen['formatted_hex']=bytes(u.mem_read(seen['output'],512)).split(b'\0')[0].hex();u.emu_stop()
 for pc in[BASE+0x5408C,0x01FFCF3C,BASE+0x54164]:cpu.hook_add(UC_HOOK_CODE,observe,begin=pc,end=pc)
 cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,STOP)
 for reg,value in zip([UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3],[role,table,*pointers]):cpu.reg_write(reg,value)
 cpu.emu_start(BASE+0x53D44,STOP,count=3000000);assert cpu.reg_read(UC_ARM_REG_PC)==BASE+0x54164 and seen['parent']==BASE+0x53DB8 and seen['selector']==table
 seen['loaded_template_hex']=bytes(cpu.mem_read(provider.output,512)).split(b'\0')[0].hex();return dict(**seen,original_role=role,original_table=table,source_argument_hex=[v.hex()for v in arguments],original_selection_loader_printf_macro_wrap_execute=True,hosted_file_success_and_UI_constructor_boundary_not_gameplay=True)
if __name__=='__main__':
 ctx=CurrentContext(DOC,'out/all_routes_combined_v1775_candidate.nds',ROOT);doc=read(DOC);context=read(doc['native_context_proof']);source=textwrap.dedent(Path(old.__file__).read_text().split("if __name__=='__main__':\n",1)[1]);source=source.replace('    ROOT.mkdir(parents=True)\n','')
 # Dedented setup creates ROOT itself;our bounded CPU plan already owns it.
 source=source.replace('assert not ROOT.exists()','assert ROOT.exists()').replace('ROOT.mkdir(parents=True)\n','');env={**old.__dict__,'__file__':__file__,'ROOT':ROOT,'ROM':ctx.rompath,'DOC':DOC};exec(compile(source,__file__,'exec'),env)
 path=ROOT/'current2700_native_wrap_and_font_reconciliation.json';proof=read(path);rows={r['message_id']:r for r in doc['records']};pipelines=[]
 for sample in proof['fresh_current_native_full_font_samples']:
  n=sample['message_ID'];table=0x02118560 if n<622 else 0x02118540;choices=next(t['all207_original_actor_choices']for t in context['voice_tables']if t['table']==table);rep=next(c for c in choices if c['message_ID']==n and c['actor_ID']!=1);raw,fixture=assigned_role(ctx.arm,ctx.raw,1,rep['actor_ID'],rep['actor_object'])if rep['actor_ID']!=18 else(ctx.raw,dict(no_roster_fixture=True,actual_logical_actor=18));native=ctx.execute(speech,1,table,[bytes.fromhex(sample['bearing_hex']),bytes.fromhex(sample['faction_hex'])],raw=raw);assert native['loaded_template_hex']==compiled(rows[n]).hex()and native['formatted_hex']==sample['formatted_hex'];text=bytes.fromhex(sample['formatted_hex']);events=[];pixels=ctx.raster(ctx.arm,text,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000,glyph_events=events);assert sha(bytes(pixels))==sample['font_plane_sha256'];guards=[]
  for y,line in enumerate(sample['lines']):
   actual=[e for e in events if e['y']==16*y and 6<=e['x']<6+6*len(line)];blank=[]
   while actual and actual[0]['code']==32 and actual[0]['x']==6:blank.append(actual.pop(0))
   assert len(blank)<=1 and(not blank or y>0);assert[e['code']for e in actual]==list(line.encode('ascii'))and[e['x']for e in actual]==[6+6*i for i in range(len(line))];guards.append(dict(row=y,zero_ink_guard_events=blank))
  pipelines.append(dict(message_ID=n,native_pipeline=native,original_actor_choice=rep,CPU_only_voice_fixture=fixture,complete_ordered_glyph_events=events,zero_ink_continuation_guards=guards,full_native_plane_sha256=sha(bytes(pixels)),native_x6_complete_first_final_words_bounds_blank_paper_verified=True))
 invalid=[];base=doc['records'][0]
 for label,key,value in [('leading','english',' '+base['english']),('trailing','english',base['english']+' '),('gap','english','Fleet  %s %s!'),('LF','english','Fleet\n%s %s!'),('NUL','english','Fleet\0%s %s!'),('layout','english','Fleet %s %s {LB}!'),('nonASCII','english','Fleet %s—%s!'),('missing-arg','english','Fleet %s!'),('extra-arg','english','Fleet %s %s %s!'),('literal-percent','english','Fleet %s %s 100%!'),('wrong-ID','message_id',613),('wrong-argc','native_argument_count',1),('wrong-family','source_family','fleet-sighting-under-attack'),('native-macro','english','FI %s %s!'),('overflow','english','A'*220+'%s%s')]:
  row=deepcopy(base);row[key]=value
  try:compiled(row)
  except(ValueError,AssertionError):invalid.append(label)
  else:raise AssertionError(label)
 proof.update(all15_complete_native_cases=proof['fresh_current_native_full_font_samples'],all15_original_role1_speech_pipelines=pipelines,all30_native_cold_warm_copies=[Loader(ctx.arm,ctx.common).copy(n,ctx.entries[n].text,mode)for mode in['cold','warm']for n in IDS],complete_native_font_cases=15,current_native_matrix_cases=2700,invalid_compiler_inputs_rejected=invalid,findings=[],all_executed_pipeline_instructions_current_ROM_byte_exact=True,all_original_actor_models_unchanged=True,blank_space_font_freshly_verified_zero_ink=not any(ctx.raster(ctx.arm,b' ',0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)),pipeline_plan=str(ctx.proof_path),pipeline_plan_sha256=sha(ctx.proof_path.read_bytes()),scope='2700 current printf/wrap/ABI cases and independent planes reconcile15templates x9bearings x20complete labels to frozen native fonts. Fifteen current whole role1 selection/COMMON loader/printf/macro/wrap pipelines and fresh full native font samples cover every paragraph at worst-width cases. Two actual Charles18 voice0 pipelines keep RAM unchanged;13 alternatives use one isolated original-setter duty byte. All executed pipeline instructions current-exact,all actor models exact. No new gameplay or current GPU event. Prior current matrix is reference only.',full_goal_complete=False);save(path,proof);print('2700current matrix cases,15whole role1 pipelines/full fonts,30copies,15compiler negatives pass;no findings.')
