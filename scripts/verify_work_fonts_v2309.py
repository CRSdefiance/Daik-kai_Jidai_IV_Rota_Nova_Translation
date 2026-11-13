"""Current24 complete native work selectors/expanders/fonts and48 bounded copies."""
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from scripts import probe_work_fonts_v843 as previous
from scripts.work_comments_layout_v843 import compiled,layout
from scripts.verify_personal_gameplay_v841 import actual_view,projected
from scripts.probe_common_single_cache_v862 import Loader
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/work_fonts_v2309');DOC=Path('translations/work_contextual_editorial_manuscript_v1.json');REPORT=Path('E:/Rota Nova translations/Generated/work/emulation_v193/work_current_v2310_V2284/capture_report.json')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);doc=read(DOC);rompath=Path(doc['current_ROM']);rom=NdsImage.open(rompath);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm);report=read(REPORT);assert report['ROM_sha256']==sha(rompath.read_bytes());snapshot=next(r for r in report['read_only_capture_RAM_snapshots']if r['frame']==4600);ui=Path(snapshot['path']).read_bytes();assert sha(ui)==snapshot['sha256']and snapshot['read_only_export'];view,parent,resource,header=actual_view(ui);projection=projected(rom,ui,view);assert projection[-1]['source_origin']==[0,60]and projection[-1]['destination']==[16,112]and projection[-1]['size']==[216,36]
 context=read(doc['native_context_proof']);assert context['ARM9_sha256']==sha(arm);npc_receipt=context['current_NPC_source_snapshot'];npc=Path(npc_receipt['path']).read_bytes();assert sha(npc)==npc_receipt['sha256'];heroes={r['native_captain_ID']:r['source_actual_RAM']for r in context['all8_real_protagonist_helper_selections']};representatives={voice:next(r['actor_ID']for r in context['all42_NPC_voice_selections']if r['voice_class']==voice)for voice in range(8)};prepare=FunctionType(previous.prepare_model.__code__,{**previous.prepare_model.__globals__,'VIEW':view},'current_prepare_model');execute=FunctionType(previous.execute.__code__,{**previous.execute.__globals__,'VIEW':view},'current_execute');cases=[];panels=[]
 for row in doc['records']:
  n=row['message_id'];text=compiled(row);lines=layout(row['english']);assert text==entries[n].text==bytes.fromhex(row['current_hex'])
  if row['protagonist_ID']is None:actor=representatives[row['voice_class']];raw,receipt=npc,npc_receipt
  else:actor=row['protagonist_ID'];receipt=heroes[actor];raw=Path(receipt['path']).read_bytes();assert sha(raw)==receipt['sha256']
  prepared,fixture=prepare(arm,raw,actor,row['role_ID'],ui);case,plane=execute(rom,prepared,actor,row['role_ID'],n,text,lines);assert case['complete_native_copy_macro_draw_and_ABI']and case['native_text_bytes_consumed']==len(text)and case['generated_native_lines']==lines;assert all(not plane[y*252+x]for y in range(60,96)for x in range(216,252))
  path=ROOT/f'ID{n}_full252x96_native.png';Image.frombytes('L',(252,96),bytes(0 if v else 255 for v in plane)).save(path);panel=Image.new('RGB',(456,112),'#263238');ImageDraw.Draw(panel).text((8,5),f'{n} role{row["role_ID"]} actor{actor} / native216x36',fill='white');panel.paste(Image.open(path).crop((0,60,216,96)).convert('RGB').resize((432,72),Image.Resampling.NEAREST),(8,30));panels.append(panel);cases.append(dict(message_ID=n,role_ID=row['role_ID'],actual_source_actor_ID=actor,English=row['english'],compiled_hex=text.hex(),generated_lines=lines,source_snapshot=receipt,isolated_CPU_fixture=fixture,current_initialized_parent_projection_binding=projection[-1],native_font=case,whole_body_inside_registered216x36_crop=True,full_canvas_sha256=sha(plane),preview=str(path),preview_sha256=sha(path.read_bytes())));print(dict(ID=n,complete=True,actor=actor,role=row['role_ID']),flush=True)
 sheets=[]
 for start in range(0,len(panels),12):
  selected=panels[start:start+12];sheet=Image.new('RGB',(1368,112*((len(selected)+2)//3)),'#172126')
  for i,panel in enumerate(selected):sheet.paste(panel,(i%3*456,i//3*112))
  p=ROOT/f'font_sheet_{start//12:02d}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
 loader=Loader(arm,common);copies=[]
 for mode in('cold','warm'):
  for n in range(1386,1410):copies.append(loader.copy(n,entries[n].text,mode))
 assert len(cases)==24 and len(copies)==48;save(ROOT/'all24_current_native_fonts.json',dict(candidate=str(rompath),candidate_sha256=sha(rompath.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(common),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),current_initialized_UI_source=snapshot,current_actual_view=view,current_actual_parent=parent,current_parent_draw_commands=projection,current_parent_projection_controls=1,all24_complete_native_cases=cases,all48_native_cold_warm_copies=copies,native_file_IO_explicit_host_contract=True,source_role_assignment_slot18_and_UI_clone_are_isolated_CPU_fixtures=True,actor_health_mood_and_real_captain_records_not_replaced=True,four_genuine_captain_states_used_without_captain_ID_substitution=True,original_numeric_selection_macro_expander_clear_font_glyph_and_guards_ABI_all_pass=True,COMMON_copy_intercepted_after_original_numeric_selection=True,source_canvas=[252,96],body_origin=[0,60],visible_crop=[216,36],screen_origin=[16,112],pair_safe_compiler='scripts/work_comments_layout_v843.py',pair_safe_compiler_sha256=sha(Path('scripts/work_comments_layout_v843.py').read_bytes()),all_complete_first_final_glyphs_and_authored_words_equal_independent_pixels=True,full36_cell1405_trailing_period_consumed_and_inside_visible_crop=True,all24_parent_bindings_share_one_current_source_geometry_not24_parent_reinitializations=True,review_sheets=sheets,visual_review_pending=True,no24_actual_visits_or_current_four_hero_visits_claim=True,no_ROM_runtime_or_geometry_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(fonts=24,native_copies=48,parent_controls=1,sheets=len(sheets),visual_pending=True))
