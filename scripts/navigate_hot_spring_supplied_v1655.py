"""Successor:inspect-confirmed2239 acknowledgement and declared low-food refill."""
from pathlib import Path

if __name__ == '__main__':
    path = Path('scripts/navigate_hot_spring_crew_v1652.py')
    source = path.read_text(encoding='utf-8')
    old = "'KNOWN': previous.KNOWN | {339}"
    assert source.count(old) == 1
    source = source.replace(old, "'KNOWN': previous.KNOWN | {339, 2239}")
    source = source.replace('bounded_navigator_v1652.jsonl', 'bounded_navigator_v1655.jsonl')
    needle = "            send(237, ['Y'])\"\"\""
    replacement = """            import struct
            ptr = 0x02450000
            get(0x34EB0, fleet, ptr)
            quantities = struct.unpack('<2I', cpu.mem_read(ptr, 8))
            if 0 < quantities[1] < 100:
                record({'frame': frame, 'declared_original_test_supply_refill': True, 'before_water_food': list(quantities)})
                send(30, fixture={'testing_provisions': 'balanced_original_capacity'})
                assert masks(CAP / f'frame_{frame:06d}_navigation.png') == reference
            send(237, ['Y'])\"\"\""""
    assert source.count(needle) == 1
    source = source.replace(needle, replacement)
    exec(compile(source, __file__, 'exec'), {'__name__': '__main__', '__file__': __file__})
