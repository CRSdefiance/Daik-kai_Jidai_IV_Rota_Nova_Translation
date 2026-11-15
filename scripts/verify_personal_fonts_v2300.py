"""All25 current Deck selections, expansion, native fonts and parent projections."""
from pathlib import Path
from types import FunctionType
import struct
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from scripts import probe_personal_fonts_v836 as fontprobe
from scripts import verify_personal_projection_v837 as parentprobe
from scripts.verify_personal_gameplay_v841 import actual_view
from scripts.personal_chatter_layout_v837 import compiled,layout
from scripts.probe_common_single_cache_v862 import Loader
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/personal_fonts_v2300');DOC=Path('translations/personal_contextual_editorial_manuscript_v1.json');REPORT=Path('E:/Rota Nova translations/Generated/work/emulation_v193/personal_current_v2301_V2284/capture_report.json')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);doc=read(DOC);rompath=Path(doc['current_ROM']);rom=NdsImage.open(rompath);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm);report=read(REPORT);assert report['ROM_sha256']==sha(rompath.read_bytes())and report['cold_boot']and not report['savestate_loaded'];snapshot=next(r for r in report['read_only_capture_RAM_snapshots']if r['frame']==4600);raw=Path(snapshot['path']).read_bytes();assert sha(raw)==snapshot['sha256']and snapshot['read_only_export'];view,parent,resource,header=actual_view(raw);assert struct.unpack_from('<2I',arm,0x1147B8)==(216,36)
 execute=FunctionType(fontprobe.execute.__code__,{**fontprobe.execute.__globals__,'VIEW':view},'execute_current_personal_font');composition=FunctionType(parentprobe.composition.__code__,{**parentprobe.composition.__globals__,'VIEW':view,'current_entries':current_entries},'current_parent_composition');results=[];panels=[]
 for row in doc['records']:
  n=row['message_id'];text=compiled(row);lines=layout(row['english']);assert text==entries[n].text==bytes.fromhex(row['current_hex']);case,plane=execute(rom,raw,row['actor_ID'],text,lines);assert case['complete_native_copy_macro_draw_and_ABI']and case['native_text_bytes_consumed']==len(text)
  assert all(not plane[y*252+x]for y in range(60,96)for x in range(216,252));projection=composition(rom,raw,text,False,actor=row['actor_ID'],state=1);assert projection['selected_IDs']==[n]and projection['draws'][-1]['source_origin']==[0,60]and projection['draws'][-1]['destination']==[16,112]and projection['draws'][-1]['size']==[216,36]
  path=ROOT/f'ID{n}_full252x96_native.png';Image.frombytes('L',(252,96),bytes(0 if v else 255 for v in plane)).save(path);visible=Image.open(path).crop((0,60,216,96)).convert('RGB');panel=Image.new('RGB',(456,112),'#263238');ImageDraw.Draw(panel).text((8,5),f"{n} {row['speaker']} / retain / native216x36",fill='white');panel.paste(visible.resize((432,72),Image.Resampling.NEAREST),(8,30));panels.append(panel)
  results.append(dict(message_ID=n,actor_ID=row['actor_ID'],English=row['english'],compiled_hex=text.hex(),generated_lines=lines,native_font=case,native_original_parent_projection=projection,complete_body_inside_216x36_visible_crop=True,full_canvas_sha256=sha(plane),preview=str(path),preview_sha256=sha(path.read_bytes())));print(dict(ID=n,complete_font=True,parent_crop=[216,36]),flush=True)
 sheets=[]
 for start in range(0,len(panels),12):
  subset=panels[start:start+12];sheet=Image.new('RGB',(1368,112*((len(subset)+2)//3)),'#172126')
  for i,panel in enumerate(subset):sheet.paste(panel,(i%3*456,i//3*112))
  p=ROOT/f'font_sheet_{start//12:02d}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
 loader=Loader(arm,common);copies=[]
 for mode in('cold','warm'):
  for n in range(1361,1386):copies.append(loader.copy(n,entries[n].text,mode))
 assert len(copies)==50
 save(ROOT/'all25_current_native_fonts_and_projection.json',dict(candidate=str(rompath),candidate_sha256=sha(rompath.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(common),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_current_actual_report=str(REPORT),source_current_actual_report_sha256=sha(REPORT.read_bytes()),genuine_current_snapshot=snapshot,current_actual_view=view,current_actual_parent=parent,all25_complete_native_font_and_parent_cases=results,all50_native_cold_warm_copies=copies,native_file_IO_is_explicit_host_contract=True,full_body_bitmap=[252,96],body_origin=[0,60],original_parent_source_crop=[0,60,216,36],actual_screen_rectangle=[16,112,232,148],current_crop_metadata_unchanged=True,room_type5_header_actor_and_state1_are_declared_CPU_inputs=True,native_COMMON_copy_intercepted_only_after_original_actor_ID_selection=True,original_macro_expansion_clear_fonts_and_glyph_functions_unstubbed=True,parent_SDK_GPU_blit_boundary_intercepted_not_actual25_UI_visits=True,pair_phase_handled_by_frozen_v837_serializer=True,all25_complete_independent_words_first_final_glyphs_guards_and_ABI_pass=True,review_sheets=sheets,visual_review_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(fonts=25,parent_projections=25,native_copies=50,sheets=len(sheets),visual_review_pending=True))
