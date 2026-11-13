"""Lossless reviewed name migration on the complete artwork-caption release."""

import json
import struct
from collections import defaultdict
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.confirmed_character_names import FIELDS
from dk4tool.patch.confirmed_name_message_catalog import CALLS, MACRO
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from dk4tool.patch.message_actor_integrity import HEADER
from dk4tool.patch.reviewed_name_catalog import helper, pack_complete_strings, table_bytes
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.script.common_native_reblocking import plan as common_plan
from scripts.probe_common_display_name_hook import branch_link


def shared_fields(source, clean):
    result, changes = bytearray(source), []
    for ident, index, column, offset, capacity, japanese, old, english in FIELDS:
        field, pointer = 0x120B80 + index * 32 + column, BASE + offset
        if any(struct.unpack_from('<I', arm, field)[0] != pointer for arm in (source, clean)):
            raise ValueError('Original shared-name table ownership differs')
        if (source[offset:offset + capacity] != (old.encode('cp932') + b'\0').ljust(capacity, b'\0')
                or clean[offset:offset + capacity] != (japanese.encode('cp932') + b'\0').ljust(capacity, b'\0')):
            raise ValueError('Shared-name source allocation differs')
        word = struct.pack('<I', pointer)
        if [i for i in range(len(source) - 3) if source[i:i + 4] == word] != [field]:
            raise ValueError('Unclassified shared-name pointer alias')
        text = english.encode('ascii') + b'\0'
        if len(text) > capacity:
            raise ValueError('Complete shared name does not fit')
        result[offset:offset + capacity] = text.ljust(capacity, b'\0')
        changes.append({'id': ident, 'index': index, 'column': column, 'offset': offset,
                        'capacity': capacity, 'table_field': field, 'before': old, 'after': english})
    restored = bytearray(result)
    for row in changes:
        at, size = row['offset'], row['capacity']
        restored[at:at + size] = source[at:at + size]
    if restored != source:
        raise ValueError('Unrelated shared-name bytes change')
    return bytes(result), changes


def routes(source_files, prep, clean_files, canonical_files, actor_positions):
    if len(prep['records']) != 444 or prep['errors']:
        raise ValueError('Complete reviewed packet required')
    containers = {p: IlnkContainer.parse(raw) for p, raw in source_files.items()}
    originals = {p: IlnkContainer.parse(raw).blocks for p, raw in clean_files.items()}
    canonical = {p: IlnkContainer.parse(raw).blocks for p, raw in canonical_files.items()}
    blocks = {p: [bytearray(b) for b in c.blocks] for p, c in containers.items()}
    changed, spans = [], {p: [] for p in source_files}
    for row in prep['records']:
        path, ident = row['file_path'], row['id']
        number, index = int(ident.split('_B')[1].split('_')[0]), int(ident.split('_R')[1])
        parts = containers[path].blocks[number].split(b'\0')
        raw, original, baked = parts[index], originals[path][number].split(b'\0')[index], canonical[path][number].split(b'\0')[index]
        if (raw.hex() != row['current_key_hex'] or original.hex() != row['clean_source_hex']
                or baked.hex() != row['canonical_source_hex']):
            raise ValueError('Reviewed current/clean/canonical route lock differs')
        if row['storage'] != 'fixed':
            continue
        target = bytes.fromhex(row['fixed_target_hex'])
        at = sum(len(s) + 1 for s in parts[:index])
        if len(target) != len(raw) or b'\0' in target:
            raise ValueError('Fixed route allocation changes')
        if row['native_actor'] is not None and (raw[0] != row['native_actor'] or target[0] != raw[0]):
            raise ValueError('Fixed route actor changes')
        if any(n == number and lo < at + len(target) and at < hi for n, lo, hi in spans[path]):
            raise ValueError('Fixed route spans overlap')
        blocks[path][number][at:at + len(target)] = target
        spans[path].append((number, at, at + len(target)))
        changed.append({'file_path': path, 'id': ident, 'block': number, 'native_offset': at, 'span': len(target)})
    result = {}
    for path, container in containers.items():
        for n, (before, after) in enumerate(zip(container.blocks, blocks[path], strict=True)):
            if len(before) != len(after) or any(a != b and not any(k == n and lo <= i < hi for k, lo, hi in spans[path])
                                              for i, (a, b) in enumerate(zip(before, after, strict=True))):
                raise ValueError('Unrelated route bytes or command addresses change')
        container.blocks = [bytes(b) for b in blocks[path]]
        result[path] = container.to_bytes()
        if len(result[path]) != len(source_files[path]):
            raise ValueError('Route archive extent changes')
    checked = 0
    for path, rows in actor_positions.items():
        for number, source_index, at, actor in rows:
            clean_parts = originals[path][number].split(b'\0')
            original_at = sum(len(s) + 1 for s in clean_parts[:source_index])
            if (clean_parts[source_index][0] != actor
                    or originals[path][number][original_at - 5:original_at] != HEADER
                    or containers[path].blocks[number][at - 5:at] != HEADER
                    or containers[path].blocks[number][at] != actor):
                raise ValueError('Original native actor ownership differs')
            checked += 1
    if len(changed) != 197 or checked != 19254:
        raise ValueError('Full fixed/actor coverage differs')
    return result, {'fixed_records': changed, 'original_actor_records': checked,
                    'all_archive_block_and_native_command_addresses_preserved': True}


