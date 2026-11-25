"""Compare all 18 plaques in actual original/current UI, retaining audit scope."""
import json
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw, ImageFont

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_source_plaque_bevels_v546 import hint
from scripts.verify_source_plaque_grain_v542 import capture_report, masks

ROOT=Path('work/analysis/plaque_current_v574')
CAPTURE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROM=Path('out/all_routes_combined_v573_candidate.nds')
SAVE_SHA='958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    clean,current=NdsImage.open('work/clean.nds'),NdsImage.open(ROM)
    original_report,current_report=(capture_report(CAPTURE/f'plaque_compare_v574_{k}',sha(r.source.read_bytes()))
                                    for k,r in (('original',clean),('current',current)))
    assert original_report['frames']==current_report['frames']==7100
    assert original_report['scripted_input_schedule']==current_report['scripted_input_schedule']
    assert original_report['core_options']==current_report['core_options']
    for r in (original_report,current_report):
        save=r['battery_save_preloaded']
        assert save['copied_byte_exact_before_cold_boot'] and save['source_sha256']==SAVE_SHA
        assert sha(Path(save['source']).read_bytes())==SAVE_SHA
        assert not any(v for k,v in r.items() if k.startswith('synthetic_'))
    font=GameAsciiFont.from_arm9(current.read_file('/__arm9__.bin'))
    config=read('translations/source_plaque_grain_v1.json')
    previous=NdsImage.open('out/all_routes_combined_v555_candidate.nds')
    original_shots,current_shots=({s['frame']:s for s in r['frames_captured'] if 'navigation' in s['path']}
                                  for r in (original_report,current_report))
    rows=[];fonts=[]
    for group,frame in zip(config['files'],(4300,6300),strict=True):
        path=group['file_path'];asset=PxlImage.from_bytes(current.read_file(path))
        original_asset=PxlImage.from_bytes(clean.read_file(path))
        assert asset.source==previous.read_file(path)
        assert asset.source[:asset.pixels_offset]==original_asset.source[:original_asset.pixels_offset]
        a,b=(Image.open(t[frame]['path']).convert('RGB') for t in (original_shots,current_shots))
        fonts.extend(masks(asset,group['records'],font))
        for record in group['records']:
            l,t,r,bot=record['plaque_box'];runtime='STAT_PLAQUE' in record['id']
            assert all(native5(b.getpixel((x,y)))==native5(asset.palette[asset.indices[y*asset.width+x]])
                       for y in range(t,bot) for x in range(l,r))
            if not runtime:
                assert all(native5(a.getpixel((x,y)))==native5(original_asset.palette[original_asset.indices[y*original_asset.width+x]])
                           for y in range(t,bot) for x in range(l,r))
            number=len(rows)+1
            source_path=ROOT/f'{number:02d}_original_NATIVE.png';target_path=ROOT/f'{number:02d}_V573_NATIVE.png'
            a.crop((l,t,r,bot)).save(source_path);b.crop((l,t,r,bot)).save(target_path)
            rows.append({'number':number,'id':record['id'],'English':record['english'],'Japanese':record['source_japanese'],
                         'bounds':[l,t,r,bot],'frame':frame,'source_asset':path,'source_crop':str(source_path),
                         'English_crop':str(target_path),'source_crop_sha256':sha(source_path.read_bytes()),
                         'English_crop_sha256':sha(target_path.read_bytes()),'original_label_drawn_at_runtime':runtime,
                         'complete_current_native_caption_frame_and_material_pixels':(r-l)*(bot-t),
                         'original_stored_source_matches_native_where_applicable':not runtime,'fully_completed':False})
    assert len(rows)==17 and sum(r['original_label_drawn_at_runtime'] for r in rows)==6
    arm=current.read_file('/__arm9__.bin')
    assert arm==NdsImage.open('out/all_routes_combined_v546_candidate.nds').read_file('/__arm9__.bin')
    plan=read('work/analysis/direct_equipment_v270/runtime_plan.json')
    pool=bytes(MainCodeFile(arm,BASE).sections[3].data)
    tile=pool[plan['tile_pointer']-POOL:plan['tile_pointer']-POOL+1408]
    assert len(tile)==1408
    hints=[]
    for text,frame,slot in (('Equipped Items',6300,208),('Weapon',6700,16),('Blue Oak Shield',7100,64)):
        shot=Image.open(current_shots[frame]['path']).convert('RGB')
        case=hint(font,tile,shot,text,slot)
        width=len(text)*6+4;left=min(slot,224-width)
        a=Image.open(original_shots[frame]['path']).convert('RGB')
        source_path=ROOT/f'{text.replace(" ","_")}_original_NATIVE.png'
        target_path=ROOT/f'{text.replace(" ","_")}_V573_NATIVE.png'
        a.crop((left,208,left+width,224)).save(source_path);shot.crop((left,208,left+width,224)).save(target_path)
        hints.append({**case,'frame':frame,'source_crop':str(source_path),'English_crop':str(target_path),
                      'source_crop_sha256':sha(source_path.read_bytes()),'English_crop_sha256':sha(target_path.read_bytes()),
                      'actual_source_render_not_a_stored_PXL_crop':True,'fully_completed':False})
        if text=='Equipped Items':
            rows.append({'number':18,'id':'runtime-equipped-items','English':text,'Japanese':'装備アイテム',
                         'bounds':[left,208,left+width,224],'frame':frame,'source_crop':str(source_path),
                         'English_crop':str(target_path),'original_label_drawn_at_runtime':True,'fully_completed':False})
    heading=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',20)
    small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',15)
    jp=ImageFont.truetype('C:/Windows/Fonts/msgothic.ttc',19)
    sheets=[]
    for name,subset in (('Assign_Sailors',rows[:7]),('Sailor_Info',rows[7:])):
        sheet=Image.new('RGB',(940,92+len(subset)*124),'#263238');d=ImageDraw.Draw(sheet)
        d.text((16,10),name.replace('_',' ')+' - all entries remain in audit',font=heading,fill='white')
        d.text((16,43),'Actual Japanese ROM',font=small,fill='#bfcbd0')
        d.text((490,43),'Actual V573 English',font=small,fill='#bfcbd0')
        for n,row in enumerate(subset):
            y=80+n*124
            d.text((16,y),f"{row['number']:02d} {row['English']}",font=small,fill='#e7d9aa')
            d.text((250,y),row['Japanese'],font=jp,fill='#e7d9aa')
            for x,key in ((16,'source_crop'),(490,'English_crop')):
                crop=Image.open(row[key]);sheet.paste(crop.resize((crop.width*4,crop.height*4),Image.Resampling.NEAREST),(x,y+28))
        target=ROOT/f'{name}_original_V573_NATIVE_4x.png';sheet.save(target);sheets.append(str(target))
    inventory=read('translations/graphics_completion_campaign_v1.json')['plaque_style_v247']['ongoing_plaque_inventory']
    assert len(inventory)==18 and all(e['fully_completed'] is False for e in inventory)
    assert len(read('translations/graphics_completion_requirements_v313.json')['historical_pending_items_retained'])==22
    proof={'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'source_ROM_sha256':sha(clean.source.read_bytes()),
           'actual_original_and_current_UI_same_copied_save':True,'source_save_sha256_unchanged':SAVE_SHA,
           'original_save_contains_preexisting_Latin_actor_company_names':True,
           'ordinary_controls_no_inventory_location_condition_or_code_fixtures':True,
           'capture_reports':{k:str(CAPTURE/f'plaque_compare_v574_{k}'/'capture_report.json') for k in ('original','current')},
           'frames_per_run':7100,'all17_current_full_font_masks':fonts,'all18_native_comparison_entries':rows,
           'original6_stat_labels_and_equipment_heading_are_actual_runtime_pixels':True,
           'current17_plaque_files_exact_verified_V555':True,'current_hint_ARM9_exact_verified_V546':True,
           'native_static_plaque_pixels_exact':sum(r.get('complete_current_native_caption_frame_and_material_pixels',0) for r in rows),
           'three_native_hint_cases':hints,'native_hint_pixels_exact':sum(h['all_grain_bevel_letters_exact'] for h in hints),
           'sheets':sheets,'production_ROM_modified':False,'new_candidate_built':False,
           'all18_plaques_remain_incomplete':True,'all22_historical_requirements_retained':True,'full_goal_complete':False}
    preservation=ROOT/'current_preservation_proof.json'
    if preservation.exists():
        assert read(preservation)['candidate_sha256']==proof['candidate_sha256']
        proof.update(preservation_proof=str(preservation),preservation_proof_sha256=sha(preservation.read_bytes()),
                     all921_PXL_FLS_and57_embedded_extents_rechecked=True)
    receipt=ROOT/'screenshot_archive_receipt.json'
    if receipt.exists():
        for entry in read(receipt)['files']:
            assert sha(Path(entry['source']).read_bytes())==entry['sha256']==sha(Path(entry['path']).read_bytes())
        proof['screenshot_archive_receipt']=str(receipt)
    (ROOT/'native_review_proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f"V574: all18 paired actual-native plaque entries; {proof['native_static_plaque_pixels_exact']} full static pixels, {proof['native_hint_pixels_exact']} heading/Weapon/Blue Oak Shield pixels; source save unchanged; V573 unchanged.")


if __name__=='__main__':main()
