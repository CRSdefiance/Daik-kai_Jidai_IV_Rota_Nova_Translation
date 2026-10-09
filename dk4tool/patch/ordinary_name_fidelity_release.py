"""Review original name/role labels and prepare a boot-safe terminal correction."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha

BASE, POOL, STAGE = 0x02000000, 0x02387A20, 0x023A7200
SOURCE = '21e2be34e965fd17fc56dd18e919e411b7da87a3c8f56f9e7e6fd8c39100940b'
REVISIONS = {
    10: ('シエン', 'Xien', 'Match the established Maria/Lil dialogue spelling.'),
    25: ('イファ', 'Yifa', 'Match the established companion spelling in all route manuscripts.'),
    64: ('ユリス', 'Yuris', 'Match the established bounty-event spelling.'),
    65: ('プレット', 'Plett', 'Match the established Plett Perrault bounty-event spelling.'),
    131: ('総督', 'Governor', 'Retain the complete title without an unnecessary abbreviation.'),
    134: ('高僧', 'Senior Monk', 'Retain the senior religious rank; do not add a particular office.'),
    136: ('高僧', 'Senior Monk', 'Retain the senior religious rank; do not add a particular office.'),
    137: ('高僧', 'Senior Monk', 'Retain the senior religious rank; do not add a particular office.'),
    164: ('カップル男', 'Man in a Couple', 'Preserve the couple relationship without inventing age or marital status.'),
    165: ('カップル女', 'Woman in a Couple', 'Preserve the couple relationship without inventing age or marital status.'),
    169: ('妖艶な女', 'Alluring Woman', 'Describes attractiveness, without suggesting supernatural powers.'),
    170: ('謎の老人', 'Mysterious Old Man', 'Retain the mystery qualifier and the elderly male description.'),
    171: ('研究生', 'Research Student', 'Retain the research-specific student role.'),
    172: ('行き倒れ', 'Collapsed Person', 'Retain the collapsed-person description without assuming a shipwreck.'),
    173: ('怪しい人', 'Suspicious Person', 'Retain the suspicious qualifier without inventing a profession.'),
    185: ('ダンディー', 'Dandy', 'Preserve the phonetic nickname rather than changing it to the place/name Dundee.'),
    203: ('さくら', 'Sakura', 'Preserve the Japanese name reading in the sequence of named women; do not substitute its literal flower meaning.'),
}
STATIC = {10: 8, 25: 8, 64: 8, 65: 12, 185: 12, 203: 8}


def cstring(raw, offset):
    return raw[offset:raw.index(0, offset)]


def transform(source, clean):
    if sha(source) != SOURCE or sha(clean) != '0d1541022ef95afe02ad7a1a381a1fc3e5e74442a5f0408f436d68a5d306d731':
        raise ValueError('Exact complete V153 and clean ARM9 sources required')
    code = MainCodeFile(source, BASE)
    if len(code.sections) != 4 or code.sections[3].ramAddress != STAGE or len(code.sections[3].data) != 1552:
        raise ValueError('Verified staged name allocation differs')
    old_payload = bytes(code.sections[3].data[:1504])
    original_main = bytes(code.sections[0].data)
    inherited = json.loads(Path('translations/persistent_name_allocation_v1.json').read_text(encoding='utf-8'))
    if old_payload != bytes.fromhex(inherited['payload_hex']):
        raise ValueError('Complete inherited name/item payload differs')
    replacements, rows = {}, []
    for index, (japanese, english, note) in REVISIONS.items():
        field = 0x120B80 + index * 32
        pointer, jp_pointer = [struct.unpack_from('<I', data, field)[0] for data in (source, clean)]
        if cstring(clean, jp_pointer - BASE).decode('cp932') != japanese:
            raise ValueError('Clean given-name meaning differs')
        old = cstring(old_payload, pointer - POOL) if POOL <= pointer < POOL + 1504 else cstring(source, pointer - BASE)
        row = {'id': f'ORDINARY_GIVEN_NAME_{index}', 'index': index, 'table_field': field,
               'japanese': japanese, 'clean_pointer': jp_pointer, 'clean_hex': japanese.encode('cp932').hex(),
               'before_pointer': pointer, 'before_english': old.decode('cp932'), 'english': english,
               'speaker': 'Ordinary character nameplate',
               'context': 'Clean native ordinary-name table identity and role qualifiers; no actor eligibility assumptions.',
               'source_meaning': japanese + ' — ' + english,
               'localization_note': note, 'translation_policy': 'natural-dialogue-v2',
               'review': {gate: gate != 'formatting' for gate in ('source', 'context', 'localization', 'naturalness', 'formatting')}}
        rows.append(row)
        if POOL <= pointer < POOL + 1504:
            if pointer in replacements and replacements[pointer] != english.encode('ascii'):
                raise ValueError('Shared owner has conflicting revisions')
            replacements[pointer] = english.encode('ascii')
        elif index in STATIC:
            at, capacity = pointer - BASE, STATIC[index]
            expected_jp = (japanese.encode('cp932') + b'\0').ljust(capacity, b'\0')
            if clean[at:at + capacity] != expected_jp or source[at:at + capacity] != (old + b'\0').ljust(capacity, b'\0'):
                raise ValueError('Static name allocation or neighboring bytes differ')
            word = struct.pack('<I', pointer)
            references = [at for at in range(len(source) - 3) if source[at:at + 4] == word]
            if references != [field]:
                raise ValueError('Static given name has unexplained aliases')
            new = (english.encode('ascii') + b'\0').ljust(capacity, b'\0')
            if len(new) != capacity:
                raise ValueError('Full proper name exceeds verified static allocation')
            code.sections[0].data[at:at + capacity] = new
            row.update({'static_span': [at, at + capacity], 'static_before_hex': source[at:at + capacity].hex()})
        elif index != 131:
            raise ValueError('Unmapped role ownership')
    packed, addresses, moves = bytearray(), {}, []
    for move in inherited['moves']:
        field, pointer = move['field'], move['runtime_pointer']
        if struct.unpack_from('<I', source, field)[0] != pointer:
            raise ValueError('Inherited complete-name pointer differs')
        if pointer not in addresses:
            while len(packed) % 4:
                packed.append(0)
            text = replacements.get(pointer, cstring(old_payload, pointer - POOL))
            addresses[pointer] = POOL + len(packed)
            packed.extend(text + b'\0')
        struct.pack_into('<I', code.sections[0].data, field, addresses[pointer])
        moves.append({'field': field, 'before_pointer': pointer, 'after_pointer': addresses[pointer]})
    # Governor's original eight-byte slot cannot hold the complete English title.
    # Relocate its verified sole reference into the reserved, aligned name pool.
    governor = next(row for row in rows if row['index'] == 131)
    pointer = governor['before_pointer']
    if [i for i in range(len(source) - 3) if source[i:i + 4] == struct.pack('<I', pointer)] != [governor['table_field']]:
        raise ValueError('Governor owner has unexplained references')
    while len(packed) % 4:
        packed.append(0)
    governor['after_pointer'] = POOL + len(packed)
    struct.pack_into('<I', code.sections[0].data, governor['table_field'], governor['after_pointer'])
    packed.extend(b'Governor\0')
    used = len(packed)
    size = (used + 31) & ~31
    if size > 1632:
        raise ValueError('Reviewed name expansion exceeds bounded reserve plan')
    packed.extend(bytes(size - used))
    entry = STAGE + size
    stub = struct.pack('<12I', 0xE92D400F, 0xE59F0018, 0xE59F1018, 0xE59F2018,
                       0xE4903004, 0xE4813004, 0xE2522004, 0x1AFFFFFB,
                       0xE8BD800F, STAGE, POOL, size)
    old_stub = bytes(code.sections[3].data[1504:])
    if old_stub[:-4] != stub[:-4] or struct.unpack_from('<I', source, 0xE45DC)[0] != POOL + 1504:
        raise ValueError('Staged copier or heap reservation differs')
    struct.pack_into('<I', code.sections[0].data, 0x8E4, 0xEB000000 | (((entry - BASE - 0x8E4 - 8) // 4) & 0xFFFFFF))
    struct.pack_into('<I', code.sections[0].data, 0xE45DC, POOL + size)
    code.sections[3].data = bytearray(packed + stub)
    saved = bytes(code.save())
    parsed = MainCodeFile(saved, BASE)
    if (parsed.sections[3].ramAddress != STAGE or bytes(parsed.sections[3].data) != packed + stub
            or any(bytes(parsed.sections[n].data) != bytes(MainCodeFile(source, BASE).sections[n].data) for n in (1, 2))):
        raise ValueError('Name correction changes native ITCM/DTCM or staged ownership')
    for row in rows:
        row['after_pointer'] = struct.unpack_from('<I', saved, row['table_field'])[0]
    allowed = {0x8E4, 0xE45DC, governor['table_field'], *(m['field'] for m in moves)}
    restored = bytearray(parsed.sections[0].data)
    for at in allowed:
        restored[at:at + 4] = original_main[at:at + 4]
    for row in rows:
        if 'static_span' in row:
            start, end = row['static_span']
            restored[start:end] = original_main[start:end]
    off = code.codeSettingsOffs
    restored[off:off + 12] = original_main[off:off + 12]
    if bytes(restored) != original_main:
        raise ValueError('Name correction changes unrelated main code, data or rendering')
    return saved, {'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(saved), 'records': rows,
                   'inherited_pointer_moves': moves, 'pool_used_bytes': used, 'pool_payload_bytes': size,
                   'final_pool_span': [POOL, POOL + size], 'staging_span': [STAGE, STAGE + size + 48],
                   'copy_entry': entry, 'ITCM_DTCM_fonts_and_renderers_preserved': True}


def apply_release(source, clean, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-ordinary-name-fidelity-release-v1':
        raise ValueError('Wrong name fidelity release format')
    saved, plan = transform(source, clean)
    if config['source_arm9_sha256'] != sha(source) or config['target_arm9_sha256'] != sha(saved):
        raise ValueError('Name fidelity release identities differ')
    manuscript_path = Path(config['manuscript'])
    if sha(manuscript_path.read_bytes()) != config['manuscript_sha256']:
        raise ValueError('Name fidelity manuscript changed')
    manuscript = json.loads(manuscript_path.read_text(encoding='utf-8'))
    if (manuscript['translation_policy'] != 'natural-dialogue-v2' or manuscript['target_locale'] != 'en-US'
            or manuscript['source_arm9_sha256'] != sha(clean) or len(manuscript['records']) != 17):
        raise ValueError('Name fidelity source/localization review differs')
    for row, expected in zip(manuscript['records'], plan['records'], strict=True):
        if (not all(row['review'][gate] for gate in ('source', 'context', 'localization', 'naturalness', 'formatting'))
                or {k: v for k, v in row.items() if k != 'review'} != {k: v for k, v in expected.items() if k != 'review'}):
            raise ValueError('Name fidelity complete source/text/layout review differs')
    proof_path = Path(config['native_proof'])
    if sha(proof_path.read_bytes()) != config['native_proof_sha256']:
        raise ValueError('Name fidelity native proof changed')
    proof = json.loads(proof_path.read_text(encoding='utf-8'))
    pixels_path = Path(config['paired_pixels'])
    if (sha(pixels_path.read_bytes()) != config['paired_pixels_sha256']
            or proof['paired_pixels_sha256'] != config['paired_pixels_sha256']
            or proof['source_arm9_sha256'] != sha(source) or proof['target_arm9_sha256'] != sha(saved)
            or proof['reviewed_indices'] != sorted(REVISIONS) or proof['native_getter_count'] != 207
            or proof['preserved_other_names'] != 190 or proof['inherited_pointer_count'] != 239
            or proof['shared_copy_matrix_cases'] != 704 or proof['common_selections_preserved'] != 3668
            or proof['paired_pixel_cases'] != 34 or not proof['visual_review']['complete']):
        raise ValueError('Name fidelity native coverage incomplete')
    boot = proof['boot']
    if (boot['arm7_source_changed_bytes_after_arm9_autoload'] or not all(
            r['matches_original'] for r in boot['arm7_native_loaded_sections']) or not all(
                boot[k] for k in ('repaired_pool_matches_complete_payload',
                                  'repair_returns_with_stack_preserved', 'actual_startup_call_preserves_r0_r3'))):
        raise ValueError('Name fidelity boot ownership proof incomplete')
    visual = proof['visual_review']
    if sha(Path(visual['sheet']).read_bytes()) != visual['sheet_sha256']:
        raise ValueError('Reviewed name raster sheet changed')
    return saved, {**{k: v for k, v in plan.items() if k not in ('records', 'inherited_pointer_moves')},
                   'changed_records': [r['id'] for r in plan['records']], 'native_getter_count': 207,
                   'paired_pixel_cases': 34, 'other_getter_strings_preserved': 190,
                   'physical_gameplay_verified': False}
