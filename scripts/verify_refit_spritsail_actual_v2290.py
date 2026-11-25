"""Actual revised help/caption, complete native calls and eight startup controls."""
from pathlib import Path
import struct
from PIL import Image,ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_PC,UC_ARM_REG_SP
from scripts.probe_primary_town_glyph_pitch_v2062b import REGS
from scripts.verify_production_compact_capacity_v2138 import captured_machine
from scripts.finish_refit_display_v712 import HINTS,WHITE,load
from scripts.verify_full_fleet_battle_v652 import fleet_models
from scripts.verify_full_fleet_victory_v654 import funds
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.refit_help import compile_paragraph
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
ROOT=Path('work/analysis/refit_spritsail_actual_verification_v2290');CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);rompath=Path('out/all_routes_combined_v2284_candidate.nds');rom=NdsImage.open(rompath);digest=sha(rompath.read_bytes());arm=rom.read_file('/__arm9__.bin');font=GameAsciiFont.from_arm9(arm);rpt,shots,receipt=load(CAP/'refit_spritsail_v2287_refit_V2284',digest,17401);assert read('work/analysis/refit_spritsail_runs_v2287/refit_terminal.json')['terminal'];obsfile=CAP/'refit_spritsail_v2287_refit_V2284/refit_observer/requests.json';obs=read(obsfile);assert not obs['errors']and not obs['mismatches']and obs['all_host_slots_restored_and_core_file_exact']
 doc=read('translations/refit_contextual_editorial_manuscript_v2.json');rows={r['message_id']:r for r in doc['records']};native=[]
 for label in(1280,1268,'ARM9_REFIT_SPRITSAIL_LABEL'):
  row=next(r for r in obs['rows']if r['source_request']['ID']==label and(r['direct_help_payload_match']if isinstance(label,int)else r['direct_aux_label']));text=bytes.fromhex(row['text_hex']);assert text==(compile_paragraph(rows[label]['english'])[0][:-1]if isinstance(label,int)else b'Spritsail');assert row['bounds']==[0,0,168,108]
  cpu=captured_machine(arm,row);ctx=row['registers'][0];parent=row['registers'][8];header=parent+0x1C38;assert struct.unpack('<3I',cpu.mem_read(header,12))==(4,42,108);pixels=(header+struct.unpack('<I',cpu.mem_read(header+16,4))[0])&0xffffffff;packed=bytes(cpu.mem_read(pixels,9072));initial=bytes(v for b in packed for v in(b&15,b>>4));expected=bytearray(initial)
  if isinstance(label,int):assert not any(initial);lines=compile_paragraph(rows[label]['english'])[1];origin_y=0
  else:assert struct.unpack('<2I',cpu.mem_read(ctx+0x24,8))==(0,72)and not any(initial[60*168:]);lines=['Spritsail'];origin_y=72
  for y,line in enumerate(lines):
   for i,char in enumerate(line):
    glyph=font.decode(char)
    for gy in range(11):
     for gx in range(6):
      if glyph.getpixel((gx,gy)):expected[(origin_y+y*12+gy)*168+i*6+gx]=1
  sp=cpu.reg_read(UC_ARM_REG_SP);saved=[cpu.reg_read(REGS[i])for i in range(4,12)];cpu.emu_start(row['PC'],row['LR'],count=2000000);assert cpu.reg_read(UC_ARM_REG_PC)==row['LR']and cpu.reg_read(UC_ARM_REG_R0)==row['font_input_pointer']+len(text)and sp==cpu.reg_read(UC_ARM_REG_SP)and saved==[cpu.reg_read(REGS[i])for i in range(4,12)]
  after=bytes(cpu.mem_read(pixels,9072));plane=bytes(v for b in after for v in(b&15,b>>4));assert plane==expected and bytes(cpu.mem_read(row['font_input_pointer'],len(text)+1))==text+b'\0'
  native.append(dict(ID=label,frame=row['frame'],complete_native_return=True,full168x108_plane_equal_independent_font=True,full_plane_sha256=sha(plane),original_bounds_and_metrics_not_changed=True,SP_callee_saved_and_input_preserved=True,heading_native_y72_projected_separately_to_UI_y40=origin_y==72,all_native_glyph_and_font_instructions_unstubbed=True))
 baseline,oldshots,oldreceipt=load(CAP/'refit_actual_v2276_V2171','4df01b870562dc04d623fb5c0011d38100bc4062371d32ad2be12f352292260a',20601);background=Image.new('RGB',(168,84))
 for y in range(84):
  for x in range(168):
   colours={oldshots[f].getpixel((64+x,80+y))for f in HINTS if oldshots[f].getpixel((64+x,80+y))!=WHITE};assert len(colours)==1;background.putpixel((x,y),colours.pop())
 actual=[]
 for frame,n in((14000,1280),(14300,1268)):
  _,lines=compile_paragraph(rows[n]['english']);expected=background.copy();ink=set()
  for y,line in enumerate(lines):
   for i,char in enumerate(line):
    glyph=font.decode(char)
    for gy in range(11):
     for gx in range(6):
      if glyph.getpixel((gx,gy)):point=(i*6+gx,y*12+gy);expected.putpixel(point,WHITE);ink.add(point)
   assert all(any(i*6<=x<(i+1)*6 and y*12<=yy<y*12+11 for x,yy in ink)for i in(0,len(line)-1))
  assert shots[frame].crop((64,80,232,164)).tobytes()==expected.tobytes();actual.append(dict(frame=frame,message_ID=n,lines=lines,all_complete_foreground_first_final_glyphs_and_blank_background_equal=True,all_body_rows_start_x64_without_clipping=True))
 heading={(64+i*6+x,40+y)for i,c in enumerate('Spritsail')for y in range(11)for x in range(6)if font.decode(c).getpixel((x,y))};observed={(x,y)for y in range(40,52)for x in range(64,232)if shots[14300].getpixel((x,y))==WHITE};assert observed==heading
 startup=[];startup_images=[]
 for mode,folder,frames,ref_folder,ref_frames,selected in [('newgame','refit_spritsail_v2287_newgame_V2284',4001,'town_trade_port_v2171_newgame',4000,[1,60,180,1600,2000,3200,4000]),('title','refit_spritsail_v2289_title',1150,'town_trade_port_v2171_title',1150,[1100])]:
  current,images,currentreceipt=load(CAP/folder,digest,frames);old,oldimages,reference=load(CAP/ref_folder,'4df01b870562dc04d623fb5c0011d38100bc4062371d32ad2be12f352292260a',ref_frames);assert current['scripted_input_schedule']==old['scripted_input_schedule']and current['core_options']==old['core_options']and not current.get('battery_save_preloaded')and not any(v for k,v in current.items()if k.startswith('synthetic_'))
  for f in selected:assert images[f].tobytes()==oldimages[f].tobytes();startup.append(dict(mode=mode,frame=f,current=currentreceipt,reference=reference,full_two_screen_RGB_equal_to_V2171=True));startup_images.append((f'{mode} {f}',images[f]))
 states=[]
 for f in(3200,11900,14000,14300):
  snapshot=next(r for r in rpt['read_only_capture_RAM_snapshots']if r['frame']==f);raw=Path(snapshot['path']).read_bytes();assert sha(raw)==snapshot['sha256'];money=funds(arm,raw);fleet=fleet_models(arm,raw,1);assert money==25975 and len(fleet)==5;states.append(dict(frame=f,funds=money,fleet=fleet))
 assert all(s['fleet']==states[0]['fleet']for s in states)
 selected=[(f'refit {f}',shots[f])for f in(3200,11900,14000,14300)]+startup_images;sheet=Image.new('RGB',(1024,1236),'#263238');draw=ImageDraw.Draw(sheet)
 for i,(label,image)in enumerate(selected):x,y=i%4*256,i//4*412;draw.text((x+4,y+4),'V2284 '+label,fill='white');sheet.paste(image,(x,y+28))
 p=ROOT/'revised_help_caption_and_startup_sheet.png';sheet.save(p)
 save(ROOT/'actual_revised_help_caption_and_startup.json',dict(candidate=str(rompath),candidate_sha256=digest,actual_report=receipt,baseline_background_reference=oldreceipt,observer=str(obsfile),observer_sha256=sha(obsfile.read_bytes()),all3_actual_native_returns=native,actual_revised_help_holds=actual,actual_auxiliary_caption_complete_foreground_and_blank_ink_equal=True,heading_native_y72_UI_y40_distinct_from_body_UI_y80=True,all8_title_NewGame_full_frame_controls=startup,four_current_fleet_and_funds_controls=states,current_five_ship_battery_is_inherited_test_context_not_earned_progress=True,no_new_RAM_code_gameplay_fixture_or_savestate=True,initial_test_declined_cancellation_so_normal_exit_is_separate_pending=True,extra_newgame4001_and_refit17401_terminal_images_retained=True,review_sheet=str(p),review_sheet_sha256=sha(p.read_bytes()),visual_review_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(actual_revised_IDs=[1268,1280],actual_auxiliary_label=True,complete_native_calls=3,startup_fullframe_controls=8,normal_exit_pending=True))
