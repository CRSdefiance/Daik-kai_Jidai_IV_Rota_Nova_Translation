"""Apply the source-reviewed artwork captions without changing artwork pixels."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from scripts.probe_common_display_name_hook import branch_link

SOURCE = '5d152c714ab1218e9f3df796c6dfc7c3e58f2ae0fff12cb45c76932605962db0'


def transform(source, clean, review, manuscripts):
    if sha(source) != SOURCE or not cache_plan(source):
        raise ValueError('Exact complete V275/V296 ARM9 required')
    rows = review['records']
    if len(rows) != 16 or len({r['pointer_field'] for r in rows}) != 16:
        raise ValueError('Exactly sixteen reviewed artwork caption fields required')
    source_rows = {r['id']: r for manuscript in manuscripts for r in manuscript['records']}
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    packed, stored, changes = bytearray(before[3][:-48]), {}, []
    for row in rows:
        original = source_rows[row['id']]
        field = row['pointer_field']
        if row['kind'] == 'scene':
            at, raw, expected_field = original['source_offset'], original['source_hex'], original['pointer_field']
        elif row['kind'] == 'gallery':
            lock = original['source_fields'][0]
            at, raw, expected_field = lock['source_pointer'] - BASE, lock['source_hex'], lock['field']
        else:
            raise ValueError('Unknown artwork caption consumer')
        if clean[at:clean.index(0, at)].hex() != raw or expected_field != field:
            raise ValueError('Original Japanese caption or pointer field differs')
        if original['japanese'] != row['source_Japanese'] or original['english'] != row['prior_english']:
            raise ValueError('Reviewed source context differs')
        if not all(row['review'].get(k) for k in ('source', 'context', 'localization', 'naturalness', 'formatting')):
            raise ValueError('Incomplete caption review')
        pointer = struct.unpack_from('<I', source, field)[0]
        old = (bytes(packed[pointer - POOL:]).split(b'\0', 1)[0] if pointer >= POOL else
               source[pointer - BASE:source.index(0, pointer - BASE)])
        if old.rstrip(b' ') != row['prior_english'].encode('ascii'):
            raise ValueError('Current complete caption differs')
        text = row['compiled_text'].encode('ascii')
        if not text or b'\0' in text or text.rstrip(b' ') != row['english'].encode('ascii'):
            raise ValueError('Incomplete or malformed English caption')
        if text not in stored:
            packed.extend(bytes(-len(packed) % 4))
            stored[text] = POOL + len(packed)
            packed.extend(text + b'\0')
        struct.pack_into('<I', code.sections[0].data, field, stored[text])
        changes.append({'id': row['id'], 'kind': row['kind'], 'pointer_field': field,
                        'old_pointer': pointer, 'target_pointer': stored[text],
                        'source_Japanese': row['source_Japanese'], 'English': row['english'],
                        'compiled_text_hex': text.hex()})
    packed.extend(bytes(-len(packed) % 32))
    size = len(packed) + 64
    if POOL + size > STAGE or STAGE + size + 48 > 0x023F4000:
        raise ValueError('Owned caption memory exceeds safe bounds')
    packed.extend(wrapper(STAGE + len(packed), STAGE + size, size, source))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack('<I', size)
    struct.pack_into('<I', code.sections[0].data, 0x8E4, branch_link(BASE + 0x8E4, STAGE + size - 64))
    struct.pack_into('<I', code.sections[0].data, 0xE45DC, POOL + size)
    saved = bytes(code.save())
    parsed = MainCodeFile(saved, BASE)
    restored = bytearray(parsed.sections[0].data)
    for field in [r['pointer_field'] for r in rows] + [0x8E4, 0xE45DC]:
        restored[field:field + 4] = before[0][field:field + 4]
    at = code.codeSettingsOffs
    restored[at:at + 12] = before[0][at:at + 12]
    if (restored != before[0] or any(bytes(parsed.sections[n].data) != before[n] for n in (1, 2))
            or bytes(parsed.sections[3].data[:len(before[3]) - 48]) != before[3][:-48]):
        raise ValueError('Unrelated native code or inherited payload changes')
    return saved, {'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(saved),
                   'records': changes, 'changed_records': [r['id'] for r in rows],
                   'pool_payload_bytes': size, 'inherited_pool_bytes_preserved': len(before[3]) - 48,
                   'all_other_native_code_ITCM_DTCM_and_artwork_bytes_preserved': True,
                   'all16_complete_strings_first_final_letters_and_NUL_retained': True,
                   'cache': cache_plan(saved)}


def apply_release(source, clean, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-artwork-name-captions-release-v1':
        raise ValueError('Unknown artwork caption release')
    documents = {}
    for filename, digest in config['dependencies_sha256'].items():
        raw = Path(filename).read_bytes()
        if sha(raw) != digest:
            raise ValueError('Artwork caption dependency differs: ' + filename)
        documents[filename] = json.loads(raw.decode('utf-8'))
    saved, report = transform(source, clean, documents[config['review']],
                              [documents[p] for p in config['manuscripts']])
    if sha(source) != config['source_arm9_sha256'] or sha(saved) != config['target_arm9_sha256']:
        raise ValueError('Artwork caption source or target lock differs')
    return saved, report