def catalog(source_arm, clean_arm, source_files, prep):
    named, names = shared_fields(source_arm, clean_arm)
    requests, selected = defaultdict(list), {}
    for row in prep['records']:
        if row['storage'] != 'catalog':
            continue
        owner, key, target = (row['file_path'], row['id']), bytes.fromhex(row['current_key_hex']), bytes.fromhex(row['target_hex'])
        selected[owner] = row
        requests[key].append((owner, 'whole', target))
        if row['native_actor'] is not None:
            if key[0] != target[0] or key[0] != row['native_actor']:
                raise ValueError('Catalog actor differs')
            requests[key[1:]].append((owner, 'body', target[1:]))
    rows = []
    for key in sorted(requests):
        items = requests[key]
        if len({item[2] for item in items}) != 1:
            raise ValueError('Conflicting full translations for one catalog key')
        mask = 0
        for owner, _, _ in items:
            mask |= 1 << int(owner[0][8])
        rows.append({'key': key, 'target': items[0][2], 'route_mask': mask,
                     'requests': [{'owner': list(o), 'form': f} for o, f, _ in items]})
    lookup, covered, rejected, scanned = {r['key']: r for r in rows}, set(), [], 0
    for route in range(4):
        path = f'/data/SC{route}.DK4'
        for number, data in enumerate(IlnkContainer.parse(source_files[path]).blocks):
            for index, raw in enumerate(data.split(b'\0')):
                scanned += 1
                owner = path, f'DK4_MES_B{number:02d}_R{index:04d}'
                for form, key in [('whole', raw), ('body', raw[1:])] if raw else []:
                    row = lookup.get(key)
                    if row is None:
                        continue
                    if not row['route_mask'] & (1 << route):
                        rejected.append({'owner': list(owner), 'form': form})
                        continue
                    if owner not in selected:
                        raise ValueError('Unintended active catalog match after fixed edits')
                    expected = bytes.fromhex(selected[owner]['target_hex'])
                    if row['target'] != (expected[1:] if form == 'body' else expected):
                        raise ValueError('Catalog owner target differs')
                    covered.add(owner)
    if covered != set(selected) or len(selected) != 247 or len(rows) != 467:
        raise ValueError('Full catalog coverage differs')
    code = MainCodeFile(named, BASE)
    before = [bytes(s.data) for s in code.sections]
    if code.sections[3].ramAddress != STAGE or not cache_plan(named):
        raise ValueError('Owned pool source differs')
    packed, pointers = pack_complete_strings([raw for r in rows for raw in (r['key'], r['target'])], POOL, before[3][:-48])
    packed.extend(bytes(-len(packed) % 4))
    table = POOL + len(packed)
    packed.extend(table_bytes(rows, pointers))
    entry = POOL + len(packed)
    implementation = helper(entry, table, len(rows))
    packed.extend(implementation)
    for field in CALLS:
        if struct.unpack_from('<I', source_arm, field)[0] != branch_link(BASE + field, MACRO):
            raise ValueError('Native catalog caller differs')
        struct.pack_into('<I', code.sections[0].data, field, branch_link(BASE + field, entry))
    packed.extend(bytes(-len(packed) % 32))
    size = len(packed) + 64
    if POOL + size > STAGE or STAGE + size + 48 > 0x023F4000:
        raise ValueError('Complete catalog exceeds owned memory')
    packed.extend(wrapper(STAGE + len(packed), STAGE + size, size, named))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack('<I', size)
    struct.pack_into('<I', code.sections[0].data, 0x8E4, branch_link(BASE + 0x8E4, STAGE + size - 64))
    struct.pack_into('<I', code.sections[0].data, 0xE45DC, POOL + size)
    saved = bytes(code.save())
    parsed, restored = MainCodeFile(saved, BASE), bytearray(MainCodeFile(saved, BASE).sections[0].data)
    for at in (*CALLS, 0x8E4, 0xE45DC):
        restored[at:at + 4] = before[0][at:at + 4]
    at = code.codeSettingsOffs
    restored[at:at + 12] = before[0][at:at + 12]
    if (restored != before[0] or any(bytes(parsed.sections[n].data) != before[n] for n in (1, 2))
            or bytes(parsed.sections[3].data[:len(before[3]) - 48]) != before[3][:-48]):
        raise ValueError('Catalog changes unrelated instructions or inherited artwork pool')
    return saved, {'source_arm9_sha256': sha(source_arm), 'target_arm9_sha256': sha(saved), 'name_fields': names,
                   'records': [{'key_hex': r['key'].hex(), 'target_hex': r['target'].hex(),
                                'key_pointer': pointers[r['key']], 'target_pointer': pointers[r['target']],
                                'route_mask': r['route_mask'], 'requests': r['requests']} for r in rows],
                   'entry': entry, 'table': table, 'helper_bytes': len(implementation),
                   'catalog_source_records': len(selected), 'unique_route_scoped_keys': len(rows),
                   'route_segments_scanned': scanned, 'unintended_matches': [], 'foreign_route_matches_rejected': rejected,
                   'pool_payload_bytes': size, 'remaining_before_stage': STAGE - POOL - size,
                   'inherited_pool_bytes_preserved': len(before[3]) - 48, 'cache': cache_plan(saved)}


