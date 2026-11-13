"""Exact original/new numeric predicates and monthly table membership/ABI."""
from pathlib import Path
import struct,hashlib
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_R3,UC_ARM_REG_R12
from scripts.research_scheme_selector_v775 import REGS
from scripts.verify_arrival_native_v792 import prepared
from scripts.probe_button_prompt_native import STACK,STOP
from scripts.primary_town_runtime_v2070 import SOURCE,DIRECT,TAIL,YESNO,ROOT as PAYLOAD
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/town_services_runtime_predicates_v2071')
NUMBERS=(*range(65536),0x10000,0x10001,0x7FFFFFFF,0x80000000,0xFFFFFF00,0xFFFFFFFE,0xFFFFFFFF)
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 plan=read(PAYLOAD/'runtime_plan.json');old=NdsImage.open('out/all_routes_combined_v2047_candidate.nds').read_file('/__arm9__.bin');new=Path(plan['research_ARM9']).read_bytes()
 assert sha(old)==SOURCE and sha(new)==plan['target_ARM9_sha256']
 receipts=[]
 for name,arm in(('current',old),('research',new)):
  for kind in('direct','yes-no'):
   cpu=prepared(arm);targets=(0x01FFCF78,0x01FFCBD8 if kind=='direct'else 0x01FFCD98)
   for t in targets:cpu.hook_add(UC_HOOK_CODE,lambda u,p,s,d:u.emu_stop(),begin=t,end=t)
   control={r:0xA5A50000+i for i,r in enumerate(REGS)if r!=UC_ARM_REG_R3};cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,STOP)
   for r,v in control.items():cpu.reg_write(r,v)
   digest=hashlib.sha256();active=0
   for n in NUMBERS:
    cpu.reg_write(UC_ARM_REG_R3,n if kind=='direct'else 0x02053FCC);cpu.reg_write(UC_ARM_REG_R12,n)
    pc=DIRECT if kind=='direct'else YESNO
    cpu.emu_start(pc,STOP,count=1000);actual=cpu.reg_read(UC_ARM_REG_PC)
    selected=(675<=n<=681 or 688<=n<=741 or n==761)if kind=='direct'else n==742
    selected|=name=='research'and n<=63
    assert actual==targets[0 if selected else 1],(name,kind,n,hex(actual))
    assert cpu.reg_read(UC_ARM_REG_SP)==STACK and cpu.reg_read(UC_ARM_REG_LR)==STOP
    assert cpu.reg_read(UC_ARM_REG_R3)==(n if kind=='direct'else 0x02053FCC)
    assert all(cpu.reg_read(r)==v for r,v in control.items())
    digest.update(struct.pack('<2I',n,actual));active+=selected
   receipts.append(dict(version=name,kind=kind,cases=len(NUMBERS),selected=active,trace_sha256=digest.hexdigest(),all_exact_routes_preserved_registers_SP_LR=True))
   print(receipts[-1],flush=True)
 monthly=[]
 for name,arm in(('current',old),('research',new)):
  cpu=prepared(arm);targets=(0x01FFCF40,0x02147B98)
  for t in targets:cpu.hook_add(UC_HOOK_CODE,lambda u,p,s,d:u.emu_stop(),begin=t,end=t)
  old_members=next(r[3]for r in read(PAYLOAD/'runtime_plan.json')['contract_rows']if r[0]==0x02053F40)
  expected=set(old_members)-({0x89C0}if name=='current'else set())
  numbers=(*range(0x7000,0x9000),0,0xFFFF,0x10000)
  digest=hashlib.sha256();selected=[]
  for low in numbers:
   controls={r:0xA5A50000+i for i,r in enumerate(REGS)}
   for r,v in controls.items():cpu.reg_write(r,v)
   cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,STOP)
   for off,v in((0x264,0x02053F40),(0x274,0x02110000|low),(0x27C,0),(0x270,0)):cpu.mem_write(STACK+off,struct.pack('<I',v))
   cpu.emu_start(0x02132020,STOP,count=10000);actual=cpu.reg_read(UC_ARM_REG_PC)
   hit=low in expected;assert actual==targets[int(hit)],(name,low,hex(actual))
   assert cpu.reg_read(UC_ARM_REG_SP)==STACK and cpu.reg_read(UC_ARM_REG_LR)==STOP
   for r,v in controls.items():assert cpu.reg_read(r)==(0x02053F40 if r==UC_ARM_REG_R3 and not hit else v)
   digest.update(struct.pack('<2I',low,actual))
   if hit:selected.append(low)
  assert set(selected)==expected
  monthly.append(dict(version=name,cases=len(numbers),selected_low_table_words=selected,trace_sha256=digest.hexdigest(),strict_alignment_high_word_and_ABI_pass=True))
  print(dict(version=name,monthly_cases=len(numbers),selected=len(selected)),flush=True)
 assert set(monthly[1]['selected_low_table_words'])-set(monthly[0]['selected_low_table_words'])=={0x89C0}
 save(ROOT/'exact_numeric_and_monthly_predicate_preservation.json',dict(source_ARM9_sha256=sha(old),target_ARM9_sha256=sha(new),runtime_plan=str(PAYLOAD/'runtime_plan.json'),runtime_plan_sha256=sha((PAYLOAD/'runtime_plan.json').read_bytes()),
  numeric_cases=receipts,monthly_cases=monthly,total_numeric_cases=sum(r['cases']for r in receipts),total_monthly_cases=sum(r['cases']for r in monthly),
  only_new_numeric_IDs0_to63_under_two_exact_original_parents=True,ritual64_and_all64_to65535_and_fullword_edges_unchanged=True,
  all_old_direct_ranges_and_yes_no742_exact=True,only_monthly_table189C0_added=True,
  glyphs_current_ROM_repacking_gameplay_and_registration_not_proven_here=True,no_ROM_registry_mutation=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
