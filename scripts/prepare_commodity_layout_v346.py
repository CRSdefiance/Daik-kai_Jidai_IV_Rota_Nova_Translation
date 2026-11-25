"""Source-locked specialty layout research; never a registered release build."""

import json
import struct
from pathlib import Path

from dk4tool.patch.commodity_compact_layout import transform
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/commodity_layout_v346')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    parent = NdsImage.open('out/all_routes_combined_v342_candidate.nds')
    source = parent.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    manuscript = json.loads(Path('translations/commodity_name_manuscript_v343.json').read_text(encoding='utf-8'))
    allocation = json.loads(Path('work/analysis/commodity_layout_v345/allocation.json').read_text())
    target, plan = transform(source, clean, manuscript, allocation)
    # Percentage sources move; every other original crop remains exact.
    for i in (*range(8), *range(16, 21)):
        row = struct.unpack_from('<7i', source, 0x11A65C + i * 28)
        assert row[4] + row[6] <= 72
        assert target[0x11A65C + i * 28:0x11A65C + (i + 1) * 28] == source[0x11A65C + i * 28:0x11A65C + (i + 1) * 28]
    (ROOT / 'research_arm9.bin').write_bytes(target)
    (ROOT / 'plan.json').write_text(json.dumps(plan, indent=2) + '\n')
    # Existing source-backed Maria visibility fixture; no save flags changed.
    assert target[0x9F068] == 3
    fixture = bytearray(target)
    fixture[0x9F068] = 4
    for name, substitutions in [('normal_names', []), ('long_names', [(42, 115), (51, 103), (62, 108)])]:
        data = bytearray(fixture)
        for displayed, label in substitutions:
            field = 0x15EF18 + displayed * 12
            data[field:field + 4] = target[0x15EF18 + label * 12:0x15EF18 + label * 12 + 4]
        rom = NdsImage.open('out/all_routes_combined_v342_candidate.nds')
        rom.replace_file('/__arm9__.bin', bytes(data))
        rom.save(ROOT / ('research_only_' + name + '_Maria.nds'))
    print('Prepared two unregistered source-locked fixtures; no startup or heap growth.')


if __name__ == '__main__':
    main()
