"""Carry verified environmental artwork forward without repeating emulator runs."""

from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_seoul_v516 import background, icon
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/environment_reconciliation_v718')
ROM = Path('out/all_routes_combined_v712_candidate.nds')
DIGEST = '6534e5619673ea6bdffa3a2342622b99ef393bef52ef58cac131ee94ae0f4030'
PROOFS = {
    'decisions': 'translations/contextual_graphics_decisions_v177.json',
    'native': 'work/analysis/contextual_environment_v206/native_environment_proof.json',
    'assignment': 'work/analysis/environment_assignments_v425/assignment_proof.json',
    'hangzhou_port': 'work/analysis/east_asian_town_v343/live_environment_proof.json',
    'hangzhou_street': 'work/analysis/maria_asia_v515/hangzhou_proof.json',
    'seoul': 'work/analysis/maria_asia_v516/seoul_proof.json',
    'nagasaki': 'work/analysis/shiraki_surname_v518/release_proof.json',
    'japan': 'work/analysis/japan_location_v519/location_proof.json',
}


def main():
    ROOT.mkdir(exist_ok=True)
    assert not (ROOT / 'proof.json').exists()
    current = NdsImage.open(ROM)
    assert sha(ROM.read_bytes()) == DIGEST
    clean = NdsImage.open('work/clean.nds')
    proofs = {key: read(value) for key, value in PROOFS.items()}
    arm = current.read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    releases = [ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
        Path('translations/release_stack.json'), Path('out/raphael_natural_v2_accepted_base.nds')]
    release_hashes = {str(p): sha(p.read_bytes()) for p in releases}
    assets = []
    for row in proofs['decisions']['records']:
        path = row['path']
        source = current.read_file(path)
        assert source == clean.read_file(path)
        assert sha(source) == row['source_sha256']
        image = PxlImage.from_bytes(source)
        assert [image.width, image.height] == row['dimensions']
        assert row['decision'] == 'retain-original-contextual-art'
        assets.append({'path': path, 'sha256': sha(source), 'dimensions': row['dimensions'],
            'decision': row['decision'], 'reason': row['reason']})
    assert len(assets) == 6

    # These are dependency checks for carrying prior native evidence forward,
    # not a claim that the newer ROM was executed in the historical captures.
    historical = {}
    for key in ('hangzhou_port', 'hangzhou_street', 'seoul', 'nagasaki', 'japan'):
        proof = proofs[key]
        path = proof.get('candidate', proof.get('candidate_unchanged', proof.get('production_candidate')))
        digest = proof.get('candidate_sha256', proof.get('production_candidate_sha256'))
        assert sha(Path(path).read_bytes()) == digest
        old = NdsImage.open(path)
        old_arm = old.read_file('/__arm9__.bin')
        assert GameAsciiFont.from_arm9(old_arm).glyphs == font.glyphs
        ranges = [(0xB65E4, 0xB82AC), (0xD1604, 0xD191C), (0x125A20, 0x125A60)]
        for lo, hi in ranges:
            assert arm[lo:hi] == old_arm[lo:hi], (key, hex(lo), hex(hi))
        old_machine, now = machine(old_arm), machine(arm)
        captions = []
        for index, expected in ((4, 'Tavern'), (8, 'Inn')):
            results = []
            for cpu in (old_machine, now):
                call(cpu, 0xB8220, (index,))
                pointer = cpu.reg_read(UC_ARM_REG_R0)
                text = bytes(cpu.mem_read(pointer, 64)).split(b'\0')[0].decode('ascii')
                assert text == expected
                results.append({'pointer': pointer, 'English': text})
            captions.append({'facility_id': index, 'old_and_current_native_getter': results})
        historical[key] = {'ROM': path, 'ROM_sha256': digest,
            'all_six_art_files_exact_current': all(old.read_file(a['path']) == current.read_file(a['path']) for a in assets),
            'town_controller_selector_loader_and_caption_code_ranges_exact': [
                {'ARM9_range': [lo, hi], 'sha256': sha(arm[lo:hi])} for lo, hi in ranges],
            'ASCII_font_exact': True, 'original_native_caption_getters': captions}
        assert historical[key]['all_six_art_files_exact_current']

    # Re-read complete recorded reports and captured PNG hashes. No emulator is
    # started, and no prior reports/proofs are overwritten.
    report_paths = {
        proofs['hangzhou_port']['capture_report']: proofs['hangzhou_port']['capture_report_sha256'],
        proofs['hangzhou_street']['capture_report']: proofs['hangzhou_street']['capture_report_sha256'],
    }
    for key in ('seoul', 'japan'):
        for row in proofs[key]['reports']:
            report_paths[row['path']] = row['sha256']
    report_paths['work/emulation_v193/japan_facilities_v517/capture_report.json'] = None
    reports, images = [], {}
    for path, digest in report_paths.items():
        path = Path(path)
        if digest is not None:
            assert sha(path.read_bytes()) == digest
        report = read(path)
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert sha(Path(report['ROM']).read_bytes()) == report['ROM_sha256']
        for row in report['frames_captured']:
            p = Path(row['path'])
            assert sha(p.read_bytes()) == row['PNG_sha256']
            images[str(p)] = row
        reports.append({'path': str(path), 'sha256': sha(path.read_bytes()), 'frames': report['frames'],
            'ROM_sha256': report['ROM_sha256'], 'all_recorded_PNG_hashes_checked': True,
            'historical_capture_not_new_V712_run': True})

    used = {}

    def picture(path):
        p = Path(path)
        assert str(p) in images, str(p)
        assert sha(p.read_bytes()) == images[str(p)]['PNG_sha256']
        used[str(p)] = images[str(p)]['PNG_sha256']
        return Image.open(p).convert('RGB')

    backgrounds = []
    report = read(proofs['hangzhou_port']['capture_report'])
    for row in proofs['hangzhou_port']['background_patches'][:1]:
        shot = next(x for x in report['frames_captured'] if x['frame'] == row['frame'])
        image = picture(shot['path'])
        source = PxlImage.from_bytes(current.read_file('/towngrp/towngrp32.pxl')).render().convert('RGB')
        l, t, r, b = row['source_box']
        ox, oy = row['native_origin']
        count = 0
        for y in range(t, b):
            for x in range(l, r):
                assert tuple(c >> 3 for c in image.getpixel((x + ox, y + oy))) == tuple(c >> 3 for c in source.getpixel((x, y)))
                count += 1
        assert count == row['exact_source_pixels'] == 3000
        backgrounds.append({'town': 'Hangzhou', 'source': '/towngrp/towngrp32.pxl',
            'image': shot['path'], 'native_origin': [ox, oy], 'source_box': [l, t, r, b], 'native5_pixels_exact': count,
            'portrait_and_dialogue_occlusions_not_counted': True})
    report = read(proofs['hangzhou_street']['capture_report'])
    # The precise historical source box has 16,320 pixels, distinct from the
    # 17,440-pixel source35/47 helper used below.
    source = PxlImage.from_bytes(current.read_file('/towngrp/towngrp33.pxl')).render().convert('RGB')
    # Original V515 verifier pins this source comparison to frame18400.
    shot = next(r for r in report['frames_captured'] if r['frame'] == 18400)
    image = picture(shot['path'])
    box = proofs['hangzhou_street']['source_background33_box']
    for y in range(box[1], box[3]):
        for x in range(box[0], box[2]):
            assert tuple(c >> 3 for c in image.getpixel((x, y + 192))) == tuple(c >> 3 for c in source.getpixel((x, y)))
    backgrounds.append({'town': 'Hangzhou', 'source': '/towngrp/towngrp33.pxl',
        'image': shot['path'], 'native_origin': [0, 192], 'source_box': box, 'native5_pixels_exact': 16320,
        'portrait_and_dialogue_occlusions_not_counted': True})
    for row in proofs['seoul']['background35_source_exact_and_actual_full_unoccluded_regions']:
        image = picture(row['image'])
        source = PxlImage.from_bytes(current.read_file(row['source'])).render()
        count = background(image, source)
        assert count == row['full_unoccluded_source_pixels'] == 17440
        backgrounds.append({'town': 'Seoul', 'source': row['source'], 'image': row['image'],
            'native5_pixels_exact': count, 'portrait_and_dialogue_occlusions_not_counted': True})
    for row in proofs['japan']['actual_background_cases']:
        image = picture(row['image'])
        source = PxlImage.from_bytes(current.read_file(row['source'])).render().convert('RGB')
        if row['town'] == 'osaka':
            expected = [tuple(c >> 3 for c in p) for p in source.get_flattened_data()]
            actual = [tuple(c >> 3 for c in p) for p in image.crop((0, 0, 256, 192)).get_flattened_data()]
            assert actual == expected
            count = 49152
        else:
            count = background(image, source)
        backgrounds.append({'town': row['town'], 'source': row['source'], 'image': row['image'],
            'native5_pixels_exact': count, 'authorized_location_fixture_not_normal_voyage': True})

    signs = []
    cases = [r for r in proofs['nagasaki']['normal_Nagasaki_alternate_sign_and_caption_cases']
        if 'japan_facilities_v517' in r['image']]
    assert len(cases) == 2
    cases = [dict(r, town='Nagasaki', source='/_pxl/' + r['actual_alternate_icon'] + '.pxl') for r in cases]
    cases += proofs['japan']['complete_alternate_signs_and_English_captions']
    for row in cases:
        image = picture(row['image'])
        text = row['English']
        bounds = row['bounds']
        ink, actual_bounds = complete_mask(font, text, image, bounds[0], bounds[1], (0, 8, 0))
        assert list(actual_bounds) == bounds and ink == (72 if text == 'Tavern' else 35)
        sprite_origin = (50, 192) if text == 'Tavern' else (0, 240)
        pixels = icon(image, PxlImage.from_bytes(current.read_file(row['source'])), *sprite_origin)
        assert pixels == (923 if text == 'Tavern' else 1248)
        signs.append({'town': row['town'], 'English': text, 'source': row['source'],
            'image': row['image'], 'complete_nontransparent_source_pixels_exact': pixels,
            'all_letters_and_blank_cells_exact': True, 'native_caption_bounds': bounds,
            'ordinary_Nagasaki_or_authorized_Osaka_Naha_context': True})
    assert len(signs) == 6
    proof = {'format': 'dk4-environment-coverage-reconciliation-v718',
        'candidate': str(ROM), 'candidate_sha256': DIGEST,
        'six_retained_source_art_decisions': assets,
        'evidence': {k: {'path': p, 'sha256': sha(Path(p).read_bytes())} for k, p in PROOFS.items()},
        'unchanged_current_dependencies': historical, 'historical_reports_checked': reports,
        'current_source_against_historical_native_background_pixels': backgrounds,
        'current_source_font_against_six_historical_alternate_sign_caption_cases': signs,
        'reused_screenshots': used, 'verifier_sha256': sha(Path(__file__).read_bytes()),
        'release_hashes_unchanged': release_hashes,
        'six_contextual_art_source_native_visible_regions_and_two_facility_caption_families_complete': True,
        'eight_village_cards_and_other_legacy_environmental_copies_not_closed': True,
        'no_new_emulator_run_full_scene_or_earned_travel_claim': True,
        'Osaka_Naha_original_docking_after_authorized_coordinate_fixtures': True,
        'full_goal_complete': False}
    save(ROOT / 'proof.json', proof)
    print(f'V718: six retained art decisions,{len(backgrounds)} visible background regions and six alternate signs/captions carried to V712; no new native run.', flush=True)


if __name__ == '__main__':
    main()
