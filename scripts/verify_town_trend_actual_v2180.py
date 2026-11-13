"""Actual revised trend RGB, full native continuations, declared fixtures and transitions."""
from pathlib import Path
from PIL import Image,ImageDraw
from scripts.verify_village_wrap_v608 import read,save
from scripts.primary_town_native_font_v2102 import font_tools,glyph_codes
from scripts.verify_shipyard_gameplay_v760 import independent_font,models
from scripts.verify_market_gameplay_v753 import state
from scripts.native_town_trend_fixture_v2177 import assign
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/town_trend_actual_verification_v2180')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 rompath=Path('out/all_routes_combined_v2171_candidate.nds');rom=NdsImage.open(rompath);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');kanji=rom.read_file('/GRP/KANJI.FNT');raster,_,_=font_tools(rom);entries=current_entries(common,arm);blocks=IlnkContainer.parse(common).blocks
 layout=read('work/analysis/town_trend_balanced_layouts_v2163/all248_revised_product_layouts.json');holds=[];runs=[];frame_sets=[]
 for level,n in((50,655),(150,654)):
  run=Path(f'work/analysis/town_trend_actual_v2178_{level}');cap=CAP/f'town_trend_actual_v2178_{level}_V2171';plan,terminal,report,obs=[read(p)for p in(run/'run_plan.json',run/'terminal.json',cap/'capture_report.json',cap/'common_observer/requests.json')]
  assert terminal['terminal']and terminal['all_observer_host_slots_restored']and report['frames']==6501 and report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']and not obs['errors']and not obs['mismatches']and obs['all_host_slots_restored_and_core_file_exact']
  assert sha(rompath.read_bytes())==plan['candidate_sha256']==report['ROM_sha256'];assert sha(Path(plan['original_genuine_save']).read_bytes())==plan['donor_sha256']=='d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
  assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']and len(report['synthetic_town_trend_fixtures'])==1 and not any(v for k,v in report.items()if k.startswith('synthetic_')and k!='synthetic_town_trend_fixtures')
  assert len(obs['rows'])==1;row=obs['rows'][0];assert row['source_request']['ID']==n and row['bounds']==[0,0,228,48]and row['font_input_offset']in(0,2)
  native=read(f'work/analysis/town_trend_continuations_v2179_{level}/actual_snapshot_native_font_continuations.json')['cases'][0];assert native['message_ID']==n and native['complete_native_return']and native['SP_preserved']and native['callee_registers_preserved']and not native['faults']and not native['error']
  text=bytes.fromhex(row['text_hex']);case=next(x for x in layout['cases']if x['id']==n and x['values_hex']==[b'Olive Oil'.hex()]);assert text.hex()==case['formatted_hex'];events=[];plane=raster(arm,text,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000,glyph_events=events)
  lines=[x.strip().decode('cp932')for x in text.split(b'\n')];assert plane==independent_font(arm,kanji,lines)and[e['code']for e in events if e['code']!=32]==glyph_codes(text)and[e['code']for e in native['glyph_events']if e['code']!=32]==glyph_codes(text)
  assert sorted({x['y']for x in native['glyph_events']})==list(range(0,12*len(lines),12))
  frames={r['frame']:r for r in report['frames_captured']};frame_sets.append(frames);expected={(16+j%228,296+j//228)for j,v in enumerate(plane)if v==1}
  for f in(4600,4800):
   image=Image.open(frames[f]['path']).convert('RGB');assert sha(Path(frames[f]['path']).read_bytes())==frames[f]['PNG_sha256'];actual={(x,y)for y in range(294,360)for x in range(16,244)if image.getpixel((x,y))==(0,8,0)};assert actual==expected,(n,f,len(expected-actual),len(actual-expected))
   holds.append(dict(message_ID=n,font_frame=row['frame'],hold_frame=f,text_hex=text.hex(),lines=lines,capture=frames[f]['path'],capture_sha256=frames[f]['PNG_sha256'],complete_native_actual_independent_foreground_equal=True,logical_row_origins=sorted({x['y']for x in native['glyph_events']})))
  snapshots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']};snapshots.update({r['frame']:r for r in report['read_only_pause_RAM_snapshots']})
  raw=Path(snapshots[3200]['path']).read_bytes();assert sha(raw)==snapshots[3200]['sha256'];after,receipt=assign(arm,raw,dict(level=level,seed=2));assert receipt=={k:v for k,v in report['synthetic_town_trend_fixtures'][0].items()if k!='frame'}and 2<=len(receipt['changes'])<=6
  states=[]
  for f in(3200,4600,6501):
   raw=Path(snapshots[f]['path']).read_bytes();assert sha(raw)==snapshots[f]['sha256'];states.append(dict(frame=f,state=state(arm,raw),models=models(arm,raw),RAM_sha256=sha(raw)))
   if f==4600:
    block=blocks[entries[n].block];assert raw.find(block)>=0 and raw.find(block,raw.find(block)+1)==-1
  assert all(x['state']==states[0]['state']and x['models']==states[0]['models']for x in states)
  journal=read(cap/'navigation_command_journal.json');assert [x['frame']for x in journal['commands_received']]==[3200,6501]and journal['commands_received'][-1]['command']=={'stop':True}and all(x['validation_passed']for x in journal['commands_received'])
  runs.append(dict(level=level,seed=2,message_ID=n,frames=6501,fixture=report['synthetic_town_trend_fixtures'][0],state_model_controls=states,report=str(cap/'capture_report.json'),report_sha256=sha((cap/'capture_report.json').read_bytes()),observer=str(cap/'common_observer/requests.json'),observer_sha256=sha((cap/'common_observer/requests.json').read_bytes()),native_continuation=f'work/analysis/town_trend_continuations_v2179_{level}/actual_snapshot_native_font_continuations.json',resident_complete_common_block_exact=True))
 controls=[]
 for f in frame_sets[0]:
  a,b=[Image.open(q[f]['path']).convert('RGB')for q in frame_sets];scope='whole-frame'
  if f in(4600,4800):
   a.paste((255,0,255),(16,294,244,360));b.paste((255,0,255),(16,294,244,360));scope='every-pixel-outside-revised-body'
  assert a.tobytes()==b.tobytes(),('paired-control',f);controls.append(dict(frame=f,scope=scope,exact_between_two_declared_trend_runs=True))
 sheet=Image.new('RGB',(1024,410),'#263238');draw=ImageDraw.Draw(sheet)
 for i,h in enumerate(holds):draw.text((i*256+4,4),f'ID{h["message_ID"]} frame{h["hold_frame"]}',fill='white');sheet.paste(Image.open(h['capture']).convert('RGB'),(i*256,22))
 p=ROOT/'four_actual_revised_trend_holds.png';sheet.save(p)
 save(ROOT/'actual_revised_trends_and_preservation.json',dict(candidate=str(rompath),candidate_sha256=sha(rompath.read_bytes()),actual_holds=holds,runs=runs,paired_frame_controls=controls,complete_654_655_actual_foreground_and_native_returns=True,production_logical_view=[228,48],production_font_metrics=[6,12],physical_oracle_pitch=16,physical64plane_does_not_define_logical_capacity=True,original_genuine_donor_core_unchanged_and_host_slots_restored=True,no_savestate=True,declared_bounded_trend_and_original_SDK_RNG_fixtures=True,ordinary_trend_creation_not_claimed=True,no_money_inventory_model_or_location_change=True,dialogue_dismissal_and_return_captured=True,only654_655_actual_new_visits_claimed=True,review_sheet=str(p),review_sheet_sha256=sha(p.read_bytes()),visual_review_pending=True,not_full_playthrough_or_hardware_verification=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(actual_holds=len(holds),runs=2,frame_controls=len(controls),state_model_controls=6,sheet=str(p)))
