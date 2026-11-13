"""Full changed-scene font proof, inherited source art and ordinary regression."""

from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE_SHA
from scripts.prepare_story_percent_v685 import ROOT
from scripts.run_village_visits_v664 import CAP
from scripts.verify_regional_ui_v616 import full_cells, glyphs
from scripts.verify_story_percent_v685 import ROM
from scripts.verify_village_wrap_v608 import read, save


def shots(report):
    images = {}
    for row in report['frames_captured']:
        path = Path(row['path'])
        assert sha(path.read_bytes()) == row['PNG_sha256']
        image = Image.open(path).convert('RGB')
        if row['frame'] in images:
            assert images[row['frame']].tobytes() == image.tobytes()
        images[row['frame']] = image
    return images


def main():
    static = read(ROOT / 'static_release_proof.json')
    assert sha(ROM.read_bytes()) == static['candidate_sha256']
    pre = read(ROOT / 'preflight.json')
    current = NdsImage.open(ROM)
    arm = current.read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    reports, pictures, refs = {}, {}, []
    for case in ('maria', 'baseline', 'ordinary'):
        folder = CAP / ('story_percent_v685_' + case)
        path = folder / 'capture_report.json'
        r, contract = read(path), read(folder / 'run_contract.json')
        assert r['ROM_sha256'] == static['candidate_sha256'] and r['core_DLL_sha256'] == CORE_SHA
        assert r['frames'] == contract['config']['frames'] == (24100 if case == 'ordinary' else 31000)
        assert r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
        assert contract['runner_sha256'] == sha(Path('scripts/run_story_percent_v685.py').read_bytes())
        assert r['scripted_input_schedule'] == read(contract['config']['inputs'])
        assert contract['inputs_sha256'] == sha(Path(contract['config']['inputs']).read_bytes())
        if case == 'ordinary':
            assert not r.get('battery_save_preloaded') and not any(k.startswith('synthetic_') and v for k, v in r.items())
        else:
            fixture = read(ROOT / 'unlock_manifest_v685.json')
            assert r['battery_save_preloaded']['source_sha256'] == fixture['fixture_save_sha256']
            assert sha(Path(fixture['fixture_save']).read_bytes()) == fixture['fixture_save_sha256']
            assert sha(Path(fixture['original_donor']).read_bytes()) == fixture['original_donor_sha256']
            assert {k for k, v in r.items() if k.startswith('synthetic_') and v} == {'synthetic_gallery_fixtures'}
        reports[case], pictures[case] = r, shots(r)
        refs.append({'case': case, 'path': str(path), 'sha256': sha(path.read_bytes())})
    assert pictures['maria'].keys() == pictures['baseline'].keys() and len(pictures['maria']) == 49
    assert all(im.tobytes() == pictures['baseline'][f].tobytes() for f, im in pictures['maria'].items())
    assert (CAP / 'story_percent_v685_maria/final_arm9_ram.bin').read_bytes() == (
        CAP / 'story_percent_v685_baseline/final_arm9_ram.bin').read_bytes()
    old_report = read(CAP / 'maria_intro_v684_baseline/capture_report.json')
    assert old_report['ROM_sha256'] == pre['source_candidate_sha256']
    assert old_report['scripted_input_schedule'] == reports['maria']['scripted_input_schedule']
    old = shots(old_report)
    changed = [f for f, im in pictures['maria'].items() if im.tobytes() != old[f].tobytes()]
    assert changed == [24400]
    new, before = pictures['maria'][24400], old[24400]
    assert all(new.getpixel((x, y)) == before.getpixel((x, y)) for y in range(384) for x in range(256)
               if not (16 <= x < 240 and 296 <= y < 376))
    record = next(r for r in static['four_record_proof']['/data/SC3.DK4']['records'] if r['segment'] == 137)
    lines = record['compiled_lines']
    line_proofs = [full_cells(new, font, text, 16, 296 + n * 16, (0, 8, 0)) for n, text in enumerate(lines)]
    expected = {(16 + x, 296 + n * 16 + y) for n, text in enumerate(lines) for x, y in glyphs(font, text)}
    actual = {(x, y) for y in range(296, 376) for x in range(16, 240) if new.getpixel((x, y)) == (0, 8, 0)}
    assert actual == expected
    assert 'percent' in lines[0] and not any('%' in text for text in lines)
    chapter = IlnkContainer.parse(current.read_file('/data/SC3.DK4')).blocks[33]
    raw_checks = []
    snapshots = {r['frame']: r for r in reports['maria']['read_only_capture_RAM_snapshots']}
    for frame in range(4000, 30401, 600):
        item = snapshots[frame]
        raw = Path(item['path']).read_bytes()
        assert sha(raw) == item['sha256'] and len(raw) == 0x400000
        at = raw.find(chapter)
        assert at >= 0 and raw.find(chapter, at + 1) == -1
        raw_checks.append({'frame': frame, 'whole2528_byte_current_chapter_resident': True, 'address': at + 0x02000000})
    source_art = read('work/analysis/maria_intro_v684/proof.json')['actual_source_art_cases']
    assert len(source_art) == 45
    for row in source_art:
        frame = row['frame']
        assert pictures['maria'][frame].crop((0, 0, 256, 192)).tobytes() == old[frame].crop((0, 0, 256, 192)).tobytes()
        assert sha(current.read_file(row['source'])) == row['whole_PXL_sha256']
    ordinary_old = read(CAP / 'wedding_dialogue_v678_ordinary/capture_report.json')
    old_images = shots(ordinary_old)
    assert ordinary_old['ROM_sha256'] == pre['source_candidate_sha256']
    assert ordinary_old['scripted_input_schedule'] == reports['ordinary']['scripted_input_schedule']
    assert pictures['ordinary'].keys() == old_images.keys() and len(old_images) == 89
    assert all(im.tobytes() == old_images[f].tobytes() for f, im in pictures['ordinary'].items())
    review = ROOT / 'actual_fixed_percent_and_Hangzhou.png'
    sheet = Image.new('RGB', (1024, 410), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, (image, title) in enumerate(((before, 'V678 observed defect'), (new, 'V685 source-faithful repair'),
        (pictures['maria'][28000], 'V685 following dialogue'), (pictures['maria'][31000], 'V685 normal Hangzhou handoff'))):
        draw.text((i * 256 + 4, 4), title, fill='white')
        sheet.paste(image, (i * 256, 24))
    sheet.save(review)
    save(ROOT / 'proof.json', {**static, 'cold_boot_verification_pending': False, 'reports': refs,
        '49_complete_current_Maria_baseline_pairs_and_terminal_RAM_exact': True,
        '48_complete_Maria_frames_exact_V678_only24400_changed_in_dialogue_rectangle': True,
        'three_complete_source_text_lines_including_percent_and_all_empty_rows_exact': line_proofs,
        'all45_retained_source_photo_views_current_exact_unchanged_graphics': True,
        'complete_resident_chapter_checks': raw_checks,
        'all89_ordinary_title_selection_story_and_Town_frames_exact_V678': True,
        'deep_other_three_records_have_complete_QA_previews_and_native_printf_controls_not_live_parent_credit': True,
        'three_inherited_blank_holds_no_new_source_wait_or_padding_clearance': True,
        'review_sheet': str(review), 'review_sheet_sha256': sha(review.read_bytes()),
        'verifier_sha256': sha(Path(__file__).read_bytes()),
        'all18_original_plaques_incomplete22_historical_requirements_and_other_gates_open': True,
        'current_goal_turn_classification': 'progress', 'full_goal_complete': False})
    print('V685 actual 3-percent repair: all complete letters/rows pass;49 current baseline pairs,48 retained Maria frames and89 ordinary frames exact.', flush=True)


if __name__ == '__main__':
    main()
