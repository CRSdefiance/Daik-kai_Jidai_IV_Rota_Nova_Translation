import copy
import json
import struct
from pathlib import Path

import pytest

from dk4tool.patch.grand_race_complete_release import (
    DATA,
    DEPENDENCIES,
    compile_components,
    validate_release_batch,
)
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import apply_arm9_fixed_batches
from scripts.register_grand_race_complete_v137 import ORIGINAL_HELP, SHARED, extend


@pytest.fixture(scope='module')
def inputs():
    source = NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin')
    return source, json.loads(Path(DATA).read_text()), [Path(path) for path in DEPENDENCIES]


def test_complete_components_use_integrated_builder(inputs):
    source, _, paths = inputs
    compiled, proposed = compile_components(source)
    rebuilt, _ = apply_arm9_fixed_batches(paths, source)
    for rows in compiled.values():
        for row in rows:
            lo, size = row['offset'], len(bytes.fromhex(row['source_hex']))
            assert rebuilt[lo:lo + size] == proposed[lo:lo + size]
    assert struct.unpack_from('<I', rebuilt, 0x12ED04)[0] == 180
    assert len(compiled['code']) == 88


@pytest.mark.parametrize('missing', DEPENDENCIES)
def test_missing_component_rejected_before_insertion(inputs, missing):
    source, batch, paths = inputs
    with pytest.raises(ValueError, match='all six release dependencies'):
        validate_release_batch(batch, source, [path for path in paths if path != Path(missing)])


def test_original_help_batch_cannot_occupy_released_titles(inputs):
    source, batch, paths = inputs
    with pytest.raises(ValueError, match='in place of original help'):
        validate_release_batch(batch, source, paths + [Path('translations/grand_race_help_arm9_v2.json')])


def test_dropped_first_character_rejected(inputs):
    source, batch, paths = inputs
    changed = copy.deepcopy(batch)
    row = changed['records'][0]
    raw = bytes.fromhex(row['replacement_hex'])
    row['replacement_hex'] = (raw[1:] + b'\0').hex()
    with pytest.raises(ValueError, match='records differ'):
        validate_release_batch(changed, source, paths)


def test_extra_unowned_write_rejected(inputs):
    source, batch, paths = inputs
    changed = copy.deepcopy(batch)
    changed['records'].append({'id': 'EXTRA', 'offset': 0x100,
                               'source_hex': source[0x100:0x104].hex(),
                               'replacement_hex': '00000000'})
    with pytest.raises(ValueError, match='records differ'):
        validate_release_batch(changed, source, paths)


def test_stale_sibling_dependency_rejected(inputs):
    source, batch, paths = inputs
    changed = copy.deepcopy(batch)
    changed['native_complete_race_ui']['dependencies'][DEPENDENCIES[-1]] = '0' * 64
    with pytest.raises(ValueError, match='sibling dependencies changed'):
        validate_release_batch(changed, source, paths)


def test_profile_preserves_every_other_preceding_layer():
    registry = json.loads(Path('translations/release_stack.json').read_text())
    old = registry['profiles']['all-routes-unified-v136']
    new = extend(old)
    assert [path for path in old['batches'] if path != ORIGINAL_HELP] == [
        path for path in new['batches'][:len(old['batches'])] if path != SHARED]
    assert len(new['batches']) == len(old['batches']) + 3
    assert ORIGINAL_HELP not in new['batches']
    assert all(path in new['batches'] for path in DEPENDENCIES)
