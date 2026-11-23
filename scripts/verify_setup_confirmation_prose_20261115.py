"""Verify the revised confirmation and the normal return to the character editor."""

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_rafael_setup_labels_20261115 as workflow
from scripts import stage_setup_confirmation_prose_20261115 as stage
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask

base, ROOT = stage.base, stage.ROOT
OUTPUT = ROOT / 'gameplay_verification.json'
SHEET = ROOT / 'setup_confirmation_replay.png'
FRAME = 6191
PANEL = (12, 330, 234, 349)


def main():
    staged = base.load(stage.STORED)
    assert base.digest(stage.ROM) == staged['candidate_sha256']
    assert base.digest(stage.parent.ROM) == staged['previous_sha256']
    events, frames, end, _, _ = workflow.schedule(None)
    evidence, paired, requests = {}, [], []
    previous = ROOT.with_name('setup_confirmation_prose_20261115_v1')
    for root, side, digest in ((previous, 'before', staged['previous_sha256']),
                               (ROOT, 'after', staged['candidate_sha256'])):
        folder = root / side
        receipt, capture = folder / 'terminal.json', folder / 'capture/capture_report.json'
        terminal, report = map(base.load, (receipt, capture))
        assert terminal['ROM_sha256'] == report['ROM_sha256'] == digest
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not report.get('battery_save_preloaded') and report['scripted_input_schedule'] == events
        assert report['frames'] == end and not any(v for k, v in report.items() if k.startswith('synthetic_'))
        assert all(base.digest(p) == sha for p, sha in terminal['evidence'].items())
        evidence.update(terminal['evidence'] | {str(receipt): base.digest(receipt)})
        requests.append(terminal['target_COMMON_calls'])
        by_frame = shots(report)
        for frame in frames:
            shot = by_frame[frame]
            evidence[shot['path']] = shot['PNG_sha256']
        paired.append({n: captured(by_frame[n]) for n in frames})
    assert requests[0] == requests[1] and {r['message_ID'] for r in requests[0]} == {120}
    assert [r['frame'] for r in requests[0]] == [1800, 1800, 6003, 6003]
    a, b = paired
    equal = []
    for frame in frames:
        bounds = ImageChops.difference(a[frame], b[frame]).getbbox()
        if frame == FRAME:
            assert bounds and PANEL[0] <= bounds[0] < bounds[2] <= PANEL[2]
            assert PANEL[1] <= bounds[1] < bounds[3] <= PANEL[3]
        else:
            assert bounds is None, (frame, bounds)
            equal.append(frame)
    assert 6591 in equal
    image = base.NdsImage.open(stage.ROM)
    font = GameAsciiFont.from_arm9(image.read_file(stage.ARM))
    masks = []
    for hold, text in ((a[FRAME], 'Everything correct?'), (b[FRAME], 'Is everything OK?')):
        ink, bounds = complete_mask(font, text, hold, 16, 333, (0, 8, 0))
        actual = {(x, y) for x in range(PANEL[0], PANEL[2]) for y in range(PANEL[1], PANEL[3])
                  if hold.getpixel((x, y)) == (0, 8, 0)}
        assert len(actual) == ink
        masks.append({'text': text, 'ink_pixels': ink, 'bounds': bounds})
    sheet = Image.new('RGB', (1024, 262), '#263238')
    drawing = ImageDraw.Draw(sheet)
    for index, (caption, hold) in enumerate((('Previous', a[FRAME]), ('Revised', b[FRAME]))):
        x = index * 512
        drawing.text((x + 4, 3), caption, fill='white')
        excerpt = hold.crop((0, 260, 256, 384))
        sheet.paste(excerpt.resize((512, 248), Image.Resampling.NEAREST), (x, 14))
    sheet.save(SHEET)
    base.save(OUTPUT, {
        'candidate_sha256': staged['candidate_sha256'], 'previous_sha256': staged['previous_sha256'],
        'ordinary_rafael_new_game': True, 'original_requests': requests[1], 'held_confirmation_frame': FRAME,
        'held_masks': masks, 'exact_control_frames': equal, 'ordinary_cancel_return_frame': 6591,
        'offline_only_revisions': [122, 123], 'hardware': False,
        'sheet_sha256': base.digest(SHEET), 'evidence': evidence,
    })
    print(f'Confirmed the complete new question and {len(equal)} exact control frames.')


if __name__ == '__main__':
    main()
