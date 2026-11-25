"""Bind focused actual names, paragraphs, personality alternatives and three highlights."""
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.check_hodram_B91_B110_actual_pixels import mask,match

ROOT=Path('work/analysis/Hodram_B111_B130_actual_pixels_20261102')
NATIVE=Path('work/analysis/Hodram_B111_B130_editorial_20261101/native_v3/compiled_native_pages.json')
NAME=Path('work/analysis/Hodram_B111_B130_name_native_20261101/native_name_fields_verification_reviewed.json')
MENU=Path('work/analysis/Hodram_B111_B130_editorial_20261101/menu_v1/menu_provider_and_planes_reviewed.json')

def capture(block,frame):
    path=Path(f'work/emulation_v193/Hodram_B111_B130_English_20261102_B{block}/capture_report.json');report=load(path)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert sha(Path(report['ROM']).read_bytes())==report['ROM_sha256']
    record=next(r for r in report['frames_captured'] if r['frame']==frame)
    image=Path(record['path']);assert sha(image.read_bytes())==record['PNG_sha256']
    return Image.open(image).convert('RGB'),dict(block=block,frame=frame,capture_report=str(path),capture_report_sha256=sha(path.read_bytes()),capture=record)

def main():
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    native,name,menu=map(load,[NATIVE,NAME,MENU]);headers=[];bodies=[];captions=[]
    plane=next(p for p in name['planes'] if p['version']=='proposed' and p['text']=='Follower' and p['style']==11)
    ink=mask(plane['plane'],plane['plane_sha256'],216)
    for frame in [4460,7820,9500,10220,10700]:
        image,ref=capture(115,frame);origin=match(image,ink,(98,97,98),[16],[276])
        headers.append(dict(**ref,actor=178,label='Follower',origin=origin,normal_F_andall_name_glyphs_andblank_guards_exact=True))
    cases=[
        (115,10940,'DK4_MES_B115_R0174',1),(115,11420,'DK4_MES_B115_R0182',1),(115,12380,'DK4_MES_B115_R0196',1),
        (117,4700,'DK4_MES_B117_R0016',1),(117,5660,'DK4_MES_B117_R0031',1),(117,5900,'DK4_MES_B117_R0031',2),
        (118,3980,'DK4_MES_B118_R0007',1),(118,4700,'DK4_MES_B118_R0018',1),(118,4940,'DK4_MES_B118_R0022',1),
        (118,5520,'DK4_MES_B118_R0087',1),(118,5760,'DK4_MES_B118_R0091',1),(118,6000,'DK4_MES_B118_R0094',1),(118,6240,'DK4_MES_B118_R0098',1),
        (125,4460,'SC1_B125_STYLE_54_170',1),(125,4940,'SC1_B125_STYLE_450_238',1),
        (126,4460,'DK4_MES_B126_R0013',1),(126,4940,'DK4_MES_B126_R0021',1),(126,5180,'DK4_MES_B126_R0026',1),
        (126,5420,'DK4_MES_B126_R0029',1),(126,5900,'DK4_MES_B126_R0038',1),(126,6620,'DK4_MES_B126_R0049',1),
    ]
    rows={r['id']:r for r in native['records']}
    for block,frame,ident,number in cases:
        row=rows[ident];rendered=row['complete_native_English_display'];is_FE=row['kind']=='system-FE'
        page=rendered if is_FE else rendered['pages'][number-1]
        ink=mask(page['native_plane'],page['native_plane_sha256'],228 if is_FE else 216)
        image,ref=capture(block,frame);origin=match(image,ink,(0,8,0),[16],[296])
        bodies.append(dict(**ref,id=ident,page=number,kind=row['kind'],origin=origin,measured_story_ink_RGB=[0,8,0],
            complete_native_glyph_plane_andblank_guards_equal=True,bounded_framebuffer_alignment_only_no_backing_owner_claim=True))
    proof=next(m for m in menu['menus'] if m['block']==118)
    vm=proof['versions'][-1]['cases'][0]['native_VM'];width=vm['minimum_width_units']*6;rect=vm['native_menu_rectangle'];x=rect[0]+16
    for frame,wanted in [(5300,0),(5320,1),(5360,2)]:
        image,ref=capture(118,frame);labels=[];selected=[]
        for index in range(3):
            plane=next(p for p in menu['records'] if p['block']==118 and p['version']=='reviewed-English' and p['option']==index and p['style']==1)
            ink=mask(plane['path'],plane['sha256'],width);y=192+rect[1]+16+20*index
            assert match(image,ink,(8,8,8),[x],[y])==[x,y]
            positions={(xx,yy) for yy in range(y-4,y+16) for xx in range(x,x+width)}-{(x+xx,y+yy) for xx,yy in ink}
            cyan={p for p in positions if image.getpixel(p)==(0,165,172)}
            assert cyan==(positions if index==wanted else set())
            assert all(image.getpixel(p)==((0,165,172) if index==wanted else (205,198,180)) for p in positions)
            if cyan:selected.append(index)
            labels.append(dict(index=index,text=vm['labels'][index],origin=[x,y],complete_caption_glyphs_andblank_guards_exact=True,
                complete_selected_orunselected_rectangle_RGB_exact=True,selected=index==wanted))
        assert selected==[wanted]
        captions.append(dict(**ref,labels=labels,selected_option=wanted,all_three_complete_caption_glyphs_andblank_guards_exact=True,all_highlight_background_RGB_exact=True))
    save(ROOT/'focused_actual_pixels.json',dict(name_headers=headers,body_pages=bodies,menu_samples=captions,
        name_headers_checked=5,body_pages_checked=21,menu_caption_instances_checked=9,
        actual_Rafael0_complete_source_preamble_andfive_distinct_bodies_observed=True,
        native_FI_Hodram_expansion_observed=True,source_personality_voice4_variants_observed=True,
        lamp_both_pages_andwhole_final_sentence_observed=True,bean_question_four_rows_no_unintended_blank=True,
        ordinary_three_choice_controller_highlights_andcorrect59_branch_observed=True,
        actual_gameplay=True,disclosed_initialized_fixtures=True,natural_activation=False,hardware_verification=False,
        read_only_framebuffer_comparisons=True,whole_live_RAM_VRAM_backing_palette_orregister_ownership_not_claimed=True,
        Diogo_full_catalogue_UI_unvisited=True,other_variants_andmenus_not_individually_activated=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [NATIVE,NAME,MENU,Path(__file__)]}))
    print('PASS5 Follower headers/21 body pages/9 caption instances;all three complete highlights match native masks. No backing ownership orfull conditional coverage claim.')

if __name__=='__main__':main()
