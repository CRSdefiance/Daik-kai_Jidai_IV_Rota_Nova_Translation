"""All84 prospective paragraphs through current native formatter and font planes.

Calls the existing literal formatter explicitly; production routing is pending.
"""
from pathlib import Path
import inspect
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shipyard_editorial import LITERAL
from dk4tool.rom.nds import NdsImage
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.native_call_abi_v764 import call
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font as original_independent
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/town_services_native_formatter_v2067')
DOC=Path('translations/primary_town_services_contextual_editorial_manuscript_v3.json')
LITERALS=Path('work/analysis/town_services_literals_v2055/all84_original_printf_shared_expander_and_literal_guards.json')
BASE=0x02000000
INPUT,OUTPUT=0x02660000,0x02662000
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 doc,prior=read(DOC),read(LITERALS);assert not prior['failures']and prior['original_native_printf_calls']==488
 assert [r['english']for r in doc['records']]==[r['english']for r in read(prior['manuscript'])['records']]
 rom=NdsImage.open(doc['current_ROM']);arm=rom.read_file('/__arm9__.bin');assert sha(arm)==doc['required_runtime_ARM9_sha256']==prior['ARM9_sha256']
 raw=Path(prior['source_snapshot']['path']).read_bytes();assert sha(raw)==prior['source_snapshot']['sha256'];cpu,get=get_machine(arm,raw)
 class CurrentFont:
  @staticmethod
  def open(path):return rom
 source=inspect.getsource(original_raster);needle='struct.pack("<2I", 6, 16)';assert source.count(needle)==1
 env={**original_raster.__globals__,'NdsImage':CurrentFont};exec(compile(source.replace(needle,'struct.pack("<2I", 6, 12)'),__file__,'exec'),env);raster=env['raster']
 independent_source=inspect.getsource(original_independent);assert independent_source.count('228 * 64')==1 and independent_source.count('row * 16')==2
 independent_source=independent_source.replace('228 * 64','228 * 48').replace('row * 16','row * 12');other=dict(original_independent.__globals__)
 exec(compile(independent_source,__file__,'exec'),other);independent=other['independent_font']
 cases=[];unique={};errors=[]
 for earlier in prior['cases']:
  n=earlier['message_ID'];phase=earlier['alignment'];text=bytes.fromhex(earlier['formatted_hex'])
  try:
   cpu.mem_write(INPUT-16,b'\xa5'*1056);cpu.mem_write(INPUT+phase,text+b'\0');before_input=bytes(cpu.mem_read(INPUT-16,1056))
   cpu.mem_write(OUTPUT-16,b'\xa5'*1056);call(cpu,LITERAL-BASE,(OUTPUT+phase,INPUT+phase,0),instruction_limit=3000000)
   formatted=bytes(cpu.mem_read(OUTPUT+phase,1024)).split(b'\0')[0]
   assert b' '.join(formatted.split())==text
   assert bytes(cpu.mem_read(INPUT-16,1056))==before_input
   assert bytes(cpu.mem_read(OUTPUT-16,16+phase))==b'\xa5'*(16+phase)
   assert bytes(cpu.mem_read(OUTPUT+phase+len(formatted)+1,1024-phase-len(formatted)-1))==b'\xa5'*(1024-phase-len(formatted)-1)
   assert bytes(cpu.mem_read(BASE,len(raw)))==raw
   lines=[line.strip().decode('cp932')for line in formatted.split(b'\n')]
   assert 1<=len(lines)<=4 and all(0<len(s.encode('cp932'))<=35 for s in lines)
   key=(n,tuple(earlier['supplied_arguments']))
   if key in unique:assert unique[key]['formatted_hex']==formatted.hex()
   else:
    events=[];plane=raster(arm,formatted,0x01FFCE40-BASE,size=(228,48),instruction_limit=2000000,glyph_events=events)
    expected=independent(arm,rom.read_file('/GRP/KANJI.FNT'),lines);assert plane==expected,(n,lines)
    codes=[int.from_bytes(c.encode('cp932'),'big')for c in ''.join(lines)if c!=' ']
    assert [e['code']for e in events if e['code']!=32]==codes
    assert all(0<=e['x']and e['x']+(12 if e['code']>255 else 6)<=228 and 0<=e['y']and e['y']+12<=48 for e in events)
    issues=[]
    if len(lines)>1 and len(lines[-1].split())==1:issues.append('isolated-final-word')
    weak=[i for i,line in enumerate(lines[:-1])if line.split()[-1].strip('.,!?;:').lower()in{'a','an','the','to','of','with','for','from','on','in','as','at','and','or'}]
    if weak:issues.append('weak-line-ending')
    p=ROOT/f'plane_{len(unique):03d}_ID{n}_native.png';Image.frombytes('L',(228,48),bytes(0 if x else 255 for x in plane)).save(p)
    unique[key]=dict(message_ID=n,supplied_arguments=earlier['supplied_arguments'],formatted_hex=formatted.hex(),lines=lines,
     full228x48_6x12_native_ink_shadow_plane_equals_independent_font=True,native_font_plane_sha256=sha(plane),all_ordered_glyph_events=events,
     complete_leading_trailing_letters_bounds_whole_words_and_no_extra_page_verified=True,findings=issues,weak_line_end_indices=weak,
     preview=str(p),preview_sha256=sha(p.read_bytes()),explicit_formatter_API_not_production_routing=True)
   cases.append(dict(message_ID=n,alignment=phase,supplied_arguments=earlier['supplied_arguments'],formatted_hex=formatted.hex(),all4MiB_ABI_input_and_output_guards_exact=True))
  except Exception as exc:
   errors.append(dict(message_ID=n,alignment=phase,supplied_arguments=earlier['supplied_arguments'],error=str(exc),type=type(exc).__name__))
 save(ROOT/'partial.json',dict(cases=cases,unique_planes=list(unique.values()),errors=errors,full_goal_complete=False))
 sheets=[];previews=list(unique.values())
 for start in range(0,len(previews),20):
  subset=previews[start:start+20];sheet=Image.new('RGB',(936,120*((len(subset)+1)//2)),'#263238');draw=ImageDraw.Draw(sheet)
  for j,row in enumerate(subset):
   x,y=j%2*468,j//2*120;draw.text((x+5,y+3),f'ID{row["message_ID"]} {row["supplied_arguments"]}',fill='white')
   with Image.open(row['preview'])as p:sheet.paste(p.resize((456,96),Image.Resampling.NEAREST),(x+5,y+22))
  path=ROOT/f'native_review_sheet_{start//20:02d}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
 save(ROOT/'all84_explicit_native_formatter_and_228x48_planes.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(rom.read_file('/COMMON/MESFILE.DK4')),
  prior_printf_macro_proof=str(LITERALS),prior_printf_macro_proof_sha256=sha(LITERALS.read_bytes()),current_ROM=doc['current_ROM'],current_ROM_sha256=doc['current_ROM_sha256'],
  source_snapshot=prior['source_snapshot'],cases=cases,native_font_planes=previews,errors=errors,sheets_for_visual_review=sheets,
  effective_raster_sha256=sha(source.replace(needle,'struct.pack("<2I", 6, 12)').encode()),effective_independent_font_sha256=sha(independent_source.encode()),
  measured_geometry_source='work/analysis/town_services_consumer_audit_v2064b/actual_eight_consumers_four12pixel_rows_and_numeric_scope.json',
  original_native_formatter_shared_macro_and_complete_glyph_painters_execute=True,formatter_called_explicitly_not_a_production_dispatch_proof=True,
  applicable_path_routing_cache_repack_revised_gameplay_and_registered_release_pending=True,all_formatting_gates_remain_false=True,no_ROM_registry_profile_mutation=True,
  producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(native_formatter_calls=len(cases),unique_native_font_planes=len(unique),errors=len(errors),sheets=len(sheets)),flush=True)
 for e in errors[:4]:print(e,flush=True)
 assert not errors and len(cases)==488 and {c['message_ID']for c in cases}=={r['message_id']for r in doc['records']}
