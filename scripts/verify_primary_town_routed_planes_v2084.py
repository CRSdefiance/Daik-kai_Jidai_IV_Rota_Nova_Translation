"""Fresh native planes for every source-bound corrected route output."""
import inspect
from pathlib import Path
from scripts.verify_common_alignment_native_v257 import raster as original
from scripts.verify_shipyard_gameplay_v760 import independent_font as original_independent
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/town_services_routed_planes_v2084')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 routes_path=Path('work/analysis/town_services_research_routes_v2083/research_runtime_all84_original_BL_routes.json');routes=read(routes_path)
 prior_path=Path('work/analysis/town_services_native_formatter_v2067/all84_explicit_native_formatter_and_228x48_planes.json');prior=read(prior_path)
 plan=read('work/analysis/town_services_runtime_v2080/runtime_plan.json');arm=Path(plan['research_ARM9']).read_bytes();assert routes['ARM9_sha256']==sha(arm)and not routes['errors']
 rom=NdsImage.open('out/all_routes_combined_v2047_candidate.nds')
 class Font:
  @staticmethod
  def open(path):return rom
 source=inspect.getsource(original);needle='struct.pack("<2I", 6, 16)';assert source.count(needle)==1
 source=source.replace(needle,'struct.pack("<2I", 6, 12)');env={**original.__globals__,'NdsImage':Font};exec(compile(source,__file__,'exec'),env);raster=env['raster']
 other=inspect.getsource(original_independent);assert other.count('228 * 64')==1 and other.count('row * 16')==2
 other=other.replace('228 * 64','228 * 48').replace('row * 16','row * 12');env2=dict(original_independent.__globals__);exec(compile(other,__file__,'exec'),env2)
 output={(r['message_ID'],tuple(r['supplied_arguments'])):r['research_output_hex']for r in routes['cases']};assert len(output)==122
 bindings=[]
 for row in prior['native_font_planes']:
  key=(row['message_ID'],tuple(row['supplied_arguments']));assert output[key]==row['formatted_hex']
  events=[];plane=raster(arm,bytes.fromhex(output[key]),0x01FFCE40-0x02000000,size=(228,48),instruction_limit=2000000,glyph_events=events)
  assert plane==env2['independent_font'](arm,rom.read_file('/GRP/KANJI.FNT'),row['lines'])and sha(plane)==row['native_font_plane_sha256']
  codes=[int.from_bytes(c.encode('cp932'),'big')for c in ''.join(row['lines'])if c!=' '];assert [e['code']for e in events if e['code']!=32]==codes
  assert all(0<=e['x']and e['x']+(12 if e['code']>255 else 6)<=228 and 0<=e['y']and e['y']+12<=48 for e in events)
  bindings.append(dict(message_ID=key[0],supplied_arguments=list(key[1]),formatted_hex=output[key],lines=row['lines'],native_plane_sha256=sha(plane),all_ordered_glyph_events=events,fresh_native_independent_pixel_equality=True,first_last_glyph_bounds_and_single_panel_pass=True,findings=row['findings'],source_preview=row['preview'],source_preview_sha256=row['preview_sha256']))
 assert len(bindings)==122
 save(ROOT/'all122_original_route_native_planes.json',dict(ARM9_sha256=sha(arm),routes=str(routes_path),routes_sha256=sha(routes_path.read_bytes()),prior_prospective_planes=str(prior_path),prior_sha256=sha(prior_path.read_bytes()),planes=bindings,native_count=122,geometry_actor_source='work/analysis/town_services_consumer_audit_v2064b/actual_eight_consumers_four12pixel_rows_and_numeric_scope.json',geometry_modal_source='work/analysis/town_services_modal_geometry_v2076c/83_84_mode_zero_and_shared_native_bitmap_geometry.json',effective_raster_sha256=sha(source.encode()),effective_independent_sha256=sha(other.encode()),producer_sha256=sha(Path(__file__).read_bytes()),repack_gameplay_registration_and_individual_style_decisions_pending=True,full_goal_complete=False))
 print(dict(fresh_native_planes=122,all_equal_independent_and_original_previews=True,style_cases=sum(bool(r['findings'])for r in bindings)),flush=True)