def common(source, arm, clean, clean_arm, manuscript):
    before, original = common_message_entries(source, arm, clean=False), common_message_entries(clean, clean_arm)
    authored = {}
    for row in manuscript['records']:
        index = row['message_id']
        if (before[index].text.hex().upper() != row['current_native_lock']['text_hex']
                or original[index].text.hex().upper() != row['clean_native_lock']['text_hex']):
            raise ValueError('Original/current COMMON message identity differs')
        authored[index] = row['english'].removesuffix('{PAD}').encode('cp932')
    if set(authored) != {1360, 1361, 1362, 1363, 1683, 1830}:
        raise ValueError('Complete six-message COMMON migration required')
    result, mapped, allocation = common_plan(source, arm, authored)
    after = common_message_entries(result, mapped, clean=False)
    if any(row.text != authored.get(row.message_id, before[row.message_id].text) for row in after):
        raise ValueError('Unrelated COMMON text changes')
    if allocation['removed_english_padding_bytes'] or not allocation['executable_code_unchanged']:
        raise ValueError('COMMON reblocking changes unrelated padding or code')
    return result, mapped, {'message_IDs': list(authored), 'all3668_selections_exact': True,
                            'all3662_unselected_texts_and_padding_exact': True, 'allocation': allocation}


def help_pages(source, proposal):
    if sha(source) != proposal['source_HELP_sha256']:
        raise ValueError('Complete current HELP source differs')
    container = IlnkContainer.parse(source)
    before = list(container.blocks)
    pages = proposal['pages']
    if {p['topic_id'] for p in pages} != {0, 1, 6, 7, 37, 202, 204, 205} or len(pages) != 8:
        raise ValueError('Eight reviewed HELP pages required')
    for row in pages:
        index = row['topic_id']
        while len(container.blocks) <= index:
            container.blocks.append(b'\0')
        container.blocks[index] = bytes.fromhex(row['encoded_hex'])
    if any(after != old and n not in {0, 1, 6, 7, 37} for n, (old, after) in enumerate(zip(before, container.blocks))):
        raise ValueError('Unrelated HELP topics change')
    result = container.to_bytes()
    if sha(result) != proposal['target_HELP_sha256'] or container.blocks[203] != b'\0':
        raise ValueError('Proven HELP target or native history sentinel differs')
    return result, {'topic_IDs': [p['topic_id'] for p in pages], 'source_topic_count': len(before),
                    'target_topic_count': len(container.blocks), 'native203_history_sentinel_preserved': True}


