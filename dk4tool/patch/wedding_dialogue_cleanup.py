"""Compile two canonical natural paragraphs into their existing final-stack slots."""

import struct
from pathlib import Path

from dk4tool.dialogue.encoder import encode_fixed_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.verify_village_wrap_v608 import read

SOURCE = 'ebf015677a2b30a3d4c053bc36a3e33e48e472fc5fab8d4f18a85be11a23136c'
CANONICAL = 'c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff'
IDS = ('DK4_MES_B70_R0397', 'DK4_MES_B70_R0615')


def transform(source, canonical, batch):
    if sha(source) != SOURCE or sha(canonical) != CANONICAL:
        raise ValueError('Wedding cleanup requires exact V666 final SC2 and immutable canonical source')
    if batch.get('translation_policy') != 'natural-dialogue-v2' or batch.get('dialogue_profile') != 'lil-story-deep-route-live':
        raise ValueError('Source-locked route-aware natural-dialogue-v2 required')
    validate_natural_dialogue_batch(batch)
    rows = materialize_translation_batch(batch, canonical)
    if tuple(row['id'] for row in rows) != IDS:
        raise ValueError('Wedding cleanup owns exactly B70 R0397 and R0615 in order')
    container = IlnkContainer.parse(source)
    assert container.to_bytes() == source
    blocks = list(container.blocks)
    fields = container.blocks[70].split(b'\0')
    old_fields, changes = list(fields), []
    for row in rows:
        block, segment = [int(value) for value in row['pointer_group'].split(':')[1:]]
        assert block == 70
        original = bytes.fromhex(row['source_hex'])
        profile = get_dialogue_profile(row['dialogue_profile'])
        qa = audit_fixed_dialogue_record(original, row['english'], profile)
        if any(item['severity'] in ('error', 'warning') for item in qa['issues']):
            raise ValueError(f"{row['id']}: unwaived natural dialogue diagnostics: {qa['issues']}")
        assert qa['manual_break_count'] == 0 and qa['automatic_break_count'] == 1
        encoded = encode_fixed_dialogue(original, row['english'], profile).encoded
        assert len(encoded) == len(original) == len(fields[segment])
        assert original[:1] == encoded[:1] == fields[segment][:1] == b'\x09'
        changes.append({'id': row['id'], 'segment': segment, 'allocation': len(original),
            'canonical_Japanese_hex': original.hex(), 'before_hex': fields[segment].hex(), 'after_hex': encoded.hex(),
            'paragraph': row['english'], 'compiled_lines': qa['visible_lines'], 'padding_bytes': qa['padding_bytes'],
            'generated_breaks_only_no_warnings_or_errors': True})
        fields[segment] = encoded
    assert [i for i, (a, b) in enumerate(zip(old_fields, fields, strict=True)) if a != b] == [397, 615]
    container.blocks[70] = b'\0'.join(fields)
    target = container.to_bytes()
    assert len(target) == len(source) and len(container.blocks[70]) == len(blocks[70]) == 6764
    assert struct.unpack_from('<H', container.blocks[70], 4324)[0] == 0x4906
    assert all(container.blocks[i] == old for i, old in enumerate(blocks) if i != 70)
    return target, {'source_SC2_sha256': sha(source), 'canonical_SC2_sha256': sha(canonical),
        'target_SC2_sha256': sha(target), 'changed_records': list(IDS), 'records': changes,
        'all_record_allocations_block_headers_pointer_offsets_and_movie_command_preserved': True,
        'only_two_existing_dialogue_spans_no_growth_or_new_controls': True, 'experimental': True}


def apply_release(source, canonical, path):
    config = read(path)
    if config['format'] != 'dk4-wedding-dialogue-cleanup-v1':
        raise ValueError('Wedding cleanup config format differs')
    batch_path = Path(config['batch'])
    if sha(batch_path.read_bytes()) != config['batch_sha256']:
        raise ValueError('Wedding natural-dialogue manuscript changed after review')
    target, proof = transform(source, canonical, read(batch_path))
    if proof != config['proof']:
        raise ValueError('Wedding cleanup source, compiled output or owned fields differ')
    return target, proof
