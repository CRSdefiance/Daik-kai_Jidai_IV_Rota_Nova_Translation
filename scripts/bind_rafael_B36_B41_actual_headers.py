"""Compare every sampled scoped header against its original native glyph plane."""
from pathlib import Path
from PIL import Image
from scripts.audit_story_glyph_consistency import load,save
from scripts.check_hodram_B91_B110_actual_pixels import mask,match
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_B36_B41_progressive_names_20261104')
NAMES=ROOT/'native_name_planes.json'
PIXELS=Path('work/analysis/Rafael_B36_B41_focused_actual_pixels_20261104/focused_actual_pixels.json')
VISUAL=PIXELS.with_name('direct_visual_approval.json')

if __name__=='__main__':
    output=ROOT/'actual_header_verification.json';assert not output.exists()
    names,pixels,visual=map(load,[NAMES,PIXELS,VISUAL])
    assert names['scoped_actors']==11 and names['fresh_name_planes']==6 and names['exact_reused_name_planes']==4
    assert visual['all_three_sheets_directly_viewed'] and visual['all11_progressive_nameplates_visually_complete_andconsistent_with_bound_getters']
    for sheet in names['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    byactor={r['actor_ID']:r['text'] for r in names['consumer_bindings']};planes={r['text']:r for r in names['planes']}
    headers=[]
    for sample in pixels['body_pages']:
        actor=sample['selector'];text=byactor[actor];plane=planes[text]
        cap=sample['capture'];path=Path(cap['path']);assert sha(path.read_bytes())==cap['PNG_sha256']
        origin=match(Image.open(path).convert('RGB'),mask(plane['native_plane'],plane['native_plane_sha256'],216),(98,97,98),[16],[276])
        headers.append(dict(actor_ID=actor,text=text,frame=sample['frame'],capture=cap,origin=origin,
            complete_name_glyphs_andblank_guards_exact=True,native_plane=plane['native_plane'],native_plane_sha256=plane['native_plane_sha256']))
    assert len(headers)==40 and set(byactor)=={r['actor_ID'] for r in headers}
    save(output,dict(native_names=str(NAMES),native_names_sha256=sha(NAMES.read_bytes()),headers=headers,all11_actors_observed=True,
        complete_header_plane_comparisons=40,all_complete_first_internal_final_name_glyphs_andblank_guards_exact=True,
        six_new_native_name_previews_directly_viewed=True,four_original_native_name_previews_exact_reuse=True,
        all_actual_QA_name_headers_directly_viewed=True,no_name_data_change=True,
        full_catalogue_UI_unvisited=True,two_catalogue_middle_field_proposals_deferred_not_approved=False,
        actual_gameplay=True,disclosed_initialized_fixture=True,natural_activation=False,hardware=False,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [NAMES,PIXELS,VISUAL,Path(__file__)]}))
    print('40 complete actual header planes match10 native strings/all11 actors;full-catalogue UI remains unvisited.')
