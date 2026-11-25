"""Repeat a verified ordinary-input Guild/Market/crew/inventory UI cycle.

Consumes a completed cold-load rehearsal, not an unexecuted command journal.
Generated schedules contain controller events only; they never load a state.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO), str(REPO / '.deps'), str(REPO / '.runtime_deps')]
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.rom.nds import NdsImage
from scripts.review_ui_text_smoke import complete_mask


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rehearsal', type=Path, required=True)
    p.add_argument('--rom', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--cycles', type=int, default=20)
    args = p.parse_args()
    assert 1 <= args.cycles <= 100
    assert not args.out.exists(), 'Preserve earlier schedule/proof artifacts'
    report = json.loads(args.rehearsal.read_text(encoding='utf-8'))
    digest = sha(args.rom)
    assert report['ROM_sha256'] == digest and report['frames'] == 11000
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    font = GameAsciiFont.from_arm9(NdsImage.open(args.rom).read_file('/__arm9__.bin'))
    captured = {row['frame']: row for row in report['frames_captured']}
    landmarks = [(4400, 'Market', [0,224,256,352], [0,8,0]),
                 (5000, 'Guild', [0,224,256,352], [0,8,0]),
                 (6500, 'Market', [0,224,256,352], [0,8,0]),
                 (8600, 'Vestaros', [0,40,256,120], None),
                 (10400, 'Blue Oak Shield', [0,12,256,55], None),
                 (11000, 'Market', [0,224,256,352], [0,8,0])]
    for frame, text, region, color in landmarks:
        row = captured[frame]
        assert sha(row['path']) == row['PNG_sha256']
        complete_mask(font, text, Image.open(row['path']).convert('RGB'), region,
                      advance=5 if text == 'Blue Oak Shield' else 6, color=color)
    prefix = [e for e in report['scripted_input_schedule'] if e['start'] <= 4400]
    body = [e for e in report['scripted_input_schedule'] if 4400 < e['start'] <= 11000]
    assert len(body) == 22 and all(e['duration'] == 8 and len(e['buttons']) == 1 for e in body)
    events = list(prefix)
    checks = []
    for cycle in range(args.cycles):
        offset = cycle * 6600
        events.extend(dict(e, start=e['start'] + offset) for e in body)
        for frame, text, region, color in landmarks[1:]:
            checks.append(dict(run='repeat20', frame=frame + offset, text=text, region=region,
                               advance=5 if text == 'Blue Oak Shield' else 6,
                               **(dict(color=color) if color else {}), cycle=cycle + 1))
    args.out.mkdir(parents=True)
    documents = {
        'inputs.json': events,
        'checks.json': dict(format='dk4-ui-text-smoke-checks-v1', runs=['repeat20'], checks=checks),
        'plan.json': dict(format='dk4-ui-text-repeated-cycle-v1', ROM_sha256=digest,
                          rehearsal=str(args.rehearsal), rehearsal_sha256=sha(args.rehearsal),
                          cycles=args.cycles, cycle_start_frame=4400, cycle_frames=6600,
                          frames=4400 + args.cycles * 6600,
                          capture_at=sorted(set(c['frame'] for c in checks)),
                          ordinary_controller_events_only=True, screen_reachability_requires_final_pixel_checks=True),
    }
    for name, value in documents.items():
        (args.out / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
    print(args.cycles, 'cycles;', len(checks), 'live text checks;', documents['plan.json']['frames'], 'frames')


if __name__ == '__main__':
    main()
