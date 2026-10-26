"""Clean/current complete gift and drink branches plus original role3 price wrapper."""
from pathlib import Path
import struct
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import *
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.rom.nds import NdsImage
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.probe_button_prompt_native import BASE,STACK,STOP
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/tavern_exchange_graphs_v2185');ROM=Path('out/all_routes_combined_v2171_candidate.nds');PARENT=Path('work/analysis/tavern_context_v2184b/fresh_current_native_context.json')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);prior=read(PARENT);rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');cleanrom=NdsImage.open('work/clean.nds');clean=cleanrom.read_file('/__arm9__.bin');jp=common_message_entries(cleanrom.read_file('/COMMON/MESFILE.DK4'),clean);entries=current_entries(common,arm);raw=Path(prior['source_snapshot']['path']).read_bytes();assert sha(raw)==prior['source_snapshot']['sha256']
 for a,b in((0x5923C,0x59624),(0x59EDC,0x59F40),(0x58350,0x5839C),(0x53CB0,0x53D24)):assert arm[a:b]==clean[a:b]
 gift=[];drinks=[];extra=set()
 for version,a in(('clean',clean),('current',arm)):
  u,get=get_machine(a,raw);town=get(0xB6618);npc=get(0xB2CD8,town,13);officers=get(0xCB184);actor=officers+0x19E4;item=get(0xCB190)+4+60*20;route=struct.unpack_from('<I',a,0x5B0A0)[0]+0x48;events=[];choice=[0];rt=[0];transfers=[]
  def callback(cpu,pc,size,unused):
   if pc==BASE+0x53BD8:
    table=cpu.reg_read(UC_ARM_REG_R0);n=struct.unpack('<I',cpu.mem_read(table+4*rt[0],4))[0];events.append(dict(ID=n,kind='original-four-captain-queue-boundary',table=table));cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR))
   elif pc in(BASE+0x53FE4,BASE+0x53F9C):
    n=cpu.reg_read(UC_ARM_REG_R1);events.append(dict(ID=n,kind='original-YesNo-boundary'if pc==BASE+0x53F9C else'original-direct-speech-boundary'));cpu.reg_write(UC_ARM_REG_R0,choice[0]if pc==BASE+0x53F9C else 0);cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR))
   elif pc==BASE+0x595FC:transfers.append(dict(original_item_assignment_body_reached=True,after_reply=True));cpu.emu_stop()
   elif pc==BASE+0x3CC80:events.append(dict(native_payment_delta=cpu.reg_read(UC_ARM_REG_R1)));cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR))
  hooks=[u.hook_add(UC_HOOK_CODE,callback,begin=pc,end=pc)for pc in(BASE+0x53BD8,BASE+0x53FE4,BASE+0x53F9C,BASE+0x595FC,BASE+0x3CC80)]
  try:
   for r in range(4):
    rt[0]=r;u.mem_write(route,struct.pack('<I',r))
    for barmaid in range(66):
     for yes in(0,1):
      choice[0]=yes;events.clear();transfers.clear();u.reg_write(UC_ARM_REG_SP,STACK);u.mem_write(STACK+4,struct.pack('<5I',0,0,0,0,STOP))
      for reg,val in((UC_ARM_REG_R4,npc),(UC_ARM_REG_R5,barmaid),(UC_ARM_REG_R6,0x02471000),(UC_ARM_REG_R7,item)):u.reg_write(reg,val)
      u.emu_start(BASE+0x59288,STOP,count=30000);ids=[e['ID']for e in events];assert ids[:5]==[829,830+r,834,835+r,839]and len(ids)==6
      if yes:assert transfers and u.reg_read(UC_ARM_REG_PC)==BASE+0x595FC and ids[-1]!=841
      else:assert not transfers and ids[-1]==841 and u.reg_read(UC_ARM_REG_PC)==STOP
      extra.add(ids[-1]);gift.append(dict(version=version,route=r,supplied_barmaid_index=barmaid,Yes=bool(yes),events=list(events),transfer_body_reached=bool(transfers),item_assignment_not_executed=True))
   for kind in(0,1):
    for yes in(0,1):
     events.clear();choice[0]=yes;u.mem_write(0x02471000,struct.pack('<3I',0,0,kind));u.reg_write(UC_ARM_REG_SP,STACK)
     for reg,val in((UC_ARM_REG_R4,actor),(UC_ARM_REG_R5,npc),(UC_ARM_REG_R6,npc),(UC_ARM_REG_R7,0x02471000)):u.reg_write(reg,val)
     u.emu_start(BASE+0x59EDC,BASE+0x59F38,count=10000);assert events[0]['ID']==59
     if yes:assert events[1]['ID']==(60 if kind else 61)and events[2]['native_payment_delta']==((-20 if kind else -10)&0xffffffff)
     else:assert events==[dict(ID=59,kind='original-YesNo-boundary'),dict(ID=826,kind='original-direct-speech-boundary')]
     drinks.append(dict(version=version,formal=kind,Yes=bool(yes),events=list(events),payment_boundary_unexecuted=True))
  finally:
   for h in hooks:u.hook_del(h)
 assert[{k:v for k,v in r.items()if k!='version'}for r in gift[:528]]==[{k:v for k,v in r.items()if k!='version'}for r in gift[528:]]
 assert[{k:v for k,v in r.items()if k!='version'}for r in drinks[:4]]==[{k:v for k,v in r.items()if k!='version'}for r in drinks[4:]]
 u,get=get_machine(arm,raw);text=lambda p:bytes(u.mem_read(p,256)).split(b'\0')[0];prices=[];core=[];selected=[]
 def price_stop(cpu,pc,size,data):
  prices.append(dict(role=cpu.reg_read(UC_ARM_REG_R0),table=cpu.reg_read(UC_ARM_REG_R1),price_hex=text(cpu.reg_read(UC_ARM_REG_R2)).hex(),value=cpu.reg_read(UC_ARM_REG_R8),SP=cpu.reg_read(UC_ARM_REG_SP)));cpu.emu_stop()
 h=u.hook_add(UC_HOOK_CODE,price_stop,begin=BASE+0x53CB0,end=BASE+0x53CB0);u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_R0,0x02471000);u.emu_start(BASE+0x58350,BASE+0x5839C,count=10000);u.hook_del(h);assert len(prices)==1;price=prices[0];assert price['role']==3 and price['table']==0x02118400 and bytes.fromhex(price['price_hex']).decode('cp932')==str(price['value']).translate(str.maketrans('0123456789','０１２３４５６７８９'))
 def loader(cpu,pc,size,data):
  n=cpu.reg_read(UC_ARM_REG_R0);assert 852<=n<=858;selected.append(n);cpu.mem_write(0x02472000,entries[n].text+b'\0');cpu.reg_write(UC_ARM_REG_R0,0x02472000);cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR))
 def stop_core(cpu,pc,size,data):
  sp=cpu.reg_read(UC_ARM_REG_SP);va=cpu.reg_read(UC_ARM_REG_R3);core.append(dict(mode=cpu.reg_read(UC_ARM_REG_R0),actor=cpu.reg_read(UC_ARM_REG_R1),template_hex=text(cpu.reg_read(UC_ARM_REG_R2)).hex(),SP=sp,va_list=va,LR=cpu.reg_read(UC_ARM_REG_LR),saved_table=struct.unpack('<I',cpu.mem_read(sp+20,4))[0],argument_hex=text(struct.unpack('<I',cpu.mem_read(va,4))[0]).hex()));cpu.emu_stop()
 hs=[u.hook_add(UC_HOOK_CODE,loader,begin=BASE+0x5528C,end=BASE+0x5528C),u.hook_add(UC_HOOK_CODE,stop_core,begin=BASE+0x54058,end=BASE+0x54058)]
 try:u.emu_start(BASE+0x53CB0,BASE+0x53D24,count=30000)
 finally:
  for h in hs:u.hook_del(h)
 assert len(core)==len(selected)==1;c=core[0];assert c['mode']==1 and c['LR']==BASE+0x53D24 and c['SP']==price['SP']-32 and c['va_list']==price['SP']-8 and c['saved_table']==0x02118400 and c['argument_hex']==price['price_hex']and c['template_hex']==entries[selected[0]].text.hex()
 dependencies=[]
 for n in sorted(extra|{58,59,60,61}):dependencies.append(dict(ID=n,Japanese=jp[n].text.decode('cp932'),source_hex=jp[n].text.hex(),source_reference=dict(block=jp[n].block,offset=jp[n].block_offset,copy_end=jp[n].copy_end),current_hex=entries[n].text.hex(),current_reference=dict(block=entries[n].block,offset=entries[n].block_offset,copy_end=entries[n].copy_end),context_only_no_new_review_credit=True))
 save(ROOT/'clean_current_whole_gift_drink_and_price_graphs.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),prior_provider_proof=str(PARENT),prior_provider_sha256=sha(PARENT.read_bytes()),gift_cases=gift,drink_cases=drinks,price_provider=price,original_price_core=c,selected_price_ID=selected[0],source_context_dependencies=dependencies,all_clean_current_control_and_speech_sequences_exact=True,source_generic840_only_default_other_character_specific_responses_preserved=True,all_UI_loader_payment_and_transfer_boundaries_explicit=True,no_earned_gift_drink_or_payment_scene_claim=True,no_ROM_registry_save_changes=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(gift_cases=len(gift),drink_cases=len(drinks),price_role3_bound=True,context_dependency_IDs=[r['ID']for r in dependencies]),flush=True)
