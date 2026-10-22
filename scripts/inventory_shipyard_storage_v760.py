"""Find source-record ownership leads, never infer free space from zero padding."""

import bisect
import json
import re
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import save

BASE = 0x02000000
ROOT = Path('work/analysis/shipyard_storage_v760')
CURRENT = Path('out/all_routes_combined_v758_candidate.nds')


def units(rom):
    code = MainCodeFile(rom.read_file('/__arm9__.bin'), BASE)
    result = [(f'section{i}', POOL if i == 3 else s.ramAddress, bytes(s.data)) for i, s in enumerate(code.sections)]
    result += [(f'overlay{i}', s.ramAddress, bytes(s.data)) for i, s in loadOverlayTable(
        rom.rom.arm9OverlayTable, lambda _, f: rom.rom.files[f]).items()]
    return result


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    clean, current = [NdsImage.open(p) for p in ('work/clean.nds', CURRENT)]
    arm = current.read_file('/__arm9__.bin')
    main_size = len(MainCodeFile(arm, BASE).sections[0].data)
    candidates = {}
    for path in Path('translations').glob('*.json'):
        try:
            doc = json.loads(path.read_text(encoding='utf-8'))
        except (ValueError, UnicodeError):
            continue
        if not isinstance(doc, dict):
            continue
        for row in doc.get('records', []):
            if not isinstance(row, dict) or not isinstance(row.get('offset'), int) or not isinstance(row.get('source_hex'), str):
                continue
            at, raw = row['offset'], bytes.fromhex(row['source_hex'])
            if at < 0 or len(raw) < 24 or at + len(raw) > main_size:
                continue
            now = arm[at:at + len(raw)]
            end = now.find(b'\0')
            if end < 4 or not all(32 <= c < 127 or c in (10, 13) for c in now[:end]):
                continue
            lo, hi = BASE + at, BASE + at + len(raw)
            if lo < 0x02172464 and hi > 0x02171E48:
                continue
            key = (lo, hi)
            candidate = candidates.setdefault(key, {'lo': lo, 'hi': hi, 'current_hex': now.hex(),
                'visible': now[:end].decode('ascii'), 'source_records': [],
                'clean_aliases': [], 'current_aliases': [], 'current_branches': []})
            candidate['source_records'].append({'batch': str(path), 'id': row.get('id'), 'source_hex': row['source_hex']})
    rows = sorted(candidates.values(), key=lambda r: (r['lo'], r['hi']))
    starts = [r['lo'] for r in rows]
    # Keep overlapping historical allocations separate. A pointer into any of
    # them is retained; a broader old record cannot hide an interior owner.
    def matches(target):
        stop = bisect.bisect_right(starts, target)
        for k in range(max(0, stop - 100), stop):
            row = rows[k]
            if row['lo'] <= target < row['hi']:
                yield row
    for label, rom in (('clean', clean), ('current', current)):
        for name, base, raw in units(rom):
            for match in re.finditer(rb'(?=(...\x02))', raw, flags=re.DOTALL):
                target = int.from_bytes(match.group(1), 'little')
                if starts[0] <= target < rows[-1]['hi']:
                    for row in matches(target):
                        row[label + '_aliases'].append([name, base + match.start(), target])
            if label == 'current':
                for at in range(0, len(raw) - 3, 4):
                    word = struct.unpack_from('<I', raw, at)[0]
                    if word & 0x0E000000 != 0x0A000000:
                        continue
                    delta = word & 0xFFFFFF
                    if delta & 0x800000:
                        delta -= 0x1000000
                    target = base + at + 8 + delta * 4
                    if starts[0] <= target < rows[-1]['hi']:
                        for row in matches(target):
                            row['current_branches'].append([name, base + at, target])
    unused_leads = [r for r in rows if not r['current_aliases'] and not r['current_branches']]
    save(ROOT / 'source_record_leads_NOT_FREE.json', {'current_ROM_sha256': sha(CURRENT.read_bytes()),
        'all_source_record_candidates': rows, 'no_current_absolute_or_aligned_ARM_branch_leads': unused_leads,
        'scope': 'Candidate discovery only. Confirm complete source allocations, historical owners/replacements, packed or computed references, actual consumer and runtime write exclusions before any reuse.',
        'overlapping_record_search_window': 100, 'maximum_records_at_one_start': max(starts.count(p) for p in set(starts)),
        'producer_sha256': sha(Path(__file__).read_bytes()), 'no_ROM_or_storage_change': True})
    for row in sorted(unused_leads, key=lambda r: r['hi'] - r['lo'], reverse=True)[:30]:
        print(hex(row['lo']), row['hi'] - row['lo'], len(row['clean_aliases']), row['visible'][:100], [r['id'] for r in row['source_records'][:2]], flush=True)
    print(f'{len(rows)} source-record candidates; {len(unused_leads)} ownerless leads, not approved storage.', flush=True)


if __name__ == '__main__':
    main()
