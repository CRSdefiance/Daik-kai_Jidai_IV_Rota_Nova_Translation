"""Research COMMON text-view height inside its unchanged256x96 panel."""
from pathlib import Path
import struct
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.probe_button_prompt_native import call
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from unicorn import UC_HOOK_MEM_INVALID
ROOT=Path('work/analysis/common_four_row_view_v2128d')
BASE=0x02000000
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 plan=read('work/analysis/square_context_payload_v2124/native_payload_plan.json');arm=Path(plan['target_ARM9']).read_bytes();clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');assert arm[0x54C28:0x54CF8]==clean[0x54C28:0x54CF8]
 assert struct.unpack_from('<2I',arm,0x118AC8)==(228,48)and struct.unpack_from('<2I',arm,0x118AE8)==(256,96)
 code=MainCodeFile(arm,BASE);code.sections[0].data[0x118ACC:0x118AD0]=struct.pack('<I',64);target=bytes(code.save());path=ROOT/'ARM9_GEOMETRY_RESEARCH_ONLY.bin';path.write_bytes(target)
 obs=read('E:/Rota Nova translations/Generated/work/emulation_v193/square_context_live_v2122_V2097/common_observer/requests.json');seed=obs['rows'][0];raw=Path(seed['snapshots']['WRAM']['path']).read_bytes();assert sha(raw)==seed['snapshots']['WRAM']['sha256'];object_address=seed['registers'][9];assert struct.unpack_from('<2I',raw,object_address-BASE+0x28)==(228,48)
 cases=[]
 for height in(48,64):
  cpu,get=get_machine(arm,raw);cpu.reg_write(UC_ARM_REG_CPSR,0x1F)
  for label,addresses in [('DTCM',[seed['DTCM_base']]),('ITCM',[0,0x01FF8000])]:
   blob=Path(seed['snapshots'][label]['path']).read_bytes();assert sha(blob)==seed['snapshots'][label]['sha256']
   for address in addresses:
    try:cpu.mem_write(address,blob)
    except Exception:cpu.mem_map(address,len(blob));cpu.mem_write(address,blob)
  cpu.mem_map(0x06000000,0x100000);cpu.mem_write(0x06000000,b'\xA5'*0x100000);faults=[]
  def fault(u,access,address,size,value,data):faults.append(dict(access=access,address=address,size=size,value=value,PC=u.reg_read(UC_ARM_REG_PC)));return False
  cpu.hook_add(UC_HOOK_MEM_INVALID,fault);cpu.mem_write(BASE+0x118ACC,struct.pack('<I',height));before=bytes(cpu.mem_read(BASE,len(raw)))
  try:call(cpu,0x54C28,(object_address,),instruction_limit=2000000)
  except Exception as exc:
   save(ROOT/f'constructor_fault_{height}.json',dict(height=height,error=repr(exc),faults=faults,not_a_geometry_validation=True));print(dict(height=height,error=repr(exc),faults=faults));continue
  result=cpu.reg_read(UC_ARM_REG_R0);after=bytes(cpu.mem_read(BASE,len(raw)))
  vram=bytes(cpu.mem_read(0x06000000,0x100000));vram_changed=[i for i,v in enumerate(vram)if v!=0xA5];assert vram_changed and min(vram_changed)>=0x1A000 and max(vram_changed)<0x1D000
  bounds=struct.unpack('<2I',cpu.mem_read(object_address+0x28,8));clip=struct.unpack('<4I',cpu.mem_read(object_address+0x30,16));assert result==1 and bounds==(228,height)and clip==(0,0,228,height)
  changed=[i for i,(a,b)in enumerate(zip(before,after,strict=True))if a!=b];runs=[]
  for i in changed:
   if runs and i==runs[-1][1]:runs[-1][1]+=1
   else:runs.append([i,i+1])
  cases.append(dict(height=height,native_constructor_return=result,object_bounds=list(bounds),object_clip=list(clip),changed_byte_count=len(changed),VRAM_changed_bytes=len(vram_changed),VRAM_write_extent=[0x06000000+min(vram_changed),0x06000000+max(vram_changed)+1],VRAM_writes_stay_within_the_source256x96_panel_slot=True,VRAM_mapping_is_an_explicit_sentinel_input_not_live_GPU_contents=True,changed_runs=[[BASE+a,BASE+b]for a,b in runs],native_constructor_54C28_and_D3F80_D3A1C_D393C_execute_unstubbed=True,explicit_reused_captured_image_object_input=True,not_actual_gameplay_or_allocator_owner_proof=True))
 units=[('section'+str(i),s.ramAddress,bytes(s.data))for i,s in enumerate(MainCodeFile(arm,BASE).sections)];refs=[]
 for label,base,data in units:
  for i in range(len(data)-3):
   v=struct.unpack_from('<I',data,i)[0]
   if 0x02118AC8<=v<0x02118AD0:refs.append(dict(unit=label,address=base+i,target=v,aligned=i%4==0))
 save(ROOT/'source_and_native_constructor_research.json',dict(source_ARM9_sha256=sha(arm),target_ARM9_sha256=sha(target),research_ARM9=str(path),source_geometry_pair=[228,48],target_geometry_pair=[228,64],unchanged_panel_pair=[256,96],unchanged_source_margins=[8,16,0,0],height64_plus_top8_is72_less_than96=True,original_view_constructor_span=[0x02054C28,0x02054CF8],span_sha256=sha(arm[0x54C28:0x54CF8]),references=refs,cases=cases,sole_geometry_patch=dict(address=0x02118ACC,source_hex='30000000',target_hex='40000000'),source_snapshot=seed['snapshots']['WRAM'],GPU_upload_frame_paper_button_and_actual_fourth_row_regression_still_required=True,not_a_playable_ROM_or_release_approval=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(native_cases=[(r['height'],r['object_bounds'],r['changed_byte_count'])for r in cases],references=refs,actual_GPU_validation_pending=True))
