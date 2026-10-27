"""Complete current native logical font and separate physical glyph-plane samples."""
from pathlib import Path
from PIL import Image,ImageDraw
from scripts.verify_village_wrap_v608 import read,save
from scripts.primary_town_native_font_v2102 import font_tools,glyph_codes
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_production_compact_capacity_v2138 import probe
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/tavern_fonts_v2189');MATRIX=Path('work/analysis/tavern_layouts_v2188/all63_current_native_layouts.json');OBS=Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_trend_actual_v2178_50_V2171/common_observer/requests.json')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);matrix=read(MATRIX);assert matrix['case_count']==67454 and not matrix['findings'];rom=NdsImage.open('out/all_routes_combined_v2171_candidate.nds');arm=rom.read_file('/__arm9__.bin');kanji=rom.read_file('/GRP/KANJI.FNT');assert sha(arm)==matrix['ARM9_sha256'];row=read(OBS)['rows'][0];assert row['source_request']['ID']==655 and row['font_input_offset']==0 and row['bounds']==[0,0,228,48];raster,_,_=font_tools(rom);fonts=[]
 for number,index in enumerate(matrix['representative_full_font_indices']):
  case=matrix['cases'][index];text=bytes.fromhex(case['formatted_hex']);logical=probe(arm,row,text);assert logical['complete']and logical['logical_row_origins']==list(range(0,12*len(case['lines']),12));events=[];plane=raster(arm,text,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000,glyph_events=events);assert plane==independent_font(arm,kanji,case['lines'])and[e['code']for e in events if e['code']!=32]==glyph_codes(text);assert all(0<=e['x']and e['x']+(12 if e['code']>255 else 6)<=228 and 0<=e['y']and e['y']+12<=64 for e in events)
  path=ROOT/f'font_{number:03d}_ID{case["message_ID"]}.png';Image.frombytes('L',(228,64),bytes(0 if v else 255 for v in plane)).save(path);fonts.append(dict(matrix_index=index,message_ID=case['message_ID'],values_hex=case['values_hex'],formatted_hex=text.hex(),lines=case['lines'],native_production_control=logical,physical_native_and_independent_complete_ink_shadow_equal=True,all_ordered_physical_glyphs=events,plane_sha256=sha(plane),preview=str(path),preview_sha256=sha(path.read_bytes())))
  if number%40==0:print(dict(font_index=number,total=len(matrix['representative_full_font_indices'])),flush=True)
 sheets=[]
 for start in range(0,len(fonts),12):
  rows=fonts[start:start+12];sheet=Image.new('RGB',(1404,168*((len(rows)+2)//3)),'#263238');draw=ImageDraw.Draw(sheet)
  for i,r in enumerate(rows):
   x,y=i%3*468,i//3*168;label=f"{r['message_ID']} case{r['matrix_index']} "+' / '.join(bytes.fromhex(v).decode('cp932')for v in r['values_hex']);draw.text((x+4,y+3),label[:73],fill='white');sheet.paste(Image.open(r['preview']).convert('RGB').resize((456,128),Image.Resampling.NEAREST),(x+4,y+25))
  p=ROOT/f'font_sheet_{start//12:02d}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes()),matrix_indices=[r['matrix_index']for r in rows]))
 assert len(fonts)==310 and {r['message_ID']for r in fonts}==set(range(820,883));save(ROOT/'all63_native_font_pagination_and_physical_samples.json',dict(ARM9_sha256=sha(arm),COMMON_sha256=matrix['COMMON_sha256'],matrix=str(MATRIX),matrix_sha256=sha(MATRIX.read_bytes()),all67454_native_layouts_complete=True,full_font_samples=fonts,font_count=len(fonts),all63_message_IDs_covered=True,physical_sheets=sheets,production_logical_view=[228,48],production_metrics=[6,12],all310_single_native_pages_complete=True,physical_oracle_pitch16_not_logical_capacity=True,source_observer=str(OBS),source_observer_sha256=sha(OBS.read_bytes()),native_font_and_glyph_instructions_unstubbed=True,explicit_zero_VRAM_contract_not_live_GPU_state=True,all_sheets_visual_review_and_actual_reconciliation_pending=True,no_ROM_registry_or_patch_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(fonts=len(fonts),sheets=len(sheets),all63_complete=True),flush=True)
