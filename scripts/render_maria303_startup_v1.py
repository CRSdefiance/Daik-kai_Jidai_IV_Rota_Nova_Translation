"""Present all six candidate-owned startup checkpoints without altering complete captures."""
from pathlib import Path
from PIL import Image, ImageDraw
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/maria303_release_v1')


def main():
    report_path = ROOT/'own_startup_run_v1/capture/capture_report.json'
    report = load(report_path)
    assert report['cold_boot'] and not report['callback_errors'] and report['frames'] == 31000
    out = ROOT/'own_startup_visual_v1'
    assert not out.exists()
    frames = {c['frame']: c for c in report['frames_captured']}
    canvas = Image.new('RGB', (512, 1224), 'white')
    draw = ImageDraw.Draw(canvas)
    selected = []
    for index, frame in enumerate([1600, 2200, 3340, 4000, 16000, 31000]):
        cap = frames[frame]
        assert digest(cap['path']) == cap['PNG_sha256'] and cap['dimensions'] == [256, 384]
        x, y = (index % 2)*256, (index // 2)*408
        draw.text((x+4, y+3), f'Own Maria303 / frame {frame}', fill='black')
        canvas.paste(Image.open(cap['path']).convert('RGB'), (x, y+24))
        selected.append(cap)
    out.mkdir()
    path = out/'startup_six_frames.png'
    canvas.save(path)
    save(out/'receipt.json', dict(report=str(report_path), report_sha256=digest(report_path),
        selected_captures=selected, sheet=str(path), sheet_sha256=digest(path),
        complete_original_captures_preserved=True, direct_visual_review_pending=True, new_credit=0))
    print(path)


if __name__ == '__main__':
    main()
