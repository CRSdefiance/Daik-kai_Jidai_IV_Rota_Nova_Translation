"""Bind six directly viewed startup captures to the exact complete composite."""
from pathlib import Path
from PIL import Image
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/lil269_B243_B282_release_v1/own_startup_visual_v1')

if __name__ == '__main__':
    output = ROOT / 'direct_visual_review.json'
    assert not output.exists()
    path = ROOT / 'receipt.json'
    receipt = load(path)
    assert digest(receipt['sheet']) == receipt['sheet_sha256']
    assert [c['frame'] for c in receipt['selected_captures']] == [1600, 2200, 3340, 4000, 16000, 31000]
    with Image.open(receipt['sheet']) as sheet:
        canvas = sheet.convert('RGB')
        assert canvas.size == (512, 1224)
        for i, capture in enumerate(receipt['selected_captures']):
            assert digest(capture['path']) == capture['PNG_sha256']
            with Image.open(capture['path']) as raw:
                expected = raw.convert('RGB')
                assert expected.size == (256, 384)
            x, y = i % 2 * 256, i // 2 * 408 + 24
            assert canvas.crop((x, y, x + 256, y + 384)).tobytes() == expected.tobytes()
    save(output, dict(receipt=str(path), receipt_sha256=digest(path),
        selected_captures=receipt['selected_captures'], sheet=receipt['sheet'], sheet_sha256=receipt['sheet_sha256'],
        all_six_original_captures_andexact_composite_directly_viewed=True,
        scope='Own exact cumulative candidate title/New Game, Maria selection/opening and Hangzhou; existing system unlock is disclosed and unearned. No new Lil event activation or hardware coverage.',
        new_credit=0, main_promoted=False, evidence={str(Path(__file__)): digest(__file__)}))
