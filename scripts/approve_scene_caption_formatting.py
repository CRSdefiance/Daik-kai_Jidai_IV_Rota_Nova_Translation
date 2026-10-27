"""Approve native caption formatting only with complete wrapper/raster evidence."""

import copy
import hashlib
import json
from pathlib import Path

MANUSCRIPT = Path('translations/scene_caption_manuscript_v2.json')
RASTER = Path('work/analysis/scene_caption_complete_scoped_raster_v137/report.json')
WRAPPERS = Path('work/analysis/scene_caption_complete_wrapper_v137_proof.json')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def approve(document, raster, wrappers):
    if raster['proposed_arm9_sha256'] != wrappers['proposed_arm9_sha256']:
        raise ValueError('Caption raster/wrapper proposals differ')
    if raster['manuscript_sha256'] != wrappers['manuscript_sha256']:
        raise ValueError('Caption native proofs cover different manuscripts')
    if wrappers['status'] != 'pass-complete-native-caption-wrappers-and-inherited-compatibility':
        raise ValueError('Complete native wrapper evidence is required')
    if len(document['records']) != 164 or len({row['id'] for row in document['records']}) != 164:
        raise ValueError('Every complete scene caption is required')
    expected = {(row['id'], mode) for row in document['records'] for mode in (4, 16)}
    for proof in (raster, wrappers):
        actual = [(row['id'], row['mode']) for row in proof['cases']]
        if len(actual) != 328 or set(actual) != expected:
            raise ValueError('Full native raster case coverage is incomplete')
    if any(not row['native_cleanup_executed'] for row in wrappers['cases']):
        raise ValueError('Native wrapper cleanup is unverified')
    if len(wrappers['callers']) != 12 or len(wrappers['compatibility_cases']) != 20 or len(raster['compatibility_cases']) != 88:
        raise ValueError('Native caller/compatibility coverage is incomplete')
    pixels = {(row['id'], row['mode']): row['pixels_sha256'] for row in raster['cases']}
    records = {row['id']: row for row in document['records']}
    for case in wrappers['cases']:
        row = records[case['id']]
        if case['glyph_count'] != len(row['english']) or case['pixels_sha256'] != pixels[case['id'], case['mode']]:
            raise ValueError('Complete native wrapper text/pixels differ from caption raster')
    result = copy.deepcopy(document)
    for row in result['records']:
        if not all(row['review'][gate] is True for gate in ('source', 'context', 'localization', 'naturalness')):
            raise ValueError('Editorial review is incomplete')
        if not row['english'].isascii() or '\n' in row['english'] or len(row['english']) * 5 > 256:
            raise ValueError('Native full-caption formatting is not supported')
        row['review']['formatting'] = True
        row['presentation'] = 'native-scene-caption-complete-ascii-five-pixel-generic-class'
        row['native_centering_width_pixels'] = len(row['english']) * 5
    result['status'] = 'reviewed-native-caption-formatting-experimental-runtime-pending'
    result['native_formatting_limits'] = wrappers['limitations']
    result['integration_blockers'] = [
        'Strict staged source/ownership/dependency release component and registration remain pending.',
        'Physical screen routing, bitmap clear body, Japanese ITCM pixels and cold-boot gameplay remain unverified.',
        'Separate COMMON consumers are unresolved; this grants no COMMON integration approval.']
    return result


def main():
    raw = MANUSCRIPT.read_bytes()
    raster, wrappers = [json.loads(path.read_text()) for path in (RASTER, WRAPPERS)]
    if sha(raw) != wrappers['manuscript_sha256'] or sha(RASTER.read_bytes()) != wrappers['raster_proof_sha256']:
        raise ValueError('Native formatting evidence lineage differs')
    document = approve(json.loads(raw), raster, wrappers)
    document['native_formatting_evidence'] = {path.as_posix(): sha(path.read_bytes()) for path in (RASTER, WRAPPERS)}
    document['source_reviewed_manuscript_sha256'] = sha(raw)
    MANUSCRIPT.write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('All 164 native caption formatting reviews recorded; experimental release/runtime gates remain.')


if __name__ == '__main__':
    main()
