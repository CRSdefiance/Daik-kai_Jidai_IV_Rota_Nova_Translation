"""Current clean-source seven-voice review,567 layouts and22 fresh native planes."""
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import reinforcement_faction_prose as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_reinforcement_sniping_layout_v1030 import native_layout,TABLES
from scripts.reinforcement_sniping_layout_v1024 import compiled
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/covering_fire_current_v1818')
ROM=Path('out/all_routes_combined_v1807_candidate.nds')
DOC=Path('translations/reinforcement_sniping_editorial_manuscript_v4.json')
OLD=Path('work/analysis/current_reinforcement_matrix_v1801d/current694_native_wrap_and_font_reconciliation.json')

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    image=NdsImage.open(ROM);arm=image.read_file('/__arm9__.bin');common=image.read_file(owned.PATH);font=image.read_file('/GRP/KANJI.FNT')
    assert sha(ROM.read_bytes())==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    old=read(OLD);assert old['ARM9_sha256']==sha(arm)
    prior=NdsImage.open('out/all_routes_combined_v1775_candidate.nds');assert prior.read_file('/__arm9__.bin')==arm and prior.read_file('/GRP/KANJI.FNT')==font
    config=read(owned.CONFIG);current=owned.entries(common,arm,config['directory_sha256'])
    clean=NdsImage.open('work/clean.nds');clean_arm=clean.read_file('/__arm9__.bin');source=common_message_entries(clean.read_file(owned.PATH),clean_arm)
    assert arm[0x53F4C:0x53FE4]==clean_arm[0x53F4C:0x53FE4]
    assert arm[0x1173C0:0x1173E0]==clean_arm[0x1173C0:0x1173E0]
    rows={r['message_id']:r for r in read(DOC)['records']if 1917<=r['message_id']<=1923};reviewed=[]
    for n,row in rows.items():
        assert source[n].text.hex()==row['source_hex']and current[n].text==compiled(row)and all(row['review'].values())
        reviewed.append({'message_ID':n,'source_Japanese':source[n].text.decode('cp932'),'source_meaning':row['source_meaning'],
            'English':row['english'],'localization_note':row['localization_note'],'source_hex':source[n].text.hex(),
            'current_hex':current[n].text.hex(),'decision':row['editorial_decision']})
    original=[r for r in old['cases']if r['message_ID']in rows];assert len(original)==567
    selected={max((i for i,r in enumerate(original)if r['message_ID']==n),key=lambda i:len(original[i]['formatted_hex']))for n in rows}
    selected.update(i for i,r in enumerate(original)if r['argument_case']['hex'].startswith('8265'))
    selected.update(i for i,r in enumerate(original)if r['message_ID']==1917 and r['argument_case']['label']=='Manuel')
    assert len(selected)==22
    class CurrentFont:
        @staticmethod
        def open(path):
            assert str(path)=='out/all_routes_combined_v255_candidate.nds'
            return image
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    cpu=prepared(arm);cases=[];native=[]
    for index,prior_case in enumerate(original):
        n=prior_case['message_ID'];arg=bytes.fromhex(prior_case['argument_case']['hex'])
        result,lines=native_layout(cpu,current[n].text,n,arg,TABLES['covering_fire'])
        assert result.hex()==prior_case['formatted_hex']and lines==prior_case['lines']
        pixels=bytes(independent_font(arm,font,lines));assert sha(pixels)==prior_case['font_plane_sha256']
        row={'case_index':index,'message_ID':n,'argument_case':prior_case['argument_case'],'formatted_hex':result.hex(),'lines':lines,
            'font_plane_sha256':sha(pixels),'complete_current_printf_wrap_ABI_and_guards_pass':True,
            'current_independent_complete_plane_exact_to_previously_verified_current_native_plane':True}
        if index in selected:
            fresh=bytes(raster(arm,result,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000));assert fresh==pixels
            path=ROOT/f'current_complete_ID{n}_case{index}.png'
            Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in fresh)).save(path)
            row.update(preview=str(path),preview_sha256=sha(path.read_bytes()),fresh_current_native_complete_plane_exact=True)
            native.append(row)
        cases.append(row)
        if(index+1)%100==0:print({'current_covering_fire_layouts':index+1},flush=True)
    sheets=[]
    for start in range(0,len(native),10):
        sheet=Image.new('RGB',(936,760),'#263238');draw=ImageDraw.Draw(sheet)
        for k,r in enumerate(native[start:start+10]):
            x,y=468*(k%2),152*(k//2)
            draw.text((x+5,y+3),f"ID{r['message_ID']} / {r['argument_case']['label']}",fill='white')
            sheet.paste(Image.open(r['preview']).resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
        path=ROOT/f'current_review_sheet{start//10+1}.png';sheet.save(path);sheets.append({'path':str(path),'sha256':sha(path.read_bytes())})
    save(ROOT/'current567_layouts_and22_native_planes.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),'manuscript':str(DOC),'manuscript_sha256':sha(DOC.read_bytes()),
        'exact_clean_source_and_current_rows':reviewed,'cases':cases,'fresh_native_samples':native,'review_sheets':sheets,
        'all567_current_original_printf_wraps_and_complete_font_planes_pass':True,
        'seven_extreme_names14_fullwidth_F_names_and_one_actual_Manuel_native_planes_pass':True,
        'original_voice_selector_and_source_table_bytes_exact':True,'native_argument_kind':'compact commander label,not faction orfull character name',
        'no_new_ROM_or_completed_editorial_credit':True,'visual_review_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('567 current layouts/planes and22 fresh native raster samples pass;source/visual completion review pending.',flush=True)
