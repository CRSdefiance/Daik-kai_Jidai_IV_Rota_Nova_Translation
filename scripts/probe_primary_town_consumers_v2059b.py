"""Replay original request CPU/RAM snapshots to the first body font boundary.

Offline native continuation,not an additional live UI visit or revised proof.
"""
from pathlib import Path
import struct
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/town_services_consumers_v2059b')
OBS=Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_services_actual_v2053_V2047/common_observer/requests.json')
REGS=(UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12,UC_ARM_REG_SP,UC_ARM_REG_LR)
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 obs=read(OBS);arm=NdsImage.open('out/all_routes_combined_v2047_candidate.nds').read_file('/__arm9__.bin');rows=[]
 for r in obs['rows']:
  raw=Path(r['complete_readonly_snapshots']['WRAM']['path']).read_bytes();cpu,get=get_machine(arm,raw)
  for label,at in [('DTCM',r['DTCM_base']),('ITCM',0)]:
   data=Path(r['complete_readonly_snapshots'][label]['path']).read_bytes()
   try:cpu.mem_write(at,data)
   except Exception:
    cpu.mem_map(at,len(data));cpu.mem_write(at,data)
  cpu.reg_write(UC_ARM_REG_CPSR,0x1f)
  for reg,value in zip(REGS,r['registers']):cpu.reg_write(reg,value)
  seen=[]
  def font(u,pc,size,data):
   p=u.reg_read(UC_ARM_REG_R1)
   if not 0x02000000<=p<0x02400000:return
   value=bytes(u.mem_read(p,512)).split(b'\0')[0]
   if p!=0x0228E5A8:return
   ctx=u.reg_read(UC_ARM_REG_R0);context=bytes(u.mem_read(ctx,128));view=struct.unpack_from('<I',context)[0]
   seen.append(dict(PC=pc,LR=u.reg_read(UC_ARM_REG_LR),context_address=ctx,context128_hex=context.hex(),text_hex=value.hex(),text=value.decode('cp932'),view_address=view,view128_hex=bytes(u.mem_read(view,128)).hex()))
   u.emu_stop()
  cpu.hook_add(UC_HOOK_CODE,font,begin=0x020D5404,end=0x020D5404)
  error=None
  try:cpu.emu_start(0x020534F4,0x027E0000,count=2000000)
  except Exception as exc:error=str(exc)
  row=dict(message_ID=r['message_ID'],source_request=r,body_font_boundaries=seen,terminal_PC=cpu.reg_read(UC_ARM_REG_PC),error=error,offline_original_native_continuation_only=True)
  rows.append(row);save(ROOT/'partial.json',dict(ARM9_sha256=sha(arm),rows=rows,full_goal_complete=False))
  print(dict(ID=r['message_ID'],body_boundaries=len(seen),terminal_PC=hex(row['terminal_PC']),error=error),flush=True)
 save(ROOT/'original_request_to_body_font_continuations.json',dict(ARM9_sha256=sha(arm),source_observer=str(OBS),source_observer_sha256=sha(OBS.read_bytes()),rows=rows,original_instructions_no_formatter_macro_widget_or_getter_stubs=True,actual_live_request_snapshots_not_additional_scene_visits=True,no_ROM_save_or_emulator_mutation=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
