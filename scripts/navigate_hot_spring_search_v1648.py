"""Bounded ordinary-input navigator; stop on hot springs or unknown dialogue.

Pixel masks here identify navigation controls only. They are not translation,
glyph-completeness, or gameplay-verification evidence. No outcome is selected.
"""
import argparse
import json
import struct
import time
from pathlib import Path

from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.hot_spring_notice_editorial import current_entries
from scripts.observe_hot_spring_resilient_v1645b import mode

ROOT = Path('work/analysis/hot_spring_notice_resilient_v1645')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/hot_spring_notice_resilient_v1645_1637')
REF = CAP.parent / 'hot_spring_live_v1626_1622'
JOURNAL = ROOT / 'navigation.jsonl'
EVENTS = ROOT / 'bounded_navigator_v1648.jsonl'
BOXES = [(80, 0, 176, 16), (0, 370, 256, 384)]
KNOWN = {308, 309, 312, 2217, 2219, 2221, *range(2229, 2235), 2244, 2245}


def masks(path):
    with Image.open(path) as im:
        im = im.convert('RGB')
        return [bytes(p == (230, 230, 230) for p in im.crop(b).get_flattened_data()) for b in BOXES]


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--frame', type=int, required=True)
    p.add_argument('--attempts', type=int, default=12)
    args = p.parse_args()
    assert 1 <= args.attempts <= 20
    frame = args.frame
    rom = NdsImage.open('out/all_routes_combined_v1637_candidate.nds')
    arm = rom.read_file('/__arm9__.bin')
    entries = current_entries(rom.read_file('/COMMON/MESFILE.DK4'), arm)
    owner = struct.unpack_from('<I', arm, 0x552A0)[0] - 0x02000000
    reference = masks(REF / 'frame_010000_navigation.png')
    assert [sum(m) for m in reference] == [93, 285]

    def record(value):
        with EVENTS.open('a', encoding='utf-8') as f:
            f.write(json.dumps(value) + '\n')
        print(value, flush=True)

    def send(delta, buttons=None, fixture=None):
        nonlocal frame
        last = json.loads(JOURNAL.read_text(encoding='utf-8').splitlines()[-1])
        assert last.get('until') == frame, (frame, last)
        command = {'until': frame + delta, 'duration': 12 if buttons == ['Y'] else 4 if buttons else 1}
        if buttons:
            command['buttons'] = buttons
        if fixture:
            command['battle_fixture'] = fixture
        with JOURNAL.open('a', encoding='utf-8') as f:
            f.write(json.dumps(command) + '\n')
        target = frame + delta
        deadline = time.monotonic() + 60
        ram = CAP / f'frame_{target:06d}_arm9_ram.bin'
        png = CAP / f'frame_{target:06d}_navigation.png'
        while time.monotonic() < deadline:
            if ram.exists() and ram.stat().st_size == 4194304 and png.exists():
                with Image.open(png) as image:
                    image.load()
                frame = target
                return
            time.sleep(0.1)
        raise TimeoutError(f'No complete capture at {target}; do not restart emulator or repeat input blindly')

    attempts = 0
    for step in range(100):
        picture = CAP / f'frame_{frame:06d}_navigation.png'
        raw = (CAP / f'frame_{frame:06d}_arm9_ram.bin').read_bytes()
        assert len(raw) == 4194304
        if masks(picture) == reference:
            record({'frame': frame, 'navigation': 'Sea View controls', 'attempts': attempts})
            if attempts >= args.attempts:
                break
            send(237, ['Y'])
            observed = mode(frame)
            if observed['mode'] != 'Info Mode':
                record({'frame': frame, 'stop': 'unexpected menu after Y', 'mode': observed['mode']})
                break
            send(214, ['Y'])
            observed = mode(frame)
            if observed['mode'] != 'Search Mode':
                record({'frame': frame, 'stop': 'unexpected second menu', 'mode': observed['mode']})
                break
            send(30, fixture={'fatigue_search_context': 'coherent_source_region2_fleet_and_mobile_shore'})
            assert mode(frame)['mode'] == 'Search Mode'
            send(300, ['A'])
            attempts += 1
            continue
        template = raw[owner + 0x2030:owner + 0x2230].split(b'\0')[0]
        ids = [n for n, entry in enumerate(entries) if entry.text == template]
        record({'frame': frame, 'loaded_template_IDs': ids, 'template': template.decode('cp932'), 'attempts': attempts})
        if any(n in {310, *range(2275, 2288)} for n in ids):
            record({'frame': frame, 'stop': 'hot spring requires direct inspection and separate full verification'})
            break
        if not ids or not set(ids) <= KNOWN:
            record({'frame': frame, 'stop': 'unrecognized or unapproved routine dialogue; no input sent'})
            break
        send(220, ['A'])
    else:
        record({'frame': frame, 'stop': 'bounded step limit'})
    record({'last_frame': frame, 'attempts': attempts, 'emulator_left_running_at_capture': True,
            'no_RNG_actor_skill_event_outcome_changes': True, 'no_translation_completion_credit': True})


if __name__ == '__main__':
    main()
