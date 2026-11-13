"""Verify standalone title compositing against palette-specific blank controls."""
import json
import shutil
from pathlib import Path

from PIL import Image

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_standalone_title_gpu_v550 import (
    ORIGINAL,
    OUT,
    PARENT,
    PATHS,
    ROOT,
    STRING_OFFSET,
)
from scripts.verify_portrait_native_pixels_v202 import native5

CAPTURES = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
SCREENSHOTS = Path('E:/Rota Nova translations/Screenshots/Test fixtures/standalone_title_v550')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def contents(rom):
    return {p:data for _,p,data in rom.iter_files()}|dict(rom.iter_components())


def capture(folder,fixture,digest,inputs,frame):
    report = read(folder/'capture_report.json')
    assert report['ROM_sha256'] == digest == sha(fixture.read_bytes())
    assert report['frames'] == 4200 and report['cold_boot'] and not report['savestate_loaded']
    assert not report.get('battery_save_preloaded') and not report['callback_errors']
    assert report['scripted_input_schedule'] == inputs
    shot = next(s for s in report['frames_captured'] if s['frame']==frame)
    assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
    image = Image.open(shot['path']).convert('RGB')
    assert image.size == (256,384)
    return image,shot


def main():
    digest = sha(PARENT.read_bytes())
    assert digest == '499e0ad767b1badf899ab6873ad787f171651035c7d6316012af2b8afc8c77d3'
    parent,clean = NdsImage.open(PARENT),NdsImage.open('work/clean.nds')
    baseline = contents(parent)
    inputs = read(OUT/'opening_inputs.json')
    SCREENSHOTS.mkdir(parents=True,exist_ok=True)
    cases = []
    for path in PATHS:
        stem = Path(path).stem
        fixture = OUT/(stem+'_RESEARCH_ONLY.nds')
        manifest = read(fixture.with_suffix('.fixture.json'))
        actual = contents(NdsImage.open(fixture))
        assert baseline.keys() == actual.keys()
        assert [p for p in baseline if baseline[p]!=actual[p]] == ['/__arm9__.bin']
        current_arm,fixture_arm = baseline['/__arm9__.bin'],actual['/__arm9__.bin']
        assert fixture_arm[:STRING_OFFSET] == current_arm[:STRING_OFFSET]
        assert fixture_arm[STRING_OFFSET+len(ORIGINAL):] == current_arm[STRING_OFFSET+len(ORIGINAL):]
        assert fixture_arm[STRING_OFFSET:STRING_OFFSET+len(ORIGINAL)] == (path.encode()+b'\0').ljust(len(ORIGINAL),b'\0')
        assert actual[path] == baseline[path] and manifest['parent_sha256'] == digest
        pxl = PxlImage.from_bytes(baseline[path])
        source = PxlImage.from_bytes(clean.read_file(path))
        assert source.source[:source.pixels_offset] == pxl.source[:pxl.pixels_offset]
        keys = [i for i,colour in enumerate(pxl.palette) if native5(colour)==(0,0,0)]
        assert keys == ([255] if stem=='logo' else [0])
        key = keys[0]
        if key==255:
            control = OUT/'logo_KEY255_CONTROL_RESEARCH_ONLY.nds'
            control_folder = CAPTURES/'standalone_alpha_key255_v550_logo'
        else:
            control = OUT/'startmenu0_ZERO_KEY_CONTROL_RESEARCH_ONLY.nds'
            control_folder = CAPTURES/'standalone_alpha_control_v550_startmenu0'
        control_metadata = read(control.with_suffix('.fixture.json'))
        control_contents = contents(NdsImage.open(control))
        assert actual.keys() == control_contents.keys()
        assert [p for p in actual if actual[p]!=control_contents[p]] == [path]
        blank = PxlImage.from_bytes(control_contents[path])
        assert blank.source[:blank.pixels_offset] == pxl.source[:pxl.pixels_offset]
        assert bytes(blank.indices) == bytes([key])*49152
        results = []
        palette = [native5(rgb) for rgb in pxl.palette]
        for frame in (3600,4000,4200):
            image,shot = capture(CAPTURES/f'standalone_title_gpu_v550_{stem}',fixture,
                               manifest['research_ROM_sha256'],inputs,frame)
            background,bgshot = capture(control_folder,control,control_metadata['control_ROM_sha256'],inputs,frame)
            pixels,bgpixels = image.load(),background.load()
            assert all(native5(pixels[n%256,n//256]) ==
                       (native5(bgpixels[n%256,n//256]) if value==key else palette[value])
                       for n,value in enumerate(pxl.indices)),(stem,frame)
            assert image.crop((0,192,256,384)).tobytes() == background.crop((0,192,256,384)).tobytes()
            results.append({'frame':frame,'native_capture':shot,'control_capture':bgshot,
                            'complete49152_pixel_colour_and_key_composite_exact':True,
                            'whole_lower_screen_identical_to_control':True})
        shot = results[1]['native_capture']
        destination = SCREENSHOTS/(stem+'_synthetic_native_display.png')
        shutil.copy2(shot['path'],destination)
        assert sha(destination.read_bytes()) == shot['PNG_sha256']
        if stem=='startmenu0':
            porto = read('work/analysis/porto_review_v329/proof.json')
            retained = next(s for s in porto['source_protection'] if s['resource']==path)
            assert retained['current_sha256'] == sha(baseline[path])
            complete_letters = {'proof':'work/analysis/porto_review_v329/proof.json',
                                'source_file_sha256_bound_to_current':True,
                                'complete_independent_word_planes':[
                                    c for c in porto['complete_word_planes'] if c['resource']==path]}
        else:
            historical = NdsImage.open('out/all_routes_combined_v188_candidate.nds')
            assert historical.read_file(path) == baseline[path]
            complete_letters = {'existing_title_art_source':'translations/rota_title_logo_art_v4.json',
                                'complete_file_exact_historical_V188':True,
                                'all_existing_artwork_pixels_including_full_words_in_native_composite':True}
        cases.append({'path':path,'source_sha256':sha(baseline[path]),'native_view_extent':[256,192],
                      'transparent_palette_colour_entry':key,
                      'palette_key_foreground_pixels':sum(v!=key for v in pxl.indices),
                      'palette_key_background_pixels':sum(v==key for v in pxl.indices),
                      'all_source_pixels_and_all_transparent_background_points_checked':True,
                      'source_header_flags_palette_extent_exact':True,'complete_letter_evidence':complete_letters,
                      'native_frames':results,'fixture_manifest':str(fixture.with_suffix('.fixture.json')),
                      'control_manifest':str(control.with_suffix('.fixture.json')),
                      'screenshot_copy':str(destination),'screenshot_sha256':shot['PNG_sha256'],
                      'guide_approved':False,'borrowed_original_event_still_widget_not_original_title_scene':True})
    result={'candidate':str(PARENT),'candidate_sha256':digest,'production_ROM_changed':False,
            'all2_standalone_title_native_compositing_cases':cases,
            'all_native_instructions_and_route_operands_preserved':True,
            'explicit_filename_substitution_is_diagnostic_input':True,
            'whole49152_colour_or_transparent_key_pixels_exact_per_case_at3_distinct_frames':True,
            'rejected_index0_logo_control':'work/analysis/standalone_resource_compatibility_v550/rejected_index0_logo_control.json',
            'not_all_files_use_index0_as_transparent_colour':True,
            'original_standalone_title_scene_consumers_still_unproven':True,
            'normal_gameplay_or_other_parent_palette_alpha_states_not_proven':True,
            'all22_requirements_and18_incomplete_plaques_retained':True,'full_goal_complete':False}
    assert sha(PARENT.read_bytes()) == digest
    (ROOT/'native_compositing_proof.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('Two complete native title composites pass at3 frames:logo key255,Porto key0; existing full title art retained; original scenes remain open.')


if __name__ == '__main__':
    main()
