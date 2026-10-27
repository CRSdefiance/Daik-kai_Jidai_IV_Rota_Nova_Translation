"""Restore original native message actor bytes without discarding prose.

The two full strings use their existing native alignment byte. No command
address, block size, native code, visible wording or macro is changed.
"""

import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha

HEADER = b'\0\x40\xFF\xFF\0'


def verify_original_actors(source_files, target_files, clean_files):
    """Use stable native object positions, not NUL-entry IDs after alignment."""
    checked = 0
    for path in source_files:
        clean = IlnkContainer.parse(clean_files[path]).blocks
        source = IlnkContainer.parse(source_files[path]).blocks
        target = IlnkContainer.parse(target_files[path]).blocks
        for original, before, after in zip(clean, source, target, strict=True):
            original_parts, parts = original.split(b'\0'), before.split(b'\0')
            original_at = 0
            positions, at = [], 0
            for row in parts:
                positions.append(at)
                at += len(row) + 1
            for index, row in enumerate(original_parts):
                if row and original[max(0, original_at - 5):original_at] == HEADER:
                    if index >= len(positions):
                        raise ValueError('Original native actor object is missing')
                    actor_at = positions[index]
                    if (before[max(0, actor_at - 5):actor_at] != HEADER
                            or after[actor_at - 5:actor_at] != HEADER or after[actor_at] != row[0]):
                        raise ValueError('Original native actor metadata is not preserved')
                    checked += 1
                original_at += len(row) + 1
    if checked != 19254:
        raise ValueError('Complete original native message coverage differs')
    return checked


def repair(source_files, clean_files, census):
    rows = census['mismatches']
    if len(rows) != 378 or not all(r['current_native_header_still_exact'] for r in rows):
        raise ValueError('Complete original-header census required')
    containers = {path: IlnkContainer.parse(raw) for path, raw in source_files.items()}
    originals = {path: IlnkContainer.parse(raw) for path, raw in clean_files.items()}
    blocks = {path: [bytearray(block) for block in value.blocks] for path, value in containers.items()}
    changes = []
    allowed = {path: [] for path in containers}
    for row in rows:
        path, number, index, actor = [row[k] for k in ('file_path', 'block', 'record', 'actor')]
        original_block = originals[path].blocks[number]
        source_block = containers[path].blocks[number]
        original_parts, parts = original_block.split(b'\0'), source_block.split(b'\0')
        original_at = sum(len(raw) + 1 for raw in original_parts[:index])
        at = sum(len(raw) + 1 for raw in parts[:index])
        old = parts[index]
        if (original_parts[index].hex() != row['clean_source_hex'] or original_parts[index][0] != actor
                or original_block[original_at - 5:original_at] != HEADER
                or source_block[at - 5:at] != HEADER or old.hex() != row['current_record_hex']):
            raise ValueError('Original/current message ownership differs')
        if actor == 10 and old.startswith(b' \n '):
            # The old formatter encoded actor0A as a protected leading LF.
            # Remove only that synthetic prefix; keep every word and macro.
            body = old[3:]
            target = bytes([actor]) + body + b'  '
            method, span = 'remove-synthetic-actor-newline', len(old)
        elif old.endswith(b' '):
            body = old[:-1]
            target = bytes([actor]) + body
            method, span = 'use-one-trailing-padding-byte', len(old)
        else:
            body = old
            target = bytes([actor]) + body + b'\0'
            method, span = 'use-existing-native-alignment-byte', len(old) + 2
            obj = at - 5
            if (path != '/data/SC3.DK4' or (number, index) not in ((62, 53), (139, 177))
                    or obj % 2 or len(old) % 2 != 1
                    or source_block[at + len(old):at + len(old) + 2] != b'\0\0'):
                raise ValueError('No bounded native alignment byte available')
            end = at + span
            if source_block[end:end + 4] != b'\0\x40\xFF\xFF':
                raise ValueError('Following native command boundary differs')
            # Round-up-to-two-byte VM cursor gives the exact same next object.
            before_next = (obj + 6 + len(old) - 1 + 1 + 1) & ~1
            after_next = (obj + 6 + len(old) + 1 + 1) & ~1
            if before_next != after_next or after_next != end:
                raise ValueError('Native command extent changes')
        if method != 'use-existing-native-alignment-byte' and len(target) != span:
            raise ValueError('Fixed message allocation changes')
        if old.decode('cp932').split() != body.decode('cp932').split():
            raise ValueError('Visible words or macros change')
        token = number * 0x1000000 + at
        if any(lo < token + span and token < hi for lo, hi in allowed[path]):
            raise ValueError('Repair spans overlap')
        blocks[path][number][at:at + span] = target
        allowed[path].append((number * 0x1000000 + at, number * 0x1000000 + at + span))
        changes.append({'file_path': path, 'id': f'DK4_MES_B{number}_R{index:04d}',
                        'block': number, 'actor_offset': at, 'object_offset': at - 5,
                        'actor': actor, 'method': method, 'old_hex': old.hex(),
                        'target_hex': target.hex(), 'complete_body_hex': body.hex(),
                        'following_native_command_address_unchanged': True})
    result = {}
    for path, value in containers.items():
        value.blocks = [bytes(block) for block in blocks[path]]
        target = value.to_bytes()
        if len(target) != len(source_files[path]):
            raise ValueError('Archive extent changes')
        # Check every changed byte belongs to an exact classified span.
        before = IlnkContainer.parse(source_files[path])
        for number, (old, new) in enumerate(zip(before.blocks, value.blocks, strict=True)):
            if len(old) != len(new):
                raise ValueError('Block extent changes')
            for at, (a, b) in enumerate(zip(old, new, strict=True)):
                token = number * 0x1000000 + at
                if a != b and not any(lo <= token < hi for lo, hi in allowed[path]):
                    raise ValueError('Unrelated script bytes change')
        result[path] = target
    coverage = verify_original_actors(source_files, result, clean_files)
    return result, {'format': 'dk4-message-actor-integrity-transform-v296', 'records': changes,
                    'source_file_sha256': {p: sha(b) for p, b in source_files.items()},
                    'target_file_sha256': {p: sha(b) for p, b in result.items()},
                    'all_visible_words_and_macros_preserved': True,
                    'all_archive_block_and_native_command_addresses_preserved': True,
                    'all_original_native_message_actor_records_verified': coverage,
                    'native_alignment_padding_consumed_records': [row['id'] for row in changes
                         if row['method'] == 'use-existing-native-alignment-byte'],
                    'native_code_and_graphics_changes_required': False}


def apply_release(image, clean, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-message-actor-integrity-release-v1':
        raise ValueError('Unknown actor-integrity release')
    path = Path(config['census'])
    if sha(path.read_bytes()) != config['census_sha256']:
        raise ValueError('Actor census source lock differs')
    sources = {p: image.read_file(p) for p in config['source_file_sha256']}
    if {p: sha(b) for p, b in sources.items()} != config['source_file_sha256']:
        raise ValueError('Complete current route stack differs')
    result, report = repair(sources, {p: clean.read_file(p) for p in sources},
                            json.loads(path.read_text(encoding='utf-8')))
    if report['target_file_sha256'] != config['target_file_sha256']:
        raise ValueError('Actor-integrity target differs')
    for path, raw in result.items():
        image.replace_file(path, raw)
    return report
