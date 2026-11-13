"""Execute current source-selected53F0C pipelines with explicit immutable-code overlays."""
from pathlib import Path
import struct
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET,TABLE_OFFSET
from scripts.probe_escape_direct_source_v1186 import machine,RAW
from scripts.probe_button_prompt_native import BASE,STACK,STOP
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/escape_pipeline_v2514')
ROM=Path('out/all_routes_combined_v2284_candidate.nds')
OLDROM=Path('out/all_routes_combined_v1166_candidate.nds')

if __name__=='__main__':
 assert not ROOT.exists()
 rom,oldrom=map(NdsImage.open,(ROM,OLDROM));arm=rom.read_file('/__arm9__.bin');oldarm=oldrom.read_file('/__arm9__.bin')
 common=rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm);raw=RAW.read_bytes()
 source_report=read(RAW.parent/'capture_report.json')
 receipts=source_report['read_only_capture_RAM_snapshots']+source_report['read_only_pause_RAM_snapshots']
 receipt=next(r for r in receipts if r['frame']==6902)
 assert sha(raw)==receipt['sha256'] and source_report['ROM_sha256']==sha(OLDROM.read_bytes())
 oldplan=read('work/analysis/escape_direct_runtime_v1184c/runtime_plan.json')
 spans=[(a-BASE,b-a)for a,b in oldplan['private_spans']]+[(DIRECTORY_OFFSET,41*4),(TABLE_OFFSET,3668*2),(0x535E8,64)]
 patches=[]
 for at,size in spans:
  before=raw[at:at+size]
  assert before==oldarm[at:at+size],hex(at)
  patches.append(dict(address=BASE+at,source_hex=before.hex(),target_hex=arm[at:at+size].hex()))
 plan=dict(patches=patches)
 current_sections=MainCodeFile(arm,BASE).sections
 old_sections=MainCodeFile(oldarm,BASE).sections
 assert current_sections[3].data[:-48]==old_sections[3].data[:-48]
 cpu,get,provider=machine(arm,common,raw,plan);root=get(0xCB184)
 actors=[root+4+i*32 for i in range(207)]+[root+0x19E4]
 selected={};choices=[]
 for table in(0x02117500,0x02117620):
  for slot,actor in enumerate(actors):
   n=get(0x53F4C,actor,table);choices.append(dict(slot=slot,actor_object=actor,table=table,message_ID=n));selected.setdefault(n,(actor,table))
 assert set(selected)=={*range(1951,1957),*range(1973,1980)}
 captain=root+0x19E4;vt=struct.unpack('<I',cpu.mem_read(captain,4))[0]
 pointer=get(struct.unpack('<I',cpu.mem_read(vt+0x20,4))[0]-BASE,captain)
 name=bytes(cpu.mem_read(pointer,64)).split(b'\0')[0]
 reference=read('work/analysis/escape_direct_fonts_v1185/native_direct_escape_fonts.json')
 cases=[]
 for n,(actor,table)in sorted(selected.items()):
  cpu,get,provider=machine(arm,common,raw,plan);seen={};executed=set()
  before_actor=bytes(cpu.mem_read(root,0x1A04))
  def current_code(u,pc,size,unused):
   for section in current_sections:
    start=section.ramAddress
    if start<=pc and pc+size<=start+len(section.data):
     assert bytes(u.mem_read(pc,size))==bytes(section.data[pc-start:pc-start+size]),('executed old code',hex(pc))
     executed.add(pc)
     return
  def observe(u,pc,size,unused):
   if pc==BASE+0x5408C:
    u.reg_write(UC_ARM_REG_PC,BASE+0x54144)
   elif pc==0x01FFCF3C:
    sp=u.reg_read(UC_ARM_REG_SP)
    seen.update(parent=struct.unpack('<I',u.mem_read(sp+0x264,4))[0],table=struct.unpack('<I',u.mem_read(sp+0x274,4))[0],
     input_hex=bytes(u.mem_read(u.reg_read(UC_ARM_REG_R1),256)).split(b'\0')[0].hex(),output=u.reg_read(UC_ARM_REG_R0))
   else:
    seen['formatted_hex']=bytes(u.mem_read(seen['output'],256)).split(b'\0')[0].hex()
    u.emu_stop()
  cpu.hook_add(UC_HOOK_CODE,current_code)
  for pc in(BASE+0x5408C,0x01FFCF3C,BASE+0x54164):cpu.hook_add(UC_HOOK_CODE,observe,begin=pc,end=pc)
  cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,STOP)
  for reg,value in((UC_ARM_REG_R0,actor),(UC_ARM_REG_R1,table),(UC_ARM_REG_R2,pointer),(UC_ARM_REG_R3,0)):cpu.reg_write(reg,value)
  cpu.emu_start(BASE+0x53F0C,STOP,count=3000000)
  assert cpu.reg_read(UC_ARM_REG_PC)==BASE+0x54164 and seen['parent']==0x02053F40 and seen['table']==table
  assert seen['input_hex']==entries[n].text.replace(b'%s',name).hex()
  candidates=[r for r in reference['cases']if r['message_ID']==n and(not r['variant']or r['variant']['name_hex']==name.hex())]
  assert candidates and all(r['formatted_hex']==seen['formatted_hex']for r in candidates)
  assert bytes(cpu.mem_read(root,0x1A04))==before_actor
  cases.append(dict(message_ID=n,source_voice_actor=actor,source_table=table,actual_historical_captain_compact_name_hex=name.hex(),
   **seen,file_reads=provider.reads,file_opens=provider.opens,all_executed_instructions_in_current_ROM_sections_byte_exact=True,
   executed_distinct_current_instruction_addresses=len(executed),all_actor_and_captain_model_bytes_unchanged=True,
   original53F0C_selection_loader_printf_macro_and_corrected_wrap_execute=True,stops_before_native_painter_UI_constructor_bridge_not_gameplay=True))
  print(n,'current original direct pipeline and instruction-byte checks pass',flush=True)
 ROOT.mkdir(parents=True)
 save(ROOT/'current_direct_pipeline.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(common),
  all416_source_voice_choices=choices,all13_current_direct_pipeline_cases=cases,snapshot=str(RAW),snapshot_sha256=sha(raw),snapshot_historical_candidate=str(OLDROM),
  snapshot_historical_candidate_sha256=sha(OLDROM.read_bytes()),declared_immutable_current_code_metadata_overlays=patches,
  all_overlay_source_bytes_verified_exact_historical_ROM=True,all_executed_section_code_matches_current_ROM=True,
  complete123040_staged_payload_current_historical_equal=True,
  boundaries=['host successful COMMON file open/read','portrait object construction bypass','stop before painter at54164'],
  native_full_fonts_verified_separately=True,current_emulator_runs=0,completed_entries_added=0,
  producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print('13 current direct pipelines,416 voice choices,current executed code bytes and actor preservation pass. No gameplay or coverage credit.')
