"""Fresh current actor/name and whole-selector controls for25 Deck comments."""
from pathlib import Path
import struct,unicodedata
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_PC,UC_ARM_REG_LR
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/personal_context_v2297');ROM=Path('out/all_routes_combined_v2284_candidate.nds')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');rptpath=Path('E:/Rota Nova translations/Generated/work/emulation_v193/refit_spritsail_v2292_refit_V2284/capture_report.json');rpt=read(rptpath);assert rpt['ROM_sha256']==sha(ROM.read_bytes());snapshot=next(r for r in rpt['read_only_capture_RAM_snapshots']if r['frame']==3200);raw=Path(snapshot['path']).read_bytes();assert snapshot['read_only_export']and sha(raw)==snapshot['sha256']and len(raw)==0x400000
 spans=[(0x12104,0x12920),(0x15334,0x154E8),(0x13D80,0x13E0C),(0x15948,0x159C4),(0x1CA10,0x1CB84)]
 assert all(arm[a:b]==clean[a:b]for a,b in spans);assert struct.unpack_from('<I',arm,0x122A0)[0]==struct.unpack_from('<I',arm,0x128B0)[0]==struct.unpack_from('<I',arm,0x12918)[0]==1361
 cpu,get=get_machine(arm,raw);actors=get(0xCB184);hero=get(0x7F244);globalstate=get(0x3F0F8);fields=list(struct.unpack('<2I',cpu.mem_read(globalstate+8,8)));assert fields!=[0,1];names=[];expected={r['actor_ID']:r['speaker']for r in read('translations/personal_chatter_editorial_manuscript_v3.json')['records']}
 for actor in range(25):
  obj=actors+0x19E4 if actor==hero else actors+4+actor*32;vt=struct.unpack('<I',cpu.mem_read(obj,4))[0];fn=struct.unpack('<I',cpu.mem_read(vt+0x20,4))[0];pointer=get(fn-0x02000000,obj);native=bytes(cpu.mem_read(pointer,80)).split(b'\0')[0];name=unicodedata.normalize('NFKC',native.decode('cp932'));assert name==expected[actor],(actor,name,expected[actor]);names.append(dict(actor_ID=actor,current_native_name=name,native_hex=native.hex(),object=obj,getter=fn,pointer=pointer))
 chosen=[]
 def numeric(u,pc,size,unused):chosen.append(u.reg_read(UC_ARM_REG_R0));u.reg_write(UC_ARM_REG_R0,0x02450000);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
 h=cpu.hook_add(UC_HOOK_CODE,numeric,begin=0x0205528C,end=0x0205528C);cases=[]
 try:
  for actor in range(25):
   for fn,args in((0x12838,(actor,)),(0x12104,(actor,1)),(0x12104,(actor,3))):
    chosen.clear();result=get(fn,*args);assert chosen==[1361+actor]and result==0x02450000;cases.append(dict(actor_ID=actor,name=names[actor]['current_native_name'],function=0x02000000+fn,arguments=list(args),selected_ID=chosen[0],complete_original_selection_ABI_pass=True))
 finally:cpu.hook_del(h)
 md=Cs(CS_ARCH_ARM,CS_MODE_ARM);listings={f'{lo:06X}-{hi:06X}':[f'{i.address:08X} {i.mnemonic} {i.op_str}'for i in md.disasm(clean[lo:hi],0x02000000+lo)]for lo,hi in spans}
 save(ROOT/'native_context.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),source_report=str(rptpath),source_report_sha256=sha(rptpath.read_bytes()),genuine_current_preinteraction_snapshot=snapshot,current_hero_index=hero,current_global_context_fields_at8_and12=fields,all25_current_actor_names=names,all75_native_actor_specific_state1_and_supplementary_state3_selections=cases,all_source_code_spans_clean_exact=[dict(start=a,end=b,sha256=sha(arm[a:b]))for a,b in spans],source_disassembly=listings,original_COMMON_boundary_intercepted_only_after_numeric_selection=0x0205528C,current_COMMON_boundary_hex=arm[0x5528C:0x552A4].hex(),COMMON_loader_boundary_not_claimed_clean_exact=True,activity_comments_independent_by_actor_not_adjacent_speeches=True,normal_caller_chain=['0201CB6C Deck list-state','02013DCC ->02015948','020159B0 ->02015334','02015478 ->02012104(actor,state)','02012284 ->02012838 forstate1 under context other than[0,1]','0201288C selects1361+actor','02012894 ->COMMON loader0205528C'],source_embedded_draw=0x020154CC,source_draw_Y=60,native_216x36_crop_metadata=list(struct.unpack_from('<2I',arm,0x1147B8)),supplied_actor_and_state_inputs_are_CPU_controls_not25_actual_visits=True,no_ROM_live_RAM_save_or_gameplay_fixture_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(current_names=25,complete_native_selections=75,source_clean_spans=len(spans),no_actual_25_visit_claim=True))
