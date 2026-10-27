"""Research allocation for complete Grand Race UI prose; never write a ROM."""

import hashlib
import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_waiting_widget import rewrite_function
from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_waiting_widgets import TABLE, execute
from scripts.prepare_grand_race_remaining_ui_manuscript import (
    BASE,
    CANDIDATE,
    CANDIDATE_SHA,
    CANONICAL,
    CANONICAL_SHA,
    CLEAN_ARM9_SHA,
)
from scripts.probe_grand_race_wireless_return import balanced_lines

ALIASES = {'TITLE': 0x137A98, 'BASIC_RULES': 0x1379CC, 'ABOUT': 0x137AA8}


def merge_ranges(ranges):
    merged = []
    for lo, hi in sorted(ranges):
        if lo >= hi:
            raise ValueError('Invalid owned source range')
        if merged and lo < merged[-1][1]:
            raise ValueError('Overlapping source owners')
        if merged and lo == merged[-1][1]:
            merged[-1][1] = hi
        else:
            merged.append([lo, hi])
    return merged


def allocate(entries, free):
    """Bounded bin packing; preserve full strings even when greedy fitting fails."""
    spans = [list(span) for span in free]
    ordered = sorted(entries, key=lambda entry: (-len(entry[1]), entry[0]))
    failed, result = set(), {}
    visits = 0

    def search(index):
        nonlocal visits
        visits += 1
        if visits > 500000:
            raise ValueError('Allocation search limit reached; no incomplete plan may ship')
        if index == len(ordered):
            return True
        capacities = tuple(sorted(hi - lo for lo, hi in spans))
        state = (index, capacities)
        if state in failed:
            return False
        key, raw = ordered[index]
        choices = sorted((hi - lo, lo, slot) for slot, (lo, hi) in enumerate(spans) if hi - lo >= len(raw))
        tried = set()
        for capacity, offset, slot in choices:
            if capacity in tried:
                continue
            tried.add(capacity)
            spans[slot][0] += len(raw)
            result[key] = offset
            if search(index + 1):
                return True
            spans[slot][0] = offset
            result.pop(key)
        failed.add(state)
        return False

    if sum(len(raw) for _, raw in entries) > sum(hi - lo for lo, hi in spans) or not search(0):
        raise ValueError('Complete strings do not fit the owned pool; relocation must expand')
    return result, [span for span in spans if span[0] < span[1]]


def subtract_ranges(ranges, reserved):
    free = [list(span) for span in ranges]
    for start, end in reserved:
        next_free = []
        for lo, hi in free:
            if end <= lo or start >= hi:
                next_free.append([lo, hi])
            else:
                if lo < start:
                    next_free.append([lo, start])
                if end < hi:
                    next_free.append([end, hi])
        free = next_free
    return free


