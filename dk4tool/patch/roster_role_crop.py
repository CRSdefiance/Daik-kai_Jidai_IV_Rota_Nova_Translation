"""Preserve complete crew role names in the roster's shared sprite crop."""

import json
import struct
from pathlib import Path

from dk4tool.patch.crew_role_labels import LABELS
from dk4tool.patch.grand_race_menu_release import sha

SOURCE = 'fa441ca49e981e332b5ad27ffb09c4ff1279222b8d8ec845bccce11eb16a6c45'
DESCRIPTOR = 0x14F4B0
FIELD = DESCRIPTOR + 20
OLD = (-1, 12, 92, 0, 0, 48, 12)
WIDTH = 204


def transform(source, clean, canonical):
    assert sha(source) == SOURCE
    assert WIDTH == 204
    assert max(len(text) + len(text) % 2 for text in LABELS) * 6 <= WIDTH
    for arm in (source, clean, canonical):
        assert struct.unpack_from('<7i', arm, DESCRIPTOR) == OLD
        assert struct.unpack_from('<I', arm, 0x9C1D4)[0] == 0x02000000 + DESCRIPTOR
    assert struct.unpack_from('<7i', source, DESCRIPTOR + 56)[5] == 204
    assert OLD[3] + WIDTH <= 204
    assert OLD[1] + WIDTH <= 256 and OLD[2] + OLD[6] <= 192
    target = bytearray(source)
    struct.pack_into('<I', target, FIELD, WIDTH)
    assert target[:FIELD] == source[:FIELD] and target[FIELD + 4:] == source[FIELD + 4:]
    return bytes(target), {'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(target),
                           'descriptor': DESCRIPTOR, 'width_field': FIELD, 'before': 48, 'after': WIDTH,
                           'all16_complete_role_names_and_terminal_blank_fit': True,
                           'ship_and_rank_captions_share_existing_204_pixel_name_row_width': True,
                           'one_width_word_only_all_strings_code_pool_rows_and_art_preserved': True,
                           'changed_records': ['DK4_ROSTER_ROLE_COMPLETE_CROP']}


def apply_release(source, clean, canonical, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-roster-role-crop-release-v1'
    for file, digest in config['verification_evidence_sha256'].items():
        assert sha(Path(file).read_bytes()) == digest
    target, plan = transform(source, clean, canonical)
    assert sha(target) == config['target_arm9_sha256']
    return target, plan
