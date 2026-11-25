"""Bind the single source right-cell model; preserve every English216px andnative terminal guard."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
if __name__=='__main__':
    root=Path('work/analysis/maria_story_actual_tools_v7752c');assert not root.exists()
    binding=Path('work/analysis/maria_B35_source_rightcell_v7753/source_question_mark_actual_position_binding.json');b=read(binding)
    assert sha(Path(b['corrected_source_font']).read_bytes())==b['corrected_source_font_sha256']
    old,new=read(b['source_font']),read(b['corrected_source_font']);assert old['name_planes']==new['name_planes']
    assert [r for r in old['source_records'] if r['id']!='DK4_MES_B35_R0065']==[r for r in new['source_records'] if r['id']!='DK4_MES_B35_R0065']
    for a,c in zip(old['source_records'],new['source_records'],strict=True):
        assert a['id']==c['id'] and a['source_body_hex']==c['source_body_hex'] and a['original_current_expanded_source_hex']==c['original_current_expanded_source_hex']
    result=derive('scripts/audit_Maria_story_scenes_v7752b.py','scripts/audit_Maria_story_scenes_v7752c.py',{
        'maria_story_actual_v7752b':'maria_story_actual_v7752c',
        'work/analysis/maria_story_source_name_planes_v7751/67_clean_source_native_pages8_complete_name_planes32_literal_alignments.json':
        'work/analysis/maria_B35_source_rightcell_v7753/67_source_native_pages8_name_planes_R65_actual_rightcell_bound.json',
        'def masks(image):':"RIGHTCELL=Path('work/analysis/maria_B35_source_rightcell_v7753/source_question_mark_actual_position_binding.json')\ndef masks(image,width=216):",
        'image.crop((16,296,232,360))':'image.crop((16,296,16+width,360))',
        'return {color:{(i%216,i//216)':'return {color:{(i%width,i//width)',
        "photos[photo['frame']]=dict(reference=photo,image=im,masks=masks(im))":
        "photos[photo['frame']]=dict(reference=photo,image=im,masks=masks(im),source_rightcell_masks=masks(im,228) if version=='clean_Japanese' and blocknumber==35 else None)",
        "black={(i%216,i//216) for i,b in enumerate(pixels) if b==1};gray={(i%216,i//216) for i,b in enumerate(pixels) if b==15}":
        "width=page.get('native_viewport_width',216);assert width in [216,228]\n                black={(i%width,i//width) for i,b in enumerate(pixels) if b==1};gray={(i%width,i//width) for i,b in enumerate(pixels) if b==15}",
        "cp=expected_pixels(arm,nativefont,[e for e in page['events'] if e['kind']=='cp932'])":
        "if width==228:\n                    assert version=='clean_Japanese' and blocknumber==35 and record['id']=='DK4_MES_B35_R0065' and all(e['kind']=='cp932' or e['code']==32 for e in page['events'])\n                    assert sha(FONT.read_bytes())==read(RIGHTCELL)['corrected_source_font_sha256'];cp=pixels\n                else:cp=expected_pixels(arm,nativefont,[e for e in page['events'] if e['kind']=='cp932'])",
        "cpgray={(i%216,i//216)":"cpgray={(i%width,i//width)",
        "models.append(dict(page=page,black=black":"models.append(dict(page=page,width=width,black=black",
        "found=photo['masks'];candidate=":"found=photo['source_rightcell_masks'] if models[0]['width']==228 else photo['masks'];candidate=",
        '[FIXTURES,FONT,STORED,CURRENT,Path(__file__)]':'[FIXTURES,FONT,STORED,CURRENT,RIGHTCELL,Path(__file__)]',
    })
    root.mkdir(parents=True);save(root/'source_locked_single_source_rightcell_audit.json',dict(
        derivation=result,rightcell_binding=str(binding),rightcell_binding_sha256=sha(binding.read_bytes()),
        all_other66_source_planes_andall8_name_planes_exact=True,
        all67_English216px_black_ASCIIgray_CP932gray_andheader_guards_exact=True,
        original_type0_plus_previous_value_carry_terminal_guard_preserved=True,
        no_source_English_captures_ROMS_dialogue_controls_orcredit_changed=True,full_goal_complete=False))
    print('Frozen7752c:only original Japanese R65 uses measured228px glyph cellspan.All English216px andtype0/value-carry guards unchanged.No capture rerun.')
