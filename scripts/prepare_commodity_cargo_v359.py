"""Correct the duplicate Cargo printf/status literals without changing trade logic."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/commodity_cargo_v359')
PATCHES = [(0xC4074, 0x15A074, 0x01FFC6A0, '%s\n  %s %d%'),
           (0xC4078, 0x15A080, 0x01FFC640, '不足中'),
           (0xC407C, 0x15A088, 0x01FFC64C, '流行中')]


def transform(source):
    target = bytearray(source)
    for field, old, pointer, text in PATCHES:
        assert struct.unpack_from('<I', source, field)[0] == 0x02000000 + old
        assert source[old:source.index(0, old)].decode('cp932') == text
        struct.pack_into('<I', target, field, pointer)
    restored = bytearray(target)
    for field, *_ in PATCHES:
        restored[field:field + 4] = source[field:field + 4]
    assert bytes(restored) == source
    return bytes(target)


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    source = Path('work/analysis/commodity_price_v357/research_arm9.bin').read_bytes()
    target = transform(source)
    (ROOT / 'research_arm9.bin').write_bytes(target)
    rom = NdsImage.open('out/all_routes_combined_v358_candidate.nds')
    assert rom.read_file('/__arm9__.bin') == source
    rom.replace_file('/__arm9__.bin', target)
    rom.save(ROOT / 'research_only_cargo_fix.nds')
    plan = {'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(target),
            'exactly_three_Cargo_literal_pointers_changed': True,
            'all_code_graphics_names_trade_values_and_autoload_payload_preserved': True,
            'patches': PATCHES, 'actual_verification_pending': True, 'not_for_handoff': True}
    (ROOT / 'plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    report = json.loads(Path('work/emulation_v193/commodity_saved_production_v358/capture_report.json').read_text())
    (ROOT / 'cargo_inputs.json').write_text(json.dumps(report['scripted_input_schedule'], indent=2) + '\n')
    print('Prepared duplicate Cargo format/status correction; original transaction logic exact.')


if __name__ == '__main__':
    main()
