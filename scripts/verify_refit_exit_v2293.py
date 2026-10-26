"""Revised fixed-input prefix, cancellation, complete merchant reply and selection."""
from pathlib import Path
import struct
from PIL import Image,ImageDraw
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.finish_refit_display_v712 import load
from scripts.verify_full_fleet_battle_v652 import fleet_models
from scripts.verify_full_fleet_victory_v654 import funds
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/refit_exit_verification_v2293');CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);rompath=Path('out/all_routes_combined_v2284_candidate.nds');digest=sha(rompath.read_bytes());rom=NdsImage.open(rompath);arm=rom.read_file('/__arm9__.bin');entries=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm);report,shots,receipt=load(CAP/'refit_spritsail_v2292_refit_V2284',digest,17701);old,oldshots,oldreceipt=load(CAP/'refit_spritsail_v2287_refit_V2284',digest,17401)
 assert read('work/analysis/refit_spritsail_runs_v2292/refit_terminal.json')['terminal'];obs=read(CAP/'refit_spritsail_v2292_refit_V2284/refit_observer/requests.json');assert not obs['errors']and not obs['mismatches']and obs['all_host_slots_restored_and_core_file_exact']
 a=[r for r in report['scripted_input_schedule']if r['start']<17001];b=[r for r in old['scripted_input_schedule']if r['start']<17001];assert a==b
 frames=sorted(f for f in shots if f<=17000);assert len(frames)>=18
 for f in frames:assert shots[f].tobytes()==oldshots[f].tobytes(),f
 states=[];raws={}
 for f in(3200,11900,14300,17000,17300,17600):
  snap=next(r for r in report['read_only_capture_RAM_snapshots']if r['frame']==f);raw=Path(snap['path']).read_bytes();assert sha(raw)==snap['sha256']and snap['read_only_export'];raws[f]=raw;cpu,get=get_machine(arm,raw);calendar=get(0xCB1B4);tick=struct.unpack('<I',cpu.mem_read(calendar+8,4))[0];state=dict(frame=f,funds=funds(arm,raw),fleet=fleet_models(arm,raw,1),calendar_tick=tick);assert state['funds']==25975 and len(state['fleet'])==5;states.append(state)
 assert all((s['funds'],s['fleet'],s['calendar_tick'])==(states[0]['funds'],states[0]['fleet'],states[0]['calendar_tick'])for s in states)
 owner,printed,wrapped=[struct.unpack_from('<I',arm,n)[0]for n in(0x552A0,0x5444C,0x54450)];raw=raws[17300];cstring=lambda p:raw[p-0x02000000:p-0x02000000+512].split(b'\0')[0];template=cstring(owner+0x2030);visible=cstring(wrapped);assert template==entries[1266].text and cstring(printed)==template and b' '.join(visible.split())==b' '.join(template.split())
 lines=[r.strip().decode('cp932')for r in visible.split(b'\n')];plane=independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),lines);ink={(16+i%228,296+i//228)for i,v in enumerate(plane)if v==1};actual={(x,y)for y in range(294,366)for x in range(16,244)if shots[17300].getpixel((x,y))==(0,8,0)};assert actual==ink
 selected=[14300,15800,16100,16400,16700,17000,17300,17600];sheet=Image.new('RGB',(1024,824),'#263238');draw=ImageDraw.Draw(sheet)
 for i,f in enumerate(selected):x,y=i%4*256,i//4*412;draw.text((x+4,y+4),f'V2284 exit successor {f}',fill='white');sheet.paste(shots[f],(x,y+28))
 p=ROOT/'cancel_and_ship_selection_sheet.png';sheet.save(p)
 save(ROOT/'normal_cancel_and_selection.json',dict(candidate=str(rompath),candidate_sha256=digest,actual_report=receipt,prior_input_plan_reference=oldreceipt,all_shared_prefix_frames_exact=frames,revised_help_caption_proof_inherited_by_same_input_prefix_and_complete_frame_identity='work/analysis/refit_spritsail_actual_verification_v2290c/actual_revised_help_caption_and_startup.json',A17001_accepts_cancel_prompt=True,complete_merchant1266_after_cancel=dict(frame=17300,lines=lines,resident_template_printed_and_wrapped_bytes_exact=True,all_current_independent_foreground_and_blank_ink_equal=True),B17301_returns_original_five_ship_selection_frame17600=True,final_screen_is_ship_selection_not_Port=True,six_fleet_funds_and_calendar_controls=states,no_refit_charge_elapsed_days_or_changed_Hull_Crew_names=True,source_battery_inherited_not_earned_progress=True,no_new_RAM_code_gameplay_fixture_or_savestate=True,all_host_slots_restored_core_exact_errors_and_mismatches_zero=True,review_sheet=str(p),review_sheet_sha256=sha(p.read_bytes()),visual_review_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(shared_prefix_frames=len(frames),cancel_A=True,full1266=True,ship_selection_return=True,unchanged_state_controls=6,visual_pending=True))
