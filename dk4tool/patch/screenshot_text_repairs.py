"""Exact-span screenshot corrections after the complete registered parent stack.

Keep historical producers reproducible. In SC0 B177 R140, actor zero is the
NUL *before* the body: 8E51 is the complete Japanese glyph 参, not actor 8E.
Literal I/F are safe here only with the inherited native literal-command guard.
"""

import json
from pathlib import Path

from dk4tool.dialogue.encoder import encode_fixed_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha


def apply_release(image, baseline, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-screenshot-text-repairs-v1':
        raise ValueError('Unknown screenshot correction format')
    for name, digest in config['dependencies'].items():
        if sha(Path(name).read_bytes()) != digest:
            raise ValueError(f'Screenshot correction dependency differs: {name}')
    manuscript = json.loads(Path(config['manuscript']).read_text(encoding='utf-8'))
    validate_natural_dialogue_batch(manuscript)
    originals = {p: image.read_file(p) for p in config['source_file_sha256']}
    if {p: sha(b) for p, b in originals.items()} != config['source_file_sha256']:
        raise ValueError('Screenshot correction requires the exact complete inherited stack')
    target = dict(originals)
    changes = []
    story_path = '/data/SC0.DK4'
    container = IlnkContainer.parse(originals[story_path])
    canonical = IlnkContainer.parse(baseline.read_file(story_path))
    for row in manuscript['records']:
        if row['kind'] != 'story':
            continue
        block_number, record = row['block'], row['record']
        source = canonical.blocks[block_number].split(b'\0')[record]
        if source.hex() != row['source_hex']:
            raise ValueError('Clean Japanese story text differs')
        block = container.blocks[block_number]
        parts = block.split(b'\0')
        before = parts[record]
        at = sum(len(p) + 1 for p in parts[:record])
        if before.hex() != row['current_hex']:
            raise ValueError('Current screenshot story record differs')
        # Both exact preambles retain the original object metadata and actor.
        # R140: 00 40 FF FF 00 00 [text]. R144: 00 40 FF FF 00 0D [text].
        if block[at - 6:at].hex() != row['preceding_hex']:
            raise ValueError('Complete story object preamble differs')
        profile = get_dialogue_profile('raphael-story-live')
        qa = audit_fixed_dialogue_record(source, row['english'], profile)
        if any(i['severity'] in ('error', 'warning') for i in qa['issues']):
            raise ValueError(f'Screenshot story QA failed: {qa["issues"]}')
        result = encode_fixed_dialogue(source, row['english'], profile)
        if len(result.encoded) != len(before):
            raise ValueError('Story correction changes native command addresses')
        if record == 140 and (not source.startswith(bytes.fromhex('8e51'))
                              or not result.encoded.startswith(b'Oh dear.')):
            raise ValueError('Zero-actor Japanese glyph repair differs')
        if record == 144 and (result.encoded[0] != 0x0D or source[0] != 0x0D):
            raise ValueError('Cesare actor differs')
        container.blocks[block_number] = block[:at] + result.encoded + block[at + len(before):]
        changes.append({'file_path': story_path, 'id': row['id'], 'block': block_number,
                            'offset': at, 'before_hex': before.hex(), 'after_hex': result.encoded.hex(), 'qa': qa})
    target[story_path] = container.to_bytes()
    for spec in config['literal_spans']:
        file_path = spec['file_path']
        before, after = bytes.fromhex(spec['before_hex']), bytes.fromhex(spec['after_hex'])
        at = spec['offset']
        if len(before) != len(after) or target[file_path][at:at + len(before)] != before:
            raise ValueError('Literal correction allocation or current bytes differ')
        target[file_path] = target[file_path][:at] + after + target[file_path][at + len(before):]
        changes.append({'file_path': file_path, 'id': spec['id'], 'offset': at,
                            'before_hex': before.hex(), 'after_hex': after.hex()})
    if {p: sha(b) for p, b in target.items()} != config['target_file_sha256']:
        raise ValueError('Screenshot correction final files differ')
    for file_path, after in target.items():
        if len(after) != len(originals[file_path]):
            raise ValueError('Screenshot correction changes file size')
        if file_path == story_path:
            old = IlnkContainer.parse(originals[file_path])
            for n, (a, b) in enumerate(zip(old.blocks, container.blocks, strict=True)):
                owned = [c for c in changes if c['file_path'] == file_path and c.get('block') == n]
                if len(a) != len(b) or any(x != y and not any(
                    c['offset'] <= at < c['offset'] + len(bytes.fromhex(c['before_hex']))
                    for c in owned) for at, (x, y) in enumerate(zip(a, b, strict=True))):
                    raise ValueError('Unowned story data changed')
        else:
            owned = [c for c in changes if c['file_path'] == file_path]
            if any(x != y and not any(c['offset'] <= at < c['offset'] + len(bytes.fromhex(c['before_hex']))
                   for c in owned) for at, (x, y) in enumerate(zip(originals[file_path], after, strict=True))):
                raise ValueError('Unowned literal data changed')
        image.replace_file(file_path, after)
    return {'changed_records': changes, 'batches': [config['manuscript']],
                'source_file_sha256': config['source_file_sha256'], 'target_file_sha256': config['target_file_sha256'],
                'native_code_fonts_selectors_allocations_and_other_records_preserved': True,
                'yes_no_missing_prompt_transition_verified': False, 'status': 'experimental'}
