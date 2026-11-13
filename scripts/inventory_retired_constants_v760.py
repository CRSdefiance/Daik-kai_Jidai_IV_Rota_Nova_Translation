"""Discover original C-string constants whose explicit owners were redirected.

Discovery is not a storage approval. Retain original literals and current owners
for subsequent consumer, packed-reference and write-ownership review.
"""

import bisect
import re
import struct

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inventory_shipyard_storage_v760 import BASE, CURRENT, ROOT, units
from scripts.verify_village_wrap_v608 import save


def main():
    clean, current = [NdsImage.open(p) for p in ('work/clean.nds', CURRENT)]
    source, arm = [r.read_file('/__arm9__.bin') for r in (clean, current)]
    lo, hi = BASE + 0x130000, 0x02171E48
    candidates = {}
    for name, base, raw in units(clean):
        for match in re.finditer(rb'(?=(...\x02))', raw, flags=re.DOTALL):
            target = int.from_bytes(match.group(1), 'little')
            if not lo <= target < hi:
                continue
            at = target - BASE
            end = source.find(b'\0', at, min(at + 1024, hi - BASE))
            if end < 0 or end - at < 40 or target % 4:
                continue
            text = source[at:end]
            try:
                decoded = text.decode('cp932')
            except UnicodeError:
                continue
            if any(ord(c) < 32 and c != '\n' for c in decoded):
                continue
            if not any('\u3040' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9fff' for c in decoded):
                continue
            finish = (end + 4) // 4 * 4
            old, now = source[at:finish], arm[at:finish]
            nz = now.find(b'\0')
            if old != now and (nz < 4 or not all(32 <= b < 127 or b in (10, 13) for b in now[:nz])
                               or not set(now[nz + 1:]) <= {0, 32}):
                continue
            row = candidates.setdefault(target, {'lo': target, 'hi': BASE + finish, 'clean_text': decoded,
                'source_hex': old.hex(), 'current_hex': now.hex(), 'clean_aliases': [], 'current_aliases': [], 'current_branches': [], 'crossing_current_Cstrings': []})
            row['clean_aliases'].append([name, base + match.start(), target])
    starts = sorted(candidates)
    def matching(target):
        return [candidates[p] for p in starts if p <= target < candidates[p]['hi']]
    for name, base, raw in units(current):
        for match in re.finditer(rb'(?=(...\x02))', raw, flags=re.DOTALL):
            target = int.from_bytes(match.group(1), 'little')
            for row in matching(target):
                row['current_aliases'].append([name, base + match.start(), target])
            if lo <= target < hi:
                end = arm.find(b'\0', target - BASE, min(target - BASE + 1024, hi - BASE))
                if end >= 0:
                    for p in starts:
                        if target < p <= BASE + end:
                            candidates[p]['crossing_current_Cstrings'].append([name, base + match.start(), target, BASE + end + 1])
        for at in range(0, len(raw) - 3, 4):
            word = struct.unpack_from('<I', raw, at)[0]
            if word & 0x0E000000 == 0x0A000000:
                delta = word & 0xFFFFFF
                if delta & 0x800000:
                    delta -= 0x1000000
                for row in matching(base + at + 8 + delta * 4):
                    row['current_branches'].append([name, base + at, base + at + 8 + delta * 4])
    leads = [candidates[p] for p in starts if not candidates[p]['current_aliases'] and not candidates[p]['current_branches'] and not candidates[p]['crossing_current_Cstrings']]
    save(ROOT / 'retired_constant_leads_NOT_FREE.json', {'source_ROM_sha256': sha(clean.source.read_bytes()),
         'current_ROM_sha256': sha(CURRENT.read_bytes()), 'candidates': [candidates[p] for p in starts], 'ownerless_leads': leads,
         'scope': 'Original aligned Japanese-bearing C-string constant leads in bounded main read-only text region; absolute aliases and aligned ARM branch scan only. Packed/computed/Thumb references, source allocation provenance and runtime writes remain required. No storage modification or approval.'})
    for row in sorted(leads, key=lambda r: r['hi'] - r['lo'], reverse=True)[:40]:
        print(hex(row['lo']), row['hi'] - row['lo'], row['clean_aliases'], row['clean_text'][:65].replace('\n', ' / '), flush=True)
    print(f'{len(candidates)} original C-string candidates; {len(leads)} ownerless leads NOT approved storage.', flush=True)


if __name__ == '__main__':
    main()
