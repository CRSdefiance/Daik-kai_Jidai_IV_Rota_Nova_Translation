"""Inventory every V150 filesystem resource without claiming graphics clearance."""

import hashlib
import json
from collections import Counter
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage

SOURCE = '3a1ff1f8f1734ba41c24057cee160b6b5aa2bdbc9c38dc08da8ce896dd972a8e'
CLEAN = 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    candidate = Path('out/all_routes_combined_v150_candidate.nds')
    clean_path = Path('work/clean.nds')
    if sha(candidate.read_bytes()) != SOURCE or sha(clean_path.read_bytes()) != CLEAN:
        raise ValueError('Exact V150 and clean ROMs required')
    image = NdsImage.open(candidate)
    clean = NdsImage.open(clean_path)
    clean_files = {path: raw for _, path, raw in clean.iter_files()}
    current_files = {path: raw for _, path, raw in image.iter_files()}
    loose = {}
    for version, files in (('current', current_files), ('clean', clean_files)):
        for path, raw in files.items():
            if Path(path).suffix.lower() == '.pxl':
                loose.setdefault(sha(raw), []).append({'version': version, 'path': path})
    rows = []
    for file_id, path, raw in image.iter_files():
        extension = Path(path).suffix.lower()
        if extension in ('.pxl', '.fls'):
            status = 'covered-by-pxl-fls-thumbnail-inventory-only'
        elif path.upper().startswith('/GRP/'):
            status = 'graphics-directory-resource-review-pending'
        else:
            status = 'other-resource-content-classification-pending'
        rows.append({'file_id': file_id, 'path': path, 'extension': extension,
                     'length': len(raw), 'sha256': sha(raw),
                     'equals_clean': raw == clean_files.get(path),
                     'container_marker': 'ILNK' if raw.startswith(b'ILNK') else None,
                     'review_status': status})
    paths = [r['path'] for r in rows]
    if len(paths) != len(set(paths)) or set(paths) != set(clean_files):
        raise ValueError('Filesystem identity differs or duplicate paths exist')
    outside = [r for r in rows if r['extension'] not in ('.pxl', '.fls')]
    archives = []
    for row in outside:
        if not row['path'].upper().startswith('/GRP/') or row['container_marker'] != 'ILNK':
            continue
        raw = current_files[row['path']]
        parsed = IlnkContainer.parse(raw)
        if parsed.to_bytes() != raw:
            raise ValueError('Graphics archive roundtrip differs')
        blocks = []
        for index, block in enumerate(parsed.blocks):
            matches = loose.get(sha(block), [])
            blocks.append({'block_index': index, 'length': len(block),
                           'sha256': sha(block), 'exact_loose_pxl_matches': matches,
                           'review_status': 'exact-loose-image-copy-native-use-pending'
                           if matches else 'block-format-and-content-review-pending'})
        archives.append({'path': row['path'], 'sha256': row['sha256'],
                         'roundtrip_exact': True, 'block_count': len(blocks), 'blocks': blocks})
    report = {'source_rom_sha256': SOURCE, 'clean_rom_sha256': CLEAN,
              'filesystem_files': len(rows),
              'extensions': dict(sorted(Counter(r['extension'] for r in rows).items())),
              'outside_pxl_fls_files': len(outside),
              'grp_resources': [r for r in outside if r['path'].upper().startswith('/GRP/')],
              'grp_ilnk_archives': archives,
              'files': rows,
              'limitations': ['Filename and extension do not prove content or use.',
                              'Unchanged clean resources may still need translation.',
                              'Embedded resources, executable graphics and native crop mapping remain open.']}
    out = Path('work/analysis/other_graphics_v150_inventory.json')
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    summary = {k: report[k] for k in ('filesystem_files', 'extensions', 'outside_pxl_fls_files')}
    summary['grp_resources'] = len(report['grp_resources'])
    summary['archives'] = [{'path': r['path'], 'blocks': r['block_count'],
                            'exact_loose_pxl_matches': sum(bool(b['exact_loose_pxl_matches'])
                                                           for b in r['blocks'])}
                           for r in archives]
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
