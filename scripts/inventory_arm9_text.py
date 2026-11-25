"""Inventory Japanese/full-width C strings and text islands across ARM9/overlays."""
import argparse
import hashlib
import json
import struct
from collections import Counter
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.rom.nds import NdsImage
from dk4tool.script.arm9_profiles import PROFILES


def japanese_char(char):
    return ('\u3040' <= char <= '\u30ff' or '\u3400' <= char <= '\u9fff'
            or '\uff66' <= char <= '\uff9d')


def fullwidth_char(char):
    # Full-width Latin/digits/symbols are text-bearing UI candidates too.
    return '\uff01' <= char <= '\uff60' or '\uffe0' <= char <= '\uffe6'


def scan(data):
    """Cover all NUL spans and control-bounded printable byte islands.

    No minimum string length, two-character threshold, starting address or
    64-byte cutoff. Binary-looking candidates are retained for classification.
    """
    spans = {}
    start = 0
    for end, value in enumerate(data):
        if value == 0:
            if end > start:
                spans[start, end] = 'nul-bounded'
            start = end + 1
    if start < len(data):
        spans[start, len(data)] = 'unterminated-tail'
    start = 0
    for end, value in enumerate(data):
        if value < 32 and value not in (9, 10, 13) or value == 127:
            if end > start:
                spans.setdefault((start, end), 'control-bounded-island')
            start = end + 1
    if start < len(data):
        spans.setdefault((start, len(data)), 'unterminated-island')
    rows = []
    for (start, end), boundary in sorted(spans.items()):
        raw = data[start:end]
        try:
            text = raw.decode('cp932')
        except UnicodeDecodeError:
            continue
        if (not any(japanese_char(char) or fullwidth_char(char) for char in text)
                or not all(char.isprintable() or char in '\r\n\t\u3000' for char in text)):
            continue
        rows.append({'offset': start, 'end': end, 'length': len(raw),
                     'text': text, 'current_hex': raw.hex().upper(),
                     'boundary': boundary, 'nul_terminated': end < len(data) and data[end] == 0,
                     'japanese_character_count': sum(japanese_char(char) for char in text),
                     'fullwidth_character_count': sum(fullwidth_char(char) for char in text),
                     'halfwidth_kana_only': (any('\uff66' <= c <= '\uff9d' for c in text)
                                            and not any('\u3040' <= c <= '\u30ff'
                                                        or '\u3400' <= c <= '\u9fff' for c in text)),
                     'classification': 'unclassified-text-or-binary-candidate'})
    return rows


def pointer_references(rows, components, base):
    """Record aligned words pointing anywhere within a candidate byte span.

    An address-like word is evidence to trace, not proof of a displayed label.
    """
    targets = {}
    for index, row in enumerate(rows):
        row['aligned_pointer_candidates'] = []
        for delta in range(row['length']):
            targets.setdefault(base + row['offset'] + delta, []).append((index, delta))
    for name, _, raw in components:
        for offset in range(0, len(raw) - 3, 4):
            value = struct.unpack_from('<I', raw, offset)[0]
            for index, delta in targets.get(value, []):
                rows[index]['aligned_pointer_candidates'].append({
                    'component': name, 'word_offset': offset, 'target_address': value,
                    'interior_byte_offset': delta})


def components(image):
    result = [('arm9', 0x02000000, image.read_file('/__arm9__.bin'))]
    overlays = loadOverlayTable(image.rom.arm9OverlayTable, lambda oid, fid: image.files[fid])
    result.extend((f'arm9_overlay_{oid}', overlay.ramAddress, bytes(overlay.data))
                  for oid, overlay in overlays.items())
    return result


