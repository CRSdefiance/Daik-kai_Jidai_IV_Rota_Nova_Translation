"""Full native physical/logical font samples after exact selector ABI preservation."""
from pathlib import Path
from copy import deepcopy
from PIL import Image,ImageDraw
from scripts.verify_village_wrap_v608 import read,save
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.probe_shipyard_runtime_v759 import layout as original_layout
from scripts.primary_town_native_font_v2102 import font_tools,glyph_codes
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_production_compact_capacity_v2138 import probe
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
import inspect
ROOT=Path('work/analysis/town_trade_port_fonts_v2167');PLAN=Path('work/analysis/town_trade_port_payload_v2165/native_payload_plan.json')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);plan=read(PLAN);arm=Path(plan['target_ARM9']).read_bytes();common=Path(plan['target_COMMON']).read_bytes();entries=owned_entries(common,arm,plan['directory_sha256']);old=read('work/analysis/town_trade_port_layouts_v2155b/all_native_typed_product_name_layouts.json');changed=read('work/analysis/town_trend_balanced_layouts_v2163/all248_revised_product_layouts.json');pred=read('work/analysis/town_trend_selector_v2164/all_eight_parent_lowword_fullword_stack_and_R2_ABI.json');assert pred['allR0_toR11_including_R2_and_SP_LR_preserved']and pred['total_cases']==1057968
 alterations={r['original_matrix_index']:r for r in changed['cases']};cases=[]
 for prior in old['cases']:
  r=deepcopy(prior)
  if r['index']in alterations:r.update(alterations[r['index']]);r['output_scope']='fresh-native-execution-v2163'
  else:r['output_scope']='inherited-native-output-after-exhaustive-identical-selector-helper-input-ABI-and-unchanged-postselector-code'
  assert not r['findings'];cases.append(r)
 seen=set();indices=[]
 for r in cases:
  values=[bytes.fromhex(v)for v in r['values_hex']];n=r['message_ID'];name=values[0].hex()if n in(803,804,808)else None;key=(n,len(r['lines']),tuple(len(v.encode('cp932'))%2 for v in r['lines']),any(any(b>=128 for b in v)for v in values),name)
  if key not in seen:seen.add(key);indices.append(r['index'])
 assert len(cases)==32552 and len(alterations)==248;raw=Path(old['source_snapshot']['path']).read_bytes();obs=read('E:/Rota Nova translations/Generated/work/emulation_v193/promoter_context_live_v2144_V2143/common_observer/requests.json');row=obs['rows'][0];assert row['source_request']['ID']==675 and row['font_input_offset']==0
 rom=NdsImage.open('out/all_routes_combined_v2143_candidate.nds');kanji=rom.read_file('/GRP/KANJI.FNT');raster,_,_=font_tools(rom);source=inspect.getsource(original_layout);env=dict(original_layout.__globals__);env['YESNO']=(789,800,802,803,804,806,812,813,816,817,1246);exec(compile(source,__file__,'exec'),env);layout=env['layout'];fonts=[]
 print(dict(full_font_cases=len(indices),all_layout_cases=len(cases)),flush=True)
 for number,index in enumerate(indices):
  r=cases[index];n=r['message_ID'];values=tuple(bytes.fromhex(v)for v in r['values_hex']);cpu,_=get_machine(arm,raw)
  for p in plan['metadata_patches']+plan['runtime_patches']:cpu.mem_write(p['address'],bytes.fromhex(p['target_hex']))
  actual=layout(cpu,entries[n].text,n,values);assert actual['formatted_hex']==r['formatted_hex']and not actual['findings'],(index,n,actual,r)
  text=bytes.fromhex(actual['formatted_hex']);logical=probe(arm,row,text);assert logical['complete']and logical['logical_row_origins']==list(range(0,12*len(r['lines']),12))
  events=[];plane=raster(arm,text,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000,glyph_events=events);assert plane==independent_font(arm,kanji,r['lines'])and[e['code']for e in events if e['code']!=32]==glyph_codes(text)
  assert all(0<=e['x']and e['x']+(12 if e['code']>255 else 6)<=228 and 0<=e['y']and e['y']+12<=64 for e in events)
  path=ROOT/f'font_{number:03d}_ID{n}.png';Image.frombytes('L',(228,64),bytes(0 if v else 255 for v in plane)).save(path);fonts.append(dict(index=index,message_ID=n,values_hex=r['values_hex'],formatted_hex=r['formatted_hex'],lines=r['lines'],fresh_actual_target_native_layout_equal_expected=True,native_production_control=logical,physical_native_independent_full_ink_shadow_equal=True,physical_oracle_pitch16_not_logical_capacity=True,ordered_physical_glyphs=events,plane_sha256=sha(plane),preview=str(path),preview_sha256=sha(path.read_bytes())))
  if number%40==0:print(dict(font_index=number,total=len(indices)),flush=True)
 sheets=[]
 for start in range(0,len(fonts),12):
  rows=fonts[start:start+12];sheet=Image.new('RGB',(1404,168*((len(rows)+2)//3)),'#263238');draw=ImageDraw.Draw(sheet)
  for i,r in enumerate(rows):
   x,y=i%3*468,i//3*168;label=f"{r['message_ID']} case{r['index']} "+' / '.join(bytes.fromhex(v).decode('cp932')for v in r['values_hex']);draw.text((x+4,y+3),label[:73],fill='white');sheet.paste(Image.open(r['preview']).convert('RGB').resize((456,128),Image.Resampling.NEAREST),(x+4,y+25))
  path=ROOT/f'font_sheet_{start//12:02d}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),native_cases=[r['index']for r in rows]))
 save(ROOT/'all_native_layout_inheritance_and_full_font_samples.json',dict(ARM9_sha256=sha(arm),COMMON_sha256=sha(common),payload_plan=str(PLAN),payload_plan_sha256=sha(PLAN.read_bytes()),all32552_layouts=cases,fresh_revised_product_layouts=248,inherited_unchanged_other_layouts=32304,exhaustive_selector_proof='work/analysis/town_trend_selector_v2164/all_eight_parent_lowword_fullword_stack_and_R2_ABI.json',all220_prior_style_findings_resolved_without_English_rewrite=True,full_font_samples=fonts,full_font_count=len(fonts),all60_nonmodal_message_IDs_covered=sorted({r['message_ID']for r in fonts}),physical_sheets=sheets,production_logical_view=[228,48],production_metrics=[6,12],physical_oracle_pitch=16,all_pages_single_complete_native_page=True,distinct267_actual_binding='work/analysis/yard_modal_actual_verification_v2158/actual267_native_geometry_direct_font_and_foreground.json',all61_formatting_gates_still_pending_visual_and_final_release=True,revised_actual_gameplay_not_claimed=True,all_physical_sheets_visual_review_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(fonts=len(fonts),sheets=len(sheets),complete_native_and_independent=True),flush=True)
