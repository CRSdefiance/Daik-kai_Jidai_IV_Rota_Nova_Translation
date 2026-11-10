"""Independently compare all source/English menu caption/highlight pixels in the four existing runs."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.square_shopkeeper_font_oracles_v7020 import PROGRESSIVE_ORACLE_SOURCE
from scripts.verify_name_catalog_glyphs_v278 import expected_pixels as old_expected
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B52_actual_menu_RGB_v8654')
DEFAULT=Path('work/analysis/Hodram_B52_actual_v8651/B52/paired_actual_dialogue_headers_flow_returns.json')
OPPOSITION=Path('work/analysis/Hodram_B52_opposition_actual_v8653/B52/paired_actual_dialogue_headers_flow_returns.json')
DOC=Path('translations/hodram_B52_editorial_manuscript_v3.json')
SOURCE=Path('work/analysis/Hodram_B52_source_choice_VM_v8628b/source_menu_provider_andresponse_paths.json')
MENU=Path('work/analysis/Hodram_B52_menu_v8636/menu_provider_and_planes.json')

if __name__=='__main__':
    assert not ROOT.exists();doc,source,menu=map(read,[DOC,SOURCE,MENU])
    env={**old_expected.__globals__,'WIDTH':256,'HEIGHT':36};exec(compile(PROGRESSIVE_ORACLE_SOURCE,__file__+'::independent-font-caption-pixels','exec'),env);oracle=env['expected_pixels']
    groups=[];pictures=[]
    for choice,proofpath in [(0,DEFAULT),(1,OPPOSITION)]:
        proof=read(proofpath);assert not proof['unresolved'] and proof['all_observed_complete_body_name_holds_andnative_flow_pass']
        for g in proof['groups']:
            version=g['version'];pairs=[p for p in g['command_pairs'] if p['word']==0x2100]
            assert len(pairs)==1 and pairs[0]['native_result']==[2,choice]
            interval=pairs[0];report=read(g['capture_report']);image=NdsImage.open(g['fixture']['research_ROM'])
            assert sha(Path(g['fixture']['research_ROM']).read_bytes())==g['fixture']['research_ROM_sha256']==report['ROM_sha256']
            arm,fnt=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT')
            assert sha(arm)==doc['current_ARM9_sha256']==source['ARM9_sha256']
            labels=[r['source_Japanese'] for r in source['source_choice']['labels']] if version=='clean_Japanese' else [r['english'] for r in doc['typed_choice_records']]
            width=84 if version=='clean_Japanese' else 72;rect=source['source_menu_rectangle'] if version=='clean_Japanese' else menu['reviewed_rectangle']
            assert rect[1:4:2]==[64,128] and rect[2]-rect[0]==width+32
            x=rect[0]+16;assert x==(256-width)//2
            masks=[]
            for index,label in enumerate(labels):
                points=codes(label.encode('cp932'));advance=sum(6 if c<128 else 12 for c in points);start=(width-advance)//2;events=[];cursor=start
                for c in points:
                    events.append(dict(kind='ascii' if c<128 else 'cp932',code=c,style=8,x=cursor,y=0));cursor+=6 if c<128 else 12
                assert 0<=start and cursor<=width
                plane=oracle(arm,fnt,events,canvas_height=12);ink={(i%256,i//256) for i,b in enumerate(plane) if b}
                assert ink and all(0<=xx<width and 0<=yy<12 for xx,yy in ink);masks.append(ink)
            samples=[]
            selected_photos=[p for p in report['frames_captured'] if p['frame'] in [4090,4150,4210]]
            assert len(selected_photos)==3
            for photo in selected_photos:
                frame=photo['frame'];assert interval['start']+20<frame<interval['returned']-4 and sha(Path(photo['path']).read_bytes())==photo['PNG_sha256']
                im=Image.open(photo['path']).convert('RGB');assert im.size==(256,384)
                selected=1 if choice==1 and frame>4105 else 0;results=[]
                for index,ink in enumerate(masks):
                    y=192+rect[1]+16+20*index
                    black={(xx-x,yy-y) for yy in range(y-1,y+13) for xx in range(x-2,x+width+2) if im.getpixel((xx,yy))==(8,8,8)}
                    assert black==ink,(choice,version,frame,index,'complete independent visible caption glyphs/blank guards')
                    positions={(xx,yy) for yy in range(y-4,y+16) for xx in range(x,x+width)}-{(x+xx,y+yy) for xx,yy in ink}
                    cyan={p for p in positions if im.getpixel(p)==(0,165,172)};visible=bool(cyan)
                    assert (cyan==positions and index==selected) or not cyan,(choice,version,frame,index,'wrong orpartial selection highlight')
                    background=(0,165,172) if visible else (205,198,180)
                    assert all(im.getpixel(p)==background for p in positions),(choice,version,frame,index,'complete native background')
                    results.append(dict(option_index=index,label=labels[index],caption_origin=[x,y],logical_view=[width,12],complete_leading_internal_final_glyphs_andblank_guards_equal=True,independent_font_mask_sha256=sha(bytes(int((xx,yy) in ink) for yy in range(12) for xx in range(width))),native_background_pixels_exact=True,selected=index==selected,highlight_visible=visible))
                samples.append(dict(frame=frame,capture=photo,native_selected_option_expected_from_ordinary_input=selected,visible_selected_option_index=next((r['option_index'] for r in results if r['highlight_visible']),None),labels=results))
                pictures.append((f'{version} choice{choice} frame{frame}',im.crop((56,254,200,320))))
            groups.append(dict(version=version,choice=choice,capture_report=g['capture_report'],actual_menu_pair=interval,constructor_rectangle=rect,logical_width_px=width,labels=labels,samples=samples,source_controller_return_preserved=True))
    assert len(groups)==4 and sum(len(g['samples']) for g in groups)==12
    sheet=Image.new('RGB',(1152,480),'#263238');draw=ImageDraw.Draw(sheet)
    for i,(label,pic) in enumerate(pictures):
        x,y=i//3*288,i%3*160;draw.text((x+3,y+3),label,fill='white');sheet.paste(pic.resize((288,132),Image.Resampling.NEAREST),(x,y+23))
    ROOT.mkdir(parents=True);path=ROOT/'twelve_source_English_two_choice_menu_samples.png';sheet.save(path)
    save(ROOT/'actual_menu_RGB_glyph_geometry_highlight.json',dict(groups=groups,actual_runs_reused_without_replay=4,actual_menu_samples=12,complete_actual_caption_glyph_andbackground_checks=24,original_Japanese_andreviewed_English_two_choices_glyphs_centering_bounds_andselected_highlights_pass=True,source84_target72_constructor_based_coordinate_models_not_fit_from_glyph_pixels=True,selected_option0_andordinary_DOWN_option1_returns_match_original=True,all_captures_exact_ROM_inputs_readonly_callbacks_andwhole_source_payloads_bound_by_actual_audits=True,no_new_owner_pointer_RAM_VRAM_palette_orunowned_backing_byte_identity_claim=True,menu_backing_native_bounds_remain_the_separate_offline_native_plane_proof=str(MENU),physical_visible_output_verified_without_new_capture_orstate_changes=True,review_sheet=dict(path=str(path),sha256=sha(path.read_bytes())),direct_view_pending=True,later_transition_RNG_components_calendar_full_RGB_andsource_effect_semantics_separate_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [DEFAULT,OPPOSITION,DOC,SOURCE,MENU,Path(__file__)]}))
    print('Four existing runs:12actual menus/24complete source-Japanese andEnglish caption masks/backgrounds/highlights pass atnative84/72px geometry. Ordinary option0/1 returns preserved. No capture replay orlive owner/VRAM byte-identity claim.')
