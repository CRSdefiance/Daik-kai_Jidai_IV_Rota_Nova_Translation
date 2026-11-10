"""Check the new ordinary Rafael coldboot without borrowing another route's RAM."""
from pathlib import Path
from types import SimpleNamespace
from PIL import Image,ImageDraw,ImageFont
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from dk4tool.patch.reviewed_name_catalog import ROUTE
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.probe_escape_direct_source_v1186 import machine

ROOT=Path('work/analysis/Rafael_early_tutorial_registered_context_20261104')
RELEASE=Path('work/analysis/Hodram_B191_B210_release_verified_20261104/registered_release_verification.json')

if __name__=='__main__':
    output=ROOT/'registered_Rafael_context_v1.json';sheet_path=ROOT/'Rafael_context_QA.png'
    assert not output.exists() and not sheet_path.exists()
    report_path=ROOT/'capture_report.json';report,release=map(load,[report_path,RELEASE])
    assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded')
    assert not report['callback_errors'] and report['frames']==4001
    candidate=Path(release['candidate']);assert sha(candidate.read_bytes())==release['candidate_sha256']==report['ROM_sha256']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert not any('RIGHT' in r['buttons'] for r in report['scripted_input_schedule'])
    image=NdsImage.open(candidate);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    snapshot={**report['read_only_RAM_snapshot'], 'frame':4001,'source_report_key':'read_only_RAM_snapshot','recorded_after_final_frame_no_historical_overlay':True}
    raw=Path(snapshot['path']).read_bytes();assert snapshot['read_only_export'] and len(raw)==snapshot['bytes']==0x400000 and sha(raw)==snapshot['sha256']
    sections=MainCodeFile(arm,BASE).sections;payload=bytes(sections[3].data[:-48]);assert len(payload)==123264
    assert raw[POOL-BASE:POOL-BASE+len(payload)]==payload
    owners=[*sections,SimpleNamespace(ramAddress=POOL,data=payload)]
    cpu,get,_=machine(arm,common,raw,dict(patches=[]));executed=set()
    def exact(u,pc,size,_):
        matches=[s for s in owners if s.ramAddress<=pc and pc+size<=s.ramAddress+len(s.data)]
        assert len(matches)==1
        owner=matches[0];assert bytes(u.mem_read(pc,size))==bytes(owner.data[pc-owner.ramAddress:pc-owner.ramAddress+size]);executed.add(pc)
    hook=cpu.hook_add(UC_HOOK_CODE,exact);before=bytes(cpu.mem_read(BASE,0x400000))
    captain=get(0x7F244);root=get(0xCB184)
    assert captain==0 and int.from_bytes(cpu.mem_read(ROUTE,4),'little')==0
    assert bytes(cpu.mem_read(BASE,0x400000))==before and BASE<=root<BASE+0x400000-0x1A04
    cpu.hook_del(hook)
    wanted=report['exact_requested_capture_frames'];assert wanted==[1000,1200,1800,2200,3000,4000]
    font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',12);sheet=Image.new('RGB',(768,832),'#eee');draw=ImageDraw.Draw(sheet);captures=[]
    for index,frame in enumerate(wanted):
        cap=next(r for r in report['frames_captured'] if r['frame']==frame);path=Path(cap['path']);assert sha(path.read_bytes())==cap['PNG_sha256']
        x,y=index%3*256,index//3*416;sheet.paste(Image.open(path).convert('RGB'),(x,y+24));draw.text((x+2,y+2),'Rafael ordinary coldboot @'+str(frame),font=font,fill='black');captures.append(cap)
    sheet.resize((1536,1664),Image.Resampling.NEAREST).save(sheet_path)
    save(output,dict(candidate=str(candidate),candidate_sha256=release['candidate_sha256'],profile=release['profile'],
        capture_report=str(report_path),capture_report_sha256=sha(report_path.read_bytes()),cold_boot=True,savestate=False,frames=4001,
        actual_captain_getter=0,actual_route_word=0,actual_actor_root=root,read_only_snapshot=snapshot,
        complete_staged_payload_exact=True,current_getter_instructions_exact=True,original_getter_instruction_addresses=len(executed),native_getters_preserve_all_main_RAM=True,
        review_sheet=str(sheet_path),review_sheet_sha256=sha(sheet_path.read_bytes()),captures=captures,direct_visual_review_pending=True,
        no_battery_savestate_RAM_roster_money_RNG_orlocation_override=True,no_historical_RAM_overlay=True,
        ordinary_Rafael_startup_context_not_B42_B43_gameplay_coverage=True,no_new_dialogue_completion_credit=True,new_credit=0,guide_photos=False,
        source_control00_andtarget_tutorial_macro_formatting_still_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [RELEASE,report_path,Path(__file__)]}))
    print('Rafael ordinary coldboot captain0/route0 andown complete payload pass;one new QA sheet requires direct viewing.')
