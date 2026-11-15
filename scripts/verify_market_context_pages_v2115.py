"""Complete native town text pages at screenshot-calibrated 16-pixel pitch."""
from pathlib import Path
import inspect
from PIL import Image,ImageDraw
from scripts.primary_town_native_font_v2102 import font_tools,glyph_codes
from scripts.verify_shipyard_gameplay_v760 import independent_font as original_independent
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/market_context_pages_v2115')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 rom=NdsImage.open('out/all_routes_combined_v2097_candidate.nds');arm=rom.read_file('/__arm9__.bin');kanji=rom.read_file('/GRP/KANJI.FNT');raster,unused,meta=font_tools(rom)
 code=inspect.getsource(original_independent);assert code.count('x = 6')==1 and code.count('228 * 64')==1
 code=code.replace('def independent_font(arm, kanji, lines):','def independent_font(arm, kanji, lines, row_indents):').replace('x = 6','x = row_indents[row]').replace('228 * 64','228 * 48');env=dict(original_independent.__globals__);exec(compile(code,__file__,'exec'),env);independent=env['independent_font']
 from dk4tool.patch.primary_town_services_reference_v2 import current_entries
 from ndspy.code import MainCodeFile
 from scripts.probe_button_prompt_native import machine,BASE,STACK
 from scripts.prepare_product_pitches_v747 import native_layout
 import struct
 entries=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm)
 doc=read('translations/market_contextual_editorial_manuscript_v1.json');cpu=machine(arm);sections=MainCodeFile(arm,BASE).sections;cpu.mem_write(0x02387A20,bytes(sections[3].data[:-48]))
 jobs=[]
 for r in doc['records']:
  n=r['message_id'];raw=entries[n].text
  values=[("Governor's Office",),("Palace",)]if n==761 else[()]
  for args in values:
   cpu.mem_write(STACK+0x27C,struct.pack('<I',0x02118480))
   formatted,lines=native_layout(cpu,raw,n,args,0x02053DB8 if 754<=n<=760 else 0x02054014)
   jobs.append(dict(kind='retained-market',message_ID=n,supplied_arguments=list(args),formatted_hex=formatted.hex()))
 results=[];review=[]
 for number,row in enumerate(jobs):
  text=bytes.fromhex(row['formatted_hex']);position=0;pages=[];all_codes=[]
  while position<len(text):
   remaining=text[position:];events=[];plane,consumed=raster(arm,remaining,0x01FFCE40-0x02000000,size=(228,48),complete=False,instruction_limit=2000000,glyph_events=events)
   assert 0<consumed<=len(remaining);part=remaining[:consumed];codes=[e['code']for e in events if e['code']!=32];assert codes==glyph_codes(part),(row,position,consumed)
   assert codes and all(0<=e['x']and e['x']+(12 if e['code']>255 else 6)<=228 and 0<=e['y']and e['y']+12<=48 for e in events)
   raw_lines=part.split(b'\n')
   while raw_lines and not raw_lines[-1].strip():raw_lines.pop()
   assert 1<=len(raw_lines)<=3 and all(line.strip()for line in raw_lines)
   leading=[len(line)-len(line.lstrip(b' '))for line in raw_lines];assert leading[0]in(1,2)and all(n==2 for n in leading[1:]);indents=[6*(n-(1 if i or n==2 else 0))for i,n in enumerate(leading)];assert all(n==6 for n in indents)
   lines=[line.strip().decode('cp932')for line in raw_lines];expected=independent(arm,kanji,lines,indents);assert plane==expected,(row,position,lines,indents)
   if position+consumed<len(text):assert part.endswith(b'\n')and remaining[consumed:].lstrip(b' ')and not remaining[consumed:].startswith(b'\n')
   path=ROOT/f'case_{number:03d}_page_{len(pages)}.png';Image.frombytes('L',(228,48),bytes(0 if p else 255 for p in plane)).save(path)
   pages.append(dict(input_offset=position,consumed_bytes=consumed,remaining_after=len(text)-position-consumed,lines=lines,indents=indents,native_origins=sorted({e['y']for e in events}),ordered_glyphs=events,full_native_independent_ink_shadow_pixels_equal=True,preview=str(path),preview_sha256=sha(path.read_bytes()),plane_sha256=sha(plane),complete_leading_trailing_letters_bounds_and_no_blank_page=True))
   all_codes+=codes;position+=consumed;assert len(pages)<=3
  assert all_codes==glyph_codes(text)and position==len(text)
  results.append(dict(**row,pages=pages,page_count=len(pages),entire_native_input_consumed_without_missing_glyphs=True))
  if len(pages)>1:review.append(results[-1])
 assert len(results)==18
 tiles=[(r,p)for r in review for p in r['pages']];sheets=[]
 for start in range(0,len(tiles),20):
  subset=tiles[start:start+20];sheet=Image.new('RGB',(936,120*((len(subset)+1)//2)),'#263238');draw=ImageDraw.Draw(sheet)
  for j,(r,p)in enumerate(subset):
   x,y=j%2*468,j//2*120;draw.text((x+5,y+3),r['kind']+' '+str(r.get('name_hex',r.get('supplied_arguments')))+' / '+str(p['input_offset']),fill='white')
   with Image.open(p['preview'])as image:sheet.paste(image.resize((456,96),Image.Resampling.NEAREST),(x+5,y+22))
  path=ROOT/f'pagination_sheet_{start//20:02d}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
 save(ROOT/'all18_market_native_pages.json',dict(ARM9_sha256=sha(arm),COMMON_sha256=sha(rom.read_file('/COMMON/MESFILE.DK4')),font_model=meta,effective_independent_font_sha256=sha(code.encode()),cases=results,retained_records=17,native_cases=18,total_pages=sum(r['page_count']for r in results),multi_page_cases=len(review),pagination_sheets=sheets,actual_geometry_source='work/analysis/market_context_actual_v2112/live_requests.json',initial_two_native_guards_condensed_by_unchanged_alignment_helper=True,all_native_font_painters_unstubbed=True,old12pixel_row_capacity_and_single_panel_claims_superseded=True,actual_zero_share_762_pagination_not_claimed=True,no_ROM_or_registered_release_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(cases=18,pages=sum(r['page_count']for r in results),multi_page=len(review),sheets=len(sheets)))
