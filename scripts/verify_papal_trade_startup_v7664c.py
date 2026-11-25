"""Compare own registered cold boots and actor controls with exact V7611 counterparts."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/papal_trade_startup_verification_v7664c')
RUN=Path('work/analysis/papal_trade_startup_runs_v7663')
def run_folder(case):return Path('work/analysis/papal_trade_startup_runs_v7663b')/case if case in ['route0','route1'] else RUN/case
if __name__=='__main__':
    cases=['route0','route1','route2','town'];assert not ROOT.exists() and all(read(run_folder(c)/'terminal.json')['terminal'] for c in cases)
    release=read('work/analysis/papal_trade_release_v7661/registered_release_verification.json');rom=Path(release['candidate']);image=NdsImage.open(rom);arm=image.read_file('/__arm9__.bin');assert arm==NdsImage.open('out/all_routes_combined_v7611_candidate.nds').read_file('/__arm9__.bin')
    runs=[];photos=[];total=0
    for case in cases:
        pp=run_folder(case)/'run_plan.json';tp=run_folder(case)/'terminal.json';plan,terminal=map(read,[pp,tp]);old_terminal=read(plan['prior_terminal']);rp=Path(terminal['report']);op=Path(old_terminal['report']);report,old=map(read,[rp,op])
        assert report['ROM_sha256']==release['candidate_sha256']==terminal['candidate_sha256'] and sha(rp.read_bytes())==terminal['report_sha256'] and sha(op.read_bytes())==old_terminal['report_sha256']
        assert report['frames']==old['frames']==plan['frames'] and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['scripted_input_schedule']==old['scripted_input_schedule'] and report['core_options']==old['core_options']
        if case=='town':assert report['battery_save_preloaded'] and sha(Path(plan['source_donor']).read_bytes())==sha(Path(plan['disposable_donor']).read_bytes())==plan['source_donor_sha256']
        else:assert not report.get('battery_save_preloaded')
        oldpics={p['frame']:p for p in old['frames_captured']};pairs=[]
        for p in report['frames_captured']:
            q=oldpics[p['frame']];assert sha(Path(p['path']).read_bytes())==p['PNG_sha256'] and sha(Path(q['path']).read_bytes())==q['PNG_sha256']
            assert Image.open(p['path']).convert('RGB').tobytes()==Image.open(q['path']).convert('RGB').tobytes(),(case,p['frame'])
            pairs.append(dict(frame=p['frame'],current=p,prior=q,whole_RGB_equal=True));total+=1
        controls=[]
        chosen=[4000] if case!='town' else [f for f in [3200,4000,17400] if any(s['frame']==f for s in report['read_only_capture_RAM_snapshots'])]
        assert chosen
        for frame in chosen:
            values=[]
            for r in [old,report]:
                s=next(s for s in r['read_only_capture_RAM_snapshots'] if s['frame']==frame);raw=Path(s['path']).read_bytes();assert s['read_only_export'] and len(raw)==4194304 and sha(raw)==s['sha256']
                cpu,get=get_machine(arm,raw);root=get(0xCB184);captain=get(0x7F244);assert captain=={'route0':0,'route1':1,'route2':2,'town':1}[case]
                values.append(dict(captain=captain,actor_root=root,whole_actor_sha256=sha(bytes(cpu.mem_read(root,0x1A04)))))
            assert values[0]==values[1],(case,frame);controls.append(dict(frame=frame,prior=values[0],current=values[1],equal=True))
        selected=[2000,4000] if case!='town' else [p['frame'] for p in report['frames_captured'] if p['frame'] in [3200,17400]]
        for frame in selected:
            p=next(p for p in report['frames_captured'] if p['frame']==frame);photos.append(dict(case=case,frame=frame,capture=p['path'],sha256=p['PNG_sha256']))
        runs.append(dict(case=case,plan=str(pp),plan_sha256=sha(pp.read_bytes()),terminal=str(tp),terminal_sha256=sha(tp.read_bytes()),capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),prior_report=str(op),prior_report_sha256=sha(op.read_bytes()),whole_frame_pairs=pairs,actor_captain_controls=controls,source_and_disposable_donor_unchanged=True,inherited_battery_not_earned_progress=case=='town',measured_original_captain_ID={'route0':0,'route1':1,'route2':2,'town':1}[case]))
    ROOT.mkdir(parents=True);sheets=[]
    for start in range(0,len(photos),4):
        sheet=Image.new('RGB',(1024,410),'#263238');draw=ImageDraw.Draw(sheet)
        for i,p in enumerate(photos[start:start+4]):draw.text((i*256+3,3),f"V7660 {p['case']} frame{p['frame']}",fill='white');sheet.paste(Image.open(p['capture']).convert('RGB'),(i*256,24))
        path=ROOT/f'own_ROM_startup_town_sheet{start//4+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    save(ROOT/'own_ROM_three_NewGames_town_exact_prior_comparisons.json',dict(candidate=str(rom),candidate_sha256=release['candidate_sha256'],runs=runs,whole_RGB_frame_pairs=total,all_current_requested_andfinal_frames_equal_V7611=True,all_native_actor_andcaptain_controls_equal=True,all_three_captains0_1_2_actual_NewGames_verified=True,inherited_Stockholm_town_actual_Hodram_captain1_verified=True,historical_town_plan_route2_Lil_label_preserved_as_superseded_metadata=True,source_anddisposable_town_donors_unchanged=True,no_RAM_code_observer_savestate_ornew_gameplay_fixture=True,no_optional_papal_activation_full_route_orhardware_claim=True,review_sheets=sheets,visual_review_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print(f'Own V7660 three NewGames andtown pass:{total}whole-frame pairs/actualcaptains0_1_2/actor controls/donors matchV7611. Visual/native inputs pending.')
