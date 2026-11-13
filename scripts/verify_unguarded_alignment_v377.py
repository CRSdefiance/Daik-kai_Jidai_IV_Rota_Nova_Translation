"""Current COMMON census and native first-row/continuation preservation."""

import json
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_common_alignment_native_v257 import raster

ROOT = Path('work/analysis/unguarded_alignment_v377')
OLD, NEW = 0x0239B104 - 0x02000000, 0x01FFCE40 - 0x02000000


def match(text, width):
    first, separator, rest = text.partition(b'\n')
    return (separator and first and 33 <= first[0] <= 126
            and all(32 <= ch <= 126 for ch in first)
            and len(first) * 6 + 18 <= width and rest.startswith(b'  ')
            and len(rest) > 2 and 33 <= rest[2] <= 126)


def main():
    old_rom = NdsImage.open('out/all_routes_combined_v375_candidate.nds')
    old = old_rom.read_file('/__arm9__.bin')
    new = (ROOT / 'research_arm9.bin').read_bytes()
    rows = common_message_entries(old_rom.read_file('/COMMON/MESFILE.DK4'), old, clean=False)
    census = [{'id': r.message_id, 'text_hex': r.text.hex(),
               'first_row_bytes': len(r.text.split(b'\n')[0])} for r in rows if match(r.text, 228)]
    (ROOT / 'current_common_census.json').write_text(json.dumps({'records': census,
        'count': len(census), 'stored_text_only_runtime_macro_expansion_still_checked_by_helper': True}, indent=2) + '\n')
    positive = [b'Admiral, sailors\n  have scurvy!', b'A\n  Janus',
                b'Even phase\n  complete ending.', b'Odd phase!\n  complete ending.',
                b'Fair. I wish a good\n  opportunity would arise.',
                b'W' * 35 + b'\n  Final word.']
    negative = [b'  Business? Fair.\n  opportunity would arise.',
                b'   Deliberate indent\n  unchanged.', b'Plain single line.',
                b'No guard\ncontinuation.', b'One guard\n continuation.',
                b'Three guards\n   continuation.', b'W' * 36 + b'\n  unchanged.', b'W' * 38 + b'\n  unchanged.']
    cases = []
    for text in positive + negative:
        a = raster(old, text, OLD, size=(228, 48))
        b = raster(new, text, NEW, size=(228, 48))
        shift = text in positive
        if shift:
            expected = bytearray(a)
            for y in range(16):
                expected[y * 228:(y + 1) * 228] = bytes(6) + a[y * 228:y * 228 + 222]
            assert b == expected, (text, next((i, b[i], expected[i]) for i in range(len(b)) if b[i] != expected[i]))
        else:
            assert a == b
        cases.append({'text': text.decode(), 'shifted_first_row_only': shift,
                      'whole_native_pixels_and_input_header_buffer_ABI_guards_pass': True})
    for tracking, size in [(-1, (228, 48)), (0, (8, 48)), (0, (228, 12))]:
        text = b'A\n  B'
        a = raster(old, text, OLD, tracking=tracking, size=size, complete=False)
        b = raster(new, text, NEW, tracking=tracking, size=size, complete=False)
        assert a == b
        cases.append({'tracking': tracking, 'size': size, 'fallback_exact': True})
    proof = {'cases': cases, 'current_COMMON_stored_pattern_count': len(census),
             'all_text_controls_and_continuation_pixels_unchanged': True,
             'actual_scurvy_replay_pending': True, 'full_goal_complete': False}
    (ROOT / 'native_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print(f'{len(cases)} native complete-row/fallback cases pass; {len(census)} current stored patterns mapped.')


if __name__ == '__main__':
    main()
