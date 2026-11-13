"""Receipt-name native planes and contact sheet for ten remaining style cases."""
import inspect,struct
from pathlib import Path
from PIL import Image,ImageDraw
from scripts.verify_common_alignment_native_v257 import raster as original
from scripts.verify_shipyard_gameplay_v760 import independent_font as original_independent
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
from dk4tool.dialogue.font_audit import SJIS_MAP_OFFSET,SJIS_GLYPH_COUNT
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/town_services_visual_v2090')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 plan=read('work/analysis/town_services_runtime_v2080/runtime_plan.json');arm=Path(plan['research_ARM9']).read_bytes();rom=NdsImage.open('out/all_routes_combined_v2047_candidate.nds')
 class Font:
  @staticmethod
  def open(path):return rom
 source=inspect.getsource(original).replace('struct.pack("<2I", 6, 16)','struct.pack("<2I", 6, 12)');env={**original.__globals__,'NdsImage':Font};exec(compile(source,__file__,'exec'),env)
 other=inspect.getsource(original_independent).replace('228 * 64','228 * 48').replace('row * 16','row * 12');env2=dict(original_independent.__globals__);exec(compile(other,__file__,'exec'),env2)
 names=read('work/analysis/town_services_receipt_names_v2089/all36_original_caller_native_printf_and_modal_names.json');native=[];unsupported=[];mapping=struct.unpack_from(f'<{SJIS_GLYPH_COUNT}H',arm,SJIS_MAP_OFFSET);assert mapping==struct.unpack_from(f'<{SJIS_GLYPH_COUNT}H',rom.read_file('/__arm9__.bin'),SJIS_MAP_OFFSET)
 for row in names['cases']:
  name=bytes.fromhex(row['name_hex']);missing=[];pos=0
  while pos<len(name):
   wide=0x81<=name[pos]<=0x9F or 0xE0<=name[pos]<=0xFC;code=int.from_bytes(name[pos:pos+(2 if wide else 1)],'big');pos+=2 if wide else 1
   if wide and code not in mapping:missing.append(code)
  if missing:
   unsupported.append(dict(name_hex=row['name_hex'],amount=row['amount'],raw_missing_font_codes=sorted(set(missing)),byte_preservation_verified_by_original_caller_proof=True,pixels_not_approved_for_unsupported_stress_character=True,original_font_catalog_unchanged=True));continue
  events=[];plane=env['raster'](arm,bytes.fromhex(row['formatted_hex']),0x01FFCE40-0x02000000,size=(228,48),instruction_limit=2000000,glyph_events=events)
  assert plane==env2['independent_font'](arm,rom.read_file('/GRP/KANJI.FNT'),row['lines'])
  assert all(0<=e['x']and e['x']+(12 if e['code']>255 else 6)<=228 and 0<=e['y']and e['y']+12<=48 for e in events)
  raw=bytes.fromhex(row['formatted_hex']);codes=[];i=0
  while i<len(raw):
   b=raw[i];wide=0x81<=b<=0x9F or 0xE0<=b<=0xFC;code=int.from_bytes(raw[i:i+(2 if wide else 1)],'big');i+=2 if wide else 1
   if code not in(10,32):codes.append(code)
  assert [e['code']for e in events if e['code']!=32]==codes
  native.append(dict(name_hex=row['name_hex'],amount=row['amount'],formatted_hex=row['formatted_hex'],native_plane_sha256=sha(plane),ordered_glyphs=events,all_native_independent_pixels_and_complete_glyphs_bounds=True))
 fonts=read('work/analysis/town_services_routed_planes_v2084/all122_original_route_native_planes.json');style=[r for r in fonts['planes']if r['findings']];assert len(style)==10
 sheet=Image.new('RGB',(936,600),'#263238');draw=ImageDraw.Draw(sheet)
 for j,row in enumerate(style):
  x,y=j%2*468,j//2*120;draw.text((x+5,y+3),str(row['message_ID'])+' '+str(row['supplied_arguments']),fill='white')
  with Image.open(row['source_preview'])as picture:sheet.paste(picture.resize((456,96),Image.Resampling.NEAREST),(x+5,y+22))
 path=ROOT/'ten_style_cases.png';sheet.save(path)
 save(ROOT/'name_native_planes_and_style_sheet.json',dict(ARM9_sha256=sha(arm),native_name_plane_count=len(native),name_planes=native,unsupported_stress_cases=unsupported,unsupported_font_glyphs_not_waived=True,style_cases=style,style_sheet=str(path),style_sheet_sha256=sha(path.read_bytes()),style_decisions_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(native_name_planes=len(native),style_cases=10,sheet=str(path)))
