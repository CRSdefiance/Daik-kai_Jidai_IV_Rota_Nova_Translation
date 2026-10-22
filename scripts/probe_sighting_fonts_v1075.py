"""Complete native-font planes for2700 reviewed sighting expansions; no live claim."""
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/sighting_fonts_v1075')
MATRIX=Path('work/analysis/sighting_layout_v1074/native_layout_matrix.json')
ROM=Path('out/all_routes_combined_v1034_candidate.nds')


def main():
    assert not ROOT.exists()
    matrix=read(MATRIX);assert len(matrix['cases'])==2700 and not matrix['findings_requiring_review']
    assert sha(Path(matrix['manuscript']).read_bytes())==matrix['manuscript_sha256']
    arm=Path(matrix['research_ARM9']).read_bytes();assert sha(arm)==matrix['research_ARM9_sha256']
    rom=NdsImage.open(ROM);assert sha(ROM.read_bytes())==matrix['candidate_sha256']
    font=rom.read_file('/GRP/KANJI.FNT')
    class CurrentFont:
        @staticmethod
        def open(path):
            assert str(path)=='out/all_routes_combined_v255_candidate.nds'
            return rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},
        argdefs=original_raster.__defaults__)
    selected=set()
    for n in range(614,629):
        rows=[(i,r) for i,r in enumerate(matrix['cases']) if r['message_ID']==n]
        selected.add(rows[0][0])
        selected.add(max(rows,key=lambda p:(max(p[1]['native_cell_widths']),len(bytes.fromhex(p[1]['faction_hex']))))[0])
        selected.add(max(rows,key=lambda p:(len(p[1]['lines']),len(p[1]['lines'][-1])))[0])
        selected.add(min(rows,key=lambda p:len(bytes.fromhex(p[1]['faction_hex'])))[0])
    ROOT.mkdir(parents=True);(ROOT/'previews').mkdir()
    cases=[];cache={};previews=[]
    for i,case in enumerate(matrix['cases']):
        formatted=bytes.fromhex(case['formatted_hex'])
        if formatted not in cache:
            pixels=raster(arm,formatted,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000)
            assert pixels==independent_font(arm,font,case['lines'])
            cache[formatted]=bytes(pixels)
        pixels=cache[formatted]
        result={**case,'complete_native_font_plane_sha256':sha(pixels),
            'whole228x64_native_and_independent_font_match':True,
            'complete_leading_trailing_letters_and_uniform_native_margin':True,'not_actual_gameplay_or_UI_RGB':True}
        if i in selected:
            p=ROOT/'previews'/f'ID{case["message_ID"]}_case{i:04d}.png'
            Image.frombytes('L',(228,64),bytes(0 if v else 255 for v in pixels)).save(p)
            result.update(preview=str(p),preview_sha256=sha(p.read_bytes()));previews.append(result)
        cases.append(result)
        if (i+1)%100==0:print(i+1,'complete native sighting font cases pass',flush=True)
    sheets=[]
    for page,start in enumerate(range(0,len(previews),12)):
        sheet=Image.new('RGB',(936,912),'#263238');draw=ImageDraw.Draw(sheet)
        for k,case in enumerate(previews[start:start+12]):
            x,y=k%2*468,k//2*152
            faction=bytes.fromhex(case['faction_hex']).decode('cp932')
            draw.text((x+5,y+3),f'ID{case["message_ID"]} / {case["bearing"]["label"]} / {faction}',fill='white')
            with Image.open(case['preview']) as im:sheet.paste(im.resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
        path=ROOT/f'review_page{page+1}.png';sheet.save(path);sheets.append({'path':str(path),'sha256':sha(path.read_bytes())})
    save(ROOT/'native_font_proof.json',{'candidate':str(ROM),'candidate_sha256':matrix['candidate_sha256'],
        'matrix':str(MATRIX),'matrix_sha256':sha(MATRIX.read_bytes()),'research_ARM9':matrix['research_ARM9'],
        'research_ARM9_sha256':sha(arm),'cases':cases,'complete_native_font_cases':len(cases),
        'unique_complete_font_planes':len(cache),'preview_images':len(previews),'review_sheets':sheets,
        'visual_review_pending':True,'runtime_selector_ABI_regressions_registered_integration_and_actual_pending':True,
        'formatting_gates_not_approved':True,'no_ROM_or_live_RAM_change':True,'completed_entries_added':0,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('2700 complete native fonts pass;',len(sheets),'visual sheets pending. No ROM built.',flush=True)


if __name__=='__main__':main()
