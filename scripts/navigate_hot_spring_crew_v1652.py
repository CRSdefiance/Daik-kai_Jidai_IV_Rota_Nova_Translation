"""Successor navigator: require visible dialogue, stop on stale buffers/other UI.

Restores only declared test crew before Search when live counts become low.
No event, random value, actor identity, skill or eligibility value is selected.
"""
import inspect
from pathlib import Path
from scripts import navigate_hot_spring_search_v1648 as previous
from scripts.native_hot_spring_crew_v1650 import REQUEST
from scripts.verify_personal_gameplay_v841 import get_machine


def visible_paper(path):
    with previous.Image.open(path) as im:
        pixels = list(im.convert('RGB').crop((12, 294, 244, 368)).get_flattened_data())
    return sum(r > 180 and g > 170 and b > 130 for r, g, b in pixels) > len(pixels) * 0.55


if __name__ == '__main__':
    root = Path('work/analysis/hot_spring_crew_v1651')
    cap = Path('E:/Rota Nova translations/Generated/work/emulation_v193/hot_spring_crew_v1651_1637')
    oldcap = previous.CAP
    assert visible_paper(oldcap / 'frame_048338_navigation.png')
    assert not visible_paper(oldcap / 'frame_052958_navigation.png')
    source = inspect.getsource(previous.main)
    needle = "            send(237, ['Y'])"
    replacement = """            cpu, get = get_machine(arm, raw)
            fleet = get(0xCB1A8) + 4 + 132 * get(0x2E58C)
            counts = [get(0x55444, get(0x36C70, fleet + 12 + 8 * slot)) for slot in range(5)]
            if min(counts) < 15:
                record({'frame': frame, 'declared_test_crew_refill_before_Search': True, 'before_counts': counts})
                send(30, fixture=REQUEST)
                assert masks(CAP / f'frame_{frame:06d}_navigation.png') == reference
            send(237, ['Y'])"""
    assert source.count(needle) == 1
    source = source.replace(needle, replacement)
    needle = "        template = raw[owner + 0x2030:owner + 0x2230].split(b'\\0')[0]"
    replacement = """        if not visible_paper(picture):
            record({'frame': frame, 'stop': 'not Sea View or visible dialogue; loaded buffers may be stale; no input sent'})
            break
""" + needle
    assert source.count(needle) == 1
    source = source.replace(needle, replacement)
    env = {**previous.__dict__, 'ROOT': root, 'CAP': cap, 'JOURNAL': root / 'navigation.jsonl',
           'EVENTS': root / 'bounded_navigator_v1652.jsonl', 'visible_paper': visible_paper,
           'get_machine': get_machine, 'REQUEST': REQUEST, 'KNOWN': previous.KNOWN | {339}}
    # The original mode function is dynamically bound to its old capture path;
    # use the underlying read-only function with this successor's capture path.
    from types import FunctionType
    from scripts import observe_hot_spring_navigation_v1641b as observer
    env['mode'] = FunctionType(observer.mode.__code__, {**observer.__dict__, 'ROOT': root, 'CAP': cap}, argdefs=observer.mode.__defaults__)
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
