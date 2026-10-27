"""Repack two source-owned choice strings without changing VM command positions."""

import json
import struct
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha

BLOCK, START, END = 177, 0x8E6, 0x8FC
PATH = '/data/SC0.DK4'
CURRENT = bytes.fromhex('0021000006005965732000004e6f2020202020200000')


def compile_object(current, manuscript):
    """Original getter uses base+6+table[index]; VM advances past the last string.

    Move the last string to end at its original terminator, and point its table
    entry there. The first string may terminate earlier because its successor
    is selected by an explicit offset, not by scanning the first string.
    Preserve NUL count so later diagnostic record IDs also remain stable.
    """
    validate_natural_dialogue_batch(manuscript)
    if current != CURRENT or manuscript.get('translation_policy') != 'natural-dialogue-v2':
        raise ValueError('Exact two-choice object and reviewed policy required')
    rows = manuscript['records']
    if [r['id'] for r in rows] != ['DK4_MES_B177_R0150', 'DK4_MES_B177_R0152']:
        raise ValueError('Only the original two ship-advice choices are owned')
    labels = [r['english'].removesuffix('{PAD}').encode('ascii') for r in rows]
    if labels != [b'Yes', b'No']:
        raise ValueError('This repair retains both original English choices')
    result = bytearray(current)
    first, last_terminator = 6, len(current) - 2
    second = last_terminator - len(labels[1])
    result[first:first + len(labels[0])] = labels[0]
    result[first + len(labels[0])] = 0
    # Reclaim the old first terminator as unused inter-label storage. The next
    # original alignment NUL and all later separator counts remain unchanged.
    result[first + len(labels[0]) + 1] = 0x20
    result[12:second] = b' ' * (second - 12)
    result[second:last_terminator] = labels[1]
    struct.pack_into('<H', result, 4, second - first)
    if len(result) != len(current) or result.count(0) != current.count(0):
        raise ValueError('Choice object extent or separator count changes')
    if result[:4] != current[:4] or result[-2:] != current[-2:]:
        raise ValueError('Choice opcode, first pointer, or last VM boundary changes')
    return bytes(result)


def apply_release(image, baseline, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-ship-advice-choice-centering-v1':
        raise ValueError('Unknown choice-centering configuration')
    for name, digest in config['dependencies'].items():
        if sha(Path(name).read_bytes()) != digest:
            raise ValueError(f'Choice-centering dependency differs: {name}')
    before = image.read_file(PATH)
    if sha(before) != config['source_SC0_sha256']:
        raise ValueError('Choice repair requires the complete screenshot repair stack')
    if sha(image.read_file('/__arm9__.bin')) != config['required_ARM9_sha256']:
        raise ValueError('Choice native consumer differs')
    source = IlnkContainer.parse(baseline.read_file(PATH)).blocks[BLOCK][START:END]
    if source.hex() != config['canonical_choice_object_hex']:
        raise ValueError('Original Japanese choice object differs')
    manuscript = json.loads(Path(config['manuscript']).read_text(encoding='utf-8'))
    container = IlnkContainer.parse(before)
    block = container.blocks[BLOCK]
    replacement = compile_object(block[START:END], manuscript)
    container.blocks[BLOCK] = block[:START] + replacement + block[END:]
    after = container.to_bytes()
    if sha(after) != config['target_SC0_sha256'] or len(after) != len(before):
        raise ValueError('Final bounded choice repair differs')
    if after[:8 + (len(container.blocks) + 1) * 4] != before[:8 + (len(container.blocks) + 1) * 4]:
        raise ValueError('ILNK directory changes')
    image.replace_file(PATH, after)
    return {'changed_records': [r['id'] for r in manuscript['records']],
            'block': BLOCK, 'owned_span': [START, END], 'before_hex': CURRENT.hex(),
            'after_hex': replacement.hex(), 'source_SC0_sha256': sha(before), 'target_SC0_sha256': sha(after),
            'batches': [config['manuscript']], 'last_terminator_and_following_command_positions_exact': True,
            'native_code_fonts_geometry_and_choice_meanings_unchanged': True,
            'user_report_is_No_centering_not_missing_prompt': True, 'status': 'experimental'}
