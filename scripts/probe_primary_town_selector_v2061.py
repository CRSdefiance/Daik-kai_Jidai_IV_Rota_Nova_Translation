"""Current numeric-parent selector evidence only; no runtime modification."""
from pathlib import Path
import struct
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_SP,UC_ARM_REG_LR
from scripts import verify_palace_runtime_v796 as scope
from scripts import search_reports_runtime_v1659 as current
from scripts.verify_arrival_native_v792 import prepared
from scripts.research_scheme_selector_v775 import REGS,UC_ARM_REG_R3
from dk4tool.patch.shipyard_editorial import LITERAL
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_button_prompt_native import BASE,STACK,STOP
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/town_services_selector_v2061')
if __name__=='__main__':
 assert not ROOT.exists()
 arm=NdsImage.open('out/all_routes_combined_v2047_candidate.nds').read_file('/__arm9__.bin')
 assert arm[current.CONTRACTS-BASE:current.CONTRACTS-BASE+188]==current.table()
 assert arm[current.GATE-BASE:current.GATE-BASE+172]==current.gate()[0]
 cpu=prepared(arm);targets=(0x01FFCF40,LITERAL,scope.new.bank.COORD,scope.new.bank.STATUS)
 for target in targets:cpu.hook_add(UC_HOOK_CODE,lambda c,p,s,d:c.emu_stop(),begin=target,end=target)
 rows=[];contracts={p:(off,hi,set(keys))for p,off,hi,keys in current.contract_rows()}
 for parent in(0x02054014,0x02053FCC):
  off,high,keys=contracts[parent];assert(off,high)==(0x274,0)and not keys&set(range(85))
  for n in(*range(85),min(keys)):
   registers={reg:0xA5A50000+i for i,reg in enumerate(REGS)}
   for reg,v in registers.items():cpu.reg_write(reg,v)
   cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,STOP)
   for at,value in((0x264,parent),(0x274,n),(0x27C,0),(0x270,0)):cpu.mem_write(STACK+at,struct.pack('<I',value))
   cpu.emu_start(scope.new.bank.ENTRY,STOP,count=10000)
   expected=LITERAL if n in keys else 0x01FFCF40
   assert cpu.reg_read(UC_ARM_REG_PC)==expected
   assert cpu.reg_read(UC_ARM_REG_SP)==STACK and cpu.reg_read(UC_ARM_REG_LR)==STOP
   for reg,v in registers.items():assert cpu.reg_read(reg)==(parent if reg==UC_ARM_REG_R3 and expected==0x01FFCF40 else v)
   rows.append(dict(parent=parent,message_ID=n,route=expected,falls_back_from_numeric_formatter=n not in keys,ABI_SP_LR_exact=True))
 ROOT.mkdir(parents=True)
 save(ROOT/'early_numeric_parent_dispatch_contract.json',dict(ARM9_sha256=sha(arm),exact_current_contract_bank_sha256=sha(current.table()),exact_current_gate_sha256=sha(current.gate()[0]),cases=rows,
  all0_to84_excluded_from_two_numeric_parent_postmacro_contracts=True,ID64_negative_control_not_new_editorial_scope=True,
  monthly76_to82_uses_distinct_table_parent_and_is_not_classified_by_numeric_tests=True,
  existing_known_selected_numeric_controls_pass=True,no_glyph_geometry_or_production_runtime_approval=True,no_ROM_registry_profile_mutation=True,
  producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(native_gate_cases=len(rows),early_numeric_exclusions=170,known_selected_controls=2,no_runtime_mutation=True))
