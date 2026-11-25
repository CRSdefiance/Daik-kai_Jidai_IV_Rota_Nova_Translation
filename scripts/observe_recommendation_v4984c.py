"""Market observation with a single disclosed source-bound reward-input fixture."""
import ctypes as ct
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE,CORE_SHA,ImageReader
from scripts.inspect_resource_dispatch_v668 import tables
from scripts.observe_file_requests_v681 import assemble
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.observe_script_sources_v733 import Observer as Host
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/recommendation_actual_v4984c_unconfigured')
def configure(case,rom):
 global ROOT,ROM
 ROOT=Path('work/analysis/recommendation_actual_v4984c_'+case);ROM=Path(rom)
ROM=Path('out/all_routes_combined_v4766_candidate.nds')
REQUEST,FONT=0x020534F4,0x020D5404

def prepare_contract():
 assert not ROOT.exists()
 arm=NdsImage.open(ROM).read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
 raw=CORE.read_bytes();assert sha(raw)==CORE_SHA;base,table=tables(raw);targets=[]
 for pc in(REQUEST,FONT,0x020BBCA4):
  at=pc-0x02000000;assert arm[at:at+4]==clean[at:at+4];word=struct.unpack_from('<I',arm,at)[0];index=word>>16&0xff0|word>>4&15
  targets.append(dict(PC=pc,word=word,instruction_index=index,handler_RVA=struct.unpack_from('<Q',raw,table['file_offset']+index*8)[0]-base))
 ROOT.mkdir(parents=True);save(ROOT/'source_contract.json',dict(targets=targets,interpreter_table=table,ARM9_sha256=sha(arm),core_sha256=CORE_SHA))

