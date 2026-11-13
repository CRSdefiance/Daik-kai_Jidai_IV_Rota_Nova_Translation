"""Source-locked natural paragraphs replacing four inherited percent hazards."""

from pathlib import Path

from dk4tool.dialogue.encoder import encode_fixed_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.verify_village_wrap_v608 import read


def transform(source: bytes, canonical: bytes, spec: dict) -> tuple[bytes, dict]:
    if sha(source) != spec['current_sha256'] or sha(canonical) != spec['canonical_sha256']:
        raise ValueError('Literal percent repair requires exact current and immutable canonical story files')
    path = Path(spec['batch'])
    if sha(path.read_bytes()) != spec['batch_sha256']:
        raise ValueError('Literal percent manuscript changed after review')
    batch = read(path)
    if batch.get('translation_policy') != 'natural-dialogue-v2' or batch.get('encoder') != 'dialogue-fixed-v1':
        raise ValueError('Natural-dialogue-v2 exact-allocation paragraphs required')
    validate_natural_dialogue_batch(batch)
    rows = materialize_translation_batch(batch, canonical)
    if [r['id'] for r in rows] != spec['ids']:
        raise ValueError('Literal percent repair record scope differs')
    container = IlnkContainer.parse(source)
    before = list(container.blocks)
    changes = []
    for row in rows:
        block, segment = [int(v) for v in row['pointer_group'].split(':')[1:]]
        fields = container.blocks[block].split(b'\0')
        old = fields[segment]
        original = bytes.fromhex(row['source_hex'])
        profile = get_dialogue_profile(row['dialogue_profile'])
        qa = audit_fixed_dialogue_record(original, row['english'], profile)
        if any(i['severity'] in ('error', 'warning') for i in qa['issues']):
            raise ValueError(f"{row['id']}: unwaived natural dialogue QA: {qa['issues']}")
        encoded = encode_fixed_dialogue(original, row['english'], profile).encoded
        assert len(encoded) == len(old) == len(original) and encoded[:1] == old[:1] == original[:1]
        assert b'%' in old[1:] and b'%' not in encoded and qa['manual_break_count'] == 0
        fields[segment] = encoded
        container.blocks[block] = b'\0'.join(fields)
        changes.append({'id': row['id'], 'block': block, 'segment': segment, 'allocation': len(original),
            'canonical_Japanese_hex': original.hex(), 'before_hex': old.hex(), 'after_hex': encoded.hex(),
            'paragraph': row['english'], 'compiled_lines': qa['visible_lines'], 'padding_bytes': qa['padding_bytes'],
            'native_profile': row['dialogue_profile'], 'generated_breaks_only_no_warnings_or_errors': True})
    target = container.to_bytes()
    assert len(target) == len(source)
    owned = {r['block'] for r in changes}
    assert all(a == b for i, (a, b) in enumerate(zip(before, container.blocks, strict=True)) if i not in owned)
    for block in owned:
        old, new = before[block].split(b'\0'), container.blocks[block].split(b'\0')
        assert len(old) == len(new)
        assert {i for i, (a, b) in enumerate(zip(old, new, strict=True)) if a != b} == {
            r['segment'] for r in changes if r['block'] == block}
    return target, {'source_sha256': sha(source), 'canonical_sha256': sha(canonical),
        'target_sha256': sha(target), 'changed_records': spec['ids'], 'records': changes,
        'all_allocations_ILNK_headers_offsets_controls_and_other_records_exact': True}


def apply_release(source_files: dict, canonical_files: dict, config_path):
    config = read(config_path)
    if config.get('format') != 'dk4-story-literal-percent-v1':
        raise ValueError('Literal-percent release format differs')
    files, proof = {}, {}
    for path, spec in config['files'].items():
        files[path], proof[path] = transform(source_files[path], canonical_files[path], spec)
    if proof != config['proof']:
        raise ValueError('Literal-percent compiled output differs from reviewed source proof')
    return files, proof
