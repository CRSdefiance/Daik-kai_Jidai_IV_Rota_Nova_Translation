"""Compare installed native wrap routes for trend and balanced literal paragraphs."""
from pathlib import Path
import inspect
from unicorn import UC_HOOK_BLOCK
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.probe_shipyard_runtime_v759 import layout as original
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
ROOT=Path('work/analysis/town_trend_balance_route_v2159')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);plan=read('work/analysis/town_trade_port_payload_v2153/native_payload_plan.json');arm=Path(plan['target_ARM9']).read_bytes();common=Path(plan['target_COMMON']).read_bytes();entries=owned_entries(common,arm,plan['directory_sha256']);report=read('E:/Rota Nova translations/Generated/work/emulation_v193/promoter_context_live_v2144_V2143/capture_report.json');raw=Path(next(r for r in report['read_only_pause_RAM_snapshots']if r['frame']==3200)['path']).read_bytes();cases=[];cs=Cs(CS_ARCH_ARM,CS_MODE_ARM)
 for n,values in[(653,(b'Olive Oil',)),(654,(b'Olive Oil',)),(655,(b'Olive Oil',)),(808,(b'Hodram',)),(767,(b'Wheat',b'Cloves'))]:
  cpu,_=get_machine(arm,raw);blocks=[];active=[False]
  def observe(u,pc,size,data):
   if pc==0x01FFCF3C:active[0]=True
   if active[0]and(0x01FF8000<=pc<0x01FFD000 or 0x02130000<=pc<0x02162000 or 0x02387A20<=pc<0x023A7200)and pc not in blocks:blocks.append(pc)
  h=cpu.hook_add(UC_HOOK_BLOCK,observe);result=original(cpu,entries[n].text,n,values);cpu.hook_del(h);disassembly=[]
  for pc in blocks:
   size=24;blob=bytes(cpu.mem_read(pc,size));disassembly.append(dict(address=pc,hex=blob.hex(),instructions=[dict(address=i.address,mnemonic=i.mnemonic,operands=i.op_str)for i in cs.disasm(blob,pc)]))
  cases.append(dict(message_ID=n,arguments_hex=[v.hex()for v in values],result=result,blocks=blocks,block_source=disassembly));print(n,result['lines'],[hex(pc)for pc in blocks])
 save(ROOT/'installed_trend_versus_balanced_literal_routes.json',dict(source_ARM9_sha256=plan['source_ARM9_sha256'],metadata_only_research_ARM9_sha256=sha(arm),cases=cases,scope='Read-only native route trace. No runtime ownership or routing change approved.',source_macro_and_parent_preservation_still_required_for_any_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