def loaded_components(image):
    """Inventory each SDK section at its actual load address, not file offset."""
    code = MainCodeFile(image.read_file('/__arm9__.bin'), image.rom.arm9RamAddress)
    result = [(f'arm9_section_{number}', section.ramAddress, bytes(section.data))
              for number, section in enumerate(code.sections)]
    overlays = loadOverlayTable(image.rom.arm9OverlayTable, lambda oid, fid: image.files[fid])
    result.extend((f'arm9_overlay_{oid}', overlay.ramAddress, bytes(overlay.data))
                  for oid, overlay in overlays.items())
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--clean', type=Path, default=Path('work/clean.nds'))
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--loaded-sections', action='store_true', help='Include every auto-loaded section at its native runtime address.')
    args = parser.parse_args()
    clean, candidate = NdsImage.open(args.clean), NdsImage.open(args.candidate)
    inventory_components = loaded_components if args.loaded_sections else components
    current_components = inventory_components(candidate)
    source_components = {name: (base, raw) for name, base, raw in inventory_components(clean)}
    records = []
    for name, base, raw in current_components:
        source_base, source = source_components.get(name, (base, None))
        if base != source_base:
            raise ValueError('Source/candidate component load addresses differ')
        rows = scan(raw)
        pointer_references(rows, current_components, base)
        for row in rows:
            offset, end = row['offset'], row['end']
            original = source[offset:end] if source is not None else None
            row.update({'component': name, 'runtime_address': base + offset,
                        'clean_same_span_hex': original.hex().upper() if original is not None else None,
                        'same_span_bytes_unchanged': original == raw[offset:end] if original is not None else None,
                        'component_exists_in_clean': source is not None,
                        'profile_owners': [e.row_id for e in PROFILES['all']
                                           if name in ('arm9', 'arm9_section_0') and e.offset <= offset < e.offset + e.source_length]})
            try:
                row['clean_same_span_text'] = original.decode('cp932') if original is not None else None
            except UnicodeDecodeError:
                row['clean_same_span_text'] = None
            # Exact mapped ASCII glyph data is still reported, but cannot be
            # mistaken for untranslated dialogue just because it decodes.
            if name in ('arm9', 'arm9_section_0') and 0x125A60 <= offset and end <= 0x125A60 + 95 * 11:
                from dk4tool.dialogue.font_audit import REFERENCE_ASCII_FONT_SHA256
                if hashlib.sha256(raw[0x125A60:0x125A60 + 95 * 11]).hexdigest() == REFERENCE_ASCII_FONT_SHA256:
                    row['classification'] = 'verified-native-ascii-font-data'
        records.extend(rows)
    summary = {'candidate_count': len(records),
               'component_counts': dict(Counter(r['component'] for r in records)),
               'candidates_with_aligned_address_references': sum(bool(r['aligned_pointer_candidates']) for r in records),
               'single_japanese_character_candidates': sum(r['japanese_character_count'] == 1 for r in records),
               'fullwidth_character_candidates': sum(r['fullwidth_character_count'] > 0 for r in records),
               'ideographic_space_candidates': sum('\u3000' in r['text'] for r in records),
               'over_64_byte_candidates': sum(r['length'] > 64 for r in records),
               'before_legacy_start_candidates': sum(r['component'] in ('arm9', 'arm9_section_0') and r['offset'] < 0x110000 for r in records),
               'classification_counts': dict(Counter(r['classification'] for r in records))}
    report = {'format': 'dk4-arm9-text-candidate-inventory-v3' if args.loaded_sections else 'dk4-arm9-text-candidate-inventory-v2',
              'all_native_autoload_sections_included': args.loaded_sections,
              'candidate': args.candidate.as_posix(),
              'candidate_sha256': hashlib.sha256(args.candidate.read_bytes()).hexdigest(),
              'clean': args.clean.as_posix(), 'clean_sha256': hashlib.sha256(args.clean.read_bytes()).hexdigest(),
              'components': [{'name': n, 'load_address': b, 'size': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
                             for n, b, raw in current_components], 'summary': summary, 'records': records,
              'limitations': ['Candidate counts are not untranslated UI counts.',
                              'Random binary bytes can decode as CP932; unclassified candidates remain explicit.',
                              'Aligned address words need consumer tracing; absence does not prove unused text.',
                              'Fixed nonterminated fields, control grammars, generated strings and compressed data require separate coverage.',
                              'This does not inventory Japanese raster graphics.']}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
