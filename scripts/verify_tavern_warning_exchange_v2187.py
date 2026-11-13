"""Player825 is the interposed response to formal/casual Tavern fleet warnings."""
from pathlib import Path
import struct
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import *
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.probe_button_prompt_native import BASE,STACK
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/tavern_warning_exchange_v2187')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);a=NdsImage.open('out/all_routes_combined_v2171_candidate.nds').read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');p=read('work/analysis/tavern_context_v2184b/fresh_current_native_context.json');raw=Path(p['source_snapshot']['path']).read_bytes();assert sha(raw)==p['source_snapshot']['sha256'];cases=[]
 for version in('clean-provider-span','current-provider-span'):
  u,get=get_machine(a,raw);blob=(clean if version.startswith('clean')else a)[0x57FDC:0x58084];u.mem_write(BASE+0x57FDC,blob);assert bytes(u.mem_read(BASE+0x57FDC,len(blob)))==blob
  town=get(0xB6618);npc=get(0xB2CD8,town,13);company=get(0xCB160)+4;route=struct.unpack_from('<I',a,0x5B0A0)[0]+0x48;events=[]
  def text(ptr):return bytes(u.mem_read(ptr,100)).split(b'\0')[0]
  def observe(cpu,pc,size,data):
   if pc==BASE+0x53C24:events.append(dict(ID=cpu.reg_read(UC_ARM_REG_R0),speaker='player-admiral',arguments_hex=[]))
   else:
    n=cpu.reg_read(UC_ARM_REG_R1);count=2 if n==878 else 1;events.append(dict(ID=n,speaker='Tavern-NPC',arguments_hex=[text(cpu.reg_read(r)).hex()for r in(UC_ARM_REG_R2,UC_ARM_REG_R3)[:count]]))
   cpu.reg_write(UC_ARM_REG_R0,0);cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR))
  hooks=[u.hook_add(UC_HOOK_CODE,observe,begin=pc,end=pc)for pc in(BASE+0x53C24,BASE+0x53FE4)]
  try:
   for rt in range(4):
    u.mem_write(route,struct.pack('<I',rt))
    for formal in(0,1):
     events.clear();u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_R4,company);u.reg_write(UC_ARM_REG_R5,npc);lo,hi=(0x57FDC,0x58028)if formal else(0x5802C,0x58084);u.emu_start(BASE+lo,BASE+hi,count=20000);assert[e['ID']for e in events]==([875,825,876]if formal else[877,825,878]);cases.append(dict(version=version,route=rt,formal=formal,events=list(events)))
  finally:
   for h in hooks:u.hook_del(h)
 for before,after in zip(cases[:8],cases[8:],strict=True):
  assert before['route']==after['route']and before['formal']==after['formal']
  if before['formal']:assert before['events']==after['events']
  else:assert before['events'][:2]==after['events'][:2]and before['events'][2]['arguments_hex']==list(reversed(after['events'][2]['arguments_hex']))
 save(ROOT/'source_current_player825_and_pursuit_exchange.json',dict(cases=cases,player825_not_a_barmaid_or_keeper_line=True,formal_sequence=[875,825,876],casual_sequence=[877,825,878],source878_company_vocative_order_preserved_by_current_scoped_permutation=True,UI_boundaries_not_executed=True,source_span_reinstalled_explicitly_for_clean_provider_cases=True,ARM9_sha256=sha(a),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(exchanges=len(cases),player825='confirmed',source_current_permutation='exact'))
