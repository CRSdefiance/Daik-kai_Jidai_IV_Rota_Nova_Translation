"""Fresh source-bound startup/town RGB and native SDK/arena/copy evidence for224-byte growth."""
import struct
from pathlib import Path
from ndspy.code import MainCodeFile
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_persistent_name_arm7_boot_overlap import execute as boot
from scripts.probe_common_itcm_arena_reservation import initialize,verify as arenas
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shachihoko_boot_v6099')
RECEIPT=Path('work/analysis/shachihoko_item116_research_v6094/coordinated_research_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists();receipt=read(RECEIPT);rom=NdsImage.open(receipt['research_ROM']);arm=rom.read_file('/__arm9__.bin');plan=receipt['data_plan'];assert sha(arm)==plan['target_ARM9_sha256']
    evidence=[RECEIPT,Path(__file__)];comparisons=[];modelcases=[];pictures=[]
    for case,root in [('newgame','shachihoko_runs_v6095'),('town','shachihoko_runs_v6096')]:
        old_term_path=Path(f'work/analysis/lil_B203_runs_v6052/{case}_terminal.json');new_term_path=Path(f'work/analysis/{root}/{case}_terminal.json');oldterm,newterm=map(read,[old_term_path,new_term_path]);assert oldterm['terminal'] and newterm['terminal']
        paths=[Path(t['report']) for t in [oldterm,newterm]];old,new=map(read,paths);assert new['ROM_sha256']==receipt['research_ROM_sha256'] and old['ROM_sha256']==receipt['parent_sha256']
        for report in [old,new]:assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and not any(v for k,v in report.items() if k.startswith('synthetic_'))
        for p,t in zip(paths,[oldterm,newterm],strict=True):assert sha(p.read_bytes())==t['report_sha256']
        for a,b in zip(old['frames_captured'],new['frames_captured'],strict=True):
            assert a['frame']==b['frame'] and a['PNG_sha256']==b['PNG_sha256']
            for r in [a,b]:assert sha(Path(r['path']).read_bytes())==r['PNG_sha256']
            comparisons.append(dict(case=case,frame=a['frame'],whole_RGB_sha256=b['PNG_sha256'],parent=a['path'],target=b['path'],whole_RGB_equal=True))
            if (case,a['frame']) in [('newgame',1600),('newgame',2400),('newgame',4000),('town',11900),('town',14900),('town',17401)]:pictures.append((case+' '+str(a['frame']),b))
        selected=[4000] if case=='newgame' else [11900,13400,14900,16400,17401]
        oldarm=NdsImage.open(receipt['parent']).read_file('/__arm9__.bin');actor_pointer=struct.unpack_from('<I',arm,0xCB18C)[0];assert struct.unpack_from('<I',oldarm,0xCB18C)[0]==actor_pointer
        for frame in selected:
            snapshots=[next(s for s in report['read_only_capture_RAM_snapshots'] if s['frame']==frame) for report in [old,new]];raws=[]
            for s in snapshots:
                raw=Path(s['path']).read_bytes();assert s['read_only_export'] and len(raw)==0x400000 and sha(raw)==s['sha256'];raws.append(raw)
            a,b=[raw[actor_pointer-0x02000000:actor_pointer-0x02000000+0x1A04] for raw in raws];assert a==b
            modelcases.append(dict(case=case,frame=frame,actor_root=actor_pointer,all_actor_and_captain_bytes=0x1A04,whole_actor_model_sha256=sha(a),parent_snapshot=snapshots[0],target_snapshot=snapshots[1],all_actor_and_captain_model_bytes_equal=True))
        if case=='town':
            runplan=read(f'work/analysis/{root}/town_plan.json');assert sha(Path(runplan['source_donor']).read_bytes())==sha(Path(runplan['disposable_donor']).read_bytes())==runplan['source_donor_sha256']
        evidence.extend([old_term_path,new_term_path,*paths])
    assert len(comparisons)==31 and len(pictures)==6 and len(modelcases)==6
    payload=bytes(MainCodeFile(arm,0x02000000).sections[3].data[:-48]);assert len(payload)==123264
    native=boot(arm,bytes(rom.rom.arm7),rom.rom.arm7RamAddress,True,payload)
    for flag in ['repaired_pool_matches_complete_payload','repair_returns_with_stack_preserved','actual_startup_call_preserves_r0_r3','late_copy_reached_caller_continuation']:assert native[flag]
    assert not native['arm7_source_changed_bytes_after_arm9_autoload'] and all(r['matches_original'] for r in native['arm7_native_loaded_sections'])
    assert all(native['SDK_staged_code_cache_line_coverage'][k] for k in ['all_instruction_lines_selected','all_data_lines_selected']) and native['late_copy_cache_model']['worst_case_dirty_data_and_stale_instruction_model_visible']
    allocation=initialize(arm);resident=arenas(arm,0x01FFA000);assert allocation['low'][0]==plan['new_cache_plan']['pool_span'][1]
    ROOT.mkdir(parents=True);sheet=Image.new('RGB',(1040,2400),'#263238');draw=ImageDraw.Draw(sheet)
    for i,(label,r) in enumerate(pictures):
        im=Image.open(r['path']).convert('RGB');x,y=i%2*520,i//2*800;draw.text((x+4,y+3),'Actual expanded target '+label,fill='white');sheet.paste(im.resize((512,768),Image.Resampling.NEAREST),(x+4,y+24))
    picture=ROOT/'six_actual_startup_town_screens.png';sheet.save(picture)
    save(ROOT/'source_bound_growth_boot_input_and_native_allocation_verification.json',dict(
        research_ROM=receipt['research_ROM'],research_ROM_sha256=receipt['research_ROM_sha256'],source_parent=receipt['parent'],source_parent_sha256=receipt['parent_sha256'],
        observed_payload_growth=224,original_payload=123040,target_payload=123264,prior_V609_320_byte_failure_not_generalized_or_erased=True,
        all31_actual_same_input_whole_RGB_frames_equal_V6050=True,frame_comparisons=comparisons,all_six_postinit_whole_actor_and_captain_model_comparisons=modelcases,
        original_and_disposable_town_battery_hashes_exact=True,inherited_five_ship_battery_not_earned_progress=True,
        native_ARM9_ARM7_autoload_late_copy_cache_and_ABI=native,native_main_arena=allocation,native_resident_arena=resident,
        complete_actual123264_payload_native_copy_reservation_and_cacheline_extents_verified=True,
        actual_New_Game4001_and_town17401_cold_boot_runs_terminal=True,actual_new_cold_boots=2,actual_new_frames=21402,
        no_full_RAM_future_sequence_complete_timing_cause_or_hardware_claim=True,visual_review_pending=True,sheet=str(picture),sheet_sha256=sha(picture.read_bytes()),
        native_detail_glyph_and_registered_release_checks_pending=True,new_review_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in evidence}))
    print('Fresh expanded224-byte target:31 whole screens and6 actor/captain model checks match V6050. Native autoload/copy/cache/ABI/new arena pass. Six screens await visual review;no release claim.')
