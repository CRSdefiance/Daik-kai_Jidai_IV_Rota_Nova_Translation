"""Continue actual body-font snapshots through the original glyph painter."""
from pathlib import Path
import struct
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/town_services_glyph_pitch_v2062b')
OBS=Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_services_font_actual_v2060_V2047/common_observer/requests.json')
REGS=(UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12,UC_ARM_REG_SP,UC_ARM_REG_LR)
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 obs=read(OBS);assert len(obs['rows'])==8 and not obs['errors']and not obs['mismatches']
 arm=NdsImage.open('out/all_routes_combined_v2047_candidate.nds').read_file('/__arm9__.bin');rows=[]
 for r in obs['rows']:
  raw=Path(r['snapshots']['WRAM']['path']).read_bytes();assert sha(raw)==r['snapshots']['WRAM']['sha256'];cpu,get=get_machine(arm,raw)
  for label,at in(('DTCM',r['DTCM_base']),('ITCM',0)):
   blob=Path(r['snapshots'][label]['path']).read_bytes();assert sha(blob)==r['snapshots'][label]['sha256']
   try:cpu.mem_write(at,blob)
   except Exception:cpu.mem_map(at,len(blob));cpu.mem_write(at,blob)
  cpu.reg_write(UC_ARM_REG_CPSR,0x1f)
  for reg,value in zip(REGS,r['registers']):cpu.reg_write(reg,value)
  events=[]
  def glyph(u,pc,size,data):
   code,style=struct.unpack('<2I',u.mem_read(u.reg_read(UC_ARM_REG_SP),8))
   events.append(dict(PC=pc,code=code,style=style,x=u.reg_read(UC_ARM_REG_R2),y=u.reg_read(UC_ARM_REG_R3)))
   u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))  # Explicit glyph-paint boundary; native font control still executes.
  for pc in(0x020D16B4,0x01FF83AC):cpu.hook_add(UC_HOOK_CODE,glyph,begin=pc,end=pc)
  error=None
  try:cpu.emu_start(r['PC'],r['LR'],count=2000000)
  except Exception as exc:error=str(exc)
  expected=[int.from_bytes(c.encode('cp932'),'big')for c in r['text']if c not in(' ','\n')]
  actual=[e['code']for e in events if e['code']!=32]
  result=dict(message_ID=r['source_request']['ID'],source_font_frame=r['frame'],bounds=r['bounds'],font_dimensions=list(struct.unpack_from('<2I',raw,0x31209C)),
   text=r['text'],glyph_events=events,nonblank_glyph_order_complete=actual==expected,native_row_origins=sorted({e['y']for e in events}),
   terminal_PC=cpu.reg_read(UC_ARM_REG_PC),original_return_completed=cpu.reg_read(UC_ARM_REG_PC)==r['LR'],error=error,
   input_bytes_unchanged=bytes(cpu.mem_read(r['registers'][1],len(bytes.fromhex(r['text_hex']))+1))==bytes.fromhex(r['text_hex'])+b'\0',
   SP_preserved=cpu.reg_read(UC_ARM_REG_SP)==r['registers'][13],source_snapshot=r['snapshots']['WRAM'],offline_native_continuation_not_additional_gameplay=True)
  rows.append(result);save(ROOT/'partial.json',dict(rows=rows,full_goal_complete=False));print({k:result[k]for k in('message_ID','font_dimensions','native_row_origins','nonblank_glyph_order_complete','original_return_completed','error')},flush=True)
 save(ROOT/'eight_original_native_font_continuations.json',dict(ARM9_sha256=sha(arm),source_observer=str(OBS),source_observer_sha256=sha(OBS.read_bytes()),rows=rows,
  original_font_control_with_explicit_glyph_paint_return_boundaries=True,not_a_full_native_pixel_proof=True,no_ROM_registry_save_or_emulator_mutation=True,
  revised_batch_formatting_approval=False,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
