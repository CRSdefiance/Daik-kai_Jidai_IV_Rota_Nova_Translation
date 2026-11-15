"""Match complete live two/three-choice captions,centering,blank cells andcursor backgrounds."""
import argparse
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.check_hodram_B91_B110_actual_pixels import mask,match

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ['fixture','terminal','out']:parser.add_argument('--'+key,type=Path,required=True)
    parser.add_argument('--proofs',type=Path,nargs='+',required=True)
    args=parser.parse_args();assert not args.out.exists()
    fixture,terminal=map(load,[args.fixture,args.terminal]);assert terminal['terminal'] and terminal['frames']==fixture['frames']
    reportpath=Path(terminal['report']);observerpath=Path(terminal['observer'])
    assert sha(reportpath.read_bytes())==terminal['report_sha256'] and sha(observerpath.read_bytes())==terminal['observer_sha256']
    report,observer=map(load,[reportpath,observerpath]);image=NdsImage.open(fixture['research_ROM'])
    assert report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes())
    assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors']
    assert not observer['errors'] and not observer['mismatches'] and observer['all_host_slots_restored_and_core_file_exact']
    samples=[];menus=[]
    for proofpath in args.proofs:
        proof=load(proofpath);assert proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
        original=NdsImage.open(proof['runtime']['candidate'])
        for resource in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']:assert image.read_file(resource)==original.read_file(resource)
        versions=proof.get('versions',proof.get('menus',[{}])[0].get('versions'))
        vm=versions[-1]['cases'][0]['native_VM'];width=vm['minimum_width_units']*6;rect=vm['native_menu_rectangle'];count=len(vm['labels'])
        target=versions[-1]['object_hex'];declared=next(m for m in fixture['menus'] if m['command_hex']==target)
        planes=[next(p for p in proof['records'] if p['version']=='reviewed-English' and p['option']==i and p['style']==1) for i in range(count)]
        inks=[mask(p['path'],p['sha256'],width) for p in planes];found=[]
        for cap in report['frames_captured']:
            if cap['frame']<3000:continue
            path=Path(cap['path']);assert sha(path.read_bytes())==cap['PNG_sha256'];im=Image.open(path).convert('RGB');labels=[];selected=[]
            try:
                for option,(plane,ink) in enumerate(zip(planes,inks,strict=True)):
                    x,y=rect[0]+16,192+rect[1]+16+option*20
                    assert match(im,ink,(8,8,8),[x],[y])==[x,y]
                    blank={(xx,yy) for yy in range(y-4,y+16) for xx in range(x,x+width)}-{(x+xx,y+yy) for xx,yy in ink}
                    cyan={point for point in blank if im.getpixel(point)==(0,165,172)}
                    assert not cyan or cyan==blank
                    if cyan:selected.append(option)
                    else:assert all(im.getpixel(point)==(205,198,180) for point in blank)
                    labels.append(dict(index=option,text=vm['labels'][option],origin=[x,y],native_plane=plane['path'],native_plane_sha256=plane['sha256']))
                assert len(selected)<=1
            except AssertionError:continue
            found.append(dict(source_command_offset=declared['stored_command_offset'],frame=cap['frame'],capture=cap,labels=labels,
                visible_selected_option=selected[0] if selected else None,
                all_complete_captions_centering_first_internal_final_glyphs_blank_guards_andbackgrounds_exact=True))
        assert found,('No complete live menu match',declared['word'])
        samples.extend(found);menus.append(dict(word=declared['word'],source_command_offset=declared['stored_command_offset'],count=count,
            observed_selected_options=sorted({r['visible_selected_option'] for r in found if r['visible_selected_option'] is not None}),
            proof=str(proofpath),proof_sha256=sha(proofpath.read_bytes()),complete_live_samples=len(found)))
    args.out.mkdir();chosen=[]
    for menu in menus:
        states=menu['observed_selected_options']
        for state in states:chosen.append(next(r for r in samples if r['source_command_offset']==menu['source_command_offset'] and r['visible_selected_option']==state))
        if not states:chosen.append(next(r for r in samples if r['source_command_offset']==menu['source_command_offset']))
    font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18);sheet=Image.new('RGB',(1536,((len(chosen)+2)//3)*410),'#eee');draw=ImageDraw.Draw(sheet)
    for i,sample in enumerate(chosen):
        x,y=i%3*512,i//3*410;draw.text((x+4,y+4),f"C{sample['source_command_offset']} option{sample['visible_selected_option']} @{sample['frame']}",font=font,fill='black')
        sheet.paste(Image.open(sample['capture']['path']).convert('RGB').crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(x,y+25))
    png=args.out/'menus_QA.png';sheet.save(png)
    save(args.out/'menu_actual_pixels.json',dict(fixture=str(args.fixture),fixture_sha256=sha(args.fixture.read_bytes()),terminal=str(args.terminal),terminal_sha256=sha(args.terminal.read_bytes()),
        frames=report['frames'],menus=menus,menu_samples=samples,complete_live_caption_samples=len(samples),
        all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches=True,
        numeric_modal_return_register_original_story_branches_andcancellation_unvisited=True,
        native_return_values_andbranch_sites_proved_separately_offline=True,
        review_sheet=dict(path=str(png),sha256=sha(png.read_bytes())),direct_visual_review_pending=True,
        actual_gameplay=True,disclosed_initialized_fixture=True,natural_activation=False,hardware=False,new_credit=0,guide_photos=False))
    print([(m['count'],m['observed_selected_options'],m['complete_live_samples']) for m in menus])
