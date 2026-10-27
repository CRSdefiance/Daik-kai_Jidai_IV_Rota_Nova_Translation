"""Bind current text/fonts to preserved original Search events;no emulator run."""
import struct
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.current_common_native_context_v2620b import CurrentContext
from scripts.probe_fatigue_status_fonts_v1590 import pipeline as fatigue_pipeline
from scripts.probe_inspection_status_fonts_v1574 import pipeline as literal_pipeline,literal_independent
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_fatigue_recovery_actual_v1608 import main_frame
from scripts.verify_dialogue_palette_v628 import PALETTE,resident,captured_rgb
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/fatigue_hot_spring_history_v2626');BASE=0x02000000
OLD={
 'increase':'work/analysis/fatigue_increase_verified_v1598/fixture_free_Search_failure_original_plus3_verified.json',
 'recovery':'work/analysis/fatigue_recovery_verified_v1608/original_friendly_village_recovery10_verified.json',
 'hot':'work/analysis/hot_spring_optional_actual_v1684/original_optional_hot_spring_and_Experience_notice_verified.json',
}
def sheet(path,items,columns=2):
 image=Image.new('RGB',(columns*256,408*((len(items)+columns-1)//columns)),'#263238');draw=ImageDraw.Draw(image)
 for i,r in enumerate(items):
  x,y=i%columns*256,i//columns*408;draw.text((x+3,y+3),f'{r["run"]} frame{r["frame"]}',fill='white')
  with Image.open(r['capture'])as im:image.paste(im.convert('RGB'),(x,y+24))
 image.save(path);return dict(path=str(path),sha256=sha(path.read_bytes()))
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 ctxs={label:CurrentContext('translations/'+family+'_contextual_editorial_manuscript_v1.json','out/all_routes_combined_v'+version+'_candidate.nds',ROOT/(label+'_current_context'))for label,family,version in [('fatigue','fatigue_status','1594'),('hot','hot_spring','1676')]};ctx=ctxs['hot'];arm,common=ctx.arm,ctx.common
 clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');assert resident(arm,PALETTE,32)==resident(clean,PALETTE,32)
 assert resident(arm,0x020548C8,4)==bytes.fromhex('0f20a0e3')and resident(arm,0x020548D4,4)==bytes.fromhex('34208de5')
 palette=struct.unpack('<16H',resident(arm,PALETTE,32));colors={1:captured_rgb(palette[15]),15:captured_rgb(palette[14])};assert colors=={1:(0,8,0),15:(197,198,197)}
 runs={};bindings=[]
 for name,path in OLD.items():
  proof=read(path);audit=proof if name=='increase'else proof['preservation_audit'];rp=Path(audit['terminal_report']);assert sha(Path(proof['candidate']).read_bytes())==proof['candidate_sha256']and sha(rp.read_bytes())==audit['terminal_report_sha256'];report=read(rp)
  assert report['ROM_sha256']==proof['candidate_sha256']and not report['callback_errors']and not report['hardware_device_verification']and not report['goal_complete']
  if name=='increase':assert proof['all_inputs_RAM_PNG_and_unchanged_saves_audited']and proof['no_fixture_or_RNG_state_event_or_message_injection']
  elif name=='recovery':assert audit['all48_coordinate_byte_changes_and_other4MiB_bytes_audited']and audit['all_inputs_snapshots_PNG_hashes_and_unchanged_source_disposable_saves_audited']and audit['fixture_frames']==[5000,5650]and proof['no_health_fatigue_RNG_actor_or_event_result_writes']
  else:assert audit['all48_location20_supply10_crew_owned_bytes_and_all_other4MiB_audited']and audit['all_inputs_snapshots_PNG_hashes_and_unchanged_source_disposable_saves_audited']and audit['source_proven_crew10_fixture_frames']==audit['source_proven_supply20_fixture_frames']==[]and proof['original_optional_branch_passed_without_actor_skill_RNG_or_event_outcome_edits']
  runs[name]=dict(proof=proof,report=report,shots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']},frames={r['frame']:r for r in report['frames_captured']});bindings.append(dict(run=name,proof=path,proof_sha256=sha(Path(path).read_bytes()),report=str(rp),report_sha256=sha(rp.read_bytes()),completed_whole4MiB_input_RNG_donor_audit_hash_bound=True))
 def raw(name,frame):
  row=runs[name]['shots'][frame];data=Path(row['path']).read_bytes();assert len(data)==0x400000 and sha(data)==row['sha256'];return data
 def picture(name,frame):
  row=runs[name]['frames'][frame];assert sha(Path(row['path']).read_bytes())==row['PNG_sha256'];return Image.open(row['path']).convert('RGB')
 owner,modal,speech=[struct.unpack_from('<I',arm,p)[0]-BASE for p in [0x552A0,0x54894,0x54450]]
 def masks_match(screen,pixels):
  return all({(16+i%228,296+i//228)for i,p in enumerate(pixels)if p==index}=={(x,y)for y in range(294,366)for x in range(16,244)if screen.getpixel((x,y))==color}for index,color in colors.items())
 cases=[];negative=[];states=[]
 specs=[('increase',308,3,5500,[5700,5730]),('recovery',309,10,5900,[6050,6080]),('hot',2276,None,None,[8402,8432]),('hot',309,15,8432,[8652,8682]),('hot',2283,None,None,[8902,8932]),('hot',310,None,None,[9152,9182])]
 for name,n,amount,before_frame,frames in specs:
  context=ctxs['fatigue']if name!='hot'else ctxs['hot'];entry=context.entries[n];before=raw(name,before_frame)if before_frame else None
  if amount:native=context.execute(fatigue_pipeline,n,amount,raw=before)
  elif n==310:native=context.execute(literal_pipeline,n,raw=raw(name,frames[0]))
  else:native=context.speak(0x53D44,1,0x02116D80 if n==2276 else 0x02116D60,raw=raw(name,frames[0]))
  formatted=bytes.fromhex(native['formatted_hex']);spoken=n>=2275;pixels=ctx.raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)
  lines=[r.strip().decode('cp932')for r in formatted.split(b'\n')];assert pixels==(independent_font(arm,ctx.rom.read_file('/GRP/KANJI.FNT'),lines)if spoken else literal_independent(arm,ctx.rom.read_file('/GRP/KANJI.FNT'),lines[0]))
  for frame in frames:
   data=raw(name,frame);screen=picture(name,frame);resident_text=data[owner+0x2030:owner+0x2230].split(b'\0')[0];at=speech if spoken else modal;actual=data[at:at+512].split(b'\0')[0];assert resident_text==entry.text and actual==formatted and masks_match(screen,pixels);assert data[PALETTE-BASE:PALETTE-BASE+32]==resident(arm,PALETTE,32)
   cpu,get=get_machine(arm,data);fleet=get(0xCB1A8)+4+132*get(0x2E58C);fatigue=bytes(cpu.mem_read(fleet+0x3D,1))[0];logical=get(0x82478,get(0xCB1A8)+0x2090,1);assert logical==16
   if amount:assert fatigue==native['fatigue_after_original_clamp']and native['fatigue_before']==(6 if name!='hot'else 5)
   if name=='recovery':
    main=main_frame(data);assert struct.unpack_from('<I',data,main-0x4C)[0]==0x020795F4 and struct.unpack_from('<I',data,main-0x6C)[0]==0x02079794 and struct.unpack_from('<I',data,main-0x68)[0]==309
   if name=='hot':
    main=main_frame(data)
    if spoken:
     table=0x02116D80 if n==2276 else 0x02116D60;ret=0x0207933C if n==2276 else 0x02079380;assert struct.unpack_from('<I',data,main-0x3C)[0]==ret and struct.unpack_from('<I',data,main-0x34)[0]==table;assert get(0x53F4C,get(0xCB184)+4+32*logical,table)==n
    elif n==310:assert struct.unpack_from('<I',data,main-0x3C)[0]==0x02079394 and struct.unpack_from('<I',data,main-0x38)[0]==310
    else:assert struct.unpack_from('<I',data,main-0x2C)[0]==0x02079344 and struct.unpack_from('<I',data,main-0x4C)[0]==0x02079794
   row=runs[name]['frames'][frame];cases.append(dict(run=name,frame=frame,message_id=n,source_requested_amount=amount,fatigue_before=native.get('fatigue_before'),fatigue_after=fatigue,actual_logical_role1=logical,capture=row['path'],capture_sha256=row['PNG_sha256'],RAM_sha256=sha(data),current_resident_hex=resident_text.hex(),current_formatted_hex=actual.hex(),native_pipeline=native,complete_native_ink_and_shadow_RGB_masks_equal=True,full_native_plane_sha256=sha(bytes(pixels))))
   states.append(dict(run=name,frame=frame,mode=list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12))),fatigue=fatigue,logical_role1=logical,RAM_sha256=sha(data)))
  # Offline corruptions exercise resident/formatted first bytes, both endpoint glyphs,
  # an interior glyph (digits for numeric statuses) and blank paper.
  screen=picture(name,frames[0]);bad=bytearray(entry.text);bad[0]^=1;negative.append(dict(message_id=n,run=name,kind='resident-first-byte',rejected=bytes(bad)!=entry.text));bad=bytearray(formatted);bad[0]^=1;negative.append(dict(message_id=n,run=name,kind='formatted-first-byte',rejected=bytes(bad)!=formatted))
  ink=[i for i,p in enumerate(pixels)if p==1];assert ink
  targets=[('erase-first-glyph',min(ink,key=lambda i:(i//(228*16),i%228))),('erase-final-glyph',max(ink,key=lambda i:(i//(228*16),i%228))),('erase-interior-letter-or-digit',ink[len(ink)//2])]
  if amount:
   digit=next(i for i,p in enumerate(pixels)if p==1 and i%228>=6*len(entry.text.split(b'%s')[0]));targets.append(('erase-fullwidth-digit',digit))
  for label,index in targets:
   altered=screen.copy();altered.putpixel((16+index%228,296+index//228),(255,255,255));negative.append(dict(message_id=n,run=name,kind=label,rejected=not masks_match(altered,pixels)))
  altered=screen.copy();altered.putpixel((16,359),colors[1]);negative.append(dict(message_id=n,run=name,kind='stray-blank-paper-ink',rejected=not masks_match(altered,pixels)))
 assert len(cases)==12 and len(negative)==39 and all(r['rejected']for r in negative)
 returns=[]
 for name,frame,fatigue in [('increase',5900,9),('recovery',6200,0),('hot',9402,0),('hot',20792,39)]:
  data=raw(name,frame);screen=picture(name,frame);cpu,get=get_machine(arm,data);mode=list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12)));assert mode==[0,0,0];assert bytes(cpu.mem_read(get(0xCB1A8)+4+132*get(0x2E58C)+0x3D,1))[0]==fatigue;row=runs[name]['frames'][frame];returns.append(dict(run=name,frame=frame,mode=mode,fatigue=fatigue,capture=row['path'],capture_sha256=row['PNG_sha256'],RAM_sha256=sha(data),normal_Sea_View_by_original_completed_transition_and_current_view=True))
 flows=sheet(ROOT/'normal_Sea_View_returns.png',returns)
 for label,ids in [('fatigue',[308,309]),('hot',list(range(2275,2288))),('notice',[310])]:
  holds=[r for r in cases if r['message_id']in ids];neg=[r for r in negative if r['message_id']in ids];sheets=[sheet(ROOT/f'{label}_historical_complete_holds.png',holds),flows]
  save(ROOT/f'historical_{label}_current_binding.json',dict(candidate=str(ctx.rompath),candidate_sha256=sha(ctx.rompath.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(common),historical_proof_bindings=bindings,historical_holds=holds,historical_IDs=sorted({r['message_id']for r in holds}),complete_original_Search_exchange_context_only=[r for r in cases if r['message_id']not in ids],historical_normal_returns=returns,all12_original_role_fatigue_mode_and_saved_source_states=states,negative_controls=neg,review_sheets=sheets,completed_whole4MiB_input_RNG_and_donor_audits_hash_bound=True,only_disclosed_location_fixtures_no_crew_supply_fatigue_skill_RNG_or_outcome_forcing=True,fatigue_displays_requested_magnitude_not_postclamp_delta=True,other_hot_voices_native_and_representative_family_coverage_only=True,no_new_current_emulator_runs_or_visits=True,new_current_actual_IDs=[],scope='Historical V1594 fixture-free +3 Search failure and location-only -10 friendly village;V1676 location-only natural hot-spring discovery2276,-15 recovery,optional2283,effect310 and sailing returns. No crew/supply refills in this selected later history. Full prior preservation audits hash-bound;current complete native ink AND source shadow masks freshly checked. No earned travel,other11 individual hot voices,current startup,full-route or hardware claims.',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 save(ROOT/'all16_history_receipt.json',dict(historical_full_holds=12,negative_controls=39,normal_returns=4,all_current_native_and_source_palette_masks_pass=True,all_sheets_pending_current_visual_review=True,full_goal_complete=False));print('12 historical holds,39 corruptions,4normal returns and original saved-source states pass;no new emulator run.')
