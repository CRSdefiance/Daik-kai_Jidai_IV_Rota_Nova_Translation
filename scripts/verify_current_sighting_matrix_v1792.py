"""Current V1775 native expansion/wrap matrix and inherited exact-font planes."""
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.search_reports_editorial import current_entries
from scripts.probe_sighting_layout_v1070 import native_layout
from scripts.verify_arrival_native_v792 import prepared
from scripts.sighting_layout_v1069 import compiled
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/current_sighting_matrix_v1792')
ROM=Path('out/all_routes_combined_v1775_candidate.nds')
DOC=Path('translations/sighting_editorial_manuscript_v9.json')

if __name__=='__main__':
    assert not ROOT.exists()
    image=NdsImage.open(ROM);arm=image.read_file('/__arm9__.bin');font=image.read_file('/GRP/KANJI.FNT')
    doc=read(DOC);old=read(doc['native_font_proof']);assert sha(Path(doc['native_font_proof']).read_bytes())==doc['native_font_proof_sha256']
    assert len(old['cases'])==2700 and font==NdsImage.open('out/all_routes_combined_v1086_candidate.nds').read_file('/GRP/KANJI.FNT')
    rows={r['message_id']:r for r in doc['records']};entries=current_entries(image.read_file('/COMMON/MESFILE.DK4'),arm)
    assert all(entries[n].text==compiled(rows[n])for n in range(614,629))
    cpu=prepared(arm);cases=[];planes={};native=[]
    selected={max((i for i,r in enumerate(old['cases'])if r['message_ID']==n),key=lambda i:(max(old['cases'][i]['native_cell_widths']),len(old['cases'][i]['formatted_hex'])))for n in range(614,629)}
    class CurrentFont:
        @staticmethod
        def open(path):
            assert str(path)=='out/all_routes_combined_v255_candidate.nds'
            return image
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    ROOT.mkdir(parents=True)
    for index,prior in enumerate(old['cases']):
        n=prior['message_ID'];template=compiled(rows[n])
        value,lines=native_layout(cpu,template,n,bytes.fromhex(prior['bearing']['hex']),bytes.fromhex(prior['faction_hex']))
        assert value.hex()==prior['formatted_hex'] and lines==prior['lines'],(n,index)
        if value not in planes:
            pixels=independent_font(arm,font,lines);planes[value]=bytes(pixels)
        pixels=planes[value];assert sha(pixels)==prior['complete_native_font_plane_sha256']
        case={'case_index':index,'message_ID':n,'bearing_hex':prior['bearing']['hex'],'faction_hex':prior['faction_hex'],
            'formatted_hex':value.hex(),'lines':lines,'all_current_native_printf_wrap_ABI_and_guards_pass':True,
            'whole_current_independent_font_plane_equal_previously_verified_native_plane':True,
            'font_plane_sha256':sha(pixels)}
        cases.append(case)
        if index in selected:
            fresh=bytes(raster(arm,value,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000))
            assert fresh==pixels
            path=ROOT/f'current_full_native_ID{n}.png';Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in fresh)).save(path)
            native.append({**case,'fresh_current_full_native_plane_exact':True,'preview':str(path),'preview_sha256':sha(path.read_bytes())})
        if (index+1)%180==0:print({'ID':n,'current_native_cases':index+1},flush=True)
    assert len(cases)==2700 and len(native)==15
    sheets=[]
    for start in range(0,len(native),10):
        sheet=Image.new('RGB',(936,760),'#263238');draw=ImageDraw.Draw(sheet)
        for k,r in enumerate(native[start:start+10]):
            x,y=468*(k%2),152*(k//2);draw.text((x+5,y+3),f"Current ID{r['message_ID']} complete native plane",fill='white')
            im=Image.open(r['preview']);sheet.paste(im.resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
        path=ROOT/f'current_native_review_sheet{start//10+1}.png';sheet.save(path);sheets.append({'path':str(path),'sha256':sha(path.read_bytes())})
    save(ROOT/'current2700_native_wrap_and_font_reconciliation.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'ARM9_sha256':sha(arm),'COMMON_sha256':sha(image.read_file('/COMMON/MESFILE.DK4')),
        'manuscript':str(DOC),'manuscript_sha256':sha(DOC.read_bytes()),'cases':cases,
        'fresh_current_native_full_font_samples':native,'review_sheets':sheets,
        'all2700_current_native_expansions_and_wraps_equal_reviewed_outputs':True,
        'all2700_current_independent_font_planes_equal_prior_complete_native_planes':True,
        'all15_voice_variants_have_fresh_current_complete_native_font_plane':True,
        'entire_source_font_file_unchanged':True,'not2700_new_actual_gameplay_or_new_native_raster_runs':True,
        'visual_review_pending':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('2700 current printf/wrap cases andindependent full planes pass;15 fresh complete native font samples pass. Visual review pending.',flush=True)
