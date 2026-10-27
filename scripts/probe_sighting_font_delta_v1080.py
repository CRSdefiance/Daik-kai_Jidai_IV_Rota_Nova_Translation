"""Re-render the180 changed627 cases;retain2520 exact completed font proofs."""
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/sighting_fonts_v1080')
MATRIX=Path('work/analysis/sighting_layout_v1079/native_layout_matrix.json')
PRIOR=Path('work/analysis/sighting_fonts_v1075/native_font_proof.json')
ROM=Path('out/all_routes_combined_v1034_candidate.nds')


def main():
    assert not ROOT.exists()
    matrix,prior=read(MATRIX),read(PRIOR)
    assert len(matrix['cases'])==len(prior['cases'])==2700 and not matrix['findings_requiring_review']
    arm=Path(matrix['research_ARM9']).read_bytes();assert sha(arm)==prior['research_ARM9_sha256']==matrix['research_ARM9_sha256']
    rom=NdsImage.open(ROM);font=rom.read_file('/GRP/KANJI.FNT')
    class CurrentFont:
        @staticmethod
        def open(path):
            assert str(path)=='out/all_routes_combined_v255_candidate.nds'
            return rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    changed=[(i,r) for i,r in enumerate(matrix['cases']) if r['message_ID']==627]
    selected={changed[0][0],max(changed,key=lambda p:max(p[1]['native_cell_widths']))[0],
        min(changed,key=lambda p:len(bytes.fromhex(p[1]['faction_hex'])))[0],
        max(changed,key=lambda p:(len(p[1]['lines']),len(p[1]['lines'][-1])))[0]}
    ROOT.mkdir(parents=True);(ROOT/'previews').mkdir();cache={};cases=[];previews=[];inherited=0;rendered=0
    for i,(current,old) in enumerate(zip(matrix['cases'],prior['cases'],strict=True)):
        assert (current['message_ID'],current['bearing'],current['faction_hex'])==(old['message_ID'],old['bearing'],old['faction_hex'])
        if current['message_ID']!=627:
            assert current['compiled_hex']==old['compiled_hex'] and current['formatted_hex']==old['formatted_hex'] and current['lines']==old['lines']
            result={**old,'inherited_byte_exact_from_prior_complete_font_proof':True};inherited+=1
        else:
            value=bytes.fromhex(current['formatted_hex'])
            if value not in cache:
                pixels=raster(arm,value,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000)
                assert pixels==independent_font(arm,font,current['lines']);cache[value]=bytes(pixels)
            pixels=cache[value]
            result={**current,'complete_native_font_plane_sha256':sha(pixels),
                'whole228x64_native_and_independent_font_match':True,
                'complete_leading_trailing_letters_and_uniform_native_margin':True,'not_actual_gameplay_or_UI_RGB':True}
            rendered+=1
            if i in selected:
                path=ROOT/'previews'/f'ID627_case{i:04d}.png'
                Image.frombytes('L',(228,64),bytes(0 if v else 255 for v in pixels)).save(path)
                result.update(preview=str(path),preview_sha256=sha(path.read_bytes()));previews.append(result)
        cases.append(result)
    assert (inherited,rendered)==(2520,180)
    sheet=Image.new('RGB',(936,304),'#263238');draw=ImageDraw.Draw(sheet)
    for k,r in enumerate(previews):
        x,y=k%2*468,k//2*152
        draw.text((x+5,y+3),f'ID627 / {r["bearing"]["label"]} / '+bytes.fromhex(r['faction_hex']).decode('cp932'),fill='white')
        with Image.open(r['preview']) as im:sheet.paste(im.resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
    page=ROOT/'readaloud_review.png';sheet.save(page)
    save(ROOT/'native_font_proof.json',{'candidate':str(ROM),'candidate_sha256':matrix['candidate_sha256'],
        'matrix':str(MATRIX),'matrix_sha256':sha(MATRIX.read_bytes()),'manuscript':matrix['manuscript'],'manuscript_sha256':matrix['manuscript_sha256'],
        'research_ARM9':matrix['research_ARM9'],'research_ARM9_sha256':sha(arm),'source_font_proof':str(PRIOR),'source_font_proof_sha256':sha(PRIOR.read_bytes()),
        'cases':cases,'complete_native_font_cases':2700,'unchanged_cases_inherited_exact':inherited,'changed_cases_rerendered':rendered,
        'new_review_sheet':str(page),'new_review_sheet_sha256':sha(page.read_bytes()),'visual_review_pending':True,
        'no_source_prose_or_completion_credit_added':True,'registered_provider_copy_integration_and_actual_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('180 revised627 complete fonts pass;2520 other font cases remain exact. New read-aloud sheet pending.',flush=True)


if __name__=='__main__':main()
