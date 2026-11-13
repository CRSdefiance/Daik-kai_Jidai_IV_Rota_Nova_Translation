"""Bounded current-code CPU/font context;never replace initialized historical RAM."""
from pathlib import Path
from types import FunctionType,SimpleNamespace
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.script.common_message_table import DIRECTORY_OFFSET,TABLE_OFFSET
from scripts.probe_escape_direct_source_v1186 import machine
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.probe_button_prompt_native import BASE
from scripts.verify_village_wrap_v608 import read,save

class CurrentContext:
 def __init__(self,manuscript,historical_rom,root):
  self.doc=read(manuscript);context=read(self.doc['native_context_proof']);self.rompath=Path(self.doc['current_ROM']);self.oldpath=Path(historical_rom);self.rom=NdsImage.open(self.rompath);old=NdsImage.open(self.oldpath)
  self.arm=self.rom.read_file('/__arm9__.bin');self.common=self.rom.read_file('/COMMON/MESFILE.DK4');oldarm=old.read_file('/__arm9__.bin');self.raw=Path(context['actual_snapshot']).read_bytes();self.entries=current_entries(self.common,self.arm)
  assert sha(self.rompath.read_bytes())==self.doc['current_ROM_sha256']and sha(self.arm)==self.doc['current_ARM9_sha256']and sha(self.common)==self.doc['current_COMMON_sha256']and sha(self.raw)==context['actual_snapshot_sha256']and len(self.raw)==0x400000
  prior=read('work/analysis/escape_direct_runtime_v1184c/runtime_plan.json');audited=[(0x132020,16),(0x147B9C,212),(0x147E54,172),(0x169F78,12),(0x16A010,8),(0x16A05C,8),(0x16A0B0,16)]
  spans=[(a-BASE,b-a)for a,b in prior['private_spans']]+audited+[(DIRECTORY_OFFSET,41*4),(TABLE_OFFSET,3668*2),(0x535E8,64)];merged=[]
  for at,size in sorted(spans):
   if merged and at<=merged[-1][0]+merged[-1][1]:lo,length=merged[-1];merged[-1]=(lo,max(lo+length,at+size)-lo)
   else:merged.append((at,size))
  patches=[]
  for at,size in merged:
   before=self.raw[at:at+size];assert before==oldarm[at:at+size],hex(at);patches.append(dict(address=BASE+at,source_hex=before.hex(),target_hex=self.arm[at:at+size].hex()))
  sections=MainCodeFile(self.arm,BASE).sections;oldsections=MainCodeFile(oldarm,BASE).sections;assert len(sections[3].data)-48==len(oldsections[3].data)-48==123040
  delta=[i for i,(a,b)in enumerate(zip(oldsections[3].data[:-48],sections[3].data[:-48],strict=True))if a!=b];assert delta==list(range(0x5D4,0x5DC))
  before,after=bytes(oldsections[3].data[0x5D4:0x5DC]),bytes(sections[3].data[0x5D4:0x5DC]);assert before==bytes.fromhex('8265617469636961')and after==b'Faticia\0'and self.raw[POOL-BASE+0x5D4:POOL-BASE+0x5DC]==before
  patches.append(dict(address=POOL+0x5D4,source_hex=before.hex(),target_hex=after.hex()));self.plan=dict(patches=patches);self.sections=[*sections,SimpleNamespace(ramAddress=POOL,data=sections[3].data[:-48])];self.machines=[]
  cpu,get,_=machine(self.arm,self.common,self.raw,self.plan);self.actor_root=get(0xCB184)
  class FontROM:
   @staticmethod
   def open(path):assert str(path)=='out/all_routes_combined_v255_candidate.nds';return self.rom
  self.raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':FontROM},argdefs=original_raster.__defaults__)
  root=Path(root);assert not root.exists();root.mkdir(parents=True);self.proof_path=root/'current_native_pipeline_plan.json'
  save(self.proof_path,dict(candidate=str(self.rompath),candidate_sha256=sha(self.rompath.read_bytes()),historical_ROM=str(self.oldpath),historical_ROM_sha256=sha(self.oldpath.read_bytes()),ARM9_sha256=sha(self.arm),COMMON_sha256=sha(self.common),historical_snapshot=context['actual_snapshot'],historical_snapshot_sha256=sha(self.raw),patches=patches,current_audited_table_gate_entry_exit_extents=audited,current_deployed_payload_delta=delta,no_whole_initialized_RAM_overlay=True,helper=str(Path(__file__)),helper_sha256=sha(Path(__file__).read_bytes()),scope='Current CPU source/formatter/font context only;historical RAM is not a new emulator visit. Only declared immutable spans and the verified eight-byte label delta are overlaid.',full_goal_complete=False))
 def machine(self,a,c,r,p):
  cpu,get,provider=machine(a,c,r,p);assert get(0xCB184)==self.actor_root;before=bytes(cpu.mem_read(self.actor_root,0x1A04));executed=set()
  def exact(u,pc,size,unused):
   for section in self.sections:
    start=section.ramAddress
    if start<=pc and pc+size<=start+len(section.data):assert bytes(u.mem_read(pc,size))==bytes(section.data[pc-start:pc-start+size]),('executed old instruction',hex(pc));executed.add(pc);break
  cpu.hook_add(UC_HOOK_CODE,exact);provider.executed_current=executed;self.machines.append((cpu,before));return cpu,get,provider
 def execute(self,fn,*args,raw=None):
  names={**fn.__globals__,'machine':self.machine,'portrait_machine':self.machine};bound=FunctionType(fn.__code__,names,argdefs=fn.__defaults__);result=bound(self.arm,self.common,self.raw if raw is None else raw,self.plan,*args)
  cpu,before=self.machines[-1];assert bytes(cpu.mem_read(self.actor_root,0x1A04))==before
  return result
 def speak(self,entry,actor_or_role,table,argument=None,raw=None):return self.execute(consumer,entry,actor_or_role,table,argument,raw=raw)
