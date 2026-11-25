"""Apply a reviewed, source-locked COMMON reblocking release transform."""
from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

from dk4tool.dialogue.qa import audit_native_common_entry
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.bgm_title_tracking import PATCH_OFFSET, REPLACEMENT, apply_probe, title_geometry
from dk4tool.rom.nds import NdsImage
from dk4tool.scan.sjis_scan import contains_japanese
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.script.common_native_reblocking import plan
from dk4tool.script.common_native_repack import repack_native_records


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read_preserved_neighbors(declarations, source, current, authored):
    preserved = {}
    for row in declarations:
        i = row['message_id']
        if (not isinstance(i, int) or not 0 <= i < len(source)
                or i in authored or i in preserved
                or row.get('status') != 'untranslated-renderer-classification-pending'
                or not str(row.get('reason', '')).strip()):
            raise ValueError('Invalid, duplicate or authored preserved neighbor')
        if (bytes.fromhex(row['source_hex']) != source[i].text
                or bytes.fromhex(row['current_hex']) != current[i].text):
            raise ValueError('Preserved neighbor source/current lock differs')
        if (not contains_japanese(source[i].text.decode('cp932'))
                or not contains_japanese(current[i].text.decode('cp932'))):
            raise ValueError('Preserved untranslated neighbor must retain Japanese source/current text')
        preserved[i] = current[i].text
    return preserved


def apply_common_reblocking(common: bytes, arm9: bytes, config_path: Path) -> tuple[bytes, bytes, dict]:
    config = json.loads(config_path.read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-common-native-reblocking-v1':
        raise ValueError('Unsupported COMMON reblocking format')
    if sha256(common) != config['parent_common_sha256'] or sha256(arm9) != config['parent_arm9_sha256']:
        raise ValueError('COMMON reblocking parent layers differ from the registered source')
    clean = NdsImage.open('work/clean.nds')
    source = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    def read_authored(manuscripts):
        authored = {}
        for manuscript in manuscripts:
            read_manuscript(manuscript, authored)
        return authored

    def read_manuscript(manuscript, authored):
        path = Path(manuscript['path'])
        raw = path.read_bytes()
        if sha256(raw) != manuscript['sha256']:
            raise ValueError('Reviewed COMMON manuscript hash differs')
        payload = json.loads(raw)
        validate_natural_dialogue_batch(payload)
        for row in payload['records']:
            i = row['message_id']
            if i in authored or bytes.fromhex(row['source_hex']) != source[i].text:
                raise ValueError('Duplicate message or mismatched clean native source')
            text = row['english'].removesuffix('{PAD}')
            if re.findall(r'%[sdi]', text) != re.findall(r'%[sdi]', source[i].text.decode('cp932')):
                raise ValueError('COMMON runtime argument shapes differ from source')
            encoded = text.encode('cp932')
            if 3251 <= i <= 3288:
                if row.get('presentation') != 'sound-bgm-title-ascii':
                    raise ValueError('BGM title requires its mapped presentation')
                advance = 5 if config.get('bgm_title_tracking_renderer', False) else 6
                if not title_geometry(text, advance)['fits_panel']:
                    raise ValueError(f'Message {i}: BGM title exceeds the mapped panel')
            else:
                if row.get('presentation'):
                    raise ValueError('Unmapped COMMON presentation')
                audit = audit_native_common_entry(b' ' * len(encoded), row['english'])
                if any(issue['severity'] in {'warning', 'error'} for issue in audit['issues']):
                    raise ValueError(f'Message {i}: unreviewed formatting defect')
            authored[i] = encoded
    pre_authored = read_authored(config.get('pre_repack_manuscripts', []))
    if pre_authored:
        blocks = IlnkContainer.parse(clean.read_file('/COMMON/MESFILE.DK4')).blocks
        target_owners = {(source[i].block, source[i].record_index) for i in pre_authored}
        prefixes = {}
        for owner in target_owners:
            first = next(e for e in source if (e.block, e.record_index) == owner)
            prefixes[owner] = blocks[owner[0]].split(b'\0')[owner[1]][:first.start]
        repaired = repack_native_records(common, arm9, pre_authored, prefixes)
        common, arm9 = repaired.common, repaired.arm9
    authored = read_authored(config['manuscripts'])
    if authored.keys() & pre_authored.keys():
        raise ValueError('Duplicate pre-repack and relocated message IDs')
    current = common_message_entries(common, arm9, clean=False)
    preserved = read_preserved_neighbors(config.get('preserved_native_neighbors', []),
                                         source, current, authored)
    result_common, result_arm9, report = plan(common, arm9, authored, config['first_reblocked_block'],
                                             compact_existing_english_padding=config.get('compact_existing_english_padding', False),
                                             preserved=preserved)
    if config.get('bgm_title_tracking_renderer', False):
        if not set(range(3251, 3289)) <= authored.keys():
            raise ValueError('BGM renderer requires all 38 reviewed complete titles')
        result_arm9 = apply_probe(result_arm9)
        report.update({'executable_code_unchanged': False,
                       'common_loader_selector_code_unchanged': True,
                       'bgm_title_renderer': {'patch_offset': PATCH_OFFSET,
                                              'replacement_hex': REPLACEMENT.hex(),
                                              'ascii_advance': 5, 'runtime_verified': False}})
    report['authored_ids'] = sorted(authored.keys() | pre_authored.keys())
    if (sha256(result_common) != config['expected_common_sha256']
            or sha256(result_arm9) != config['expected_arm9_sha256']
            or report['directory_sha256'] != config['directory_sha256']):
        raise ValueError('Rebuilt COMMON bytes differ from the complete verified map')
    # Re-run the independently locked native mapper on the new directory.
    selected = common_message_entries(result_common, result_arm9, clean=False)
    if len(selected) != 3668:
        raise ValueError('Reblocked COMMON loses global message IDs')
    layout_path = Path(config['layout_batch'])
    if sha256(layout_path.read_bytes()) != config['layout_batch_sha256']:
        raise ValueError('Final native layout declaration differs')
    layout = json.loads(layout_path.read_text(encoding='utf-8'))
    declared = {r['id']: r for r in layout['records']}
    owners = defaultdict(list)
    for entry in selected:
        owners[entry.block, entry.record_index].append(entry)
    blocks = IlnkContainer.parse(result_common).blocks
    checked = set()
    for (block, record), entries in owners.items():
        key = f'DK4_MES_B{block:02d}_R{record:04d}'
        row = declared[key]
        checked.add(key)
        if (bytes.fromhex(row['replacement_hex']) != blocks[block].split(b'\0')[record]
                or row['native_message_ids'] != [e.message_id for e in entries]
                or row['entry_offsets'] != [e.start for e in entries]
                or row['entry_ends'] != [e.end for e in entries]
                or row['native_table_offsets'] != [e.table_offset for e in entries]
                or row['display_entries'] != [e.text.rstrip(b' ').decode('cp932') for e in entries]):
            raise ValueError('Final layout contradicts the native message selections')
    if checked != declared.keys() or len(declared) != len(layout['records']):
        raise ValueError('Incomplete or duplicate final layout declaration')
    report.update({'status': 'integrated-transform-verified-runtime-pending',
                   'config': config_path.as_posix(), 'config_sha256': sha256(config_path.read_bytes()),
                   'layout_batch': layout_path.as_posix(), 'layout_batch_sha256': config['layout_batch_sha256']})
    return result_common, result_arm9, report
