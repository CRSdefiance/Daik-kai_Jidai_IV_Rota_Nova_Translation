"""Compare actual source/English owned caption backing and both input-selected highlights."""
import struct
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.trace_file_ids_v683 import mapped_read
from scripts.square_shopkeeper_font_oracles_v7020 import PROGRESSIVE_ORACLE_SOURCE
from scripts.verify_name_catalog_glyphs_v278 import expected_pixels as old_expected
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B46_menu_actual_v7950c')
ACTUAL=Path('work/analysis/Rafael_B46_actual_v7948/four_runs24_unique_speeches58_occurrences_two_choices_actual_body_name_FE_return_audit.json')
CHOICES=Path('work/analysis/Rafael_B46_choice_planes_v7934/two_labels8_native_style_planes_trimmed_native_width_andthree_returns.json')
if __name__=='__main__':
    assert not ROOT.exists();actual,choices=map(read,[ACTUAL,CHOICES]);assert not actual['unresolved']
    env={**old_expected.__globals__,'WIDTH':256,'HEIGHT':36}
    exec(compile(PROGRESSIVE_ORACLE_SOURCE,__file__+'::independent-current-font-owned-caption-backing','exec'),env)
    oracle=env['expected_pixels'];ROOT.mkdir(parents=True);groups=[];unresolved=[]
    sheet=Image.new('RGB',(1152,480),'#263238');draw=ImageDraw.Draw(sheet)
    for gi,g in enumerate(actual['groups']):
        version,choice=g['version'],g['choice'];run=Path('work/analysis/Rafael_B46_scene_runs_v7945')/f'route0_{version}_{choice}'
        terminal=read(run/'terminal.json');op=Path(terminal['menu_observer']);owner=read(op)
        assert sha(op.read_bytes())==terminal['menu_observer_sha256'] and not owner['errors'] and not owner['mismatches']
        assert owner['all_host_slots_restored_and_core_file_exact'] and owner['read_only_argument_observation_not_emulated_code_or_memory_edit']
        report=read(g['capture_report']);photos={p['frame']:p for p in report['frames_captured']}
        image=NdsImage.open(g['fixture']['research_ROM']);arm,fnt=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT')
        assert sha(arm)=='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
        labels=g['fixture']['original_menu_records'];width=84 if version=='clean_Japanese' else 66
        flow=read('work/analysis/Rafael_B46_menu_flow_v7925/two_choice_native_forwarding_four_relative_sites_accept22_decline7_source_scope.json')
        native_rect=(flow['source_menu_versions'][0]['native_VM'] if version=='clean_Japanese' else choices['native_target_VM'])['native_menu_rectangle']
        assert native_rect[1:4:2]==[64,128] and native_rect[2]-native_rect[0]==width+32
        pointers={r['backing_pointer'] for r in owner['rows']};assert len(pointers)==1;pointer=next(iter(pointers))
        style_rows=[]
        for r in owner['rows']:
            index=next(l['option_index'] for l in labels if l['label_hex']==r['text_hex'])
            assert r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
            assert r['context_words'][3:5]==[width,12] and r['context_words'][12]==8
            assert r['view_words'][7:9]==[0,index*12] and r['view_words'][10:12]==[width,12]
            assert r['bitmap_header_words'][:3]==[4,64,36] and r['backing_bytes']==4608
            assert r['backing_pointer']==r['bitmap_header_address']+r['bitmap_header_words'][4]
            assert sha(Path(r['backing']).read_bytes())==r['backing_sha256']
            style_rows.append(dict(frame=r['frame'],option_index=index,logical_view=[width,12],source_view_origin=[0,index*12],style=8))
        events=[];label_masks=[]
        for label in labels:
            raw=bytes.fromhex(label['label_hex']);index=label['option_index'];points=codes(raw)
            text_width=sum(6 if c<128 else 12 for c in points);x=(width-text_width)//2
            one=[dict(kind='ascii' if c<128 else 'cp932',code=c,style=8,x=x+sum(6 if v<128 else 12 for v in points[:i]),y=index*12) for i,c in enumerate(points)]
            events.extend(one)
            page=oracle(arm,fnt,[dict(e,y=0) for e in one],canvas_height=12)
            mask={(i%256,i//256) for i,b in enumerate(page) if b}
            assert all(0<=xx<width and 0<=yy<12 for xx,yy in mask)
            label_masks.append(mask)
        expected=oracle(arm,fnt,events,canvas_height=36)
        owned=[y*256+x for y in range(24) for x in range(width)]
        expected_owned=bytes(expected[i] for i in owned);sp=Path(terminal['readonly_menu_snapshots'])
        assert sha(sp.read_bytes())==terminal['readonly_menu_snapshots_sha256'];snapshots=read(sp);samples=[]
        assert [s['frame'] for s in snapshots]==[4810,4870,4930]
        for si,s in enumerate(snapshots):
            frame=s['frame'];assert g['actual_menu_pair']['start']<frame<g['actual_menu_pair']['returned']
            files=s['files'];data={}
            for k,p in files.items():
                value=Path(p['path']).read_bytes();assert len(value)==p['bytes'] and sha(value)==p['sha256'];data[k]=value
            assert s['all_CPU_WRAM_DTCM_ITCM_andconfiguration_exact_before_after_readonly_export']
            packed=mapped_read(data['WRAM'],data['DTCM'],s['DTCM_base'],pointer,4608)
            pixels=bytes(v for b in packed for v in [b&15,b>>4])
            found_owned=bytes(pixels[i] for i in owned);assert found_owned==expected_owned,(version,choice,frame,'owned backing')
            unowned=sum(pixels[i]!=expected[i] for i in range(len(pixels)) if i not in set(owned))
            photo=photos[frame];assert sha(Path(photo['path']).read_bytes())==photo['PNG_sha256']
            im=Image.open(photo['path']).convert('RGB');selected=1 if choice=='decline' and frame>4905 else 0
            cases=[]
            x=native_rect[0]+16;assert x==(256-width)//2
            for index,ink in enumerate(label_masks):
                y=192+native_rect[1]+16+20*index
                actual_black={(xx-x,yy-y) for yy in range(y-1,y+13) for xx in range(x-2,x+width+2) if im.getpixel((xx,yy))==(8,8,8)}
                assert actual_black==ink,(version,choice,frame,index,'visible glyph mask')
                cyan={(xx,yy) for yy in range(y-4,y+16) for xx in range(x,x+width) if im.getpixel((xx,yy))==(0,165,172)}
                want={(xx,yy) for yy in range(y-4,y+16) for xx in range(x,x+width)}-{(x+xx,y+yy) for xx,yy in ink} if index==selected else set()
                positions={(xx,yy) for yy in range(y-4,y+16) for xx in range(x,x+width)}-{(x+xx,y+yy) for xx,yy in ink}
                highlight_visible=bool(cyan)
                assert (cyan==positions and index==selected) or not cyan,(version,choice,frame,index,'partial orwrong highlight')
                background=(0,165,172) if highlight_visible else (205,198,180)
                assert all(im.getpixel(p)==background for p in positions),(version,choice,frame,index,'background glyph guard')
                cases.append(dict(option_index=index,label=labels[index]['label'],caption_origin=[x,y],caption_size=[width,12],
                    full_visible_black_glyph_mask_andblank_guards_equal=True,exact_native_background_pixels_equal=True,selected_highlight_visible=highlight_visible,selected=index==selected))
            samples.append(dict(frame=frame,selected_option_index=selected,visible_selected_option_index=next((c['option_index'] for c in cases if c['selected_highlight_visible']),None),actual_owned_pixels_sha256=sha(found_owned),independent_owned_pixels_sha256=sha(expected_owned),
                actual_full_physical_plane_sha256=sha(pixels),unowned_physical_differences=unowned,
                no_claim_that_unowned_backing_is_blank_oridentical=True,capture=photo,labels=cases))
            draw.text((gi*288+3,si*160+3),f'{version} {choice} frame{frame}',fill='white')
            sheet.paste(im.crop((56,254,200,320)).resize((288,132),Image.Resampling.NEAREST),(gi*288,si*160+23))
        groups.append(dict(version=version,choice=choice,menu_native_result=g['actual_menu_pair']['native_result'],
            owner_observation=str(op),owner_observation_sha256=sha(op.read_bytes()),caption_owner_bindings=style_rows,
            actual_physical_backing=[256,36],actual_caption_view=[width,12],original_native_menu_rectangle=native_rect,samples=samples,
            actual_full_source_orEnglish_labels_visible_withmeasured_selection_state=not unresolved,
            independent_current_font_owned_backing_andall_visible_pixels_equal=True))
    assert len(groups)==4 and sum(len(g['samples']) for g in groups)==12
    for g in groups:
        visible={s['visible_selected_option_index'] for s in g['samples'] if s['visible_selected_option_index'] is not None}
        assert visible==({0} if g['choice']=='accept' else {0,1})
    off=[dict(version=g['version'],choice=g['choice'],frame=s['frame'],logical_selected_option=s['selected_option_index'])
        for g in groups for s in g['samples'] if s['visible_selected_option_index'] is None]
    assert off==[dict(version='clean_Japanese',choice='accept',frame=4930,logical_selected_option=0)]
    path=ROOT/'source_English_both_choices_three_actual_menu_holds.png';sheet.save(path)
    save(ROOT/'four_actual_menus12_full_owned_backing_andhighlight_samples.json',dict(
        actual_body_proof=str(ACTUAL),actual_body_proof_sha256=sha(ACTUAL.read_bytes()),groups=groups,unresolved=unresolved,
        original_source84_target66_constructor_widths_and256x36_backing_confirmed=True,
        all24_visible_source_English_label_samples_full_first_internal_final_glyphs_bounds_andnative_backgrounds_exact=True,source_highlight_off_samples=off,exact_cross_language_highlight_phase_equality_not_claimed=True,
        all_owned_caption_backing_matches_independent_CP932_ASCII_font_oracle=True,
        actual_ordinary_input_selection0_accept1_decline_matches_original_VM_results=True,
        source_owned_independent_oracle=PROGRESSIVE_ORACLE_SOURCE,
        unowned_physical_bytes_measured_without_blank_orequality_claim=True,
        review_sheet=dict(path=str(path),sha256=sha(path.read_bytes())),visual_review_pending=True,
        no_new_emulator_runs_orstate_orcontroller_orfont_changes=True,
        evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,CHOICES,Path(__file__)]},
        new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Four actual menus/12 backing samples/24 labels pass fullglyphs andexact native backgrounds;both logical highlights observed. One source4930 highlight-off sample retained,not phase equality. Sheet view pending.')
