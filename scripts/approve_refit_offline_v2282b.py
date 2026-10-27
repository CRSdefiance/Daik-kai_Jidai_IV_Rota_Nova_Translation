"""Use genuine captured help geometry for a controlled label font sample."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/approve_refit_offline_v2282.py')
if __name__=='__main__':
 source=OLD.read_text().replace("refit_offline_approval_v2282'","refit_offline_approval_v2282b'")
 start=" raster,_,_=font_tools(rom);labelplane=";end=" entries=owned_entries(common,arm,plan['directory_sha256'])";a,b=source.index(start),source.index(end)
 replacement=''' from scripts.verify_production_compact_capacity_v2138 import captured_machine
 from unicorn.arm_const import UC_ARM_REG_PC
 obs=read('E:/Rota Nova translations/Generated/work/emulation_v193/refit_actual_v2276_V2171/refit_observer/requests.json');capture=next(r for r in obs['rows']if r['direct_help_payload_match']);cpu=captured_machine(arm,capture);textpointer=capture['font_input_pointer'];cpu.mem_write(textpointer,b'Spritsail\\0');cpu.emu_start(capture['PC'],capture['LR'],count=2000000)
 assert cpu.reg_read(UC_ARM_REG_PC)==capture['LR']and cpu.reg_read(UC_ARM_REG_R0)==textpointer+9
 header=capture['registers'][8]+0x1C38;pixels=(header+struct.unpack('<I',cpu.mem_read(header+16,4))[0])&0xffffffff;packed=bytes(cpu.mem_read(pixels,9072));labelplane=bytes(v for byte in packed for v in(byte&15,byte>>4))
 from dk4tool.dialogue.font_audit import GameAsciiFont
 font=GameAsciiFont.from_arm9(arm);expected=bytearray(168*108)
 for i,char in enumerate('Spritsail'):
  glyph=font.decode(char)
  for y in range(11):
   for x in range(6):
    if glyph.getpixel((x,y)):expected[y*168+i*6+x]=1
 assert labelplane==expected
 from PIL import Image
 lp=ROOT/'spritsail_native_label.png';Image.frombytes('L',(168,108),bytes(0 if v else 255 for v in labelplane)).crop((0,0,60,16)).resize((480,128),Image.Resampling.NEAREST).save(lp)
'''
 source=source[:a]+replacement+source[b:]
 source=source.replace('label_complete_native60x16_font','label_controlled_native168x108_font_cropped_preview')
 source=source.replace('label_width9cells_less_than_preceding10cell_Split_Sail=True','label_actual_component_widget_still_pending=True,label_controlled_help_object_not_component_widget=True')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/refit_offline_approval_v2282b/successor_provenance.json',dict(failed_producer=str(OLD),failed_producer_sha256=sha(OLD.read_bytes()),failure='An arbitrary60x16 test header was not a valid complete native font contract. It returned incompletely and was rejected; no component widget approval follows from it.',successor_uses_captured168x108_help_context_with_supplied_label_text_and_complete_independent_plane=True,label_actual_component_widget_pending_after_registered_build=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
