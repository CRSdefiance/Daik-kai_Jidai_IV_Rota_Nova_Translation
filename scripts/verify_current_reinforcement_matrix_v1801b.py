"""Reconcile the current20 source-reviewed announcements and694 native layouts."""
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.search_reports_editorial import current_entries
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_reinforcement_sniping_layout_v1030 import native_layout,TABLES
from scripts.reinforcement_sniping_layout_v1024 import compiled
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/current_reinforcement_matrix_v1801b')
ROM=Path('out/all_routes_combined_v1775_candidate.nds')
DOC=Path('translations/reinforcement_sniping_editorial_manuscript_v2.json')

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    image=NdsImage.open(ROM);arm=image.read_file('/__arm9__.bin');font=image.read_file('/GRP/KANJI.FNT')
    doc=read(DOC);old=read(doc['native_font_proof']);assert sha(Path(doc['native_font_proof']).read_bytes())==doc['native_font_proof_sha256']
    assert len(old['cases'])==694
    source=NdsImage.open('work/clean.nds');jp=common_message_entries(source.read_file('/COMMON/MESFILE.DK4'),source.read_file('/__arm9__.bin'))
    current=current_entries(image.read_file('/COMMON/MESFILE.DK4'),arm);rows={r['message_id']:r for r in doc['records']}
    reviewed=[]
    for n,row in rows.items():
        assert jp[n].text.hex()==row['source_hex']and current[n].text==compiled(row)
        assert all(row['review'].get(g)for g in('source','context','localization','naturalness','formatting'))
        reviewed.append({'message_ID':n,'source_reference':{'block':jp[n].block,'block_offset':jp[n].block_offset,
            'table_offset':jp[n].table_offset},'source_hex':jp[n].text.hex(),'source_Japanese':jp[n].text.decode('cp932'),
            'current_reference':{'block':current[n].block,'block_offset':current[n].block_offset,'table_offset':current[n].table_offset},
            'current_hex':current[n].text.hex(),'English':row['english'],'source_meaning':row['source_meaning'],
            'localization_note':row['localization_note'],'decision':row['editorial_decision']})
    assert sorted(rows)==list(range(1911,1931))
    class CurrentFont:
        @staticmethod
        def open(path):
            assert str(path)=='out/all_routes_combined_v255_candidate.nds'
            return image
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    cpu=prepared(arm);cases=[];native=[]
    selected={max((i for i,r in enumerate(old['cases'])if r['message_ID']==n),
        key=lambda i:len(old['cases'][i]['formatted_hex']))for n in rows}
    for index,prior in enumerate(old['cases']):
        n=prior['message_ID'];argument=prior['argument_case'];template=compiled(rows[n])
        result,lines=native_layout(cpu,template,n,bytes.fromhex(argument['hex'])if argument else None,TABLES[prior['source_family']])
        assert template.hex()==prior['compiled_hex']and result.hex()==prior['formatted_hex']and lines==prior['lines']
        preview=Path(prior['preview']);assert sha(preview.read_bytes())==prior['preview_sha256']
        pixels=bytes(independent_font(arm,font,lines));plane=Image.open(preview).convert('L');assert plane.size==(228,64)
        assert all(v in(0,255)for v in plane.getdata())
        assert pixels==bytes(1 if p==0 else 0 for p in plane.getdata())
        case={'case_index':index,'message_ID':n,'argument_case':argument,'formatted_hex':result.hex(),'lines':lines,
            'complete_current_printf_wrap_ABI_and_guards_pass':True,'current_independent_plane_equal_prior_complete_native_mask':True,
            'font_plane_sha256':sha(pixels)};cases.append(case)
        if index in selected:
            fresh=bytes(raster(arm,result,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000))
            assert fresh==pixels
            path=ROOT/f'current_complete_native_ID{n}.png'
            Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in fresh)).save(path)
            native.append({**case,'fresh_current_native_plane_exact':True,'preview':str(path),'preview_sha256':sha(path.read_bytes())})
        if(index+1)%100==0:print({'current_native_cases':index+1},flush=True)
    assert len(cases)==694 and len(native)==20
    sheets=[]
    for start in range(0,20,10):
        sheet=Image.new('RGB',(936,760),'#263238');draw=ImageDraw.Draw(sheet)
        for k,r in enumerate(native[start:start+10]):
            x,y=468*(k%2),152*(k//2);draw.text((x+5,y+3),f"Current ID{r['message_ID']} complete native plane",fill='white')
            sheet.paste(Image.open(r['preview']).resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
        path=ROOT/f'current_native_review_sheet{start//10+1}.png';sheet.save(path);sheets.append({'path':str(path),'sha256':sha(path.read_bytes())})
    save(ROOT/'current694_native_wrap_and_font_reconciliation.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'ARM9_sha256':sha(arm),'COMMON_sha256':sha(image.read_file('/COMMON/MESFILE.DK4')),'manuscript':str(DOC),
        'manuscript_sha256':sha(DOC.read_bytes()),'reviewed20_exact_source_and_current_entries':reviewed,'cases':cases,
        'fresh_current_complete_native_font_samples':native,'review_sheets':sheets,
        'all694_current_original_printf_wraps_and_independent_complete_font_masks_equal_prior_native_canvases':True,
        'all20_voice_variants_have_fresh_current_complete_native_rasters':True,'not694_new_native_raster_runs_or_actual_visits':True,
        'visual_review_pending':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('694 current native layouts andindependent complete masks pass;20 fresh native rasters pass. Visual review pending.',flush=True)
