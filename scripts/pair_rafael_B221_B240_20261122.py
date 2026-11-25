"""Bind Rafael's next letter, town and item scenes to the registered candidate."""

from inspect import getsource
from pathlib import Path

from scripts import pair_rafael_B177_B180_20261121 as pairing
from scripts import register_rafael_B211_B220_20261122 as parent
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
ROOT = Path("work/analysis/rafael_B221_B240_followup_20261122")
PAIRED = ROOT / "paired_source_registered_candidate.json"
TEXT = (*pairing.TEXT, 0x4100)
EARLIER = Path("translations/rafael_B221_B240_integrated_final_review_v1.json")
source = checked_text(getsource(pairing.main), {
    'range(177, 181)': 'range(221, 241)',
    '        assert not any(r["word"] == 0x4100 for r in source_cmd)': '',
    '        records = []': '        records, style_objects = [], []',
    '            pair = zip(*(text_records(command, word) for command in raw), strict=True)':
        '''            if word == 0x4100:
                assert raw[0][:2] == raw[1][:2] and raw[0][18:20] == raw[1][18:20]
                style_objects.append(dict(source_offset=left["offset"], current_offset=right["offset"],
                                          source_command_hex=raw[0].hex(), current_command_hex=raw[1].hex()))
            pair = zip(*(text_records(command, word) for command in raw), strict=True)''',
    '                if selector is not None:': '                if word == 0x4000:',
    'prefix = bytes([selector]) if selector is not None else b""':
        'prefix = bytes([selector]) if word == 0x4000 else b""',
    'for r in source_cmd)), records=records))': 'for r in source_cmd)), records=records, style_objects=style_objects))',
    '    ROOT.mkdir(exist_ok=True)':
        '    assert sum(r["native_command_word"] == 0x4100 for r in ready) == 29\n'
        '    assert sum(len(g["style_objects"]) for g in groups) == 4\n'
        '    ROOT.mkdir(exist_ok=True)', 
    'len(ready) == 183': 'len(ready) == 270',
    'for r in ready) == 8': 'for r in ready) == 7',
    '183 exact source and current records bound across Rafael B177–180, including eight choice labels.':
        '270 exact source and current records bound across Rafael B221–240, including seven choice labels and 29 actor-style variants.',
})
scope = vars(pairing) | globals()
exec(compile(source, __file__ + "::exact-source-current-binding", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
