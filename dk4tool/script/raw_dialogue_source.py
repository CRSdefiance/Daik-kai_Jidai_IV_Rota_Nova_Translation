"""Resolve explicitly selected story text with an undecodable speaker prefix.

This does not change normal extraction or classify undecodable data as prose.
Callers must supply the exact source bytes and a speaker state already mapped
by their route profile. The whole source file is hash-locked by the batch loader.
"""
from __future__ import annotations

import re

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.scan.sjis_scan import contains_japanese


def resolve_raw_dialogue_source(
    batch: dict[str, object], record: dict[str, object], source_data: bytes
) -> dict[str, object]:
    file_path = str(batch.get('file_path', ''))
    row_id = str(record.get('id', ''))
    metadata = record.get('raw_source')
    if (batch.get('translation_policy') != 'natural-dialogue-v2'
            or record.get('encoder', batch.get('encoder')) != 'dialogue-fixed-v1'
            or not re.fullmatch(r'/data/SC[0-3]\.DK4', file_path)
            or not isinstance(metadata, dict)
            or set(metadata) != {'hex', 'presentation_prefix_hex'}):
        raise ValueError(f'{row_id}: raw source requires an explicit v2 fixed story record')
    match = re.fullmatch(r'DK4_MES_B([0-9]+)_R([0-9]+)', row_id)
    if match is None:
        raise ValueError(f'{row_id}: invalid raw source record identifier')
    block_index, segment_index = map(int, match.groups())
    container = IlnkContainer.parse(source_data)
    if block_index >= len(container.blocks):
        raise ValueError(f'{row_id}: raw source block is out of range')
    segments = container.blocks[block_index].split(b'\0')
    if segment_index >= len(segments):
        raise ValueError(f'{row_id}: raw source segment is out of range')
    raw = segments[segment_index]
    expected = bytes.fromhex(str(metadata['hex']))
    prefix = bytes.fromhex(str(metadata['presentation_prefix_hex']))
    if not raw or raw != expected:
        raise ValueError(f'{row_id}: raw source bytes do not match')
    try:
        raw.decode('cp932')
    except UnicodeDecodeError:
        pass
    else:
        raise ValueError(f'{row_id}: raw source resolution is only for undecodable records')
    profile = get_dialogue_profile(str(record.get('dialogue_profile', batch.get('dialogue_profile', 'story'))))
    if (len(prefix) != 1 or prefix[0] < 0x80
            or not raw.startswith(prefix) or prefix[0] not in profile.leading_speaker_bytes
            or not profile.pair_phase_safe_breaks):
        raise ValueError(f'{row_id}: raw source prefix is not a mapped route speaker state')
    if not str(record.get('english', '')).startswith(f'{{SPEAKER:{prefix[0]:02X}}}'):
        raise ValueError(f'{row_id}: raw source speaker state must be retained explicitly')
    body = raw[1:]
    if any(byte < 0x20 and byte != 0x0A for byte in body):
        raise ValueError(f'{row_id}: raw source body contains unmapped controls')
    text = body.decode('cp932')
    if not contains_japanese(text):
        raise ValueError(f'{row_id}: raw source has no decodable Japanese prose')
    offset = 8+(len(container.blocks)+1)*4+sum(map(len, container.blocks[:block_index]))
    offset += sum(len(segment)+1 for segment in segments[:segment_index])
    return {
        'id': row_id, 'file_path': file_path,
        'container_path': f'{file_path}#block={block_index}', 'encoding': 'shift_jis',
        'source_offset': offset, 'source_length': len(raw), 'source_hex': raw.hex().upper(),
        'japanese': text.replace('\n', '{LB}'), 'english': '', 'status': 'untranslated',
        'context': f'ILNK block {block_index}, record {segment_index}', 'speaker': '',
        'notes': f'Exact raw source; mapped presentation prefix {prefix.hex().upper()} retained.',
        'max_bytes': len(raw), 'allow_expand': 'false',
        'pointer_group': f'ILNK:{block_index}:{segment_index}',
        'control_profile': 'mesfile', 'wrap_width': 38,
    }
