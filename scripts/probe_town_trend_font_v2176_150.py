"""Continue actual compact-font snapshots without changing metrics, bounds or glyph returns."""
from pathlib import Path
import struct
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_INVALID
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_PC,UC_ARM_REG_LR,UC_ARM_REG_SP,UC_ARM_REG_CPSR
from scripts.probe_primary_town_glyph_pitch_v2062b import REGS
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/town_trend_continuations_v2176_150')
OBS=Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_trend_actual_v2175_150_V2171/common_observer/requests.json')
BASE=0x02000000
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 obs=read(OBS);assert not obs['errors']and not obs['mismatches'];arm=NdsImage.open('out/all_routes_combined_v2171_candidate.nds').read_file('/__arm9__.bin');cases=[]
 for row in obs['rows']:
  raw=Path(row['snapshots']['WRAM']['path']).read_bytes();assert sha(raw)==row['snapshots']['WRAM']['sha256'];cpu,get=get_machine(arm,raw)
  for label,addresses in [('DTCM',[row['DTCM_base']]),('ITCM',[0,0x01FF8000])]:
   data=Path(row['snapshots'][label]['path']).read_bytes();assert sha(data)==row['snapshots'][label]['sha256']
   for address in addresses:
    try:cpu.mem_write(address,data)
    except Exception:cpu.mem_map(address,len(data));cpu.mem_write(address,data)
  cpu.mem_map(0x06000000,0x100000);cpu.mem_write(0x06000000,bytes(0x100000));cpu.reg_write(UC_ARM_REG_CPSR,0x1F)
  for reg,value in zip(REGS,row['registers'][:len(REGS)],strict=True):cpu.reg_write(reg,value)
  glyphs=[];compact=[];faults=[]
  def observe(u,pc,size,data):
   if pc in(0x020D16B4,0x01FF83AC):
    code,style=struct.unpack('<2I',u.mem_read(u.reg_read(UC_ARM_REG_SP),8));glyphs.append(dict(PC=pc,code=code,style=style,x=u.reg_read(UC_ARM_REG_R2),y=u.reg_read(UC_ARM_REG_R3)))
   elif pc==0x020D1604:
    pointer=u.reg_read(UC_ARM_REG_R3);text=bytes(u.mem_read(pointer,256)).split(b'\0')[0];point=list(struct.unpack('<2I',u.mem_read(u.reg_read(UC_ARM_REG_R2),8)))
    compact.append(dict(font=u.reg_read(UC_ARM_REG_R0),destination=u.reg_read(UC_ARM_REG_R1),point=point,text_hex=text.hex()))
  for pc in(0x020D16B4,0x01FF83AC,0x020D1604):cpu.hook_add(UC_HOOK_CODE,observe,begin=pc,end=pc)
  def invalid(u,access,address,size,value,data):faults.append(dict(access=access,address=address,size=size,PC=u.reg_read(UC_ARM_REG_PC)));return False
  cpu.hook_add(UC_HOOK_MEM_INVALID,invalid);error=None
  try:cpu.emu_start(row['PC'],row['LR'],count=2000000)
  except Exception as exc:error=repr(exc)
  returned=cpu.reg_read(UC_ARM_REG_R0);expected=0x0228E5A8+len(bytes.fromhex(row['text_hex']));vram=bytes(cpu.mem_read(0x06000000,0x100000));path=ROOT/f'ID{row["source_request"]["ID"]}_VRAM.bin';path.write_bytes(vram)
  cases.append(dict(message_ID=row['source_request']['ID'],bounds=row['bounds'],font_input_offset=row['font_input_offset'],text_hex=row['text_hex'],returned_pointer=returned,expected_full_pointer=expected,complete_native_return=returned==expected and cpu.reg_read(UC_ARM_REG_PC)==row['LR'],SP_preserved=cpu.reg_read(UC_ARM_REG_SP)==row['registers'][13],callee_registers_preserved=all(cpu.reg_read(REGS[i])==row['registers'][i]for i in range(4,12)),glyph_events=glyphs,compact_bitmap_calls=compact,VRAM=dict(path=str(path),sha256=sha(vram)),faults=faults,error=error,all_native_font_and_glyph_instructions_unstubbed=True,metrics_and_bounds_and_input_text_not_changed=True))
  print(dict(ID=cases[-1]['message_ID'],complete=cases[-1]['complete_native_return'],glyphs=len(glyphs),compact_calls=len(compact),error=error,faults=faults),flush=True)
 save(ROOT/'actual_snapshot_native_font_continuations.json',dict(ARM9_sha256=sha(arm),source_observer=str(OBS),source_observer_sha256=sha(OBS.read_bytes()),cases=cases,explicit_zero_VRAM_input_mapping_not_live_GPU_capture=True,all_native_functions_unstubbed=True,not_a_ROM_change_or_geometry_approval=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
