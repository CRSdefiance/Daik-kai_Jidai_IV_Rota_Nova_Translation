"""Verify source wood repairs and explicitly substituted banner render fixtures."""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import rom_files
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_source_plaque_grain_v542 import capture_report

ROOT = Path('work/analysis/header_materials_v565')
PARENT = Path('out/all_routes_combined_v564_candidate.nds')
ROM = Path('out/all_routes_combined_v566_candidate.nds')
CAPTURE = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ALIAS = '/_pxl/tempcargo.pxl'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def prepare():
    rows = []
    for stem in ('haifuhin', 'senrihin'):
        for kind, parent in (('control', PARENT), ('actual', ROM)):
            image = NdsImage.open(parent)
            before = rom_files(image)
            path = f'/_pxl/{stem}.pxl'
            image.replace_file(ALIAS, image.read_file(path))
            target = ROOT/f'{stem}_{kind}_RENDER_FIXTURE.nds'
            image.save(target)
            after = rom_files(NdsImage.open(target))
            assert [p for p in before if before[p] != after[p]] == [ALIAS]
            rows.append({'stem': stem, 'kind': kind, 'ROM': str(target), 'sha256': sha(target.read_bytes()),
                         'parent': str(parent), 'parent_sha256': sha(parent.read_bytes()),
                         'substitution_only': ALIAS, 'source_file': path,
                         'original_event_consumer_verified': False})
    (ROOT/'render_fixtures.json').write_text(json.dumps(rows, indent=2)+'\n', encoding='utf-8')
    print('Four research-only full-width renderer fixtures prepared; original event contexts remain unverified.')


