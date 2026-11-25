"""Current actual13 help selections, native snapshot returns and spoken capacity."""
from pathlib import Path
import struct
from PIL import Image,ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_PC,UC_ARM_REG_SP
from scripts.probe_primary_town_glyph_pitch_v2062b import REGS
from scripts.verify_production_compact_capacity_v2138 import captured_machine,probe
from scripts.finish_refit_display_v712 import HINTS,WHITE,load
from scripts.verify_full_fleet_battle_v652 import fleet_models
from scripts.verify_full_fleet_victory_v654 import funds
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.dialogue.refit_help import compile_paragraph
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
ROOT=Path('work/analysis/refit_current_actual_verification_v2281')
OBS=Path('work/analysis/refit_actual_v2276/live_requests.json')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/refit_actual_v2276_V2171')
BASE=0x02000000
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);rompath=Path('out/all_routes_combined_v2171_candidate.nds');rom=NdsImage.open(rompath);arm=rom.read_file('/__arm9__.bin');font=GameAsciiFont.from_arm9(arm);report,shots,receipt=load(CAP,sha(rompath.read_bytes()),20601);oldpath=Path('out/all_routes_combined_v831_candidate.nds');oldreport,oldshots,oldreceipt=load(Path('work/emulation_v193/refit_editorial_v831_after'),sha(oldpath.read_bytes()),20600)
 assert report['scripted_input_schedule']==oldreport['scripted_input_schedule']and len(shots)==62 and shots.keys()==oldshots.keys()
 assert not any(v for k,v in report.items()if k.startswith('synthetic_'))and report['battery_save_preloaded']['source_sha256']=='febc859c5af2df6fa8023c349bb7f31b5fc15ea769fb2eea527b3a3f80521731'
 obs=read(OBS);assert obs['terminal']and not obs['errors'];helps=[r for r in obs['rows']if r['direct_help_payload_match']];assert len(helps)==13
 oldrows={r['message_id']:r for r in read('translations/refit_help_editorial_manuscript_v3.json')['records']};returns=[]
 for row in helps:
  n=row['source_request']['ID'];compiled,lines=compile_paragraph(oldrows[n]['english']);assert bytes.fromhex(row['text_hex'])==compiled[:-1]and row['bounds']==[0,0,168,108]
  cpu=captured_machine(arm,row);parent=row['registers'][8];header=parent+0x1C38;assert struct.unpack('<3I',cpu.mem_read(header,12))==(4,42,108);pixels=(header+struct.unpack('<I',cpu.mem_read(header+16,4))[0])&0xffffffff
  assert not any(cpu.mem_read(pixels,9072));before_sp=cpu.reg_read(UC_ARM_REG_SP);before_regs=[cpu.reg_read(REGS[i])for i in range(4,12)]
  cpu.emu_start(row['PC'],row['LR'],count=2000000)
  assert cpu.reg_read(UC_ARM_REG_PC)==row['LR']and cpu.reg_read(UC_ARM_REG_R0)==row['font_input_pointer']+len(compiled)-1
  assert cpu.reg_read(UC_ARM_REG_SP)==before_sp and [cpu.reg_read(REGS[i])for i in range(4,12)]==before_regs
  assert bytes(cpu.mem_read(row['font_input_pointer'],len(compiled)))==compiled
  packed=bytes(cpu.mem_read(pixels,9072));plane=bytes(nib for b in packed for nib in(b&15,b>>4));expected=bytearray(168*108)
  for y,line in enumerate(lines):
   for i,c in enumerate(line):
    glyph=font.decode(c)
    for gy in range(11):
     for gx in range(6):
      if glyph.getpixel((gx,gy)):expected[(y*12+gy)*168+i*6+gx]=1
  assert plane==expected
  returns.append(dict(message_ID=n,frame=row['frame'],native_return_complete=True,original_168x108_context_and6x12_metrics_unchanged=True,whole_plane_equal_independent_font=True,full_plane_sha256=sha(plane),SP_callee_registers_and_complete_input_preserved=True,all_native_font_glyph_instructions_unstubbed=True))
  print(dict(actual_native_ID=n,complete=True),flush=True)
 background=Image.new('RGB',(168,84))
 for y in range(84):
  for x in range(168):
   colours={shots[f].getpixel((x+64,y+80))for f in HINTS if shots[f].getpixel((x+64,y+80))!=WHITE};assert len(colours)==1;background.putpixel((x,y),colours.pop())
 actual=[];controls=0
 for frame,n in HINTS.items():
  image=shots[frame];_,lines=compile_paragraph(oldrows[n]['english']);expected=background.copy();ink=set()
  for y,line in enumerate(lines):
   for i,c in enumerate(line):
    glyph=font.decode(c)
    for gy in range(11):
     for gx in range(6):
      if glyph.getpixel((gx,gy)):p=(i*6+gx,y*12+gy);ink.add(p);expected.putpixel(p,WHITE)
   for i in(0,len(line)-1):assert any(i*6<=x<(i+1)*6 and y*12<=yy<y*12+11 for x,yy in ink);controls+=1
  assert image.crop((64,80,232,164)).tobytes()==expected.tobytes()
  assert image.crop((64,80,232,164)).tobytes()==oldshots[frame].crop((64,80,232,164)).tobytes()
  actual.append(dict(frame=frame,message_ID=n,lines=lines,complete_foreground_blank_paper_and_first_final_glyphs_equal=True,visible168x84_not_internal108_height=True,historical_help_panel_equal=True))
 selected=list(dict.fromkeys([3200,11900,*[next(f for f,v in HINTS.items()if v==n)for n in sorted(set(HINTS.values()))],20000,20600]));sheets=[]
 for start in range(0,len(selected),12):
  subset=selected[start:start+12];sheet=Image.new('RGB',(1024,412*((len(subset)+3)//4)),'#263238');draw=ImageDraw.Draw(sheet)
  for i,f in enumerate(subset):x,y=i%4*256,i//4*412;draw.text((x+4,y+4),f'V2171 frame{f} ID{HINTS.get(f,"transition")}',fill='white');sheet.paste(shots[f],(x,y+28))
  p=ROOT/f'actual_sheet_{start//12:02d}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
 states=[]
 for f in(3200,11900,19700,20000,20300,20600):
  values=[]
  for rpt,a in((report,arm),(oldreport,NdsImage.open(oldpath).read_file('/__arm9__.bin'))):
   s=next(r for r in rpt['read_only_capture_RAM_snapshots']if r['frame']==f);raw=Path(s['path']).read_bytes();assert sha(raw)==s['sha256']and s['read_only_export'];values.append(dict(funds=funds(a,raw),fleet=fleet_models(a,raw,1)))
  assert values[0]==values[1]and values[0]['funds']==25975 and len(values[0]['fleet'])==5;states.append(dict(frame=f,funds=25975,five_ship_models_equal_historical_control=True))
 source_row=next(r for r in obs['rows']if r['source_request']['ID']==1266);logical=[];research=Path('work/analysis/refit_spritsail_payload_v2278/ARM9_RESEARCH_ONLY.bin').read_bytes();assert arm[:0x133234]==research[:0x133234]and arm[0x133240:]==research[0x133240:]
 for sample in read('work/analysis/refit_spoken_layouts_v2280c/native_font_proof.json')['complete_native_font_planes']:
  row=sample['case'];text=bytes.fromhex(row['formatted_hex']);proof=probe(research,source_row,text);assert proof['complete']and proof['logical_row_origins']==list(range(0,12*len(row['lines']),12));logical.append(dict(message_ID=row['message_id'],number=row['number'],formatted_hex=text.hex(),native_production_control=proof))
 assert len(logical)==26
 save(ROOT/'actual_and_logical_proof.json',dict(candidate=str(rompath),candidate_sha256=sha(rompath.read_bytes()),actual_report=receipt,historical_reference_report=oldreceipt,all23_current_help_holds=actual,current_distinct_help_IDs=sorted(set(HINTS.values())),all13_actual_snapshot_full_native_returns=returns,first_final_glyph_presence_controls=controls,native_background_all14112_visible_pixels_have_agreeing_unoccluded_witnesses=True,whole62_frame_historical_identity=[dict(frame=f,equal=shots[f].tobytes()==oldshots[f].tobytes())for f in shots],six_paired_fleet_and_funds_controls=states,spoken26_current_logical_native_fonts=logical,logical_view=[228,48],logical_metrics=[6,12],physical16pitch_oracle_separate=True,actual_help_internal_height108_visible_crop84=True,inherited_five_ship_test_battery_not_earned_progress=True,no_new_RAM_fixture_no_savestate=True,no_current_helper_discount_rename_visit_claim=True,last_request1278_on_cancel_dialogue_is_not_a_HELP_payload_or_credit=True,actual_sheets=sheets,all_visual_review_pending=True,revised_spritsail_gameplay_and_registered_release_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(current_help_holds=23,distinct_help_IDs=13,actual_native_returns=13,spoken_logical_fonts=26,sheets=len(sheets)),flush=True)
