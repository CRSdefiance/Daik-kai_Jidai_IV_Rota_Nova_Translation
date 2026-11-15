"""Current Search text/native planes against original failure,forage and loss."""
import struct
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.current_common_native_context_v2620b import CurrentContext
from scripts import search_reports_native_consumers_v1662b as consumers
from scripts.probe_inspection_status_fonts_v1574 import literal_independent
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_search_reports_actual_v1683 import stack_word,number_at
from scripts.verify_dialogue_palette_v628 import PALETTE,resident,captured_rgb
from scripts.rebind_fatigue_hot_spring_history_v2626 import sheet
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/search_reports_history_v2632');BASE=0x02000000
OLD=Path('work/analysis/search_reports_actual_v1683/original_revised_failure_forage_and_loss312_verified.json')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);ctx=CurrentContext('translations/search_reports_contextual_editorial_manuscript_v1.json','out/all_routes_combined_v1676_candidate.nds',ROOT/'current_context');arm,common=ctx.arm,ctx.common;old=read(OLD);audit=old['preservation_audit'];rp=Path(audit['terminal_report']);report=read(rp);assert sha(rp.read_bytes())==audit['terminal_report_sha256']and report['ROM_sha256']==old['candidate_sha256']==sha(Path(old['candidate']).read_bytes());assert report['frames']==20792 and report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']and not report['hardware_device_verification']and not report['goal_complete'];assert audit['all48_location20_supply10_crew_owned_bytes_and_all_other4MiB_audited']and audit['all_inputs_snapshots_PNG_hashes_and_unchanged_source_disposable_saves_audited']and audit['source_proven_crew10_fixture_frames']==audit['source_proven_supply20_fixture_frames']==[]and old['no_actor_identity_skill_fatigue_RNG_event_or_outcome_forcing']
 shots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']};frames={r['frame']:r for r in report['frames_captured']}
 def raw(frame):
  r=shots[frame];data=Path(r['path']).read_bytes();assert len(data)==0x400000 and sha(data)==r['sha256'];return data
 def picture(frame):
  r=frames[frame];assert sha(Path(r['path']).read_bytes())==r['PNG_sha256'];return Image.open(r['path']).convert('RGB')
 clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');assert resident(arm,PALETTE,32)==resident(clean,PALETTE,32);assert resident(arm,0x020548C8,4)==bytes.fromhex('0f20a0e3')and resident(arm,0x020548D4,4)==bytes.fromhex('34208de5');palette=struct.unpack('<16H',resident(arm,PALETTE,32));colors={1:captured_rgb(palette[15]),15:captured_rgb(palette[14])};assert colors=={1:(0,8,0),15:(197,198,197)};owner,spoken,modal=[struct.unpack_from('<I',arm,p)[0]-BASE for p in[0x552A0,0x54450,0x54894]]
 def masks_match(screen,pixels):return all({(16+i%228,296+i//228)for i,p in enumerate(pixels)if p==index}=={(x,y)for y in range(294,366)for x in range(16,244)if screen.getpixel((x,y))==color}for index,color in colors.items())
 holds=[];negative=[];states=[]
 for n,kind,selected in[(2217,'failure',[7151,7181]),(2229,'forage',[10183,10213]),(312,'loss',[20542,20572])]:
  first=raw(selected[0]);amounts=[]
  if n!=312:
   role,table,ret=(1,0x02116EC0,0x02079F9C)if n==2217 else(7,0x02116E80,0x02079F60);main=stack_word(first,0x0207B190)-0xAC
   if n==2229:amounts=[number_at(first,p)[0]for p in struct.unpack_from('<2I',first,main-8)];assert amounts==[105,105]
   native=ctx.execute(consumers.speech,role,table,amounts,raw=first)
  else:
   at=stack_word(first,0x02079720);amount=number_at(first,struct.unpack_from('<I',first,at+8)[0])[0];assert amount==10;amounts=[amount];native=ctx.execute(consumers.loss,amount,raw=first)
  formatted=bytes.fromhex(native['formatted_hex']);lines=[r.strip().decode('cp932')for r in formatted.split(b'\n')];events=[];pixels=ctx.raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000,glyph_events=events);assert pixels==(literal_independent(arm,ctx.rom.read_file('/GRP/KANJI.FNT'),lines[0])if n==312 else independent_font(arm,ctx.rom.read_file('/GRP/KANJI.FNT'),lines));assert len(lines)<=4 and all(len(s.encode('cp932'))<=35 for s in lines)
  for frame in selected:
   data=raw(frame);screen=picture(frame);resident_text=data[owner+0x2030:owner+0x2230].split(b'\0')[0];at=modal if n==312 else spoken;actual=data[at:at+512].split(b'\0')[0];assert resident_text==ctx.entries[n].text and actual==formatted and masks_match(screen,pixels)and data[PALETTE-BASE:PALETTE-BASE+32]==resident(arm,PALETTE,32)
   cpu,get=get_machine(arm,data);duty=get(0xCB1A8)+0x2090
   if n!=312:
    main=stack_word(data,0x0207B190)-0xAC;assert struct.unpack_from('<3I',data,main-0x14)==(ret,role,table);identity=get(0x82478,duty,role);assert identity==18 and get(0x7E988,get(0xCB184)+4+32*identity)==0 and get(0x53F4C,get(0xCB184)+4+32*identity,table)==n
    arguments=[number_at(data,p)[1]for p in struct.unpack_from('<2I',data,main-8)]if n==2229 else[]
   else:
    at=stack_word(data,0x02079720);assert struct.unpack_from('<I',data,at+4)[0]==312;value,arg=number_at(data,struct.unpack_from('<I',data,at+8)[0]);assert value==10;arguments=[arg];identity=None
   assert native['source_ABF50_argument_hex']==[a.hex()for a in arguments]
   fleet=get(0xCB1A8)+4+132*get(0x2E58C);state=dict(frame=frame,mode=list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12))),fatigue=bytes(cpu.mem_read(fleet+0x3D,1))[0],logical_role1=get(0x82478,duty,1),logical_role7=get(0x82478,duty,7),RAM_sha256=sha(data));states.append(state);r=frames[frame];holds.append(dict(run=kind,frame=frame,message_id=n,actual_actor_ID=identity,source_amounts=amounts,capture=r['path'],capture_sha256=r['PNG_sha256'],RAM_sha256=sha(data),current_resident_hex=resident_text.hex(),current_formatted_hex=actual.hex(),native_pipeline=native,complete_native_ink_and_gray_shadow_RGB_masks_equal=True,full_native_plane_sha256=sha(bytes(pixels)),original_saved_call_and_argument_pointers_verified=True))
  bad=bytearray(ctx.entries[n].text);bad[0]^=1;negative.append(dict(message_id=n,kind='resident-first-byte',rejected=bytes(bad)!=ctx.entries[n].text));bad=bytearray(formatted);bad[0]^=1;negative.append(dict(message_id=n,kind='formatted-first-byte',rejected=bytes(bad)!=formatted));screen=picture(selected[0]);ink=[i for i,p in enumerate(pixels)if p==1]
  targets=[('erase-first-glyph',min(ink,key=lambda i:(i//(228*16),i%228))),('erase-final-glyph',max(ink,key=lambda i:(i//(228*16),i%228))),('erase-interior-letter',ink[len(ink)//2])]
  for j,event in enumerate([e for e in events if e['code']>255]):
   # One negative for each separate original number,using its first fullwidth digit.
   if j and n==2229 and j!=3:continue
   if j and n==312:continue
   if n==2229 and j not in[0,3]:continue
   target=next(i for i,p in enumerate(pixels)if p==1 and event['x']<=i%228<event['x']+12 and event['y']<=i//228<event['y']+12);targets.append((f'erase-original-number-digit-{j}',target))
  for label,index in targets:
   altered=screen.copy();altered.putpixel((16+index%228,296+index//228),(255,255,255));negative.append(dict(message_id=n,kind=label,rejected=not masks_match(altered,pixels)))
  altered=screen.copy();altered.putpixel((16,359),colors[1]);negative.append(dict(message_id=n,kind='stray-blank-paper-ink',rejected=not masks_match(altered,pixels)))
 assert len(holds)==6 and len(negative)==21 and all(c['rejected']for c in negative)
 returns=[]
 for kind,frame in [('failure',7621),('forage',10433),('loss',20792)]:
  data=raw(frame);screen=picture(frame);cpu,get=get_machine(arm,data);mode=list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12)));assert mode==[0,0,0];r=frames[frame];returns.append(dict(run=kind,frame=frame,capture=r['path'],capture_sha256=r['PNG_sha256'],RAM_sha256=sha(data),mode=mode,normal_Sea_View_after_original_dismissal=True))
 # Complete failure exchange also includes original fatigue+3;already-reviewed308
 # receives context credit only. Bind its unchanged actual resident/expanded bytes.
 data=raw(7401);screen=picture(7401);value=data[owner+0x2030:owner+0x2230].split(b'\0')[0];formatted=data[modal:modal+512].split(b'\0')[0];assert value==ctx.entries[308].text and formatted==value.replace(b'%s','３'.encode('cp932'));pixels=ctx.raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000);assert masks_match(screen,pixels);contextonly=dict(run='failure-following-fatigue-context-only',frame=7401,message_id=308,capture=frames[7401]['path'],capture_sha256=frames[7401]['PNG_sha256'],current_formatted_hex=formatted.hex(),no_extra_credit=True)
 sheets=[sheet(ROOT/'Search_original_complete_holds.png',holds),sheet(ROOT/'Search_dismissals_and_following_fatigue.png',[contextonly,*returns])];binding=dict(proof=str(OLD),proof_sha256=sha(OLD.read_bytes()),report=str(rp),report_sha256=sha(rp.read_bytes()),completed_whole4MiB_input_RNG_donor_audit_hash_bound=True)
 save(ROOT/'historical_search_current_binding.json',dict(candidate=str(ctx.rompath),candidate_sha256=sha(ctx.rompath.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(common),historical_proof_bindings=[binding],historical_holds=holds,historical_IDs=[312,2217,2229],historical_normal_returns=returns,all6_original_role_mode_and_saved_source_states=states,negative_controls=negative,following_fatigue308_context_only=contextonly,review_sheets=sheets,completed_whole4MiB_input_RNG_and_donor_audits_hash_bound=True,only_disclosed_location_fixtures_no_crew_supply_fatigue_skill_RNG_or_outcome_forcing=True,source_water_food_order_and_fullwidth_arguments_preserved=True,other8_voice_alternatives_native_and_representative_family_coverage_only=True,no_new_current_emulator_runs_or_visits=True,new_current_actual_IDs=[],scope='Historical targeted cold-boot V1676 Search replay. Original failure2217,forage2229 with105/105 and sailor-loss312 with10 have individual activation;other8 alternatives use current CPU/native and representative family coverage. Following fatigue308 is context-only. Actual equal105/105 does not alone prove argument order;the source pointers and current asymmetric numeric tests do. Location-only fixtures are disclosed;no crew/supply refill,actor,skill,fatigue,RNG,event or outcome forcing. Existing completed full4MiB/input/donor audits hash-bound without replay. Six current complete ink AND source gray-shadow masks,21 corruptions,saved calls,numeric pointers and3normal returns freshly checked. No new current startup,emulator event,earned travel,full-route or hardware claim.',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('6Search holds,21corruptions,following308 context and3normal returns pass;historical-only evidence.')
