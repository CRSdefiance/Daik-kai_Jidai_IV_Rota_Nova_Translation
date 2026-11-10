"""Make readable QA sheets, deduplicating only exact lower-screen framebuffer planes."""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixtures', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    fixtures = load(args.fixtures)
    args.out.mkdir(parents=True)
    runs = []
    for fixture in fixtures['fixtures']:
        report_path = Path(fixture['capture_folder']) / 'capture_report.json'
        report = load(report_path)
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['ROM_sha256'] == fixture['research_ROM_sha256']
        images, selected, coverage, hashes = [], [], [], {}
        for capture in report['frames_captured']:
            if capture['frame'] < 3980:
                continue
            path = Path(capture['path'])
            assert sha(path.read_bytes()) == capture['PNG_sha256']
            picture = Image.open(path).convert('RGB')
            assert picture.size == (256, 384)
            lower = picture.crop((0, 192, 256, 384))
            digest = sha(lower.tobytes())
            if digest not in hashes:
                hashes[digest] = len(images)
                images.append(lower)
                selected.append(dict(frame=capture['frame'], path=str(path), PNG_sha256=capture['PNG_sha256'], lower_plane_sha256=digest))
            coverage.append(dict(frame=capture['frame'], selected_lower_plane=hashes[digest], lower_plane_sha256=digest))
        sheets = []
        for start in range(0, len(images), 9):
            count = min(9, len(images) - start)
            sheet = Image.new('RGB', (1536, 406 * ((count + 2) // 3)), '#263238')
            draw = ImageDraw.Draw(sheet)
            for i in range(count):
                x, y = (i % 3) * 512, (i // 3) * 406
                record = selected[start + i]
                draw.text((x + 4, y + 3), f"B{fixture['block']} frame {record['frame']} actual initialized QA", fill='white')
                sheet.paste(images[start + i].resize((512, 384), Image.Resampling.NEAREST), (x, y + 22))
            path = args.out / f"B{fixture['block']}_part{start // 9 + 1}.png"
            sheet.save(path)
            sheets.append(dict(path=str(path), sha256=sha(path.read_bytes()), first_selected_index=start, images=count))
        runs.append(dict(capture_report=str(report_path), capture_report_sha256=sha(report_path.read_bytes()),
                         ROM=report['ROM'], ROM_sha256=report['ROM_sha256'], frames=report['frames'],
                         all_lower_screen_capture_coverage=coverage, selected_images=selected, review_sheets=sheets,
                         duplicate_lower_planes_reused=len(coverage) - len(selected), cold_boot=True, savestate=False,
                         hardware_verification=False, disclosed_initialized_scene_ROM_fixture=True,
                         natural_optional_activation=False, visual_review_pending=True))
    save(args.out / 'capture_sheets.json', dict(fixtures=str(args.fixtures), fixtures_sha256=sha(args.fixtures.read_bytes()),
         runs=runs, purpose='Necessary editorial/display QA; no guide photo collection.',
         terminal_processes_are_not_visual_approval=True, new_credit=0, producer_sha256=sha(Path(__file__).read_bytes())))
    print([(r['frames'], len(r['selected_images']), len(r['review_sheets'])) for r in runs])


if __name__ == '__main__':
    main()