def main():
    for path, expected in ((CANONICAL, CANONICAL_SHA), (CANDIDATE, CANDIDATE_SHA)):
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Pinned input ROM differs')
    sources = [NdsImage.open(path).read_file('/__arm9__.bin')
               for path in ('work/clean.nds', CANONICAL, CANDIDATE)]
    if hashlib.sha256(sources[0]).hexdigest() != CLEAN_ARM9_SHA:
        raise ValueError('Clean Japanese ARM9 differs')
    original = sources[2]
    manuscript_path = Path('translations/grand_race_remaining_ui_manuscript_v2.json')
    manuscript = json.loads(manuscript_path.read_text(encoding='utf-8'))
    rows = {row['id'].removeprefix('GRAND_RACE_UI_'): row for row in manuscript['records']}
    parts = [part for row in rows.values() for part in row['source_parts_in_reading_order']]
    if len(rows) != 51 or len(parts) != 59:
        raise ValueError('Complete scoped manuscript changed')
    ranges, expected_refs = [], {}
    for part in parts:
        lo, size = part['offset'], part['aligned_source_bytes_including_nul']
        raw = bytes.fromhex(part['source_hex'])
        if any(source[lo:lo + size] != raw + bytes(size - len(raw)) for source in sources):
            raise ValueError('Source text/padding differs')
        ranges.append((lo, lo + size))
        for field in part['aligned_pointer_fields']:
            if any(struct.unpack_from('<I', source, field)[0] != BASE + lo for source in sources):
                raise ValueError('Original pointer selection differs')
            expected_refs[field] = lo
    owned = merge_ranges(ranges)
    # Reconcile every aligned pointer into any owned byte, not only starts.
    for field in range(0, len(original) - 3, 4):
        target = struct.unpack_from('<I', original, field)[0] - BASE
        if any(lo <= target < hi for lo, hi in owned) and expected_refs.get(field) != target:
            raise ValueError(f'Unmapped interior/extra aligned reference at {field:#x}')
    role_report = json.loads(Path('work/qa/grand_race_wireless_roles/report.json').read_text(encoding='utf-8'))
    if role_report['manuscript_sha256'] != hashlib.sha256(manuscript_path.read_bytes()).hexdigest() or not role_report['preview_reviewed']:
        raise ValueError('Role allocation requires the current reviewed complete prose')
    proposed, code_changes = rewrite_function(original)
    proposed = bytearray(proposed)
    for lo, hi in owned:
        proposed[lo:hi] = bytes(hi - lo)
    selections, entries = [], []
    for name, row in rows.items():
        source_parts = row['source_parts_in_reading_order']
        count = 3 if name == 'HOST_SELECTING' else len(source_parts)
        lines = [selection['line'] for selection in role_report['selections']] if name == 'ROLES' else balanced_lines(row['english'], count)
        if ' '.join(lines) != row['english']:
            raise ValueError('Formatted text changes full prose')
        for index, line in enumerate(lines):
            raw = line.encode('ascii') + b'\0'
            selection = {'key': f'{name}:{index}', 'message': name, 'line': line,
                         'raw_hex': raw.hex(), 'pointer_fields': source_parts[index]['aligned_pointer_fields'] if index < len(source_parts) else []}
            if name == 'ROLES':
                if raw.hex() != role_report['selections'][index]['replacement_hex'][:len(raw) * 2]:
                    raise ValueError('Reviewed role line differs')
                entries.append((selection['key'], raw))
            elif name == 'RETURN_MENU':
                selection['offset'] = 0x16B93C + sum(len(previous['line']) + 1 for previous in selections if previous['message'] == name)
            elif name in ALIASES:
                selection['offset'] = ALIASES[name]
                if original[selection['offset']:selection['offset'] + len(raw)] != raw:
                    raise ValueError('Shared title is not exactly identical and terminated')
                selection['alias_sha256'] = hashlib.sha256(raw).hexdigest()
            else:
                entries.append((selection['key'], raw))
            selections.append(selection)
    # A complete identical native line can be shared without changing prose.
    # Prefer fixed/previously existing selections so duplicate fragments consume
    # no further owned bytes (e.g. the two "Touch the lower screen" instructions).
    representatives = {}
    entries = []
    for selection in sorted(selections, key=lambda selection: ('offset' not in selection, selection['key'])):
        raw = bytes.fromhex(selection['raw_hex'])
        if raw in representatives:
            selection['shared_key'] = representatives[raw]['key']
        else:
            representatives[raw] = selection
            if 'offset' not in selection:
                entries.append((selection['key'], raw))
    free = subtract_ranges(owned, [(0x16B93C, 0x16B980),
                                  (TABLE, TABLE + 12)])
    allocations, unused = allocate(entries, free)
    by_key = {selection['key']: selection for selection in selections}
    for selection in selections:
        if 'shared_key' not in selection:
            selection['offset'] = selection.get('offset', allocations.get(selection['key']))
    for selection in selections:
        offset = by_key[selection['shared_key']]['offset'] if 'shared_key' in selection else selection['offset']
        selection['offset'] = offset
        raw = bytes.fromhex(selection['raw_hex'])
        proposed[offset:offset + len(raw)] = raw
        for field in selection['pointer_fields']:
            struct.pack_into('<I', proposed, field, BASE + offset)
    if TABLE & 3 or not any(lo <= TABLE and TABLE + 12 <= hi for lo, hi in owned):
        raise ValueError('Extra table is outside owned aligned source data')
    if any(selection['offset'] < TABLE + 12 and TABLE < selection['offset'] + len(bytes.fromhex(selection['raw_hex'])) for selection in selections):
        raise ValueError('Extra table overlaps complete prose')
    host = [selection for selection in selections if selection['message'] == 'HOST_SELECTING']
    for index, selection in enumerate(host):
        struct.pack_into('<I', proposed, TABLE + index * 4, BASE + selection['offset'])
    struct.pack_into('<I', proposed, 0xF89DC, BASE + TABLE)
    execution = execute(proposed, tuple(BASE + selection['offset'] for selection in host), scratch_table=False)
    for selection in selections:
        offset = selection['offset']
        saved = bytes(proposed[offset:proposed.index(0, offset)])
        if saved.decode('ascii') != selection['line']:
            raise ValueError('Saved allocation lost a leading character or string boundary')
        for field in selection['pointer_fields']:
            if struct.unpack_from('<I', proposed, field)[0] != BASE + offset:
                raise ValueError('Saved text pointer differs')
    allowed = owned + [[field, field + 4] for field in expected_refs] + [[change['offset'], change['offset'] + 4] for change in code_changes] + [[0xF89DC, 0xF89E0]]
    if len(proposed) != len(original):
        raise ValueError('Research plan changes ARM9 size')
    changed = [offset for offset, (old, new) in enumerate(zip(original, proposed, strict=True)) if old != new]
    if any(not any(lo <= offset < hi for lo, hi in allowed) for offset in changed):
        raise ValueError('Research allocation changed unrelated bytes')
    output = Path('work/analysis/grand_race_ui_allocation')
    output.mkdir(parents=True, exist_ok=True)
    report = {'status': 'research-complete-prose-allocation-not-release-ready', 'rom_written': False,
              'manuscript_sha256': hashlib.sha256(manuscript_path.read_bytes()).hexdigest(),
              'candidate_sha256': CANDIDATE_SHA, 'owned_ranges': owned,
              'owned_bytes': sum(hi - lo for lo, hi in owned), 'unused_pool_ranges': unused,
              'selections': selections, 'extra_table': [TABLE, TABLE + 12],
              'bounded_native_execution': execution, 'changed_byte_count': len(changed),
              'limitations': ['Aligned pointers reconciled; unaligned/dynamic references still require consumer proof.',
                              'Three identical existing titles shared; ownership/profile dependency release gates pending.',
                              'Other menu/wireless screen consumers and exact-font layouts still pending.',
                              'Full screen composition and gameplay are not verified.',
                              'No build batch, ROM or completion/progress credit generated.']}
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f'{len(rows)} messages / {len(selections)} saved strings; {report["owned_bytes"]} owned bytes; allocation and native third-widget execution pass; no ROM written')


if __name__ == '__main__':
    main()
