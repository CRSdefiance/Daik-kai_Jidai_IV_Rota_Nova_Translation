"""Match every actual title/notice hold to complete native glyph planes and independent fonts."""
import inspect,struct
from pathlib import Path
from PIL import Image
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_name_catalog_glyphs_v278 import raster
from scripts.lil_current_font_oracles_v5918 import _expected
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shachihoko_actual_name_glyphs_v6086')
ACTUAL=Path('work/analysis/shachihoko_B204_card_actual_v6084c/complete_source_path_and_unmasked_title_acquisition_prompt_frame_differences.json')
GETTERS=Path('work/analysis/shachihoko_item_consumers_v6081b/all218_item_getters_two_original_callers_and_complete_native_title_plane.json')

def tracked_model(arm,events):
    font=GameAsciiFont.from_arm9(arm);pixels=bytearray(216*64);occupied_ink=set()
    for e in events:
        assert e['kind']=='ascii' and e['y']==0 and 0<=e['x'] and e['x']+6<=88
        cleared={(e['x']+x,y) for y in range(12) for x in range(6)}
        assert not cleared&occupied_ink,'tracking may overlap empty cell edges only,never prior ink'
        for x,y in cleared:pixels[y*216+x]=0
        cell=font.decode(chr(e['code']))
        for y in range(11):
            for x in range(6):
                if cell.getpixel((x,y)):
                    point=(e['x']+x,y+1);assert point not in occupied_ink;occupied_ink.add(point);pixels[point[1]*216+point[0]]=e['style']
    return bytes(pixels)

if __name__=='__main__':
    assert not ROOT.exists();actual,getters=map(read,[ACTUAL,GETTERS]);assert getters['only_item116_native_and_static_title_outputs_change']
    adapted=checked_text(inspect.getsource(raster),{'    events = []':'    cpu.mem_write(ctx+0x1C, struct.pack("<I", TRACKING_WORD))\n    events = []'})
    env={**raster.__globals__,'TRACKING_WORD':0xFFFFFFFF};exec(compile(adapted,__file__+'::source-established-item-tracking','exec'),env)
    cases=[]
    for case,rompath,word in [('parent','out/lil_B204_source_v6070_clean_Japanese_RESEARCH_ONLY.nds',b'Orca Figurehead'),('target','out/shachihoko_B204_card_v6082_clean_Japanese_RESEARCH_ONLY.nds',b'Shachihoko')]:
        rom=NdsImage.open(rompath);arm=rom.read_file('/__arm9__.bin');assert sha(arm)==getters['data_only_source_preservation_plan'][('source' if case=='parent' else 'target')+'_ARM9_sha256']
        for kind,tracking,text,origin,width,color in [('item_title',-1,word,(88,236),88,(230,230,230)),('acquisition_notice_text',0,word+b' acquired!',(16,296),216,(0,8,0))]:
            pixels,events,font=(env['raster'] if tracking==-1 else raster)(arm,text)
            assert pixels==(tracked_model(arm,events) if tracking==-1 else _expected(arm,font,events))
            emitted=text+(b' ' if tracking==0 and len(text)%2 else b'')
            assert [r['code'] for r in events]==list(emitted) and all(r['x']==i*(5 if tracking==-1 else 6) and r['y']==0 for i,r in enumerate(events))
            model={(i%216,i//216) for i,v in enumerate(pixels) if v};assert all(0<=x<width and 0<=y<12 for x,y in model)
            holds=[]
            for r in actual['whole_frames_with_measured_differences']:
                if not r['measured_difference_pixel_counts'][kind]:continue
                path=Path(r[case]);assert sha(path.read_bytes())==r[case+'_sha256'];im=Image.open(path).convert('RGB')
                observed={(x,y) for y in range(12) for x in range(width) if im.getpixel((origin[0]+x,origin[1]+y))==color}
                assert observed==model,(case,kind,r['frame'],len(observed^model));holds.append(dict(frame=r['frame'],PNG=str(path),PNG_sha256=sha(path.read_bytes()),whole_expected_foreground_mask_exact=True))
            assert holds
            if kind=='acquisition_notice_text':assert [r['frame'] for r in holds]==[5530,5590,5650,5710]
            cases.append(dict(case=case,kind=kind,text_hex=text.hex(),native_events=events,native_complete_plane_sha256=sha(pixels),origin=list(origin),measured_RGB_foreground=list(color),complete_native_and_independent_first_final_and_all_interior_glyphs_exact=True,all_actual_holds=holds))
    ROOT.mkdir(parents=True);save(ROOT/'four_native_planes_and_all_actual_title_notice_holds_match.json',dict(cases=cases,
        all_four_complete_native_and_independent_planes_match_actual_RGB_foreground=True,
        original_item_title_negative_one_tracking_and_notice_zero_tracking_distinguished=True,
        original216x64_raster_view_metrics_font_and_code_unchanged=True,negative_one_tracking_overlaps_only_blank_edges_not_glyph_ink=True,
        source_item_title15_and_target10_characters_and_complete_notice_substitution_observed=True,
        no_new_stored_story_object_or_generic_notice_editorial_approval=True,
        original_name_pointers_tables_code_and_other_item_names_bound_by_getters_proof=str(GETTERS),
        item_list_menu_full_effects_COMMON_description_and_registered_release_pending=True,
        actual_source_fixture_location_event_activation_full_route_and_hardware_limits_retained=True,
        timing_RNG_and_advance_prompt_differences_preserved_in_actual_proof=str(ACTUAL),
        new_emulator_runs=0,new_review_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,GETTERS,Path(__file__),Path('scripts/verify_name_catalog_glyphs_v278.py'),Path('scripts/lil_current_font_oracles_v5918.py')]},source_owned_tracking_adapter=adapted))
    print('Four native+independent planes match all actual title/notice holds. Title -1 tracking and notice0 tracking distinguished;first/final/all interior glyphs complete;no new editorial credit.')
