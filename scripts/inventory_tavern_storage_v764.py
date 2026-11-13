"""Inventory exact retired village slots against V762; no ROM mutation."""

import re
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shipyard_editorial import BANKS
from dk4tool.rom.nds import NdsImage
from scripts.inventory_shipyard_storage_v760 import BASE, units
from scripts.verify_shipyard_storage_v760 import cstring_in_units
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_storage_v764')
CURRENT = Path('out/all_routes_combined_v762_candidate.nds')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    clean, current = [NdsImage.open(p) for p in ('work/clean.nds', CURRENT)]
    source, arm = [r.read_file('/__arm9__.bin') for r in (clean, current)]
    assert sha(CURRENT.read_bytes()) == read('out/editorial_review_latest.json')['sha256']
    arm9_units = units(current)
    all_units = arm9_units + [('ARM7', current.rom.arm7RamAddress, bytes(current.rom.arm7))]
    previous = read('work/analysis/shipyard_storage_v760/owned_source_storage.json')
    for row in previous['all54_village_and3_Deck_active_replacements_verified']:
        pointer = struct.unpack_from('<I', arm, row['pointer_field'])[0]
        assert pointer == row['active_pointer']
        assert cstring_in_units(arm9_units, pointer).hex() == row['active_complete_text_hex']
    rows = []
    for row in read('translations/village_promised_words_manuscript_v1.json')['records']:
        lo = row['source_pointer']; expected = bytes.fromhex(row['source_hex']) + b'\0'
        hi = (lo + len(expected) + 3) // 4 * 4
        assert source[lo - BASE:lo - BASE + len(expected)] == expected
        assert set(source[lo - BASE + len(expected):hi - BASE]) <= {0}
        if any(a < hi and lo < b for a, b in BANKS): continue
        assert arm[lo - BASE:hi - BASE] == source[lo - BASE:hi - BASE], row['id']
        assert struct.unpack_from('<I', source, row['field'])[0] == lo
        assert struct.unpack_from('<I', arm, row['field'])[0] != lo
        rows.append({'id': row['id'], 'lo': lo, 'hi': hi,
                     'source_hex': arm[lo - BASE:hi - BASE].hex(),
                     'aliases': [], 'branches': [], 'adr': [], 'crossing_strings': []})
    for name, base, raw in all_units:
        for match in re.finditer(rb'(?=(...\x02))', raw, flags=re.DOTALL):
            target = int.from_bytes(match.group(1), 'little')
            for row in rows:
                if row['lo'] <= target < row['hi']:
                    row['aliases'].append([name, base + match.start(), target])
            if not BASE + 0x130000 <= target < 0x02171E48: continue
            end = arm.find(b'\0', target - BASE, min(len(arm), target - BASE + 1024))
            if end < 0: continue
            affected = [r for r in rows if target < r['lo'] <= BASE + end]
            if not affected: continue
            try:
                text = arm[target - BASE:end].decode('cp932')
                textual = bool(text) and all(ord(c) >= 32 or c in '\n\r\t' for c in text)
            except UnicodeError:
                textual = False
            if textual:
                for row in affected:
                    row['crossing_strings'].append([name, base + match.start(), target, BASE + end + 1])
        for at in range(0, len(raw) - 3, 4):
            word = struct.unpack_from('<I', raw, at)[0]
            if word & 0x0E000000 == 0x0A000000:
                delta = word & 0xFFFFFF
                if delta & 0x800000: delta -= 0x1000000
                target = base + at + 8 + delta * 4
                for row in rows:
                    if row['lo'] <= target < row['hi']:
                        row['branches'].append([name, base + at, target])
            if word & 0x0E0F0000 == 0x020F0000 and (word >> 21) & 15 in (2, 4):
                imm, shift = word & 255, ((word >> 8) & 15) * 2
                value = ((imm >> shift) | (imm << (32 - shift))) & 0xFFFFFFFF if shift else imm
                target = base + at + 8 + (value if (word >> 21) & 15 == 4 else -value)
                for row in rows:
                    if row['lo'] <= target < row['hi']:
                        row['adr'].append([name, base + at, target])
    eligible = sorted((r for r in rows if not any(r[k] for k in ('aliases', 'branches', 'adr', 'crossing_strings'))), key=lambda r: r['lo'])
    banks = []
    for row in eligible:
        if banks and banks[-1]['hi'] == row['lo']:
            banks[-1]['hi'] = row['hi']; banks[-1]['members'].append(row['id'])
        else:
            banks.append({'lo': row['lo'], 'hi': row['hi'], 'members': [row['id']]})
    for row in banks: row['bytes'] = row['hi'] - row['lo']
    save(ROOT / 'retired_source_inventory.json', {'source_ROM_sha256': sha(CURRENT.read_bytes()),
        'source_ARM9_sha256': sha(arm), 'source_allocations': rows, 'candidate_contiguous_banks': banks,
        'all57_active_replacements_exact': True, 'includes_current_main_autoload_overlays_and_ARM7': True,
        'scope': 'Exact retired source ownership and observed alias/branch/ADR/cross-string exclusions. No allocation approval, runtime write proof, ROM or profile mutation.',
        'producer_sha256': sha(Path(__file__).read_bytes())})
    for row in banks: print(hex(row['lo']), hex(row['hi']), row['bytes'], row['members'], flush=True)
    print('Excluded', [(r['id'], {k: len(r[k]) for k in ('aliases', 'branches', 'adr', 'crossing_strings') if r[k]}) for r in rows if r not in eligible], flush=True)


if __name__ == '__main__': main()
