"""Full visible recruitment foregrounds, native continuations and paired paid-action state."""
from pathlib import Path
import re
import struct
from PIL import Image, ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
from scripts.verify_village_wrap_v608 import read, save
from scripts.primary_town_native_font_v2102 import font_tools, glyph_codes
from scripts.verify_shipyard_gameplay_v760 import independent_font, models
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_tavern_gameplay_v767 import persistent_objects

ROOT = Path('work/analysis/recruitment_actual_verification_v2208')
RUN = Path('work/analysis/recruitment_actual_v2202')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/recruitment_actual_v2202_V2171')
NATIVE = Path('work/analysis/recruitment_actual_continuations_v2206/actual_snapshot_native_font_continuations.json')
ROM = Path('out/all_routes_combined_v2171_candidate.nds')
EXPECTED = {890:(5000,5200), 897:(5400,5600), 907:(5800,6000), 904:(6200,6400)}

if __name__ == '__main__':
    assert not ROOT.exists()
    ROOT.mkdir(parents=True)
    rom = NdsImage.open(ROM)
    arm, common, kanji = [rom.read_file(p) for p in ('/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT')]
    entries = current_entries(common, arm)
    plan, terminal, report, obs, native = [read(p) for p in (RUN/'run_plan.json',RUN/'terminal.json',CAP/'capture_report.json',CAP/'common_observer/requests.json',NATIVE)]
    assert terminal['terminal'] and terminal['all_observer_host_slots_restored']
    assert report['frames'] == 8801 and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report['hardware_device_verification']
    assert not obs['errors'] and not obs['mismatches'] and obs['all_host_slots_restored_and_core_file_exact']
    assert not any(v for k,v in report.items() if k.startswith('synthetic_'))
    assert report['ROM_sha256'] == plan['candidate_sha256'] == sha(ROM.read_bytes())
    assert sha(Path(plan['original_genuine_save']).read_bytes()) == plan['donor_sha256'] == 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
    previous = read(plan['prior_report'])
    assert sha(Path(plan['prior_report']).read_bytes()) == plan['prior_report_sha256']
    assert report['scripted_input_schedule'] == previous['scripted_input_schedule'] and report['core_options'] == previous['core_options']
    assert native['ARM9_sha256'] == sha(arm) and len(native['cases']) == len(obs['rows']) == 7
    frames = {r['frame']:r for r in report['frames_captured']}
    raster, _, _ = font_tools(rom)
    holds = []
    for row in obs['rows']:
        n = row['source_request']['ID']
        full = next(r for r in native['cases'] if r['message_ID']==n and r['text_hex']==row['text_hex'])
        assert full['complete_native_return'] and full['SP_preserved'] and full['callee_registers_preserved'] and not full['faults'] and not full['error']
        if n not in EXPECTED: continue
        assert row['bounds']==[0,0,228,48] and row['font_input_offset'] in (0,2)
        raw = Path(row['snapshots']['WRAM']['path']).read_bytes()
        assert sha(raw)==row['snapshots']['WRAM']['sha256']
        p = struct.unpack_from('<I',arm,0x5444C)[0]-0x02000000
        printf = raw[p:p+512].split(bytes(1))[0]
        match = re.fullmatch(b'(.*?)'.join(re.escape(p) for p in entries[n].text.split(b'%s')),printf)
        assert match is not None
        text = bytes.fromhex(row['text_hex'])
        assert b' '.join(text.split()) == b' '.join(printf.split())
        lines = [s.strip().decode('cp932') for s in text.split(b'\n')]
        events=[]
        plane = raster(arm,text,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000,glyph_events=events)
        assert plane==independent_font(arm,kanji,lines)
        assert [r['code'] for r in events if r['code']!=32]==glyph_codes(text)
        assert [r['code'] for r in full['glyph_events'] if r['code']!=32]==glyph_codes(text)
        assert sorted({r['y'] for r in full['glyph_events']})==list(range(0,12*len(lines),12))
        pixels={(16+i%228,296+i//228) for i,v in enumerate(plane) if v==1}
        for f in EXPECTED[n]:
            capture=frames[f]
            assert sha(Path(capture['path']).read_bytes())==capture['PNG_sha256']
            image=Image.open(capture['path']).convert('RGB')
            actual={(x,y) for y in range(294,360) for x in range(16,244) if image.getpixel((x,y))==(0,8,0)}
            assert actual==pixels,(n,f,len(actual-pixels),len(pixels-actual))
            holds.append(dict(message_ID=n,font_frame=row['frame'],hold_frame=f,lines=lines,arguments_hex=[v.hex() for v in match.groups()],formatted_hex=text.hex(),capture=capture['path'],capture_sha256=capture['PNG_sha256'],complete_native_actual_independent_foreground_equal=True))
    assert len(holds)==8 and {r['message_ID'] for r in holds}==set(EXPECTED)
    snapshots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']}
    old_snapshots={r['frame']:r for r in previous['read_only_capture_RAM_snapshots']}
    old_arm=NdsImage.open(previous['ROM']).read_file('/__arm9__.bin')
    paired=[]
    for f in (3200,5000,5400,6200,6600,7400,7800,8800):
        raw, old_raw=[Path(q[f]['path']).read_bytes() for q in (snapshots,old_snapshots)]
        assert sha(raw)==snapshots[f]['sha256'] and sha(old_raw)==old_snapshots[f]['sha256']
        current_state, old_state=state(arm,raw),state(old_arm,old_raw)
        current_models, old_models=models(arm,raw),models(old_arm,old_raw)
        assert current_state==old_state,(f,'state',current_state,old_state)
        assert current_models==old_models,(f,'models')
        assert persistent_objects(arm,raw)==persistent_objects(old_arm,old_raw),(f,'persistent')
        paired.append(dict(frame=f,state=current_state,models=current_models,current_RAM_sha256=sha(raw),reference_RAM_sha256=sha(old_raw),state_company_fleet_ship_and_persistent_objects_equal_historical_same_inputs=True))
    quote=next(r for r in holds if r['message_ID']==890)
    amount=int(bytes.fromhex(quote['arguments_hex'][0]).decode('cp932'))
    gathered=int(bytes.fromhex(next(r for r in holds if r['message_ID']==904)['arguments_hex'][0]).decode('cp932'))
    assert amount==1573 and gathered==34
    assert paired[0]['state']['cash']-paired[2]['state']['cash']==amount
    controls=[]
    for f in (6600,7000,7400,7800,8200,8600,8800):
        capture=frames[f]
        assert sha(Path(capture['path']).read_bytes())==capture['PNG_sha256']
        controls.append(dict(frame=f,capture=capture['path'],capture_sha256=capture['PNG_sha256'],scope='actual AssignSailors/unassigned confirmation/ordinary return; visual review pending; no extra editorial credit'))
    for name,rows,key in (('eight_recruitment_holds',holds,'hold_frame'),('seven_recruitment_transitions',controls,'frame')):
        sheet=Image.new('RGB',(1024,820),'#263238');draw=ImageDraw.Draw(sheet)
        for i,r in enumerate(rows):
            x,y=i%4*256,i//4*410
            draw.text((x+4,y+4),f"ID{r.get('message_ID','context')} frame{r[key]}",fill='white')
            sheet.paste(Image.open(r['capture']).convert('RGB'),(x,y+22))
        sheet.save(ROOT/(name+'.png'))
    save(ROOT/'ordinary_recruitment_foreground_state_transitions.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),source_plan=str(RUN/'run_plan.json'),source_plan_sha256=sha((RUN/'run_plan.json').read_bytes()),source_report=str(CAP/'capture_report.json'),source_report_sha256=sha((CAP/'capture_report.json').read_bytes()),source_observer=str(CAP/'common_observer/requests.json'),source_observer_sha256=sha((CAP/'common_observer/requests.json').read_bytes()),native_continuation=str(NATIVE),native_continuation_sha256=sha(NATIVE.read_bytes()),actual_holds=holds,transition_frames=controls,paired_native_state_model_controls=paired,source_quoted_cost=amount,actual_charge=amount,gathered_before_assignment=gathered,gathered_count_not_already_assigned=True,cash_before=paired[0]['state']['cash'],cash_after=paired[2]['state']['cash'],all7_native_font_returns_complete=True,all8_full_foregrounds_equal_native_and_independent=True,only890_897_907_904_current106_actual_visits_claimed=True,context1042_and71_no_new_credit=True,no_savestate_or_any_synthetic_fixture=True,no_new_startup_test_needed_for_identical_registered_binary=True,production_logical_view=[228,48],production_metrics=[6,12],physical16pixel_oracle_not_logical_capacity=True,original_genuine_donor_core_unchanged_and_host_slots_restored=True,visual_review_pending=True,not_full_route_or_hardware_verification=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(holds=len(holds),paired_controls=len(paired),cost=amount,gathered=gathered),flush=True)
