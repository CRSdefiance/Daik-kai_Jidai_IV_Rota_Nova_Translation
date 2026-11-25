"""Keep the full unmasked timing/state audit while adding distinct FE body and absent-name checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B211_actual_tools_v6569')
PANEL='''        ref=refs[at];record=st[ref['id']];pages=record['complete_pages']['pages'];assert len(pages)==1;page=pages[0];pixels=Path(page['native_plane']).read_bytes();assert sha(pixels)==page['native_plane_sha256'];fe=ref['source_selector']==254;width=228 if fe else 216;assert len(pixels)==width*64;ink={(i%width,i//width) for i,b in enumerate(pixels) if b==1};gray={(i%width,i//width) for i,b in enumerate(pixels) if b==15};complete=[];partial=[];nameholds=[];absenceholds=[]
        if fe:
            srcpanel=next(p for p in source['speech_observations'] if p['id']==ref['id']);srcphoto=srcpanel['selected_capture'];srcpic=Image.open(srcphoto['path']).convert('RGB');assert sha(Path(srcphoto['path']).read_bytes())==srcphoto['PNG_sha256'];expected_absent_region=srcpic.crop((0,192,256,294)).tobytes()
        else:
            namepixels,namewidth=nameplanes[ref['source_selector']];nameink={(i%216,i//216) for i,b in enumerate(namepixels) if b}
        for frame,(photo,im) in photos.items():
            if not entry['frame']+20<frame<row['frame']-4:continue
            crop=im.crop((16,296,16+width,360));body={(i%width,i//width) for i,c in enumerate(crop.getdata()) if c==(0,8,0)};shadow={(i%width,i//width) for i,c in enumerate(crop.getdata()) if c==(98,97,98)}
            if not fe:
                header={(x-4,y) for y in range(13) for x in range(namewidth+8) if im.getpixel((12+x,276+y))==(98,97,98)}
                if header!=nameink:failures.append(dict(id=ref['id'],frame=frame,kind='nameplate',missing=len(nameink-header),extra=len(header-nameink)))
                else:nameholds.append(dict(frame=frame,capture=photo['path'],sha256=photo['PNG_sha256'],complete_native_name_and_blank_guards_equal=True))
            if body==ink and shadow==gray:
                hold=dict(frame=frame,capture=photo['path'],sha256=photo['PNG_sha256'],complete_independent_native_body_ink_gray_and_all_glyphs_equal=True);complete.append(hold)
                if fe:
                    equal=im.crop((0,192,256,294)).tobytes()==expected_absent_region
                    if not equal:failures.append(dict(id=ref['id'],frame=frame,kind='FE-source-correct-absent-portrait-and-nameplate'))
                    else:absenceholds.append(dict(**hold,original_null_actor_absent_portrait_and_nameplate_region=[0,192,256,294],source_correct_absence_equal=True))
            else:partial.append(dict(frame=frame,missing=len(ink-body),extra=len(body-ink),gray_missing=len(gray-shadow),gray_extra=len(shadow-gray),incomplete_progressive_or_transition_frame=True))
        assert complete and (absenceholds if fe else nameholds),ref['id'];panels.append(dict(id=ref['id'],source_record_index=ref['source_record_index'],source_selector=ref['source_selector'],kind='system-FE' if fe else 'progressive',interval=pair,native_pages=1,complete_body_holds=complete,complete_name_holds=nameholds,complete_FE_absence_holds=absenceholds,incomplete_progressive_holds=partial,selected_complete_capture=complete[-1]))'''
if __name__=='__main__':
    assert not ROOT.exists();path=Path('scripts/audit_lil_B210_actual_v6522.py');text=path.read_text('utf-8');a=text.index('        ref=refs[at];record=');b=text.index('\n    assert len(panels)==10',a);oldpanel=text[a:b]
    changes={oldpanel:PANEL,
        'lil_B210_source_actual_v6510/all10_source_panels_all21_commands_and_observed_return.json':'lil_B211_source_actual_v6561/all12_source_panels_all23_commands_and_observed_return.json',
        'lil_B210_stored_v6514/all10_final_stored_targets40_alignment_cases_and10_complete_pages.json':'lil_B211_stored_v6565/all12_final_stored_targets48_alignments_and12_complete_pages.json',
        'lil_B210_name_source_planes_v6511/four_name_planes32_literal_alignments_all_source_headers_and_ten_Japanese_body_masks.json':'lil_B211_name_source_planes_v6562/four_name_planes32_alignments_all_source_headers_nine_Japanese_progressive_body_masks.json',
        'B210':'B211','actual_v6522':'actual_v6569','English_run_v6517':'English_run_v6568','English_fixture_v6516':'English_fixture_v6567','lil_B207_name_style_v6354d':'Al_Ferid_name_style_v6520',
        "labels={2:'Lil Argot',17:'Al Shin'}":"labels={2:'Lil Argot',7:'Cristina Erneco'}",'all12_source_commands_retained':'all14_source_commands_retained','source_event210':'source_event211',
        'len(panels)==10 and len(pairs)==21':'len(panels)==12 and len(pairs)==23','all21_stored_fixture_commands':'all23_stored_fixture_commands',"pairs[-1]['source_offset']==682":"pairs[-1]['source_offset']==636",'range(0,10,6)':'range(0,12,6)','all10_complete_English_panels_sheet':'all12_complete_English_panels_sheet',
        'all10_English_objects_native_body_name_holds21_commands':'all12_English_objects_native_body_FE_absence_name_holds23_commands','actual_unique_objects=10,actual_complete_native_pages=10':'actual_unique_objects=12,actual_complete_native_pages=12','all21_stored_commands_observed':'all23_stored_commands_observed','all12_original_commands_nine':'all14_original_commands_nine',
        'complete_native_name_holds=sum(len(p[\'complete_name_holds\']) for p in panels)':'complete_native_name_holds=sum(len(p[\'complete_name_holds\']) for p in panels),complete_FE_absence_holds=sum(len(p[\'complete_FE_absence_holds\']) for p in panels),actual_progressive_objects=9,actual_FE_objects=3',
        'name_field_typography_fix_is_separate_unapplied_in_these_content_fixtures':'no_new_name_asset_edit_both_fixtures_inherit_same_V6541_name_data','natural_event210':'natural_event211','actual_objects=10,pages=10':'actual_objects=12,pages=12','commands=21':'commands=23'}
    assert all(k in text for k in changes);proof=derive(str(path),'scripts/audit_lil_B211_actual_v6569.py',changes);ROOT.mkdir(parents=True);save(ROOT/'source_locked_actual_audit.json',dict(proof=proof,full_timing_RNG_duration_same_frame_RGB_and_five_final_native_groups_retained=True,distinct_FE228x64_ink_gray_and_source_correct_absent_portrait_name_region_checks_added=True,no_pixel_edit_masking_retiming_forced_state_or_weaker_native_guard=True,all_native_high_integer_constants_and_multiplicity_preserved=True,full_goal_complete=False))
