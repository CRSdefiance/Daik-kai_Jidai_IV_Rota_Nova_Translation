"""Fresh current Tavern source graphs and typed native providers; no earned-scene claim."""
from pathlib import Path
import struct
from itertools import product
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import *
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
from dk4tool.patch.tavern_editorial_runtime import TYPE_HELPER
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.probe_button_prompt_native import BASE,STACK,STOP
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/tavern_context_v2184');ROM=Path('out/all_routes_combined_v2171_candidate.nds');REPORT=Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_trend_actual_v2178_50_V2171/capture_report.json')
COUNTS={820:3,821:3,843:5,844:3,845:3,846:1,847:1,848:1,849:2,850:2,851:2,863:2,868:0,869:1,870:3,871:2,872:2,873:1,874:0,875:1,876:1,877:1,878:2,879:2,880:2,881:2,882:2}
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');entries=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm);report=read(REPORT);snap=next(x for x in report['read_only_pause_RAM_snapshots']if x['frame']==3200);raw=Path(snap['path']).read_bytes();assert sha(raw)==snap['sha256']and report['ROM_sha256']==sha(ROM.read_bytes())
 spans=((0x57A5C,0x599DC),(0x59C9C,0x59F30),(0x53BD8,0x54058));owners={};plans=[]
 for name in('tavern_storage_v764/owned_storage_and_native_research.json','tavern_coordinates_v766/owned_runtime_plan.json','tavern_runtime_v769/owned_runtime_plan.json'):
  p=Path('work/analysis')/name;d=read(p);plans.append(dict(path=str(p),sha256=sha(p.read_bytes())))
  for row in d['patches']:
   at=row['address']-BASE;blob=bytes.fromhex(row['target_hex'])
   if any(at<b and at+len(blob)>a for a,b in spans):
    assert arm[at:at+len(blob)]==blob
    for j,value in enumerate(blob):owners[at+j]=dict(owner=str(p),value=value)
 diffs=[]
 for a,b in spans:
  for at in range(a,b):
   if arm[at]!=clean[at]:assert at in owners and arm[at]==owners[at]['value'];diffs.append(dict(address=BASE+at,source=clean[at],current=arm[at],owner=owners[at]['owner']))
 cs=Cs(CS_ARCH_ARM,CS_MODE_ARM);graphs=[]
 for a,b in((0x5923C,0x59340),(0x5950C,0x59624),(0x59EDC,0x59F30),(0x58350,0x58570)):
  graphs.append(dict(start=BASE+a,end=BASE+b,source_hex=clean[a:b].hex(),current_hex=arm[a:b].hex(),instructions=[dict(PC=i.address,hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str)for i in cs.disasm(clean[a:b],BASE+a)]))
 u,get=get_machine(arm,raw)
 def ptr(at):return struct.unpack('<I',u.mem_read(at,4))[0]
 def text(at):return bytes(u.mem_read(at,256)).split(b'\0')[0]
 def name(obj):return text(get(ptr(ptr(obj)+8)-BASE,obj))
 officers,town_root,goods_root,force_root,item_root,fleet_root=[get(at)for at in(0xCB184,0xCB178,0xCB124,0xCB160,0xCB190,0xCB1A8)]
 actor=officers+0x19E4;town=get(0xB6618);npc=get(0xB2CD8,town,13);route=struct.unpack_from('<I',arm,0x5B0A0)[0]+0x48
 towns=[dict(index=i,object=town_root+4+i*108,name_hex=name(town_root+4+i*108).hex())for i in range(90)]
 goods=[dict(index=i,object=goods_root+4+i*16,name_hex=name(goods_root+4+i*16).hex())for i in range(124)]
 companies=[dict(index=i,object=force_root+4+i*0x4C,name_hex=name(force_root+4+i*0x4C).hex())for i in range(20)]
 items=[dict(index=i,object=item_root+4+i*20,name_hex=name(item_root+4+i*20).hex(),region=get(0x4A3F0,item_root+4+i*20))for i in range(218)]
 surn=text(get(ptr(ptr(actor)+0x24)-BASE,actor));town_name=name(town);item=items[60]['object'];item_name=bytes.fromhex(items[60]['name_hex']);events=[];cases=[]
 def capture(cpu,pc,size,unused):
  n=cpu.reg_read(UC_ARM_REG_R1);assert n in COUNTS,n;pointers=[cpu.reg_read(UC_ARM_REG_R2),cpu.reg_read(UC_ARM_REG_R3),*struct.unpack('<3I',cpu.mem_read(cpu.reg_read(UC_ARM_REG_SP),12))];events.append(dict(id=n,arguments_hex=[text(p).hex()for p in pointers[:COUNTS[n]]],stopped_at_original_UI_boundary=True));cpu.emu_stop()
 hook=u.hook_add(UC_HOOK_CODE,capture,begin=BASE+0x53FE4,end=BASE+0x53FE4)
 def fragment(a,b,regs,stack=()):
  events.clear();u.reg_write(UC_ARM_REG_SP,STACK)
  for reg,val in regs:u.reg_write(reg,val)
  for off,val in stack:u.mem_write(STACK+off,struct.pack('<I',val))
  u.emu_start(BASE+a,BASE+b,count=30000);assert len(events)==1 and u.reg_read(UC_ARM_REG_PC)==BASE+0x53FE4;return dict(events[0])
 def add(event,n,values,**extra):
  assert event['id']==n and event['arguments_hex']==[v.hex()for v in values],(event,n,values);cases.append(dict(**event,**extra))

 try:
  for dx,dy,xd,yd in product((149,150,499,500,1999,2000,2001),(149,150,499,500,1999,2000,2001),range(2),range(2)):
   ev=fragment(0x58D4C,0x58EA4,((UC_ARM_REG_R4,item),(UC_ARM_REG_R9,xd)),((0x10,actor),(0x18,yd),(0x24,dx),(0x28,dy)));dist=lambda d:(b'a little',b'far',b'very far')[2 if d>=2000 else 1 if d>=500 else 0]
   if dx>=150 and dy>=150:n,values=843,[item_name,dist(dy),(b'north',b'south')[yd],dist(dx),(b'east',b'west')[xd]]
   elif dx>=150:n,values=844,[item_name,dist(dx),(b'east',b'west')[xd]]
   elif dy>=150:n,values=845,[item_name,dist(dy),(b'north',b'south')[yd]]
   else:n,values=846,[item_name]
   add(ev,n,values,supplied_axis_distances=[dx,dy],directions=[xd,yd])
  pairs=[(c,towns[0])for c in companies]+[(companies[0],t)for t in towns[1:]]
  for c,t in pairs:
   profession=text(get(TYPE_HELPER-BASE,c['object']));assert profession in(b'trader',b'pirate',b'soldier',b'conqueror')
   for n in(820,821):
    ev=fragment(0x59C9C,0x59CE4,((UC_ARM_REG_R7,actor),(UC_ARM_REG_R5,t['object']),(UC_ARM_REG_R6,c['object']),(UC_ARM_REG_R4,actor),(UC_ARM_REG_R8,n)));add(ev,n,[surn,bytes.fromhex(t['name_hex']),profession])
  for level,g in product((49,50),goods):
   ev=fragment(0x58A70,0x58A98,((UC_ARM_REG_R0,g['object']),(UC_ARM_REG_R4,actor),(UC_ARM_REG_R7,level)));add(ev,847 if level<50 else 848,[bytes.fromhex(g['name_hex'])],trend=level)
  trend_pairs=[(towns[0],g)for g in goods]+[(t,goods[0])for t in towns[1:]]
  for level,(t,g) in product((49,50),trend_pairs):
   ev=fragment(0x58990,0x589D4,((UC_ARM_REG_R4,t['object']),(UC_ARM_REG_R5,g['object']),(UC_ARM_REG_R6,level)),((4,actor),));add(ev,849 if level<50 else 850,[bytes.fromhex(t['name_hex']),bytes.fromhex(g['name_hex'])],trend=level)
  for c,t in pairs:
   ev=fragment(0x587A4,0x5880C,((UC_ARM_REG_R4,c['index']),(UC_ARM_REG_R5,t['object'])),((4,npc),));add(ev,851,[bytes.fromhex(c['name_hex']),bytes.fromhex(t['name_hex'])])
  regions=(b'the North Sea',b'the Mediterranean',b'Africa',b'the Indian Ocean',b'Southeast Asia',b'East Asia',b'the New World')
  for it in items:
   if not 0<=it['region']<7:continue
   ev=fragment(0x59950,0x59994,((UC_ARM_REG_R5,it['region']),(UC_ARM_REG_R6,it['object'])));add(ev,863,[bytes.fromhex(it['name_hex']),regions[it['region']]],native_item_region=it['region'])
  for rt in range(4):
   u.mem_write(route,struct.pack('<I',rt));sex=get(0x7E9B8,actor);address=b'Sir'if sex==0 else b"Ma'am";surname=text(get(ptr(ptr(actor)+0x24)-BASE,actor));u.mem_write(0x02470100,surname+b'\0');u.mem_write(0x02470000,address+b'\0')
   for a,b,n,regs,values in((0x5845C,0x5846C,869,((UC_ARM_REG_R7,npc),(UC_ARM_REG_R11,0x02470100)),[surname]),(0x58480,0x5849C,871,((UC_ARM_REG_R4,sex),(UC_ARM_REG_R6,npc),(UC_ARM_REG_R7,npc),(UC_ARM_REG_R11,0x02470100)),[surname,address]),(0x584CC,0x584E8,872,((UC_ARM_REG_R4,sex),(UC_ARM_REG_R6,npc),(UC_ARM_REG_R7,npc),(UC_ARM_REG_R11,0x02470100)),[surname,address]),(0x57FDC,0x58000,875,((UC_ARM_REG_R5,npc),),[surname]),(0x5802C,0x58058,877,((UC_ARM_REG_R5,npc),),[address]),(0x58308,0x58318,873,((UC_ARM_REG_R5,npc),(UC_ARM_REG_R6,0x02470000)),[address])):
    add(fragment(a,b,regs),n,values,route=rt)
   for c in companies:
    cname=name(c['object']);add(fragment(0x58008,0x58028,((UC_ARM_REG_R4,c['object']),(UC_ARM_REG_R5,npc))),876,[cname],route=rt);add(fragment(0x58060,0x58084,((UC_ARM_REG_R4,c['object']),(UC_ARM_REG_R5,npc),(UC_ARM_REG_R6,0x02470000))),878,[address,cname],route=rt,existing_native_argument_permutation=True)
   for it in items:
    if 0<=it['region']<7:add(fragment(0x5829C,0x582F0,((UC_ARM_REG_R4,it['object']),(UC_ARM_REG_R5,npc),(UC_ARM_REG_R9,it['region']))),870,[address,bytes.fromhex(it['name_hex']),regions[it['region']]],route=rt)
  for a,b,n in((0x599BC,0x599C8,868),(0x584FC,0x58508,874)):add(fragment(a,b,((UC_ARM_REG_R4,npc),(UC_ARM_REG_R6,npc))),n,[])
  current_fleet=fleet_root+4+get(0x2E58C)*0x84;fleet_source=bytes(u.mem_read(current_fleet,0x84))
  for category,formal,(c,t) in product(('destination','docked'),(0,1),pairs):
   fleet=bytearray(fleet_source);fleet[0x3F if category=='destination'else 0x3C]=t['index']
   if category=='docked':fleet[0x50]&=~8
   u.mem_write(0x02474000,bytes(fleet));u.mem_write(0x02474100,struct.pack('<3I',0,0,formal))
   if category=='destination':a,b,n,regs=0x57DDC,0x57E4C,879 if formal else 880,((UC_ARM_REG_R4,0x02474000),(UC_ARM_REG_R7,c['index']),(UC_ARM_REG_R6,npc))
   else:a,b,n,regs=0x57BA4,0x57C18,881 if formal else 882,((UC_ARM_REG_R5,0x02474000),(UC_ARM_REG_R4,c['index']),(UC_ARM_REG_R6,npc))
   add(fragment(a,b,regs,((0,0x02474100),)),n,[bytes.fromhex(c['name_hex']),bytes.fromhex(t['name_hex'])],fleet_field='3F'if category=='destination'else'3C',formal=formal)
 finally:u.hook_del(hook)
 voices=[]
 for i in range(40):
  obj=officers+4+i*32;voice=get(0x7E988,obj);chosen=get(0x53F4C,obj,0x02118400);assert chosen==(852 if voice in(0,1)else 851+voice);voices.append(dict(actor=i,voice=voice,ID=chosen))
 assert get(0x53F4C,0,0x02118400)==852
 tables=[]
 for table,ids in((0x021166E0,range(830,834)),(0x02116610,range(835,839)),(0x021166F0,range(859,863)),(0x02116810,range(864,868))):
  assert tuple(struct.unpack('<4I',u.mem_read(table,16)))==tuple(ids)
  for rt,n in enumerate(ids):u.mem_write(route,struct.pack('<I',rt));assert get(0x53C6C,table)==n;tables.append(dict(table=table,route=rt,ID=n))
 u.mem_write(route,raw[route-BASE:route-BASE+4]);coordinates=[]
 for it in items:
  get(ptr(ptr(it['object'])+0x20)-BASE,0x02450000,it['object']);position=bytes(u.mem_read(0x02450000,8))
  if position==b'\xff'*8:continue
  value=text(get(0x51580,0x02450000));assert value.startswith(b'\n ')and all(c<128 for c in value);coordinates.append(dict(item_ID=it['index'],original_position_hex=position.hex(),argument_hex=value.hex()))
 save(ROOT/'fresh_current_native_context.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),clean_ARM9_sha256=sha(clean),source_snapshot=snap,declared_provider_patch_dependencies=plans,all_provider_differences_owned=diffs,source_graphs=graphs,current_companies=companies,current_towns=towns,current_goods=goods,current_items=items,native_provider_fragments=cases,voice_selectors=voices,four_captain_tables=tables,coordinate_formatter_outputs=coordinates,original_role_price_wrapper_and_complete_gift_graph_still_pending=True,all_UI_calls_stopped_before_execution=True,supplied_inputs_and_scratch_fleet_objects_not_earned_events=True,no_ROM_registry_or_save_changes=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(provider_cases=len(cases),voice_cases=len(voices),captain_tables=len(tables),coordinates=len(coordinates),gift_and_price_remaining=True),flush=True)
