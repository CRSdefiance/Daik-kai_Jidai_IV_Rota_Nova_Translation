"""Bind clean source header captures to the reviewed English fixture."""
from pathlib import Path

from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B166_B167_current1674_20261105')
SOURCE=ROOT/'source_actor8_fixture_v2'
CLEAN_REPORT=Path('work/r166jp2/capture_report.json')
ENGLISH=ROOT/'actual_pixels_v2/focused_actual_pixels.json'
OUTPUT=SOURCE/'actor8_alias_resolution.json'
FRAMES={584:4080,658:4320,770:4560,779:4800}
CLIP=(16,276,196,289)


def digest(p):
    return sha(Path(p).read_bytes())


def main():
    assert not OUTPUT.exists()
    fixture,report,pixels=map(load,(SOURCE/'fixture.json',CLEAN_REPORT,ENGLISH))
    assert report['ROM_sha256']==fixture['rom_sha256']==digest(fixture['rom'])
    assert report['frames']==fixture['frames']==6201 and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report.get('battery_save_preloaded')
    assert fixture['full_canonical_serialized_clean_inverse'] and fixture['exact_source_queries_and_speech_commands']
    assert pixels['all_complete_native_body_andheader_planes_andblank_guards_match']
    assert pixels['exact_black_and_CP932_shadow_masks_for_four_source_ellipses']
    caps={c['frame']:c for c in report['frames_captured']}
    pane,observed=[],[]
    for index,frame in FRAMES.items():
        ident=f'DK4_MES_B166_R{index:04d}'
        cap=caps[frame]
        assert digest(cap['path'])==cap['PNG_sha256']
        with Image.open(cap['path']) as img:
            pane.append(sha(img.convert('RGB').crop(CLIP).tobytes()))
        speech=next(r for r in fixture['copied'] if r['id']==ident and r['word']==0x4000)
        assert speech['source_speaker']==8
        target=next(r for r in pixels['body_pages'] if r['id']==ident)
        matching=next(h for h in pixels['headers'] if h['actor_ID']==8 and h['frame']==target['frame'])
        assert matching['text']=='Arcadius Eudoxios' and matching['complete_name_glyphs_andblank_guards_exact']
        observed.append(dict(id=ident,source_speech=speech,source_capture=cap,source_visible_header='アルカディウス・エウドシオス',
            localized_header=matching['text'],localized_capture=matching['capture'],source_header_pixel_sha256=pane[-1]))
    assert len(set(pane))==1
    source_modal=caps[3360]
    assert digest(source_modal['path'])==source_modal['PNG_sha256']
    with Image.open(source_modal['path']) as img:
        assert sha(img.convert('RGB').crop(CLIP).tobytes())!=pane[0]
    english_modal=next(r for r in pixels['body_pages'] if r['id']=='DK4_MES_B166_R0183')
    assert english_modal['selector']==254 and bytes.fromhex(english_modal['text_hex']).startswith(b'Eirene:')
    assert not any(r['frame']==english_modal['frame'] for r in pixels['headers'])
    sheet=SOURCE/'source_nameplate_sheet.png'
    save(OUTPUT,dict(actors=observed,private_FE_source_heading='＜エイレネ＞',private_FE_localized_heading='Eirene:',
        private_FE_source_capture=source_modal,private_FE_localized_capture=english_modal['capture'],
        exact_four_identical_clean_header_crops=True,source_sheet=str(sheet),source_sheet_sha256=digest(sheet),
        source_and_english_headers_and_FE_visually_reviewed=True,
        retain_Arcadius_as_source_progressive_header_Eirene_as_scene_voice_and_FE_heading=True,
        original_conditions_and_story_activation_not_claimed=True,hardware=False,
        evidence={str(p):digest(p) for p in (SOURCE/'fixture.json',CLEAN_REPORT,ENGLISH,sheet,Path(__file__))}))
    print('Four clean and reviewed English progressive headers retain Arcadius. Named FE panel remains Eirene.')


if __name__=='__main__':
    main()
