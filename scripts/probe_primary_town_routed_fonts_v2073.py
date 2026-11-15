"""Bind117 nonmodal research-route outputs to complete228x48 native planes."""
from pathlib import Path
import inspect
from PIL import Image,ImageDraw
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font as original_independent
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/town_services_routed_fonts_v2073')
ROUTES=Path('work/analysis/town_services_research_routes_v2072/research_runtime_all84_original_BL_routes.json')
FONTS=Path('work/analysis/town_services_native_formatter_v2067/all84_explicit_native_formatter_and_228x48_planes.json')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 route,fonts=read(ROUTES),read(FONTS);plan=read(route['runtime_plan']);arm=Path(plan['research_ARM9']).read_bytes();rom=NdsImage.open(fonts['current_ROM']);old=rom.read_file('/__arm9__.bin')
 assert sha(arm)==route['ARM9_sha256']==plan['target_ARM9_sha256']and sha(old)==fonts['ARM9_sha256']
 for lo,hi in((0xD15C8,0xD5B00),(0x125A20,0x1278DC)):assert old[lo:hi]==arm[lo:hi]
 a,b=map(lambda x:MainCodeFile(x,0x02000000),(old,arm));assert all(bytes(a.sections[i].data)==bytes(b.sections[i].data)for i in(1,2,3))
 assert bytes(a.sections[4].data[0xE40:0xEC0])==bytes(b.sections[4].data[0xE40:0xEC0])
 class CurrentFont:
  @staticmethod
  def open(path):return rom
 src=inspect.getsource(original_raster);needle='struct.pack("<2I", 6, 16)';assert src.count(needle)==1
 env={**original_raster.__globals__,'NdsImage':CurrentFont};exec(compile(src.replace(needle,'struct.pack("<2I", 6, 12)'),__file__,'exec'),env);raster=env['raster']
 src2=inspect.getsource(original_independent).replace('228 * 64','228 * 48').replace('row * 16','row * 12');other=dict(original_independent.__globals__);exec(compile(src2,__file__,'exec'),other);independent=other['independent_font']
 baseline={(r['message_ID'],tuple(r['supplied_arguments'])):r for r in fonts['native_font_planes']};unique={};modal=[]
 for case in route['cases']:
  key=case['message_ID'],tuple(case['supplied_arguments'])
  if case['message_ID']in(83,84):modal.append(case);continue
  if key in unique:assert unique[key]['formatted_hex']==case['research_output_hex'];continue
  formatted=bytes.fromhex(case['research_output_hex']);lines=case['research_lines'];assert 1<=len(lines)<=4 and all(len(x.encode('cp932'))<=37 for x in lines)
  inherited=case['research_output_hex']==baseline[key]['formatted_hex']
  if inherited:
   previous=baseline[key];assert sha(Path(previous['preview']).read_bytes())==previous['preview_sha256']
   row=dict(message_ID=case['message_ID'],supplied_arguments=case['supplied_arguments'],formatted_hex=case['research_output_hex'],lines=lines,inherited_exact_formatted_bytes_and_font_runtime=True,
    full_native_plane=previous,native_font_plane_sha256=previous['native_font_plane_sha256'],preview=previous['preview'],preview_sha256=previous['preview_sha256'])
  else:
   events=[];plane=raster(arm,formatted,0x01FFCE40-0x02000000,size=(228,48),instruction_limit=2000000,glyph_events=events)
   assert plane==independent(arm,rom.read_file('/GRP/KANJI.FNT'),lines)
   expected=[int.from_bytes(c.encode('cp932'),'big')for c in ''.join(lines)if c!=' ']
   assert [e['code']for e in events if e['code']!=32]==expected
   assert all(e['x']>=0 and e['x']+(12 if e['code']>255 else 6)<=228 and e['y']>=0 and e['y']+12<=48 for e in events)
   p=ROOT/f'changed_plane_{len([x for x in unique.values()if not x["inherited_exact_formatted_bytes_and_font_runtime"]]):02d}_ID{case["message_ID"]}.png'
   Image.frombytes('L',(228,48),bytes(0 if x else 255 for x in plane)).save(p)
   row=dict(message_ID=case['message_ID'],supplied_arguments=case['supplied_arguments'],formatted_hex=case['research_output_hex'],lines=lines,inherited_exact_formatted_bytes_and_font_runtime=False,
    all_ordered_glyph_events=events,full228x48_native_and_independent_ink_shadow_planes_equal=True,native_font_plane_sha256=sha(plane),preview=str(p),preview_sha256=sha(p.read_bytes()))
  row['formatting_complete']=False
  row['style_findings']=[]
  if len(lines)>1 and len(lines[-1].split())==1:row['style_findings'].append('isolated-final-word')
  if any(x.split()[-1].strip('.,!?;:').lower()in{'a','an','the','to','of','with','for','from','on','in','as','at','and','or'}for x in lines[:-1]):row['style_findings'].append('weak-line-ending')
  unique[key]=row
 assert len(unique)==117 and len(modal)==5
 fresh=[r for r in unique.values()if not r['inherited_exact_formatted_bytes_and_font_runtime']];sheet=Image.new('RGB',(936,120*((len(fresh)+1)//2)),'#263238');draw=ImageDraw.Draw(sheet)
 for j,row in enumerate(fresh):
  x,y=j%2*468,j//2*120;draw.text((x+5,y+3),f'ID{row["message_ID"]} {row["supplied_arguments"]}',fill='white')
  with Image.open(row['preview'])as p:sheet.paste(p.resize((456,96),Image.Resampling.NEAREST),(x+5,y+22))
 p=ROOT/'ten_changed_route_native_planes.png';sheet.save(p)
 save(ROOT/'all117_nonmodal_routed_plane_bindings.json',dict(source_ARM9_sha256=sha(old),target_ARM9_sha256=sha(arm),route_proof=str(ROUTES),route_proof_sha256=sha(ROUTES.read_bytes()),prior_font_proof=str(FONTS),prior_font_proof_sha256=sha(FONTS.read_bytes()),
  cases=list(unique.values()),new_full_native_planes=len(fresh),exact_formatted_and_unchanged_font_runtime_inherited_planes=len(unique)-len(fresh),
  font_renderer_metrics_bitmaps_SJIS_map_ITCM_late123040_and_alignment_helper_exact=True,
  changed_plane_review_sheet=dict(path=str(p),sha256=sha(p.read_bytes())),remaining_modal83_84_cases=modal,
  modal_geometry_and_native_planes_distinct_gate_still_pending=True,style_findings_remain_open=True,all_manuscript_formatting_gates_remain_false=True,
  no_ROM_registry_manuscript_mutation=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(nonmodal_parameter_cases=len(unique),new_native_planes=len(fresh),inherited=len(unique)-len(fresh),modal_cases_pending=len(modal)))
