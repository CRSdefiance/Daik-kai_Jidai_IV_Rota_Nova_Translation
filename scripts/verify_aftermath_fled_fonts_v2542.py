"""Current role1 pipelines and six complete portrait fonts, with bounded overlays."""
from pathlib import Path
from types import FunctionType,SimpleNamespace
import struct
from ndspy.code import MainCodeFile
from PIL import Image,ImageDraw
from unicorn import UC_HOOK_CODE
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET,TABLE_OFFSET
from scripts.probe_escape_direct_source_v1186 import machine
from scripts.probe_battle_aftermath_fonts_v1256 import consumer,assigned_role_raw
from scripts.probe_reinforcement_sniping_layout_v1030 import native_layout
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.battle_aftermath_native_plan_v1255 import compiled
from scripts.probe_common_single_cache_v862 import Loader
from scripts.probe_button_prompt_native import BASE
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/aftermath_fled_fonts_v2542');ROM=Path('out/all_routes_combined_v2284_candidate.nds');OLDROM=Path('out/all_routes_combined_v1224_candidate.nds')
DOC=Path('translations/aftermath_fled_contextual_editorial_manuscript_v1.json')
if __name__=='__main__':
 assert not ROOT.exists()
 rom,oldrom=map(NdsImage.open,(ROM,OLDROM));arm=rom.read_file('/__arm9__.bin');oldarm=oldrom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm)
 doc=read(DOC);context=read(doc['native_context_proof']);raw=Path(context['actual_snapshot']).read_bytes()
 assert sha(raw)==context['actual_snapshot_sha256']and sha(ROM.read_bytes())==doc['current_ROM_sha256']
 oldplan=read('work/analysis/escape_direct_runtime_v1184c/runtime_plan.json')
 audited=[(0x132020,16),(0x147B9C,212),(0x147E54,172),(0x169F78,12),(0x16A010,8),(0x16A05C,8),(0x16A0B0,16)]
 spans=[(a-BASE,b-a)for a,b in oldplan['private_spans']]+audited+[(DIRECTORY_OFFSET,41*4),(TABLE_OFFSET,3668*2),(0x535E8,64)]
 merged=[]
 for at,size in sorted(spans):
  if merged and at<=merged[-1][0]+merged[-1][1]:lo,length=merged[-1];merged[-1]=(lo,max(lo+length,at+size)-lo)
  else:merged.append((at,size))
 patches=[]
 for at,size in merged:
  before=raw[at:at+size];assert before==oldarm[at:at+size],hex(at)
  patches.append(dict(address=BASE+at,source_hex=before.hex(),target_hex=arm[at:at+size].hex()))
 sections=MainCodeFile(arm,BASE).sections;oldsections=MainCodeFile(oldarm,BASE).sections
 assert len(sections[3].data)-48==len(oldsections[3].data)-48==123040
 delta=[i for i,(a,b)in enumerate(zip(oldsections[3].data[:-48],sections[3].data[:-48],strict=True))if a!=b]
 assert delta==list(range(0x5D4,0x5DC))
 before=bytes(oldsections[3].data[0x5D4:0x5DC]);after=bytes(sections[3].data[0x5D4:0x5DC]);assert before==bytes.fromhex('8265617469636961')and after==b'Faticia\0'
 assert raw[POOL-BASE+0x5D4:POOL-BASE+0x5DC]==before
 patches.append(dict(address=POOL+0x5D4,source_hex=before.hex(),target_hex=after.hex()));plan=dict(patches=patches)
 sections=[*sections,SimpleNamespace(ramAddress=POOL,data=sections[3].data[:-48])]
 cpu,get,_=machine(arm,common,raw,plan);root=get(0xCB184);captain=get(0x7F244)
 representatives={}
 for row in context['all208_original_voice_selections']:
  if row['actor_ID']!=captain:representatives.setdefault(row['message_ID'],row)
 assert set(representatives)==set(range(2046,2052))
 def current_machine(a,c,r,p):
  cpu,get,provider=machine(a,c,r,p);executed=set()
  def exact(u,pc,size,unused):
   for section in sections:
    start=section.ramAddress
    if start<=pc and pc+size<=start+len(section.data):
     assert bytes(u.mem_read(pc,size))==bytes(section.data[pc-start:pc-start+size]),('executed old instruction',hex(pc))
     executed.add(pc);break
  cpu.hook_add(UC_HOOK_CODE,exact);provider.executed_current=executed
  return cpu,get,provider
 run=FunctionType(consumer.__code__,{**consumer.__globals__,'portrait_machine':current_machine},argdefs=consumer.__defaults__)
 class CurrentFont:
  @staticmethod
  def open(path):
   assert str(path)=='out/all_routes_combined_v255_candidate.nds'
   return rom
 raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
 ROOT.mkdir(parents=True);save(ROOT/'current_native_pipeline_plan.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(common),historical_snapshot=context['actual_snapshot'],historical_snapshot_sha256=sha(raw),historical_ROM=str(OLDROM),historical_ROM_sha256=sha(OLDROM.read_bytes()),patches=patches,current_audited_table_gate_entry_exit_extents=audited,current_deployed_payload_delta=delta,no_whole_initialized_RAM_overlay=True,full_goal_complete=False))
 cases=[];previews=[];pipelinecases=[];fixtures=[];findings=[];prior=read('work/analysis/battle_aftermath_fonts_v1260/native_font_proof.json')
 for row in doc['records']:
  n=row['message_id'];text=compiled(row);assert text==entries[n].text==bytes.fromhex(row['current_hex'])
  if n==2046:assigned,fixture=raw,None
  else:
   r=representatives[n];assigned,fixture=assigned_role_raw(arm,raw,r['actor_ID'],r['actor_object']);fixtures.append(fixture)
  result=run(arm,common,assigned,plan,0x53D44,1,0x02117900,None)
  assert result['input_hex']==text.hex()and result['parent']==0x02053DB8 and result['selector_offset']==0x27C and result['selector']==0x02117900
  result.update(message_ID=n,source_role=1,role_fixture=fixture,all_executed_section_instructions_current_including_deployed_pool=True);pipelinecases.append(result)
  formatted,lines=native_layout(prepared(arm),text,n,None,0x02117900)
  assert formatted.hex()==result['formatted_hex']and ' '.join(lines)==row['english']
  pixels=raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)
  assert pixels==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),lines)
  old=next(c for c in prior['cases']if c['message_id']==n and c['name_case']is None)
  assert formatted.hex()==old['native_formatted_hex']and lines==old['lines']
  historicalpixels=Image.open(old['preview']).convert('L');assert sha(Path(old['preview']).read_bytes())==old['preview_sha256']
  assert historicalpixels.tobytes()==bytes(0 if v else255 for v in pixels)
  weak=[i for i,line in enumerate(lines[:-1])if line.split()[-1].strip('.,!?;:').lower()in{'a','an','the','to','of','with','for','from','on','in','as','at'}]
  orphan=len(lines)>1 and len(lines[-1].split())==1
  assert not weak and not orphan
  p=ROOT/f'ID{n}_complete_current_role1_font.png';Image.frombytes('L',(228,64),bytes(0 if v else255 for v in pixels)).save(p)
  case=dict(message_ID=n,message_id=n,compiled_hex=text.hex(),native_formatted_hex=formatted.hex(),lines=lines,native_cell_widths=[len(s)for s in lines],native_font_sha256=sha(pixels),native_pipeline=result,role_fixture=fixture,
   complete_native_original_printf_wrap_ABI_scratch_guards_words_first_final_glyphs_and228x64_independent_font_pass=True,all_current_historical_native_formatted_bytes_and_full_font_planes_equal=True,
   four_row_limit_35_cells_uniform_x6_margins_pass=True,weak_line_end_indices=weak,single_word_final_row=orphan,preview=str(p),preview_sha256=sha(p.read_bytes()))
  cases.append(case);previews.append(dict(path=str(p),sha256=sha(p.read_bytes()),message_ID=n,lines=lines));print(n,lines,'current original role1 pipeline and full228x64 font pass',flush=True)
 sheet=Image.new('RGB',(936,462),'#263238');draw=ImageDraw.Draw(sheet)
 for i,item in enumerate(previews):
  x,y=i%2*468,i//2*154;draw.text((x+5,y+3),'ID'+str(item['message_ID'])+' current role1 portrait font',fill='white');sheet.paste(Image.open(item['path']).resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
 p=ROOT/'all6_current_fled_victory_native_fonts.png';sheet.save(p)
 loader=Loader(arm,common);copies=[loader.copy(n,entries[n].text,mode)for mode in('cold','warm')for n in range(2046,2052)]
 assert len(cases)==6 and len(copies)==12
 save(ROOT/'native_font_proof.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(common),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
  cases=cases,all6_complete_native_cases=cases,all12_native_cold_warm_copies=copies,native_file_IO_explicit_host_contract=True,
  all6_source_numeric_selection_complete_ABI_words_and_visible_ink_pass=True,current_parent_projection_controls=0,current_portrait_consumer_no_Deck_or_duel_projection_claim=True,
  all6_original_role1_pipelines=pipelinecases,all_executed_pipeline_instructions_current_ROM_byte_exact=True,all_five_CPU_original_single_roster_byte_fixtures=fixtures,
  source_no_current_emulator_run_or_earned_assignment_claim=True,complete_native_font_cases=6,findings=findings,
  pipeline_plan=str(ROOT/'current_native_pipeline_plan.json'),pipeline_plan_sha256=sha((ROOT/'current_native_pipeline_plan.json').read_bytes()),
  review_sheets=[dict(path=str(p),sha256=sha(p.read_bytes()))],visual_review_pending=True,
  scope='Current isolated CPU original53D44 role1 selection,COMMON loader,printf,macro,scoped formatter,complete native fonts and ABI. Five alternatives use original setter82BB8 on one empty duty byte in CPU copies;all actor IDs and remaining4MiB model bytes stay exact. Historical snapshot is not a new visit. File success,portrait UI construction bypass and stop before runtime painter are explicit source-pipeline boundaries;full native painter executes separately.',
  producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print('Six current role1 pipelines,full native fonts and12 cold/warm copies pass;historical gameplay binding remains separate.')