def transform(files, clean_files, canonical_files, prep, common_manuscript, help_proposal, actors):
    paths = [f'/data/SC{i}.DK4' for i in range(4)]
    routed, route_report = routes({p: files[p] for p in paths}, prep, {p: clean_files[p] for p in paths},
                                  {p: canonical_files[p] for p in paths}, actors)
    common_raw, mapped, common_report = common(files['/COMMON/MESFILE.DK4'], files['/__arm9__.bin'],
                                              clean_files['/COMMON/MESFILE.DK4'], clean_files['/__arm9__.bin'], common_manuscript)
    arm, catalog_report = catalog(mapped, clean_files['/__arm9__.bin'], routed, prep)
    help_raw, help_report = help_pages(files['/COMMON/HELP.DK4'], help_proposal)
    return {**routed, '/__arm9__.bin': arm, '/COMMON/MESFILE.DK4': common_raw, '/COMMON/HELP.DK4': help_raw}, {
        'route': route_report, 'catalog': catalog_report, 'COMMON': common_report, 'HELP': help_report,
        'source_file_sha256': {p: sha(raw) for p, raw in files.items()},
        'target_file_sha256': {p: sha(raw) for p, raw in {**routed, '/__arm9__.bin': arm,
                                                       '/COMMON/MESFILE.DK4': common_raw, '/COMMON/HELP.DK4': help_raw}.items()}}


def apply_release(image, clean, canonical, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-reviewed-name-integration-release-v1':
        raise ValueError('Unknown reviewed name integration release')
    for filename, digest in config.get('verification_evidence_sha256', {}).items():
        if sha(Path(filename).read_bytes()) != digest:
            raise ValueError('Current native name evidence differs: ' + filename)
    documents = {}
    for filename, digest in config['dependencies_sha256'].items():
        raw = Path(filename).read_bytes()
        if sha(raw) != digest:
            raise ValueError('Reviewed-name dependency differs: ' + filename)
        documents[filename] = json.loads(raw.decode('utf-8'))
    files = {p: image.read_file(p) for p in config['source_file_sha256']}
    if {p: sha(raw) for p, raw in files.items()} != config['source_file_sha256']:
        raise ValueError('Full inherited name-integration source differs')
    clean_files, canonical_files = {p: clean.read_file(p) for p in files}, {p: canonical.read_file(p) for p in files}
    if ({p: sha(raw) for p, raw in clean_files.items()} != config['clean_file_sha256']
            or {p: sha(raw) for p, raw in canonical_files.items()} != config['canonical_file_sha256']):
        raise ValueError('Clean/canonical integration source differs')
    targets, report = transform(files, clean_files, canonical_files,
                                *[documents[config[k]] for k in ('preparation', 'COMMON_manuscript', 'HELP_proposal', 'actor_positions')])
    if report['target_file_sha256'] != config['target_file_sha256']:
        raise ValueError('Reviewed name integration target differs')
    for filename, raw in targets.items():
        image.replace_file(filename, raw)
    return report
