"""Reject dropped ink, dropped shadow and extra marks in the two exact foreign cries."""
from pathlib import Path
from PIL import Image
from scripts import analyze_reviewed_opaque_fixture_v3 as model
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/Hodram_B0_B41_clean_20261107')

def main():
    out=ROOT/'opaque_pixel_model_qualification_v1.json';assert not out.exists()
    # The CLI normally supplies sha through its unchanged original analyzer imports.
    model.body_colors_exact.__globals__['sha']=sha
    native=load(ROOT/'storage_inputs_v2/native_pages.json');cases=[]
    for ident,frame in [('DK4_MES_B40_R0088',43560),('DK4_MES_B40_R0092',43800)]:
        row=next(x for x in native['records'] if x['id']==ident);page=row['complete_native_English_display']['pages'][0]
        expected=dict(page=1,text_hex=row['expanded_native_hex'],id=ident,
            native_plane_sha256=page['native_plane_sha256'],pixel_mask_sha256=sha(bytes(bool(v) for v in Path(page['native_plane']).read_bytes())))
        path=ROOT/f'bounded_capture_1_v1/frame_{frame:06d}_cold_boot.png';before=sha(path.read_bytes())
        crop=Image.open(path).convert('RGB').crop((16,296,232,360))
        assert model.body_colors_exact(crop,expected)
        plane=Path(page['native_plane']).read_bytes();points={v:next(i for i,n in enumerate(plane) if n==v) for v in [0,1,15]}
        for label,value,color in [('missing-ink',1,(255,0,255)),('missing-shadow',15,(255,0,255)),
                                  ('extra-ink',0,(0,8,0)),('extra-shadow',0,(197,198,197))]:
            changed=crop.copy();i=points[value];changed.putpixel((i%216,i//216),color)
            assert not model.body_colors_exact(changed,expected)
            cases.append(dict(id=ident,mutation=label,rejected=True))
        assert sha(path.read_bytes())==before
    save(out,dict(cases=cases,all8_mutations_rejected=True,independent_native_ink_andshadow_positions_exact=True,
        both_original_captures_accepted_without_modification=True,no_ROM_native_plane_orcapture_mutation=True,
        scoped_IDs=['DK4_MES_B40_R0088','DK4_MES_B40_R0092'],native_palette_mapping={'1':[0,8,0],'15':[197,198,197]},new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path(model.__file__),Path('scripts/analyze_reviewed_opaque_fixture_v1.py')]}))
    print('Both complete source-bound ink/shadow masks accepted;8 dropped/extra pixel mutations rejected. Original evidence unchanged.')

if __name__=='__main__':main()
