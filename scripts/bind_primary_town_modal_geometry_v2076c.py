"""Bind83/84 mode-zero caller and native228x48 bitmap-constructor arguments."""
from pathlib import Path
import struct
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from capstone.arm import ARM_OP_IMM,ARM_REG_R0
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.common_single_cache_v861 import entries
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import BASE,STACK,STOP
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/town_services_modal_geometry_v2076c')
OBS=Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_services_actual_v2053_V2047/common_observer/requests.json')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 image=NdsImage.open('out/all_routes_combined_v2047_candidate.nds');arm=image.read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
 observer=read(OBS);seed=next(r for r in observer['rows']if r['message_ID']==55)['complete_readonly_snapshots']['WRAM'];raw=Path(seed['path']).read_bytes();assert sha(raw)==seed['sha256']
 directory=read('translations/reinforcement_faction_prose_release_v1.json')['directory_sha256'];messages=entries(image.read_file('/COMMON/MESFILE.DK4'),arm,directory)
 api=[]
 for n in(83,84):
  cpu,get=get_machine(arm,raw);cpu.mem_write(0x02660000,b'Li Clan\0');cpu.mem_write(0x02660200,'１'.encode('cp932')+b'\0')
  cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,STOP)
  for reg,value in((UC_ARM_REG_R0,n),(UC_ARM_REG_R1,0x02660000),(UC_ARM_REG_R2,0x02660200),(UC_ARM_REG_R3,0)):cpu.reg_write(reg,value)
  cpu.emu_start(BASE+0x546B8,BASE+0x54774,count=1000000)
  assert cpu.reg_read(UC_ARM_REG_PC)==BASE+0x54774
  assert cpu.reg_read(UC_ARM_REG_R0)==0 and cpu.reg_read(UC_ARM_REG_R3)==0 and cpu.reg_read(UC_ARM_REG_LR)==BASE+0x546E8
  at=cpu.reg_read(UC_ARM_REG_R1);template=bytes(cpu.mem_read(at,512)).split(b'\0')[0];assert template==messages[n].text
  vector=cpu.reg_read(UC_ARM_REG_R2);args=list(struct.unpack('<3I',cpu.mem_read(vector,12)));assert args[:2]==[0x02660000,0x02660200]
  api.append(dict(message_ID=n,original_entry=BASE+0x546B8,terminal_PC=BASE+0x54774,mode_R3=0,parent=BASE+0x546E8,loaded_current_template_hex=template.hex(),native_vararg_vector=vector,arguments=args,real_common_lookup_no_loader_or_formatter_stubs=True,offline_API_call_not_income_event_activation=True))
 cpu,get=get_machine(arm,raw);obj=0x02670000;cpu.mem_write(obj-16,b'\xa5'*512);call(cpu,0x54DB0,(obj,),instruction_limit=300000)
 fields=list(struct.unpack('<4I',cpu.mem_read(obj+0x40,16)));assert fields==[8,16,0,0]
 cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,STOP);cpu.reg_write(UC_ARM_REG_R0,obj)
 error=None
 try:cpu.emu_start(BASE+0x54C28,BASE+0xD3A1C,count=300000)
 except Exception as exc:error=str(exc)
 reached=cpu.reg_read(UC_ARM_REG_PC)==BASE+0xD3A1C
 if reached:
  pointer=cpu.reg_read(UC_ARM_REG_R1);size=list(struct.unpack('<2I',cpu.mem_read(pointer,8)));assert pointer==BASE+0x118AC8 and size==[228,48]and cpu.reg_read(UC_ARM_REG_R0)==obj
 else:size=None;pointer=None
 cs=Cs(CS_ARCH_ARM,CS_MODE_ARM);cs.detail=True;source_calls=[]
 for n in(83,84):
  needle=struct.pack('<I',0xE3A00000|n);start=0;found=[]
  while True:
   at=clean.find(needle,start)
   if at<0:break
   start=at+4
   if at&3:continue
   sequence=list(cs.disasm(clean[at:at+32],BASE+at))
   for i in sequence[1:]:
    if i.mnemonic=='bl'and i.operands[0].type==ARM_OP_IMM:
     if i.operands[0].imm==BASE+0x546B8:
      end=i.address-BASE+4;assert arm[at:end]==clean[at:end];found.append(dict(call_PC=i.address,start=BASE+at,hex=arm[at:end].hex()))
     break
    if ARM_REG_R0 in i.regs_access()[1]:break
  if n==83 and not found:
   # The source keeps83 in sb across the beneficiary loop,then moves sb to r0.
   assert struct.unpack_from('<I',clean,0xB253C)[0]==0xE3A09053
   assert struct.unpack_from('<I',clean,0xB25A4)[0]==0xE1A00009
   assert next(cs.disasm(clean[0xB25A8:0xB25AC],BASE+0xB25A8)).op_str=='#0x20546b8'
   assert arm[0xB2534:0xB2590]==clean[0xB2534:0xB2590]and arm[0xB2594:0xB25CC]==clean[0xB2594:0xB25CC]
   assert next(cs.disasm(arm[0xB2590:0xB2594],BASE+0xB2590)).op_str=='#0x1ff9ba0'  # Registered display-only F/I escape,not an unexplained difference.
   from unicorn.arm_const import UC_ARM_REG_R5,UC_ARM_REG_R9,UC_ARM_REG_R10
   native,get=get_machine(arm,raw);native.mem_write(0x02660000,b'Li Clan\0')
   for reg,value in((UC_ARM_REG_SP,STACK),(UC_ARM_REG_LR,STOP),(UC_ARM_REG_R5,600),(UC_ARM_REG_R9,83),(UC_ARM_REG_R10,0x02660000)):native.reg_write(reg,value)
   native.emu_start(BASE+0xB2594,BASE+0x546B8,count=300000)
   assert native.reg_read(UC_ARM_REG_PC)==BASE+0x546B8 and native.reg_read(UC_ARM_REG_R0)==83 and native.reg_read(UC_ARM_REG_R1)==0x02660000
   argument=bytes(native.mem_read(native.reg_read(UC_ARM_REG_R2),64)).split(b'\0')[0];assert argument=='６００'.encode('cp932')
   found.append(dict(call_PC=BASE+0xB25A8,start=BASE+0xB2534,end=BASE+0xB25CC,hex=arm[0xB2534:0xB25CC].hex(),
    native_original_sb83_and_amount_name_register_propagation_executed=True,native_amount_argument_hex=argument.hex(),eligibility_and_income_event_not_activated=True,registered_display_name_hook_at_B2590=dict(clean_hex=clean[0xB2590:0xB2594].hex(),current_hex=arm[0xB2590:0xB2594].hex(),meaning="Display-only F/I escape before printf;all other caller bytes clean-exact.")))
  assert found;source_calls.append(dict(message_ID=n,source_income_callers=found))
 spans=[]
 for lo,hi in((0x546B8,0x546F8),(0x54774,0x54798),(0x5479C,0x54830),(0x54C28,0x54CF8),(0x54DB0,0x54E44),(0x118AC8,0x118AF8)):
  assert arm[lo:hi]==clean[lo:hi]
  spans.append(dict(start=BASE+lo,end=BASE+hi,hex=arm[lo:hi].hex(),sha256=sha(arm[lo:hi])))
 save(ROOT/'83_84_mode_zero_and_shared_native_bitmap_geometry.json',dict(ARM9_sha256=sha(arm),source_snapshot=seed,original_API_cases=api,source_income_callers=source_calls,clean_exact_shared_constructor_spans=spans,
  native_54DB0_fields=fields,native_54C28_reached_bitmap_factory=reached,native_bitmap_size_argument=size,native_bitmap_size_pointer=pointer,constructor_probe_error=error,
  mode_zero_outer_size=[256,96],shared_text_client_size=[228,48],client_size_from_original_factory_arguments_not_outer_window_size=True,
  source_bound_same_text_client_constructor_for_actor_and_mode_zero=True,prior_eight_actual_actor_font_contexts='work/analysis/town_services_consumer_audit_v2064b/actual_eight_consumers_four12pixel_rows_and_numeric_scope.json',
  offline_mode_zero_geometry_binding_not_actual83_84_income_visits=True,no_ROM_registry_or_save_mutation=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(original_modal_API_cases=2,source_income_callers=sum(len(r['source_income_callers'])for r in source_calls),native_constructor_to_factory=reached,size=size,error=error))
 assert reached