class Observer:
 install,close=Host.install,Host.close
 def __init__(self,core,folder):
  self.core,self.folder=core,Path(folder);self.folder.mkdir(parents=True,exist_ok=True)
  self.native,self.image=NativeMemory(),ImageReader(core);self.source=read(ROOT/'source_contract.json')
  self.cpu=self.image.anchor('9REG',4,16)-16;self.wram=self.image.anchor('WRAM',1,0x400000)
  self.dtcm=self.image.anchor('DTCM',1,0x4000);self.dtcm_base=self.image.anchor('MDTC',4,1);self.itcm=self.image.anchor('ITCM',1,0x8000)
  self.header=(ct.c_uint32*4)(0,1,0,0);self.rows,self.requests,self.errors,self.slots,self.seen=[],[],[],[],set();self.closed=False;self.last=None;self.fixtures=[]
  def callback(frame):
   try:
    cpu=ct.string_at(self.cpu,128);v=struct.unpack('<32I',cpu);pc=v[2]
    target=next(t for t in self.source['targets']if t['PC']==pc);assert v[1]==target['word']
    if frame<2000:return
    if pc==0x020BBCA4:
     assert not self.fixtures,'Only one declared reward-input fixture is permitted'
     assert v[8]==2,'The genuine sale still contains two cargo holds'
     before={k:ct.string_at(ptr,length) for k,ptr,length in [('CPU',self.cpu,128),('WRAM',self.wram,0x400000),('DTCM',self.dtcm,0x4000),('ITCM',self.itcm,0x8000)]}
     sp=v[17];address=sp+0x10;db=struct.unpack('<I',self.image.read(self.dtcm_base,4))[0]
     if 0x02000000<=address<=0x023FFFFC:host=self.wram+address-0x02000000;kind='WRAM';offset=address-0x02000000
     else:
      assert db<=address<=db+0x3FFC,(hex(address),hex(db))
      host=self.dtcm+address-db;kind='DTCM';offset=address-db
     old_flag=ct.c_uint32.from_address(host).value;assert old_flag in [0,1]
     ct.c_uint32.from_address(self.cpu+4*4).value=2
     ct.c_uint32.from_address(self.cpu+8*4).value=16
     ct.c_uint32.from_address(host).value=1
     after={k:ct.string_at(ptr,length) for k,ptr,length in [('CPU',self.cpu,128),('WRAM',self.wram,0x400000),('DTCM',self.dtcm,0x4000),('ITCM',self.itcm,0x8000)]}
     diffs={k:[i for i,(a,b) in enumerate(zip(before[k],after[k],strict=True)) if a!=b] for k in before}
     assert set(diffs['CPU'])<=set(range(16,20))|set(range(32,36))
     assert all(set(diffs[k])<=(set(range(offset,offset+4)) if k==kind else set()) for k in ['WRAM','DTCM','ITCM'])
     files={}
     for version,data in [('before',before),('after',after)]:
      for k,value in data.items():
       path=self.folder/f'qualification_{version}_{k}.bin';path.write_bytes(value);files[version+'_'+k]=dict(path=str(path),bytes=len(value),sha256=sha(value))
     self.fixtures.append(dict(frame=frame,PC=pc,original_instruction_word=v[1],original_qualification_result=v[4],supplied_qualification_result=2,
      original_sale_hold_total=v[8],supplied_reward_quantity_input=16,original_bonus_flag=old_flag,supplied_bonus_flag=1,
      stack_field_address=address,stack_memory_kind=kind,stack_memory_offset=offset,exact_changed_offsets=diffs,snapshots=files,
      all_other_CPU_WRAM_DTCM_ITCM_bytes_exact=True,no_PC_code_RNG_cash_or_cargo_quantity_write=True,
      counterfactual_qualification_and_quantity_inputs_not_an_earned_letter_or_large_real_sale=True))
     return
    if pc==REQUEST:
     self.last=dict(frame=frame,ID=v[5],caller_LR=v[18]);self.requests.append(self.last);return
    if not self.last or not 0<=self.last['ID']<3668 or v[5] not in (0x0228E5A8,0x0228E5AA):return
    ctx=v[4];assert 0x02000000<=ctx<0x023FFF80
    context=ct.string_at(self.wram+ctx-0x02000000,128);text=ct.string_at(self.wram+0x0228E5A8-0x02000000,512).split(b'\0')[0]
    key=self.last['ID'],v[18],context[:32],text
    if key in self.seen:return
    self.seen.add(key);raw=ct.string_at(self.wram,0x400000);dtcm=self.image.read(self.dtcm,0x4000);itcm=self.image.read(self.itcm,0x8000);md=self.image.read(self.dtcm_base,4)
    prefix=self.folder/f'font_{len(self.rows):03d}_ID{self.last["ID"]}';snapshots={}
    for label,data in(('WRAM',raw),('DTCM',dtcm),('ITCM',itcm),('CPU',cpu)):
     p=prefix.with_name(prefix.name+'_'+label+'.bin');p.write_bytes(data);snapshots[label]=dict(path=str(p),bytes=len(data),sha256=sha(data))
    assert ct.string_at(self.cpu,128)==cpu and ct.string_at(self.wram,0x400000)==raw
    assert self.image.read(self.dtcm,0x4000)==dtcm and self.image.read(self.itcm,0x8000)==itcm and self.image.read(self.dtcm_base,4)==md
    self.rows.append(dict(frame=frame,font_input_pointer=v[5],font_input_offset=v[5]-0x0228E5A8,source_request=dict(self.last),PC=pc,LR=v[18],registers=list(v[4:20]),context128_hex=context.hex(),bounds=list(struct.unpack_from('<4I',context,4)),text_hex=text.hex(),text=text.decode('cp932'),snapshots=snapshots,DTCM_base=struct.unpack('<I',md)[0],CPU_WRAM_DTCM_ITCM_configuration_exact=True))
   except BaseException as exc:self.errors.append(repr(exc));self.header[1]=0
  self.callback=ct.WINFUNCTYPE(None,ct.c_uint32)(callback)
  groups={}
  for target in self.source['targets']:groups.setdefault(target['instruction_index'],[]).append(target)
  for index,targets in groups.items():
   slot=core._handle+self.source['interpreter_table']['RVA']+index*8;original=self.image.qword(slot)
   assert all(original==core._handle+t['handler_RVA']for t in targets)
   address=self.native.alloc(None,4096,0x3000,0x04);code,assembly=assemble(self.cpu,ct.addressof(self.header),ct.cast(self.callback,ct.c_void_p).value,original,targets,address)
   assert len(code)<4096;ct.memmove(address,code,len(code));old=ct.c_uint32()
   assert self.native.protect(address,4096,0x20,ct.byref(old))and self.native.flush(self.native.process,address,len(code))
   self.slots.append(dict(slot=slot,original=original,address=address,code_hex=code.hex(),assembly=assembly))
 def next_frame(self):
  self.header[0]+=1
  counts=(len(self.rows),len(self.requests),len(self.errors))
  if counts!=getattr(self,'live_counts',None):
   self.live_counts=counts
   save(ROOT/'live_requests.json',dict(frame=self.header[0],rows=self.rows,source_requests=self.requests,errors=self.errors,partial=True,terminal=False,full_goal_complete=False))
 def save(self):
  assert self.closed
  save(self.folder/'requests.json',dict(rows=self.rows,source_requests=self.requests,synthetic_recommendation_reward_input_fixtures=self.fixtures,errors=self.errors,callbacks=self.header[2],mismatches=self.header[3],all_host_slots_restored_and_core_file_exact=True,source_contract_sha256=sha((ROOT/'source_contract.json').read_bytes()),observer_sha256=sha(Path(__file__).read_bytes()),host_filters=self.slots,full_goal_complete=False))
  for row in self.slots:assert self.native.free(row['address'],0,0x8000)
  assert not self.errors and not self.header[3]