def main():
    digest = sha(ROM.read_bytes())
    old, new, clean = (NdsImage.open(p) for p in (PARENT, ROM, Path('work/clean.nds')))
    before, after = rom_files(old), rom_files(new)
    changed = sorted(p for p in before if before[p] != after[p])
    assert changed == ['/_pxl/haifuhin.pxl', '/_pxl/senrihin.pxl'] and before.keys() == after.keys()
    config = read('translations/header_wood_textures_v1.json')
    prototype = read(ROOT/'wood_header_prototypes.json')
    rows = []
    for row, source_proof in zip(config['records'], prototype, strict=True):
        path, text = row['file_path'], row['english']
        original, inherited, image = (PxlImage.from_bytes(r.read_file(path)) for r in (clean, old, new))
        assert image.source[:image.pixels_offset] == original.source[:original.pixels_offset]
        assert sha(image.source) == row['target_sha256']
        assert image.source == (ROOT/(Path(path).stem+'_RESEARCH_ONLY.pxl')).read_bytes()
        english = {n for n, v in enumerate(image.indices) if v == 15}
        assert english == {n for n, v in enumerate(inherited.indices) if v == 15}
        batch = read('translations/interface_'+('distributed_goods' if 'haifuhin' in path else 'spoils')+'_graphics_v1.json')
        l, t, r, b = batch['records'][0]['box']
        font_size = batch['records'][0]['maximum_size']
        font = ImageFont.load_default(size=font_size)
        box = font.getbbox(text)
        assert box[2]-box[0] <= r-l and box[3]-box[1] <= b-t
        mask = Image.new('L', (r-l, b-t))
        ImageDraw.Draw(mask).text(((r-l-box[2]+box[0])//2-box[0], (b-t-box[3]+box[1])//2-box[1]),
                                 text, font=font, fill=255)
        expected = {(t+y)*256+l+x for y in range(b-t) for x in range(r-l) if mask.getpixel((x, y)) >= 128}
        assert english == expected
        assert sum(a != b for a, b in zip(inherited.indices, image.indices, strict=True)) == source_proof['changed_pixels']
        rows.append({'file': path, 'english': text, 'font_size': font_size, 'complete_font_ink_pixels': len(english),
                     'source_reconstruction': {k: v for k, v in source_proof.items() if k != 'research_only'}})
    manifest, prior = read(ROM.with_suffix('.manifest.json')), read(PARENT.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == digest and manifest['profile'] == 'all-routes-unified-v566'
    assert manifest['base_sha256'] == prior['base_sha256']
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['batches'] == prior['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == prior['required_batches']
    assert len(read('translations/release_stack.json')['accepted_layers']) == 114
    for row in rows:
        stage = manifest['relocations'][row['file']]['header_wood_textures']
        assert stage['target_sha256'] == sha(new.read_file(row['file']))
    fixtures = read(ROOT/'render_fixtures.json')
    cases = []
    for stem in ('haifuhin', 'senrihin'):
        pair = [next(f for f in fixtures if f['stem'] == stem and f['kind'] == kind) for kind in ('control', 'actual')]
        reports = []
        for fixture in pair:
            fixture_rom = NdsImage.open(fixture['ROM'])
            parent = NdsImage.open(fixture['parent'])
            a, b = rom_files(parent), rom_files(fixture_rom)
            assert [p for p in a if a[p] != b[p]] == [ALIAS]
            assert b[ALIAS] == a[fixture['source_file']]
            assert sha(Path(fixture['ROM']).read_bytes()) == fixture['sha256']
            reports.append(capture_report(CAPTURE/f"header_wood_v566_{stem}_{fixture['kind']}", fixture['sha256']))
        assert reports[0]['scripted_input_schedule'] == reports[1]['scripted_input_schedule']
        assert reports[0]['core_options'] == reports[1]['core_options']
        source_save = Path(reports[1]['battery_save_preloaded']['source'])
        assert sha(source_save.read_bytes()) == reports[1]['battery_save_preloaded']['source_sha256']
        tables = [{s['frame']: s for s in report['frames_captured']} for report in reports]
        images = [PxlImage.from_bytes(r.read_file(f'/_pxl/{stem}.pxl')) for r in (old, new)]
        for frame in (4300, 4600):
            shots = [Image.open(table[frame]['path']).convert('RGB') for table in tables]
            for y in range(384):
                for x in range(256):
                    colour = native5(shots[0].getpixel((x, y)))
                    if 261 <= y < 277:
                        n = (y-261)*256+x
                        assert colour == native5(images[0].palette[images[0].indices[n]])
                        colour = native5(images[1].palette[images[1].indices[n]])
                    assert native5(shots[1].getpixel((x, y))) == colour, (stem, frame, x, y)
            cases.append({'stem': stem, 'frame': frame, 'complete_both_screen_pixels_exact': 98304,
                          'complete_banner_pixels_exact': 4096, 'substituted_renderer_fixture': True,
                          'original_event_consumer_verified': False})
    fresh = capture_report(CAPTURE/'header_wood_v566_fresh', digest)
    prior_fresh = capture_report(CAPTURE/'cargo_banner_v564_fresh', sha(PARENT.read_bytes()))
    assert fresh['scripted_input_schedule'] == prior_fresh['scripted_input_schedule']
    assert fresh['core_options'] == prior_fresh['core_options']
    assert [r['PNG_sha256'] for r in fresh['frames_captured']] == [r['PNG_sha256'] for r in prior_fresh['frames_captured']]
    assert fresh['frames'] == 21200 and len({r['frame'] for r in fresh['frames_captured']}) == 56
    patch = ROM.with_suffix('.xdelta')
    make_xdelta(Path('work/clean.nds'), ROM, patch)
    reconstructed = ROOT/'v566_reconstructed.nds'
    apply_xdelta(Path('work/clean.nds'), patch, reconstructed)
    assert reconstructed.read_bytes() == ROM.read_bytes()
    for name in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        plaques = read(Path('translations')/name)['plaque_style_v247']['ongoing_plaque_inventory']
        assert len(plaques) == 18 and all(r['fully_completed'] is False for r in plaques)
    assert len(read('translations/graphics_completion_requirements_v313.json')['historical_pending_items_retained']) == 22
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
             'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
             'patch_sha256': sha(patch.read_bytes()), 'exact_clean_patch_reconstruction': True,
             'only_changed_internal_files_from_V564': changed, 'all_code_and_other_art_exact_V564': True,
             'all470_batches114_layers_retained': True, 'stored_font_and_material_cases': rows,
             'native_fixture_cases': cases, 'total_fixture_screen_pixels_exact': 393216,
             'total_fixture_banner_pixels_exact': 16384, 'unchanged_unique_startup_frames': 56,
             'original_header_event_consumers_still_unverified': True, 'experimental': True,
             'canonical_promoted': False, 'all18_plaques_remain_incomplete': True, 'full_goal_complete': False}
    (ROOT/'v566_release_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('Two headers:341 complete ink points,4 full controlled screens,16384 banner pixels,56 unchanged startup captures and exact patch pass. Original event contexts remain open.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare-fixtures', action='store_true')
    if parser.parse_args().prepare_fixtures:
        prepare()
    else:
        main()
