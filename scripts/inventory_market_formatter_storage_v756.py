"""Classify complete retired source slots, including registered compact labels."""

import bisect
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.rom.nds import NdsImage
from scripts.probe_market_balanced_v756 import ROOT
from scripts.review_market_stock_v755 import CURRENT
from scripts.verify_village_wrap_v608 import read, save


def main():
    r = NdsImage.open(CURRENT)
    arm = r.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    old = read('work/analysis/market_stock_v755/readonly_source_span_inventory_RESEARCH.json')
    candidates = {s['lo']: {**s, 'owners': [], 'branches': []} for s in old['free']}
    path = Path('translations/shipyard_guild_mystery_ui_arm9_v2.json')
    for row in read(path)['records']:
        if not row['id'].startswith('DK4_ITEM_TYPE_'):
            continue
        at = row['offset']
        source = bytes.fromhex(row['source_hex'])
        compiled = (row['english'].encode('ascii') + b'\0').ljust(len(source), b'\0')
        assert len(compiled) == len(source) and clean[at:at + len(source)] == source
        assert arm[at:at + len(source)] == compiled
        candidates[0x02000000 + at] = {'lo': 0x02000000 + at,
            'hi': 0x02000000 + at + len(source), 'row': row['id'],
            'source_hex': compiled.hex(), 'clean_Japanese_hex': source.hex(),
            'registered_earlier_translation': str(path), 'owners': [], 'branches': []}
    keys = sorted(candidates)
    code = MainCodeFile(arm, 0x02000000)
    units = [(f'section{i}', POOL if i == 3 else s.ramAddress, bytes(s.data))
             for i, s in enumerate(code.sections)]
    units += [(f'overlay{i}', s.ramAddress, bytes(s.data)) for i, s in loadOverlayTable(
        r.rom.arm9OverlayTable, lambda _, f: r.rom.files[f]).items()]
    def owner(target, key, label, address):
        k = bisect.bisect_right(keys, target) - 1
        if k >= 0 and target < candidates[keys[k]]['hi']:
            candidates[keys[k]][key].append([label, address, target])
    for label, base, raw in units:
        for at in range(len(raw) - 3):
            owner(struct.unpack_from('<I', raw, at)[0], 'owners', label, base + at)
        for at in range(0, len(raw) - 3, 4):
            word = struct.unpack_from('<I', raw, at)[0]
            if word & 0x0E000000 != 0x0A000000:
                continue
            delta = word & 0xFFFFFF
            if delta & 0x800000:
                delta -= 0x1000000
            owner(base + at + 8 + delta * 4, 'branches', label, base + at)
    free = [candidates[k] for k in keys if not candidates[k]['owners'] and not candidates[k]['branches']]
    merged = []
    for s in free:
        if merged and merged[-1][1] == s['lo']:
            merged[-1][1] = s['hi']
        else:
            merged.append([s['lo'], s['hi']])
    save(ROOT / 'readonly_source_span_inventory.json', {'free': free, 'merged': merged,
        'excluded_with_owners': [s for s in candidates.values() if s['owners'] or s['branches']],
        'current_ARM9_sha256': sha(arm), 'earlier_translation_batch_sha256': sha(path.read_bytes()),
        'scanned_units': [r[0] for r in units], 'producer_sha256': sha(Path(__file__).read_bytes()),
        'no_ROM_or_storage_change': True})
    print('Proven retired slots:', [(hex(lo), hi - lo) for lo, hi in merged], flush=True)


if __name__ == '__main__':
    main()
