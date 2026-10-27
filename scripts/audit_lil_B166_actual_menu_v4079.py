"""Reconcile focused actual menus,complete caption masks,selection highlights andnative backing ownership."""
import struct
from pathlib import Path
from PIL import Image,ImageDraw
from scripts.native_menu_backing_surface_v4079 import paint
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B166_actual_menu_v4079')
RUN=Path('work/analysis/lil_B166_menu_run_v4077')
FIXTURE=Path('work/analysis/lil_B166_menu_fixture_v4076/focused_typed_menu_constructor_fixtures.json')
if __name__=='__main__':
    assert not ROOT.exists();fixture=read(FIXTURE);widths=read('work/analysis/lil_B166_menu_diagnostic_v4070/original_VM_widths_and_preserved_failed_probe.json');rows=[];views=[]
    for spec in fixture['fixtures']:
        case=spec['case'];plan=read(RUN/(case+'_plan.json'));tp=RUN/(case+'_terminal.json');terminal=read(tp);assert terminal['terminal'];rp=Path(terminal['report']);report=read(rp);assert sha(rp.read_bytes())==terminal['report_sha256'] and report['ROM_sha256']==terminal['ROM_sha256']==spec['research_ROM_sha256']
        assert report['frames']==3501 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'];assert report['scripted_input_schedule']==read(plan['inputs']) and sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256']
        im=NdsImage.open(spec['research_ROM']);arm=im.read_file('/__arm9__.bin');vm=next(r['VM'] for r in widths['cases'] if r['version']==case);width=spec['logical_menu_width_px'];rect=vm['native_menu_rectangle'];origin_x=rect[0]+16;observations=[]
        for frame,highlight in [(3000,0),(3500,1)]:
            cap=next(c for c in report['frames_captured'] if c['frame']==frame);p=Path(cap['path']);assert sha(p.read_bytes())==cap['PNG_sha256'];screen=Image.open(p).convert('RGB');sn=next(c for c in report['read_only_capture_RAM_snapshots'] if c['frame']==frame);raw=Path(sn['path']).read_bytes();assert sha(raw)==sn['sha256']
            # The captured native full-bottom-screen view directly owns this
            # bitmap header and preserves its256x192 extent in both cold boots.
            view=0x0229ED64;words=struct.unpack_from('<16I',raw,view-0x02000000);assert words[0]==0x0216017C and words[8:12]==(0,0,256,192)
            header=words[4];h=struct.unpack_from('<5I',raw,header-0x02000000);assert h[:3]==(4,64,192);pointer=(header+h[4])&0xFFFFFFFF;assert 0x02000000<=pointer and pointer+24576<=0x02400000;stored=raw[pointer-0x02000000:pointer-0x02000000+24576];pixels=bytes(n for b in stored for n in (b&15,b>>4));cases=[]
            for option,label in enumerate(vm['labels']):
                oy=rect[1]+12+option*20;native,proof=paint(arm,label.encode('ascii'),1,width,(origin_x,oy));expected=bytes(int(x==1) for x in native);rgb=screen.crop((origin_x,192+oy,origin_x+width,192+oy+20));actual=bytes(int(p==(8,8,8)) for p in rgb.getdata());backing=bytes(int(pixels[(oy+y)*256+origin_x+x]==1) for y in range(20) for x in range(width));assert actual==expected==backing,(case,frame,option)
                bg=(0,165,172) if option==highlight else (206,199,181);background=[p for p,x in zip(rgb.getdata(),expected) if not x];assert len(set(background))==1 and background[0]==bg,(case,frame,option,set(background))
                assert proof['independent_complete_native_pixels_match'] and proof['storage_padding_all_blank'];cases.append(dict(option_index=option,stored_label=label,logical_width=width,view_origin=[origin_x,oy],complete_native_actual_RGB_and_captured_backing_masks_equal=True,foreground_pixels=sum(expected),whole_mask_sha256=sha(expected),native_proof=proof,actually_highlighted=option==highlight))
            observations.append(dict(frame=frame,highlight_index=highlight,capture=str(p),capture_sha256=cap['PNG_sha256'],captured_RAM=sn,whole_bottom_screen_view=view,view_words=list(words),bitmap_header=header,header_words=list(h),backing_pointer=pointer,backing_bytes=24576,backing_plane_sha256=sha(pixels),caption_cases=cases));views.append(dict(case=case,frame=frame,path=str(p),sha256=cap['PNG_sha256']))
        rows.append(dict(case=case,report=str(rp),report_sha256=sha(rp.read_bytes()),terminal=str(tp),terminal_sha256=sha(tp.read_bytes()),observations=observations))
    ROOT.mkdir(parents=True);sheet=Image.new('RGB',(1024,410),'#263238');draw=ImageDraw.Draw(sheet)
    for i,v in enumerate(views):draw.text((i*256+3,3),v['case']+' frame'+str(v['frame']),fill='white');sheet.paste(Image.open(v['path']).convert('RGB'),(i*256,24))
    sp=ROOT/'current_and_reviewed_actual_menus.png';sheet.save(sp)
    save(ROOT/'complete_current_reviewed_caption_masks_and_native_backing.json',dict(runs=rows,actual_two3501_frame_cold_boots=True,actual_four_full_frames_and_eight_complete_caption_masks_pass=True,actual_original_and_reviewed_initial_P_and_all_final_internal_glyphs_complete=True,ordinary_DOWN_changes_highlight0_to1_without_RAM_fixture=True,highlight_navigation_not_choice_return_or_B166_branch_activation=True,captured_native_bitmap_256x192_full_bottom_backing_bound=True,source_logical_label_widths60_and54_unchanged=True,standalone_tight_bitmap_failure_was_pair_flush_wrapping_into_next_row=True,no_ROM_renderer_guard_or_label_padding_change_needed=True,source_B166_menu_only_not_full_story_or_natural_event_coverage=True,viewed_full_screen_captures=views,review_sheet=str(sp),review_sheet_sha256=sha(sp.read_bytes()),visual_review_pending=True,new_emulator_runs=2,source_prose_or_completion_credit_added=0,evidence={str(p):sha(p.read_bytes()) for p in [FIXTURE,Path('scripts/native_menu_backing_surface_v4079.py'),Path('scripts/trace_lil_B166_menu_subglyphs_v4075.py'),Path(__file__)]},full_goal_complete=False));print('Actual current/reviewed menus:8complete native/RGB/backing masks andboth highlight positions pass;256x192 backing bound. View sheet pending.')
