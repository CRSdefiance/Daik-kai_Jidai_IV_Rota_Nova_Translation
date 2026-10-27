"""All numeric modal IDs through the original physical BL and caller frame."""
from pathlib import Path
import struct
from unicorn.arm_const import UC_ARM_REG_R0
from scripts.probe_primary_town_research_routes_v2083 import callsite
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.probe_button_prompt_native import BASE,STACK
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/town_services_modal_scope_v2086')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 plan=read('work/analysis/town_services_runtime_v2080/runtime_plan.json');prior=read('work/analysis/town_services_literals_v2055/all84_original_printf_shared_expander_and_literal_guards.json');raw=Path(prior['source_snapshot']['path']).read_bytes()
 old=NdsImage.open('out/all_routes_combined_v2047_candidate.nds').read_file('/__arm9__.bin');new=Path(plan['research_ARM9']).read_bytes();cpus=[]
 for arm in(old,new):
  cpu,get=get_machine(arm,raw);expected=bytearray(raw)
  if arm==new:
   for p in plan['patches']:
    value=bytes.fromhex(p['target_hex']);cpu.mem_write(p['address'],value);off=p['address']-BASE
    if 0<=off<len(raw):expected[off:off+len(value)]=value
  cpus.append((cpu,bytes(expected)))
 text=b' Complete words and every original leading and trailing letter remain intact throughout this notice.'
 def run(cpu,parent,n):
  cpu.mem_write(STACK+0xC4,struct.pack('<I',parent));cpu.mem_write(STACK+0xD0,struct.pack('<I',n));cpu.mem_write(0x02660000,text+b'\0');cpu.mem_write(0x02662000-16,b'\xa5'*1056)
  callsite(cpu,BASE+0x54798,(0x02662000,0x02660000,0));value=bytes(cpu.mem_read(0x02662000,1024)).split(b'\0')[0]
  assert cpu.reg_read(UC_ARM_REG_R0)==0
  assert bytes(cpu.mem_read(0x02660000,len(text)+1))==text+b'\0'
  assert bytes(cpu.mem_read(0x02662000-16,16))==b'\xa5'*16 and bytes(cpu.mem_read(0x02662000+len(value)+1,1023-len(value)))==b'\xa5'*(1023-len(value))
  return value
 receipts=[]
 for n in range(3668):
  before,after=[run(c,0x020546E8,n)for c,e in cpus]
  if n not in(83,84):assert before==after,n
  else:assert b' '.join(after.split())==text.strip()
  receipts.append(dict(message_ID=n,before_sha256=sha(before),after_sha256=sha(after),unchanged=before==after,intended_literal_selection=n in(83,84)))
 controls=[]
 for parent in(0,0xFFFFFFFF,0x120546E8,0x0205469C,0x02054720,0x02054764,0x02054014):
  for n in(0,1,82,83,84,85,127,269,321,327,346,347,348,3667,65535,65536,0x7FFFFFFF,0x80000000,0xFFFFFFFF):
   assert run(cpus[0][0],parent,n)==run(cpus[1][0],parent,n);controls.append([parent,n])
 for n in(65535,65536,0x7FFFFFFF,0x80000000,0xFFFFFFFF):assert run(cpus[0][0],0x020546E8,n)==run(cpus[1][0],0x020546E8,n)
 for cpu,expected in cpus:assert bytes(cpu.mem_read(BASE,len(raw)))==expected
 save(ROOT/'all3668_original_BL_modal_scope_and_ABI.json',dict(source_ARM9_sha256=sha(old),target_ARM9_sha256=sha(new),cases=receipts,wrong_parent_controls=controls,fullword_edges=5,all3666_unselected_outputs_exact=True,all_native_input_output_whole4MiB_register_SP_LR_and_R0zero_guards_pass=True,physical_BL=BASE+0x54798,no_live_conditional_event_or_gameplay_claim=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(modal_IDs=3668,unselected_exact=3666,wrong_parent_controls=len(controls),edges=5))
