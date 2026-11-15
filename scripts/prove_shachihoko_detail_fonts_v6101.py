"""Both native item-detail consumers in4/16-bit modes;all fields,glyphs,pixels and parent crops."""
import inspect,struct
from copy import deepcopy
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.execute_scene_caption_raster import execute as old_execute
from scripts.verify_item_interface_research import expected_draws,glyph_codes
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels as old_expected
from scripts.probe_item_parent_crops import verify as parent_crops
from scripts.verify_item_parent_layout import EXPECTED,compose
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shachihoko_detail_fonts_v6101')
RECEIPT=Path('work/analysis/shachihoko_item116_research_v6094/coordinated_research_receipt.json')
BIND=Path('work/analysis/shachihoko_description_consumers_v6092/current218_live_description_getters_two_item_callers_and_exact_owned_representations.json')

def oracle():
    source=inspect.getsource(old_expected);at=source.index('        if code not in mapping:');prefix=source[:at];assert prefix.count('canvas[y + row][x + column]')==2
    prefix=prefix.replace('canvas[y + row][x + column]','canvas[y + row + 1][x + column]');adapted=prefix+source[at:]
    assert __import__('scripts.source_locked_derivation_v5118',fromlist=['native_numbers']).native_numbers(source)==__import__('scripts.source_locked_derivation_v5118',fromlist=['native_numbers']).native_numbers(adapted)
    env=dict(old_expected.__globals__);exec(compile(adapted,__file__+'::current-ascii-ink-independent-pixels','exec'),env)
    return env['expected_pixels'],adapted

if __name__=='__main__':
    assert not ROOT.exists();receipt,binding=map(read,[RECEIPT,BIND]);data=receipt['data_plan'];expected,oracle_source=oracle();cases=[];photos=[];parents=[];by={}
    adapted=checked_text(inspect.getsource(old_execute),{
        'from dk4tool.script.common_message_table import DIRECTORY_OFFSET, common_message_entries':'from dk4tool.script.common_message_table import DIRECTORY_OFFSET\n            from dk4tool.patch.duel_editorial import owned_entries as current_owned_entries',
        'entries = common_message_entries(item_common, source, clean=False)':'entries = current_owned_entries(item_common, source, CURRENT_DIRECTORY_SHA256)',
    })
    for version,path,directory in [('parent',receipt['parent'],binding['COMMON_directory_sha256']),('target',receipt['research_ROM'],data['new_directory_sha256'])]:
        image=NdsImage.open(path);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4');font=image.read_file('/GRP/KANJI.FNT');plan=deepcopy(read('work/analysis/item_interface_plan.json'))
        env={**old_execute.__globals__,'CURRENT_DIRECTORY_SHA256':directory};exec(compile(adapted,__file__+'::exact-current-COMMON-directory','exec'),env);execute=env['execute']
        if version=='target':plan['item_advice_projection'][116].update(logical=data['description'],compiled='\n'.join(data['compiled_rows']),pointer=data['new_compiled_pointer'])
        parent=parent_crops(arm);assert [(r['source_origin'],r['size'],r['destination_origin']) for r in parent['requests']]==EXPECTED;parents.append(dict(version=version,native=parent))
        for ident in [115,116,117]:
            for page in ['main','standalone']:
                for mode in [4,16]:
                    config=(0,4 if page=='main' else 1);native=execute(arm,'fixture',item_page=page,item_case=config,surface_size=(240,96),kanji_font=font,mode=mode,item_resource_index=ident,item_common=common)
                    draws=expected_draws(arm,plan,page,config,item_index=ident);assert native['item_draws']==draws
                    codes=[code for draw in draws for code in glyph_codes(draw['text'],draw['tracking'])];assert [r['code'] for r in native['glyph_events']]==codes
                    assert native['pixels']==expected(arm,font,native['glyph_events'],mode,background=0)
                    assert all(0<=r['x'] and r['x']+(6 if r['kind']=='ascii' else 12)<=240 and 0<=r['y'] and r['y']+12<=96 for r in native['glyph_events'])
                    paragraph=[r['text'] for r in draws if r['y']>=(36 if page=='main' else 24) and r['y']<84]
                    expected_lines=plan['item_advice_projection'][ident]['compiled'].splitlines();assert paragraph==expected_lines
                    composed,cells=compose(native,parent['requests']) if page=='main' else (None,[])
                    row=dict(version=version,item_ID=ident,page=page,mode=mode,draws=draws,glyph_events=native['glyph_events'],glyph_count=len(codes),
                        full_native_plane_sha256=sha(native['pixels']),complete_fields_words_first_final_interior_glyphs_bounds_and_independent_pixels_pass=True,
                        native_selected_COMMON_IDs=native['item_actual_common_ids'],paragraph_rows=paragraph,parent_complete_glyph_cells=cells,
                        parent_whole_plane_sha256=sha(composed) if composed else None,native_provider_contracts=native['item_provider_contracts'])
                    cases.append(row);by[version,ident,page,mode]=native['pixels']
                    if mode==16 and ident==116:
                        pixels=composed if composed else native['pixels'];im=Image.new('RGB',(256,192));im.putdata([(230,222,197) if x==0 else (110,100,85) if x==14 else (0,0,0) for x in struct.unpack('<49152H',pixels)]);photos.append((version+' '+page,im))
    assert len(cases)==24
    for ident in [115,117]:
        for page in ['main','standalone']:
            for mode in [4,16]:assert by['parent',ident,page,mode]==by['target',ident,page,mode]
    ROOT.mkdir(parents=True);sheet=Image.new('RGB',(1040,840),'#263238');draw=ImageDraw.Draw(sheet)
    for i,(label,im) in enumerate(photos):
        x,y=i%2*520,i//2*420;draw.text((x+4,y+3),label+' native CPU text/parent;artwork boundary',fill='white');sheet.paste(im.resize((512,384),Image.Resampling.NEAREST),(x+4,y+24))
    picture=ROOT/'both_native_item116_detail_consumers.png';sheet.save(picture)
    save(ROOT/'both_detail_consumers_three_items_two_modes_complete_native_planes.json',dict(cases=cases,native_parent_versions=parents,
        all24_native_field_word_glyph_pixel_bounds_and_parent_crop_cases_pass=True,all16_unselected_neighbor_item_planes_exact=True,
        all_four_target_item116_detail_planes_have_complete_three_row_description=True,
        current_native_ascii_ink_y_plus_one_independent_oracle=True,only_source_font_model_offset_rebound_no_metrics_width_or_clip_change=True,
        original240x96_geometry_minus_one_tracking_three_row_limits_and_parent_crops_preserved=True,
        explicit_source_warm_COMMON_cache_view_font_origin_artwork_and_item_metadata_provider_contracts=True,
        native_COMMON_loader_selection_and_private_override_independently_run_on_actual_snapshot_in6098=True,
        not_actual_GPU_gameplay_item_menu_or_earned_inventory=True,no_full_route_hardware_or_complete_effect_claim=True,
        sheet=str(picture),sheet_sha256=sha(picture.read_bytes()),visual_review_pending=True,
        source_locked_current_directory_adapter=adapted,independent_current_font_oracle_source=oracle_source,
        new_emulator_runs=0,new_review_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [RECEIPT,BIND,Path(__file__),Path('scripts/execute_scene_caption_raster.py'),Path('scripts/probe_map_tooltip_cp932_pixels.py')]}))
    print('24 complete native detail planes pass;both modes/both consumers/three items,all16 neighbor planes unchanged. Target description has3 complete rows;original parent crops preserve every glyph. Visual review pending.')
