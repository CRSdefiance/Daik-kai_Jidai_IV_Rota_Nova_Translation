"""Original receipt caller, native printf and modal literal name preservation."""
from pathlib import Path
import struct
from unicorn.arm_const import UC_ARM_REG_CPSR,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R5,UC_ARM_REG_R9
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.native_call_abi_v764 import call
from scripts.probe_primary_town_research_routes_v2083 import callsite
from scripts.probe_button_prompt_native import BASE,STACK,STOP
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/town_services_receipt_names_v2085')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 plan=read('work/analysis/town_services_runtime_v2080/runtime_plan.json');arm=Path(plan['research_ARM9']).read_bytes();prior=read('work/analysis/town_services_literals_v2055/all84_original_printf_shared_expander_and_literal_guards.json');raw=Path(prior['source_snapshot']['path']).read_bytes()
 clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');assert arm[0xB2534:0xB25CC]==clean[0xB2534:0xB25CC]
 row=next(r for r in read('translations/primary_town_services_contextual_editorial_manuscript_v3.json')['records']if r['message_id']==83);template=row['english'].encode('cp932')
 names=[b'FI',b'FA',b'FO',b'IC',b'F'*18,b'I'*18,b'FA'*9,b'IC'*9,b'Bergstrom Fleet',b'Li Clan','李一族李一族李一族'.encode('cp932'),b'\x87\x90'*9]
 receipts=[]
 for name in names:
  assert 0<len(name)<=18;name.decode('cp932')
  for amount in(0,600,999999999):
   cpu,get=get_machine(arm,raw)
   for p in plan['patches']:cpu.mem_write(p['address'],bytes.fromhex(p['target_hex']))
   cpu.mem_write(0x02660000,name+b'\0');cpu.reg_write(UC_ARM_REG_CPSR,0x1F)
   for reg,value in((UC_ARM_REG_SP,STACK),(UC_ARM_REG_LR,STOP),(UC_ARM_REG_R0,0x02660000),(UC_ARM_REG_R5,amount),(UC_ARM_REG_R9,83)):cpu.reg_write(reg,value)
   cpu.emu_start(BASE+0xB2590,BASE+0x546B8,count=500000)
   assert cpu.reg_read(UC_ARM_REG_PC)==BASE+0x546B8 and cpu.reg_read(UC_ARM_REG_R0)==83 and cpu.reg_read(UC_ARM_REG_R1)==0x02660000
   numeric=bytes(cpu.mem_read(cpu.reg_read(UC_ARM_REG_R2),64)).split(b'\0')[0];expected_digits=str(amount).translate(str.maketrans('0123456789','０１２３４５６７８９')).encode('cp932');assert numeric==expected_digits
   cpu.mem_write(0x02660800,numeric+b'\0');cpu.mem_write(0x02664000,template+b'\0');cpu.mem_write(0x02665000-16,b'\xa5'*1056)
   call(cpu,0xD7720,(0x02665000,0x02664000,0x02660000,0x02660800),instruction_limit=1000000)
   expanded=template.replace(b'%s',name,1).replace(b'%s',numeric,1);assert bytes(cpu.mem_read(0x02665000,len(expanded)+1))==expanded+b'\0'
   cpu.mem_write(STACK+0xC4,struct.pack('<I',0x020546E8));cpu.mem_write(STACK+0xD0,struct.pack('<I',83));cpu.mem_write(0x02666000-16,b'\xa5'*1056)
   callsite(cpu,BASE+0x54798,(0x02666000,0x02665000,0));output=bytes(cpu.mem_read(0x02666000,1024)).split(b'\0')[0]
   assert b' '.join(output.split())==expanded and bytes(cpu.mem_read(0x02660000,len(name)+1))==name+b'\0'
   assert bytes(cpu.mem_read(0x02666000-16,16))==b'\xa5'*16 and bytes(cpu.mem_read(0x02666000+len(output)+1,1023-len(output)))==b'\xa5'*(1023-len(output))
   lines=[line.strip().decode('cp932')for line in output.split(b'\n')];assert 1<=len(lines)<=4 and all(len(line.encode('cp932'))<=35 for line in lines)
   receipts.append(dict(name_hex=name.hex(),amount=amount,native_amount_hex=numeric.hex(),formatted_hex=output.hex(),lines=lines,source_caller_clean_exact=True,original_name_bytes_and_native_printf_and_original_modal_BL_pass=True))
 save(ROOT/'all36_original_caller_native_printf_and_modal_names.json',dict(ARM9_sha256=sha(arm),cases=receipts,count=len(receipts),caller_span=[BASE+0xB2534,BASE+0xB25CC],caller_sha256=sha(arm[0xB2534:0xB25CC]),source_snapshot=prior['source_snapshot'],no_income_eligibility_or_event_activation_claim=True,producer_sha256=sha(Path(__file__).read_bytes()),full_native_name_pixels_and_other_release_gates_pending=True,full_goal_complete=False))
 print(dict(native_caller_printf_and_modal_cases=len(receipts),max_name_bytes=18,aliases_preserved=True))
