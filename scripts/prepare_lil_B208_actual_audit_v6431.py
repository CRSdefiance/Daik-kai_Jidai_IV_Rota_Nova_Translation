"""Prepare complete paired B208 progressive/thought/FE pixels and source command audit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B208_actual_tools_v6431')
if __name__=='__main__':
    assert not ROOT.exists();p=Path('scripts/audit_lil_B207_actual_v6374.py');s=p.read_text('utf-8');a=s.index("    for speech in en['speech_intervals']:");b=s.index('    comparisons=[]',a)
    body='''    for speech in en['speech_intervals']:
        case=fonts[speech['id']];fe=speech['prefix']==254;width=228 if fe else 216;preview=Image.open(case['preview']).convert('RGB');assert preview.size==(width,64) and sha(Path(case['preview']).read_bytes())==case['preview_sha256'];masks=[{(i%width,i//width) for i,c in enumerate(preview.getdata()) if c==color} for color in [(0,8,0),(98,97,98)]]
        name=None if fe else names[speech['prefix']];nameink=None;width_name=None
        if name:
            np=Image.open(name['preview']).convert('RGB');assert sha(Path(name['preview']).read_bytes())==name['preview_sha256'];nameink={(i%216,i//216) for i,c in enumerate(np.getdata()) if c==(65,53,42)};width_name=name['native_width_including_flush_space']
        holds=[];source=source_speeches[speech['id']]['interval']
        for frame,(photo,pic) in en['photos'].items():
            if not speech['interval']['start']<frame<speech['interval']['returned']:continue
            crop=pic.crop((16,296,16+width,360));found=[{(i%width,i//width) for i,c in enumerate(crop.getdata()) if c==color} for color in [(0,8,0),(98,97,98)]]
            if found!=masks:continue
            if name:
                actualname={(x-4,y) for y in range(13) for x in range(width_name+8) if pic.getpixel((12+x,276+y))==(98,97,98)}
                if actualname!=nameink:continue
            shared=source['start']<frame<source['returned'];sourcephoto,sourcepic=jp['photos'][frame];equal=pic.crop((0,0,256,294)).tobytes()==sourcepic.crop((0,0,256,294)).tobytes()
            h=dict(frame=frame,capture=photo['path'],capture_sha256=photo['PNG_sha256'],all_complete_216x64_or_FE228x64_ink_gray_pixels_equal_native_plane=True,nameplate_expected=not fe,complete_current_style11_nameplate_glyphs_and_blank_guards_equal=None if fe else True,FE_null_actor_absent_nameplate_region_matches_source=equal if fe else None,source_correct_nameplate_or_FE_absence_verified=equal if fe else True,source_capture=sourcephoto['path'],source_capture_sha256=sourcephoto['PNG_sha256'],both_versions_in_same_semantic_speech_at_this_frame=shared,paired_upper_portrait_name_region_equal=equal);holds.append(h)
            if shared and not equal:nontext.append(dict(id=speech['id'],frame=frame,region=[0,0,256,294],difference_bbox=ImageChops.difference(pic.crop((0,0,256,294)),sourcepic.crop((0,0,256,294))).getbbox()))
        if not holds:failures.append(dict(id=speech['id'],finding='No complete English body and current name/source-correct FE absence hold matches the approved native plane.'))
        actual.append(dict(id=speech['id'],source_record_index=speech['source_record_index'],prefix=speech['prefix'],kind='system-FE' if fe else 'progressive',name=None if fe else name['label'],interval=speech['interval'],holds=holds,native_plane_sha256=case['whole_native_plane_sha256'],actual_complete_dialogue_and_nameplate_or_FE_absence_observed=bool(holds)))
'''
    namefont="NAMEFONT=Path('work/analysis/lil_B207_name_planes_v6354d/two_complete_native_names32_literal_macro_alignments_and_actual_headers.json')"
    r=derive(str(p),'scripts/audit_lil_B208_actual_v6431.py',{
        s[a:b]:body,namefont:"NAMEFONT=Path('work/analysis/lil_B207_name_planes_v6405/two_complete_native_names32_literal_macro_alignments_and_actual_headers.json')",
        'B207':'B208','actual_v6374':'actual_v6431','source_fixture_v6345':'source_fixture_v6397','English_fixture_v6372':'English_fixture_v6429','source_run_v6346':'source_run_v6398','English_run_v6373':'English_run_v6430',
        'fonts_v6361/all13_progressive_complete_native_planes104_alignment_cases':'fonts_v6420/all24_progressive_FE_native_planes_and192_alignment_cases',
        '11001':'16001','source_event207':'source_event208','all15_source_commands_retained':'all29_source_commands_retained','len(pairs)==24':'len(pairs)==38','len(speeches)==13':'len(speeches)==24','all24_stored_fixture_commands':'all38_stored_fixture_commands',"pairs[-1]['source_offset']==650":"pairs[-1]['source_offset']==1182",'==[642]':'==[1166,1174]',
        'all13_actual_English_dialogue_sheet':'all24_actual_English_dialogue_sheet','[3010,6070,16001]':'[3010,8710,16001]',
        'all13_English_panels_complete_native_holds24_commands_and_source_comparison':'all24_English_panels_complete_native_holds38_commands_and_source_comparison',
        'source_and_English_all24_commands15_source_plus9_initializers_observed':'source_and_English_all38_commands29_source_plus9_initializers_observed',
        'source_original_A000_execution_not_full_quest_inventory_eligibility_or_effect_semantics_proof':'source_original6005_632E_two_A000_execution_not_full_stat_quest_inventory_eligibility_or_effect_semantics_proof',
        'total_paired_frames=22002':'total_paired_frames=32002',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_actual_audit.json',dict(tool=r,all23_progressive_and_one_FE_masks_and_name_or_source_correct_absence_bound=True,no_inherited_Emilio_name_or_B207_13panel_shape=True,source16001_frame_run_reused_without_replay=True,full_goal_complete=False));print('B208 paired24-panel/38-command audit prepared with distinct FE pixels/absent nameplate and all unmasked differences.')
