import copy
import json
from pathlib import Path

import pytest

from dk4tool.patch.grand_race_menu_release import compile_records, validate_release_batch
from dk4tool.rom.nds import NdsImage


@pytest.fixture(scope='module')
def inputs():
    source = NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin')
    manuscript = json.loads(Path('translations/grand_race_menu_manuscript_v2.json').read_text(encoding='utf-8'))
    batch = json.loads(Path('translations/grand_race_menu_arm9_v2.json').read_text(encoding='utf-8'))
    return source, manuscript, batch


def test_complete_reviewed_labels_recompile_and_validate(inputs):
    source, manuscript, batch = inputs
    assert compile_records(manuscript, source) == batch['records']
    validate_release_batch(batch, source)


@pytest.mark.parametrize('gate', ['source', 'context', 'localization', 'naturalness', 'formatting'])
def test_missing_individual_review_gate_rejects(inputs, gate):
    source, manuscript, _ = inputs
    changed = copy.deepcopy(manuscript)
    changed['records'][0]['review'][gate] = False
    with pytest.raises(ValueError, match='review gate'):
        compile_records(changed, source)


def test_complete_english_overallocation_rejects_instead_of_truncating(inputs):
    source, manuscript, _ = inputs
    changed = copy.deepcopy(manuscript)
    changed['records'][0]['english'] = 'A' * 40
    with pytest.raises(ValueError, match='allocation/display'):
        compile_records(changed, source)


def test_removed_consumer_lock_rejects(inputs):
    source, _, batch = inputs
    changed = copy.deepcopy(batch)
    changed['native_menu_labels']['consumer_locks'].pop()
    with pytest.raises(ValueError, match='consumer coverage'):
        validate_release_batch(changed, source)


def test_changed_clear_string_rejects(inputs):
    source, _, batch = inputs
    changed = bytearray(source)
    changed[0x116438] = ord('X')
    with pytest.raises(ValueError, match='menu context changed'):
        validate_release_batch(batch, changed)


def test_stale_replacement_rejects(inputs):
    source, _, batch = inputs
    changed = copy.deepcopy(batch)
    changed['records'][0]['english'] = changed['records'][0]['english'][1:]
    with pytest.raises(ValueError, match='complete reviewed manuscript'):
        validate_release_batch(changed, source)
