import copy
import json
import struct
from pathlib import Path

import pytest

from dk4tool.patch.grand_race_help_release import compile_records, validate_release_batch
from dk4tool.rom.nds import NdsImage
from scripts.register_grand_race_help_v134 import patched_arm9


@pytest.fixture(scope='module')
def inputs():
    source = NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin')
    japanese = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    manuscript = json.loads(Path('translations/grand_race_rules_manuscript_v2.json').read_text(encoding='utf-8'))
    batch = json.loads(Path('translations/grand_race_help_arm9_v2.json').read_text(encoding='utf-8'))
    return source, japanese, manuscript, batch


def test_complete_help_patch_roundtrips_all_descriptors(inputs):
    source, japanese, manuscript, batch = inputs
    records, selections, used = compile_records(manuscript, source, japanese)
    assert records == batch['records']
    assert len(records) == 18 and used == 1794
    rebuilt = patched_arm9(source, batch)
    for row in selections:
        title, body = struct.unpack_from('<II', rebuilt, row['descriptor'])
        assert rebuilt[title - 0x02000000:].split(b'\0', 1)[0].decode('ascii') == row['title']
        assert rebuilt[body - 0x02000000:].split(b'\0', 1)[0] == bytes.fromhex(row['encoded_hex'])
    validate_release_batch(batch, source)


def test_incomplete_formatting_gate_blocks_release(inputs):
    source, japanese, manuscript, _ = inputs
    altered = copy.deepcopy(manuscript)
    altered['records'][0]['review']['formatting'] = False
    with pytest.raises(ValueError, match='review gate'):
        compile_records(altered, source, japanese)


def test_missing_page_blocks_release(inputs):
    source, japanese, manuscript, _ = inputs
    altered = copy.deepcopy(manuscript)
    altered['records'].pop()
    with pytest.raises(ValueError, match='all nine'):
        compile_records(altered, source, japanese)


def test_altered_body_pointer_blocks_release(inputs):
    source, _, _, batch = inputs
    altered = copy.deepcopy(batch)
    altered['records'][0]['replacement_hex'] = '00000000'
    with pytest.raises(ValueError, match='automatically formatted manuscript'):
        validate_release_batch(altered, source)


def test_heading_padding_cannot_overwrite_unrelated_data(inputs):
    source, japanese, manuscript, _ = inputs
    altered = bytearray(source)
    altered[0x1379B2] = 1
    with pytest.raises(ValueError, match='Heading differs'):
        compile_records(manuscript, bytes(altered), japanese)


def test_missing_consumer_lock_blocks_release(inputs):
    source, _, _, batch = inputs
    altered = copy.deepcopy(batch)
    altered['native_text_repack']['consumer_locks'].pop()
    with pytest.raises(ValueError, match='consumer lock coverage'):
        validate_release_batch(altered, source)
