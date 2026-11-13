"""Bind completed initialized Maria samples to observed resupply and sailing returns."""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--runs', type=int, nargs='+', required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    args.out.mkdir()
    runs = []
    evidence = {}
    for choice in args.runs:
        terminal_path = args.root/f'display_run_menu{choice}_v1/terminal.json'
        pixel_path = args.root/f'display_pixels_menu{choice}_v1/focused_actual_pixels.json'
        terminal, pixel = map(load, [terminal_path, pixel_path])
        report, observer = map(load, [terminal['report'], terminal['observer']])
        assert terminal['terminal'] and terminal['frames'] == report['frames'] == pixel['frames']
        assert digest(terminal['report']) == terminal['report_sha256']
        assert digest(terminal['observer']) == terminal['observer_sha256']
        assert pixel['all_selected_pages_observed_in_exact_fixture_order']
        assert pixel['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert not observer['errors'] and not observer['mismatches']
        assert observer['all_host_slots_restored_and_core_file_exact']
        last = pixel['ordered_selected_source_calls'][-1]['frame']
        later = [r for r in observer['rows'] if r['kind'] == 'modal_paint' and r['frame'] > last]
        supply = next(r for r in later if r['text_CP932'] == ' Want to resupply for ６００ gold?')
        departure = next(r for r in later if 'Departed Hangzhou.' in r['text_CP932'])
        assert last < supply['frame'] < departure['frame'] < report['frames']
        samples = []
        for label, event in [('resupply', supply), ('departure', departure)]:
            capture = next(c for c in report['frames_captured'] if c['frame'] >= event['frame']+90)
            assert digest(capture['path']) == capture['PNG_sha256']
            samples.append(dict(kind=label, event_frame=event['frame'], event_text=event['text_CP932'], capture=capture))
        final = report['frames_captured'][-1]
        assert final['frame'] == report['frames'] and digest(final['path']) == final['PNG_sha256']
        samples.append(dict(kind='final sailing', capture=final))
        sheet = Image.new('RGB', (1536, 800), '#eee')
        draw = ImageDraw.Draw(sheet)
        for i, sample in enumerate(samples):
            draw.text((i*512+4, 4), sample['kind']+' @'+str(sample['capture']['frame']), fill='black')
            with Image.open(sample['capture']['path']) as im:
                sheet.paste(im.convert('RGB').resize((512, 768), Image.Resampling.NEAREST), (i*512, 25))
        path = args.out/f'menu{choice}_transitions.png'
        sheet.save(path)
        runs.append(dict(choice=choice, frames=report['frames'], samples=samples,
            review_sheet=dict(path=str(path), sha256=digest(path))))
        for p in [terminal_path, pixel_path, Path(terminal['report']), Path(terminal['observer'])]:
            evidence[str(p)] = digest(p)
    save(args.out/'receipt.json', dict(runs=runs, evidence=evidence,
        initialized_QA_hosts_reach_resupply_departure_andfinal_sailing=True,
        direct_visual_review_pending=True, original_optional_story_conditions_not_activated=True,
        full_original_story_scene_control_flow_not_claimed=True, new_credit=0, guide_photos=False))
    print('Bound', len(runs), 'actual initialized host returns without replay.')


if __name__ == '__main__':
    main()
