"""All 694 original-argument research font canvases, with no ROM build."""
from pathlib import Path
from types import FunctionType
from PIL import Image, ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_reinforcement_sniping_layout_v1030 import native_layout, TABLES
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/reinforcement_sniping_v1031')
MATRIX=Path('work/analysis/reinforcement_sniping_v1030/native_layout_matrix.json')
RUNTIME=Path('work/analysis/reinforcement_sniping_v1029/native_runtime_verification.json')
ARM=Path('work/analysis/reinforcement_sniping_v1025/ARM9_RUNTIME_RESEARCH_ONLY.bin')
ROM=Path('out/all_routes_combined_v997_candidate.nds')


def main():
    assert not ROOT.exists()
    matrix, runtime, arm=read(MATRIX), read(RUNTIME), ARM.read_bytes()
    assert sha(arm)==matrix['ARM9_sha256']==runtime['research_ARM9_sha256']
    assert len(matrix['cases'])==694 and not matrix['findings_requiring_review']
    assert sha(ROM.read_bytes())==matrix['candidate_sha256']==runtime['candidate_sha256']
    for path, digest in runtime['all_completed_source_proofs'].items():
        assert sha(Path(path).read_bytes())==digest
    rom=NdsImage.open(ROM);kanji=rom.read_file('/GRP/KANJI.FNT')
    class CurrentFont:
        @staticmethod
        def open(path):
            assert path=='out/all_routes_combined_v255_candidate.nds'
            return rom
    raster=FunctionType(original_raster.__code__, {**original_raster.__globals__, 'NdsImage':CurrentFont},
                        argdefs=original_raster.__defaults__)
    ROOT.mkdir(parents=True);(ROOT/'previews').mkdir()
    cases=[]
    for i, case in enumerate(matrix['cases']):
        value=case['argument_case'];n=case['message_ID']
        result,lines=native_layout(prepared(arm),bytes.fromhex(case['compiled_hex']),n,
                                  bytes.fromhex(value['hex']) if value else None,TABLES[case['source_family']])
        assert result.hex()==case['formatted_hex'] and lines==case['lines']
        pixels=raster(arm,result,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000)
        assert pixels==independent_font(arm,kanji,lines),(n,value)
        assert all(line==line.strip() and '  ' not in line for line in lines)
        path=ROOT/'previews'/f'ID{n}_variant{case["variant"]:02d}_complete_native.png'
        Image.frombytes('L',(228,64),bytes(0 if v else 255 for v in pixels)).save(path)
        cases.append({**case,'preview':str(path),'preview_sha256':sha(path.read_bytes()),
            'whole228x64_native_independent_font_and_input_bitmap_guards_pass':True,
            'all_leading_trailing_and_CP932_name_glyphs_complete':True,
            'uniform_x6_visible_row_origin_no_authored_indentation':True,
            'not_actual_gameplay_or_UI_RGB':True})
        if (i+1)%100==0:print(i+1,'complete native font canvases pass',flush=True)
    selected=[]
    for n in range(1911,1931):
        rows=[r for r in cases if r['message_ID']==n]
        choices=[rows[0],rows[-1]]
        if rows[0]['argument_case']:
            choices += [min(rows,key=lambda r:len(bytes.fromhex(r['argument_case']['hex']))),
                        max(rows,key=lambda r:len(bytes.fromhex(r['argument_case']['hex'])))]
            choices += [r for r in rows if bytes.fromhex(r['argument_case']['hex']).startswith(b'\x82\x65')][:1]
        for r in choices:
            if r not in selected:selected.append(r)
    sheets=[]
    for page,start in enumerate(range(0,len(selected),12)):
        sheet=Image.new('RGB',(936,912),'#263238');draw=ImageDraw.Draw(sheet)
        for k,case in enumerate(selected[start:start+12]):
            x,y=k%2*468,k//2*152
            label=(case['argument_case'] or {}).get('label','static')
            draw.text((x+5,y+3),f'ID{case["message_ID"]} / {label} / native only',fill='white')
            with Image.open(case['preview']) as im:
                sheet.paste(im.resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
        path=ROOT/f'review_page{page+1}.png';sheet.save(path)
        sheets.append({'path':str(path),'sha256':sha(path.read_bytes())})
    save(ROOT/'native_font_proof.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'research_ARM9':str(ARM),'research_ARM9_sha256':sha(arm),
        'matrix':str(MATRIX),'matrix_sha256':sha(MATRIX.read_bytes()),
        'runtime_proof':str(RUNTIME),'runtime_proof_sha256':sha(RUNTIME.read_bytes()),
        'cases':cases,'complete_native_font_canvases':len(cases),'boundary_findings':[],
        'native_exact_CP932_fullwidth_leading_F_preserved':True,
        'review_sheets':sheets,'visual_review_pending':True,
        'registered_repack_exact_patch_and_actual_gameplay_pending':True,
        'completed_entries_added':0,'full_goal_complete':False,'producer_sha256':sha(Path(__file__).read_bytes())})
    print(len(cases),'complete native fonts pass;',len(sheets),'visual sheets pending. No ROM built.',flush=True)


if __name__=='__main__':main()
