"""Apply reviewed fixed native messages after frozen historical release stages.

Source Japanese still comes from the canonical batch input. Every current byte,
native header, speaker byte and target allocation is independently locked.
"""

import json
from pathlib import Path

from dk4tool.dialogue.encoder import encode_fixed_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.translation_batch import materialize_translation_batch

HEADER = b'\0\x40\xFF\xFF\0'


def apply_release(image, baseline, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-late-story-editorial-release-v1':
        raise ValueError('Unknown late story editorial release')
    for path,digest in config['dependencies'].items():
        if sha(Path(path).read_bytes()) != digest:
            raise ValueError(f'Late story editorial dependency differs:{path}')
    for path,digest in config['required_runtime_sha256'].items():
        if sha(image.read_file(path)) != digest:
            raise ValueError(f'Late story editorial runtime differs:{path}')
    originals = {path:image.read_file(path) for path in config['source_file_sha256']}
    if {p:sha(b) for p,b in originals.items()} != config['source_file_sha256']:
        raise ValueError('Late story editorial complete source differs')
    containers = {p:IlnkContainer.parse(b) for p,b in originals.items()}
    changes, seen, paths = [], set(), []
    for spec in config['batches']:
        path = Path(spec['path'])
        if sha(path.read_bytes()) != spec['sha256']:
            raise ValueError('Late story editorial batch differs')
        header = json.loads(path.read_text(encoding='utf-8'))
        validate_natural_dialogue_batch(header)
        if (header.get('translation_policy') != 'natural-dialogue-v2'
                or header.get('encoder') != 'dialogue-fixed-v1'):
            raise ValueError('Late story editorial requires fixed natural-dialogue-v2')
        file_path = header['file_path']
        rows = materialize_translation_batch(header,baseline.read_file(file_path))
        for row in rows:
            key = file_path,row['id']
            if key in seen:
                raise ValueError('Late story editorial records overlap')
            seen.add(key)
            _,block_number,record_number = str(row['pointer_group']).split(':')
            block_number,record_number = int(block_number),int(record_number)
            container = containers[file_path]
            block = container.blocks[block_number]
            parts = block.split(b'\0')
            at = sum(len(part)+1 for part in parts[:record_number])
            before = parts[record_number]
            canonical = bytes.fromhex(str(row['source_hex']))
            expected = bytes.fromhex(spec['current_record_hex'][str(row['id'])])
            if before != expected or block[at-5:at] != HEADER:
                raise ValueError('Late story editorial current message/header differs')
            profile = get_dialogue_profile(str(row['dialogue_profile']))
            if not profile.guard_linebreaks or not profile.pair_phase_safe_breaks:
                raise ValueError('Late story editorial requires a live guarded profile')
            result = encode_fixed_dialogue(canonical,str(row['english']),profile)
            after = result.encoded
            if len(after) != len(before) or before[0] != canonical[0] or after[0] != canonical[0]:
                raise ValueError('Late story editorial allocation or original actor changes')
            if after == before:
                raise ValueError('Late story editorial has no changed text')
            container.blocks[block_number] = block[:at]+after+block[at+len(before):]
            changes.append(dict(file_path=file_path,id=row['id'],block=block_number,
                record=record_number,offset=at,bytes=len(before),before_hex=before.hex(),after_hex=after.hex(),
                original_native_header_and_actor_exact=True,following_command_address_exact=True,
                formatted_markup=result.formatted_markup,padding_bytes=result.padding_bytes))
        paths.append(str(path))
    targets = {p:c.to_bytes() for p,c in containers.items()}
    if {p:sha(b) for p,b in targets.items()} != config['target_file_sha256']:
        raise ValueError('Late story editorial complete target differs')
    for path,after in targets.items():
        before = originals[path]
        if len(after) != len(before):
            raise ValueError('Late story editorial archive size changes')
        old_blocks = IlnkContainer.parse(before).blocks
        for index,(old,new) in enumerate(zip(old_blocks,containers[path].blocks,strict=True)):
            if len(old) != len(new):
                raise ValueError('Late story editorial block size changes')
            allowed = [r for r in changes if r['file_path'] == path and r['block'] == index]
            for at,(a,b) in enumerate(zip(old,new,strict=True)):
                if a != b and not any(r['offset'] < at < r['offset']+r['bytes'] for r in allowed):
                    raise ValueError('Late story editorial changes unrelated or actor bytes')
        image.replace_file(path,after)
    return dict(changed_records=changes,batches=paths,
        source_file_sha256=config['source_file_sha256'],target_file_sha256=config['target_file_sha256'],
        all_unowned_bytes_original_headers_actors_and_native_command_addresses_exact=True)
