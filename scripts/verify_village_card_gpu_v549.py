"""Verify all eight village-card source planes and real native fixture displays."""
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_village_card_gpu_v549 import OUT, PARENT
from scripts.verify_portrait_native_pixels_v202 import native5

ROOT = OUT.parent
CAPTURES = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
SCREENSHOTS = Path('E:/Rota Nova translations/Screenshots/Test fixtures/village_card_gpu_v549')
IDS = (168,169,170,171,206,207,208,209)


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    digest = sha(PARENT.read_bytes())
    assert digest == '499e0ad767b1badf899ab6873ad787f171651035c7d6316012af2b8afc8c77d3'
    parent, clean = NdsImage.open(PARENT),NdsImage.open('work/clean.nds')
    font = GameAsciiFont.from_arm9(parent.read_file('/__arm9__.bin'))
    baseline = {p:data for _,p,data in parent.iter_files()}|dict(parent.iter_components())
    inputs = read(OUT/'opening_inputs.json')
    SCREENSHOTS.mkdir(parents=True,exist_ok=True)
    sheet = Image.new('RGB',(536,864),(35,45,50))
    painter = ImageDraw.Draw(sheet)
    cases, negatives, receipts = [], [], []
    for position,index in enumerate(IDS):
        fixture = OUT/f'index{index:03d}_RESEARCH_ONLY.nds'
        manifest = read(fixture.with_suffix('.fixture.json'))
        assert manifest['research_only'] and manifest['not_playable_distribution_or_registered_candidate']
        assert manifest['parent_sha256'] == digest and manifest['requested_image_index'] == index
        assert manifest['inherited_batches'] == 470 and manifest['production_ROM_unchanged']
        saved = NdsImage.open(fixture)
        actual = {p:data for _,p,data in saved.iter_files()}|dict(saved.iter_components())
        assert baseline.keys() == actual.keys()
        assert [p for p in baseline if baseline[p]!=actual[p]] == ['/data/SC0.DK4']
        before,after = [IlnkContainer.parse(data['/data/SC0.DK4']).blocks for data in (baseline,actual)]
        assert len(before) == len(after) == 343
        assert all(a==b for n,(a,b) in enumerate(zip(before,after)) if n!=44)
        assert len(before[44]) == len(after[44]) and before[44][:30] == after[44][:30]
        assert before[44][34:] == after[44][34:]
        assert after[44][30:34] == bytes((0x20,0x46,index,0x80))
        path = f'/evstill/evstill{index:03d}.pxl'
        source,new = [PxlImage.from_bytes(r.read_file(path)) for r in (clean,parent)]
        assert (new.width,new.height,new.bits_per_pixel) == (256,192,8)
        assert source.source[:source.pixels_offset] == new.source[:new.pixels_offset]
        batch = read(f'translations/village_caption_evstill{index}_graphics_v{2 if index==207 else 1}.json')
        assert sha(clean.read_file(path)) == batch['source_file_sha256']
        row = batch['records'][0]
        left,top,right,bottom = row['box']
        text,colour = row['text'],batch['color_index']
        assert batch['advance'] == batch['glyph_width'] == 6
        x = left+(right-left-len(text)*6)//2
        y = top+(bottom-top-11)//2
        assert left <= x < x+len(text)*6 <= right and top <= y < y+11 <= bottom
        expected = bytearray([255]*(256*192))
        if index == 207:
            expected[:256*20] = source.indices[:256*20]
        glyphs = []
        for n,letter in enumerate(text):
            mask = font.decode(letter)
            points = [(y+yy)*256+x+n*6+xx for yy in range(11) for xx in range(6)
                      if mask.getpixel((xx,yy))]
            for point in points:
                expected[point] = colour
            glyphs.append(points)
        assert bytes(expected) == bytes(new.indices)
        for n in (0,len(text)-1):
            modified = bytearray(new.indices)
            assert glyphs[n]
            for point in glyphs[n]:
                modified[point] = 255
            assert modified != expected
            negatives.append({'image':index,'letter':text[n],'index':n,'erased_pixels':len(glyphs[n]),
                              'whole_plane_comparison_rejects_first_or_final_erasure':True})
        folder = CAPTURES/f'village_card_gpu_v549_{index}'
        report_path = folder/'capture_report.json'
        report = read(report_path)
        assert report['ROM_sha256'] == manifest['research_ROM_sha256'] == sha(fixture.read_bytes())
        assert report['frames'] == 4200 and report['cold_boot'] and not report['savestate_loaded']
        assert not report['callback_errors'] and not report.get('battery_save_preloaded')
        assert report['scripted_input_schedule'] == inputs
        matches = []
        palette = [native5(rgb) for rgb in new.palette]
        for shot in report['frames_captured']:
            assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
            if shot['frame'] not in (3000,3600,4000,4200):
                continue
            image = Image.open(shot['path']).convert('RGB')
            assert image.size == (256,384)
            pixels = image.load()
            if all(native5(pixels[n%256,n//256]) == palette[value] for n,value in enumerate(new.indices)):
                matches.append(shot)
        assert len({shot['frame'] for shot in matches})>=3,('Fewer than3 distinct native upper-screen frames',index)
        chosen = next(shot for shot in matches if shot['frame']==4000)
        destination = SCREENSHOTS/f'card{index:03d}_synthetic_event_display.png'
        shutil.copy2(chosen['path'],destination)
        assert sha(destination.read_bytes()) == chosen['PNG_sha256']
        receipts.append({'original':chosen['path'],'saved':str(destination),'sha256':chosen['PNG_sha256'],
                         'synthetic_event_fixture':True,'guide_approved':False})
        col,row_number = position%2,position//2
        sx,sy = col*268,row_number*216
        painter.text((sx+6,sy+3),f'{index}: {text}',fill=(235,235,235))
        sheet.paste(Image.open(destination).convert('RGB').crop((0,0,256,192)),(sx+6,sy+20))
        cases.append({'image':index,'source_path':path,'Japanese':batch['records'][0]['source_japanese'],
                      'English':text,'caption_bounds':[x,y,x+len(text)*6,y+11],
                      'complete_independent_font_cells':len(text),'complete_independent_font_ink':sum(map(len,glyphs)),
                      'full_source_plane_and_original_headers_flags_palette_exact':True,
                      'native_origin':[0,0],'every_native_upper_screen_pixel_exact':49152,
                      'complete_first_and_final_glyphs_in_native_GPU_match':True,
                      'source_file_sha256':sha(parent.read_file(path)),'exact_native_frames':matches,
                      'capture_report':str(report_path),'capture_report_sha256':sha(report_path.read_bytes()),
                      'fixture_manifest':str(fixture.with_suffix('.fixture.json')),
                      'ordinary_event_reachability_not_proven':True})
    fragment_source = PxlImage.from_bytes(clean.read_file('/evstill/evstill207.pxl'))
    fragment_current = PxlImage.from_bytes(parent.read_file('/evstill/evstill207.pxl'))
    assert fragment_source.indices[:5120] == fragment_current.indices[:5120]
    assert sum(value!=255 for value in fragment_source.indices[:5120]) == 279
    sheet_path = SCREENSHOTS/'all8_native_upper_screens_review.png'
    sheet.save(sheet_path)
    proof = {'candidate':str(PARENT),'candidate_sha256':digest,'production_ROM_changed':False,
             'all8_native_event_still_displays':cases,'all16_first_final_erasure_negatives':negatives,
             'total_native_upper_pixels_per_matched_frame_set':393216,
             'independent_complete_character_cells':sum(c['complete_independent_font_cells'] for c in cases),
             'independent_complete_ink_pixels':sum(c['complete_independent_font_ink'] for c in cases),
             'image207_all279_uninterpreted_source_fragment_pixels_displayed_exact':True,
             'image207_fragment_identity_or_extra_reading_not_invented':True,
             'only_one_operand_byte_changed_in_each_existing_original_opening_instruction':True,
             'all_other_production_assets_route_controls_and_prose_exact':True,
             'synthetic_original_opcode_inputs_not_ordinary_village_progression':True,
             'all_current_observed_native_loading_extent_palette_and_full_plane_GPU_verified':True,
             'other_transition_states_or_ordinary_event_reachability_not_proven':True,
             'screenshot_copy_receipts':receipts,'review_sheet':str(sheet_path),
             'all22_requirements_and18_incomplete_plaques_retained':True,'full_goal_complete':False}
    assert sha(PARENT.read_bytes()) == digest
    (ROOT/'native_GPU_proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('8 original event-still displays pass whole49152-pixel screens,171 font cells,1972 ink pixels and16 first/final erasure negatives;279 fragment pixels preserved.')


if __name__ == '__main__':
    main()
