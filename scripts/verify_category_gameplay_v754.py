"""Actual full category730 text, unchanged compact Square menus and return."""

from pathlib import Path

from PIL import Image, ImageChops

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_category_trend_fixture_v754 import assign
from scripts.verify_category_lookup_v754 import ROOT
from scripts.verify_specialty_gameplay_v752 import snapshot
from scripts.verify_village_wrap_v608 import read, save

CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
SAVE_SHA='d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'


def captures(folder,frames,product=None):
    report=read(CAP/folder/'capture_report.json')
    assert report['frames']==frames and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report['hardware_device_verification']
    assert report['core_DLL_sha256']=='42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert sha(Path(report['ROM']).read_bytes())==report['ROM_sha256']
    fixtures=report.get('synthetic_category_trend_fixtures',[])
    assert len(fixtures)==int(product is not None)
    assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k!='synthetic_category_trend_fixtures')
    if product is not None:
        donor=report['battery_save_preloaded'];assert donor['source']!=donor['destination']
        assert sha(Path(donor['source']).read_bytes())==donor['source_sha256']==SAVE_SHA
        assert donor['copied_byte_exact_before_cold_boot']
        arm=NdsImage.open(report['ROM']).read_file('/__arm9__.bin');_,receipt=assign(arm,snapshot(report,3200),{'product':product})
        assert fixtures[0]['frame']==3200 and receipt=={k:v for k,v in fixtures[0].items() if k!='frame'}
        adapter=report['controlled_category_harness_adapter'];assert adapter['original_harness_file_unchanged']
        assert adapter['adapter_sha256']==sha(Path('scripts/run_category_capture_v754.py').read_bytes())
        assert adapter['unchanged_original_harness_sha256']==sha(Path('scripts/headless_desmume_v193.py').read_bytes())
    else:assert not report.get('battery_save_preloaded')
    rows={}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes())==row['PNG_sha256'];rows[row['frame']]=row
    return report,rows


def main():
    rom=NdsImage.open('out/all_routes_combined_v754_candidate.nds');arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4')
    block=IlnkContainer.parse(common).blocks[common_message_entries(common,arm,clean=False)[730].block]
    font=GameAsciiFont.from_arm9(arm);native=read(ROOT/'native_review.json');layouts={r['category']:r for r in native['all18_complete_dialogue_font_planes']}
    checks,controls,reports=[],{},[]
    for product in read(ROOT/'actual_fixture_products.json'):
        old,before=captures(f'category_v754_{product}_753',6501,product)
        new,after=captures(f'category_v754_{product}_754',6501,product)
        assert old['scripted_input_schedule']==new['scripted_input_schedule'] and old['core_options']==new['core_options']
        assert set(before)==set(after)
        category=new['synthetic_category_trend_fixtures'][0]['category'];case=layouts[category];controls[str(product)]=[]
        for frame in sorted(after):
            a,b=(Image.open(rows[frame]['path']).convert('RGB') for rows in (before,after));diff=ImageChops.difference(a,b)
            if frame not in (4600,4800):
                assert diff.getbbox() is None,(product,frame,diff.getbbox());controls[str(product)].append(frame);continue
            expected=set()
            for row,line in enumerate(case['lines']):
                for col,char in enumerate(line):
                    glyph=font.decode(char)
                    for y in range(11):
                        for x in range(6):
                            if glyph.getpixel((x,y)):expected.add((22+col*6+x,296+row*16+y))
            body=(16,294,244,366)
            actual={(x,y) for y in range(body[1],body[3]) for x in range(body[0],body[2]) if b.getpixel((x,y))==(0,8,0)}
            assert actual==expected,(product,frame,len(actual-expected),len(expected-actual))
            diff.paste((0,0,0),body);assert diff.getbbox() is None,(product,frame,diff.getbbox())
            assert snapshot(new,frame).count(block)==1
            checks.append({'product':product,'category':category,'full_argument':case['full_argument'],'frame':frame,
                'message_id':730,'lines':case['lines'],'capture':after[frame],
                'all_text_pixels_blank_cells_and_every_outside_pixel_exact':True,
                'compact_shop_captions_borders_portraits_and_palette_exact':True,'unique_whole_resident_block_exact':True})
        reports.extend([str(CAP/f'category_v754_{product}_{v}/capture_report.json') for v in (753,754)])
    game,new_rows=captures('category_v754_newgame',4000)
    old,old_rows=captures('market_v753_newgame',4000)
    assert game['scripted_input_schedule']==old['scripted_input_schedule'] and set(new_rows)==set(old_rows)
    assert all(Path(new_rows[f]['path']).read_bytes()==Path(old_rows[f]['path']).read_bytes() for f in new_rows)
    protected=Path('E:/Rota Nova translations/Saves/hodram-istanbul-golden-cutlass-blue-oak-v474.dsv')
    disposable=Path('E:/Rota Nova translations/Saves/Test fixtures/V751 disposable Istanbul donor.dsv')
    assert sha(protected.read_bytes())==sha(disposable.read_bytes())==SAVE_SHA
    save(ROOT/'gameplay_verification.json',{'candidate':'out/all_routes_combined_v754_candidate.nds','candidate_sha256':game['ROM_sha256'],
        'six_terminal6501_frame_paired_cold_boots':True,'declared_original_trend_and_seed_fixtures_only':True,
        'actual_complete_category730_holds':checks,'whole_two_screen_unchanged_menu_and_return_controls':controls,
        'ordinary4000_frame_New_Game_and7_whole_baseline_frame_pairs':sorted(new_rows),
        'protected_and_disposable_source_save_sha256':SAVE_SHA,'source_saves_unchanged':True,'capture_reports':reports,
        'three_actual_argument_classes_and_other15_native_font_classes_not_all_physical_scenes':True,
        'no_hardware_full_route_earned_trend_or_exact_UI_RNG_draw_count_claim':True,
        'verifier_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('V754 three full category arguments,6 complete holds,compact UI/return and New Game pass.',flush=True)


if __name__=='__main__':main()
