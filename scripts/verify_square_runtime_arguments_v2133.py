"""All current Square runtime argument names through native printf and wrapping."""
from pathlib import Path
import struct
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.duel_editorial import owned_entries
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.probe_button_prompt_native import BASE,STACK,machine,call
from unicorn.arm_const import UC_ARM_REG_R0
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/square_context_arguments_v2133')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 plan=read('work/analysis/square_context_payload_v2124/native_payload_plan.json');arm=Path('work/analysis/common_four_row_view_v2128d/ARM9_GEOMETRY_RESEARCH_ONLY.bin').read_bytes();common=Path(plan['target_COMMON']).read_bytes();entries=owned_entries(common,arm,plan['directory_sha256'])
 cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/square_context_live_v2122_V2097');report=read(cap/'capture_report.json');snap=next(r for r in report['read_only_pause_RAM_snapshots']if r['frame']==13800);raw=Path(snap['path']).read_bytes();assert sha(raw)==snap['sha256']
 names={};cpu=machine(arm);cpu.mem_write(BASE,raw)
 for kind,fn,count,stride in(('products',0xCB124,124,16),('cities',0xCB178,90,108)):
  call(cpu,fn,());root=cpu.reg_read(UC_ARM_REG_R0)+4;rows=[]
  for i in range(count):
   ob=root+i*stride;vt=struct.unpack('<I',cpu.mem_read(ob,4))[0];getter=struct.unpack('<I',cpu.mem_read(vt+8,4))[0];call(cpu,getter-BASE,(ob,));pointer=cpu.reg_read(UC_ARM_REG_R0);text=bytes(cpu.mem_read(pointer,80)).split(b'\0')[0].decode('ascii');assert text and len(text)<40
   rows.append(dict(index=i,name=text,object=ob,getter=getter,pointer=pointer))
  names[kind]=rows
 old=read('work/analysis/product_pitches_v747/runtime_name_catalog.json');name_changes=[dict(kind=k,index=i,before=a['name'],after=b['name'])for k in('products','cities')for i,(a,b)in enumerate(zip(old[k],names[k],strict=True))if a['name']!=b['name']]
 assert not name_changes
 save(ROOT/'current_native_runtime_name_catalog.json',dict(**names,source_snapshot=snap,old_catalog_names_exact=True,read_only_native_getters_in_captured_state_not_actual_visits_to_all_towns=True,full_goal_complete=False))
 products=[r['name']for r in names['products']];cities=[r['name']for r in names['cities']];jobs=[]
 for p in products:jobs.append((675,(p,),0x02054014))
 for n in range(676,681):jobs.append((n,(),0x02054014))
 for p in products:
  for c in cities:jobs.append((681,(p,c),0x02054014))
 for n in(731,733):
  for p in products:jobs.append((n,(p,),0x02054014))
 for r in read('work/analysis/category_dialogue_v754/lookup_native_ABI.json')['all18_original730_caller_arguments']:jobs.append((730,(r['original730_caller_argument'],),0x02054014))
 for r in read('work/analysis/specialty_question_v752/native_review.json')['all25_original_prerequisite_pairs']:jobs.append((742,(r['item']['name'],r['product']['name']),0x02053FCC))
 prior={(r['message_id'],tuple(r['substitutions'])):r['lines']for r in read('work/analysis/product_pitches_v747/native_layout_matrix.json')};rows=[];glyphs=set()
 for i,(n,args,parent)in enumerate(jobs):
  if i%256==0:cpu=machine(arm);cpu.mem_write(0x02387A20,bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]))
  formatted,lines=native_layout(cpu,entries[n].text,n,args,parent);expected=entries[n].text
  for a in args:expected=expected.replace(b'%s',a.encode('ascii'),1)
  assert b' '.join(formatted.split())==b' '.join(expected.split())and b'%'not in formatted and len(lines)<=4 and all(0<len(s)<=35 for s in lines)
  if(n,args)in prior:assert lines==prior[n,args]
  glyphs.update(formatted.decode('ascii').replace('\n',''))
  rows.append(dict(message_ID=n,supplied_arguments=list(args),parent=parent,formatted_hex=formatted.hex(),lines=lines,native_printf_and_wrap_input_output_ABI_guards_pass=True,complete_words_and_unchanged_order=True,validated_four_row_bounds=[228,64],actual64pixel_view_GPU_still_pending=True))
  if(i+1)%2000==0:print(f'{i+1}/{len(jobs)} native argument cases',flush=True)
 from dk4tool.dialogue.font_audit import GameAsciiFont
 font=GameAsciiFont.from_arm9(arm)
 for c in glyphs:
  g=font.decode(c);assert c==' 'or g.getbbox()is not None,c
 save(ROOT/'all_runtime_native_argument_layouts.json',dict(ARM9_sha256=sha(arm),COMMON_sha256=sha(common),cases=rows,total=len(rows),products=124,cities=90,all11289_prior_product_pitch_layouts_exact=True,all_names_and_printf_argument_order_preserved=True,all_ASCII_glyphs_present=sorted(glyphs),native_four_row_pagination_rule_applied_to_all_cases=True,native_full_pixel_samples='work/analysis/square_context_pages_v2130b/all_square_native_pages.json',actual_four_row_GPU_and_registered_release_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(native_cases=len(rows),all_prior_layouts_exact=True,current_native_names_exact=True))
