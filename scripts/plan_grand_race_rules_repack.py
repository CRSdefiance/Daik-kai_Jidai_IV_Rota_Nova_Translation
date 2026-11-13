"""Research allocation for all nine complete race-help paragraphs; no ROM build."""
import argparse
import hashlib
import json
import struct
from pathlib import Path

from dk4tool.rom.nds import NdsImage


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--formatted', action='store_true')
    args = parser.parse_args()
    manuscript_path = Path('translations/grand_race_rules_manuscript_v2.json')
    manuscript = json.loads(manuscript_path.read_text(encoding='utf-8'))
    candidate = NdsImage.open('out/all_routes_combined_v133_candidate.nds')
    source = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    original = candidate.read_file('/__arm9__.bin')
    rows = sorted(manuscript['records'], key=lambda r: r['source_offset'])
    formatted = {}
    if args.formatted:
        report = json.loads(Path('work/qa/grand_race_help/report.json').read_text(encoding='utf-8'))
        if report['manuscript_sha256'] != hashlib.sha256(manuscript_path.read_bytes()).hexdigest():
            raise ValueError('Formatted report has stale manuscript hash')
        formatted = {r['id']: r for r in report['entries']}
        if set(formatted) != {r['id'] for r in rows}:
            raise ValueError('Formatted selection set differs')
    assert len(rows) == 9
    start = rows[0]['source_offset']
    end = rows[-1]['source_offset'] + len(bytes.fromhex(rows[-1]['source_hex']))
    assert (start, end) == (0x137B90, 0x138294)
    if source[start:end] != original[start:end]:
        raise ValueError('Complete race-help source region differs')
    cursor = start
    for row in rows:
        offset = row['source_offset']
        raw = bytes.fromhex(row['source_hex'])
        if source[offset:offset + len(raw)] != raw or not raw.endswith(b'\0'):
            raise ValueError('Clean page source differs')
        if any(source[cursor:offset]):
            raise ValueError('Nonzero data between complete help strings')
        cursor = offset + len(raw)
    rebuilt = bytearray(original)
    region = bytearray(end - start)
    cursor = 0
    mappings = []
    for row in rows:
        # D5404 reads bodies with LDRSB/LDRB. Only pointer fields require
        # word alignment; complete NUL-terminated bodies are byte strings.
        if not args.formatted:
            cursor = (cursor + 3) & ~3
        body = bytes.fromhex(formatted[row['id']]['encoded_hex']) if args.formatted else row['english'].encode('ascii')
        if args.formatted and (' '.join(formatted[row['id']]['visible_lines']) != row['english'] or b'\0' in body):
            raise ValueError('Formatted paragraph differs from complete manuscript')
        raw = body + b'\0'
        if cursor + len(raw) > len(region):
            raise ValueError('Complete English exceeds the original help region')
        region[cursor:cursor + len(raw)] = raw
        pointer_field = row['descriptor_offset'] + 4
        expected = 0x02000000 + row['source_offset']
        if struct.unpack_from('<I', original, pointer_field)[0] != expected:
            raise ValueError('Mapped body descriptor changed')
        new_offset = start + cursor
        struct.pack_into('<I', rebuilt, pointer_field, 0x02000000 + new_offset)
        mappings.append({'id': row['id'], 'old_offset': row['source_offset'],
                         'new_offset': new_offset, 'pointer_field': pointer_field,
                         'bytes_including_nul': len(raw)})
        cursor += len(raw)
    rebuilt[start:end] = region
    allowed = set(range(start, end))
    for mapping in mappings:
        allowed.update(range(mapping['pointer_field'], mapping['pointer_field'] + 4))
        pointer = struct.unpack_from('<I', rebuilt, mapping['pointer_field'])[0] - 0x02000000
        selected = bytes(rebuilt[pointer:]).split(b'\0', 1)[0].decode('ascii')
        row = next(r for r in rows if r['id'] == mapping['id'])
        expected = bytes.fromhex(formatted[row['id']]['encoded_hex']).decode('ascii') if args.formatted else row['english']
        if selected != expected:
            raise ValueError('Mapped selection drops or changes text')
    assert len(rebuilt) == len(original)
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(original, rebuilt, strict=True)))
    out = Path('work/analysis/grand_race_rules_formatted_repack' if args.formatted else 'work/analysis/grand_race_rules_repack')
    out.mkdir(parents=True, exist_ok=True)
    (out / 'ARM9.bin').write_bytes(rebuilt)
    report = {'status': 'formatted-research-allocation-not-playable' if args.formatted else 'research-allocation-only-unformatted-not-playable',
              'source_candidate': str(candidate.source),
              'source_arm9_sha256': hashlib.sha256(original).hexdigest(),
              'research_arm9_sha256': hashlib.sha256(rebuilt).hexdigest(),
              'manuscript_sha256': hashlib.sha256(manuscript_path.read_bytes()).hexdigest(),
              'region_start': start, 'region_end': end, 'region_bytes': len(region),
              'body_alignment_bytes': 1 if args.formatted else 4,
              'paragraphs_and_alignment_bytes': cursor,
              'remaining_bytes_before_actual_formatting': None if args.formatted else len(region) - cursor,
              'remaining_bytes_after_actual_formatting': len(region) - cursor if args.formatted else None,
              'all_nine_complete_paragraphs_selected_exactly': True,
              'changes_only_original_help_blob_and_nine_body_pointer_fields': True,
              'ARM9_size_unchanged': True, 'mappings': mappings,
              'limitations': ['No live page/navigation behavior verified.',
                              'Formatted mode uses the traced context and protected-break codec; raw mode has no presentation approval.',
                              'No playable ROM created or profile registered.',
                              'Consumer/reference coverage must be finished before relocation is integrated.']}
    (out / 'plan.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('status', 'region_bytes', 'paragraphs_and_alignment_bytes',
                                           'remaining_bytes_before_actual_formatting',
                                           'remaining_bytes_after_actual_formatting')}))


if __name__ == '__main__':
    main()
