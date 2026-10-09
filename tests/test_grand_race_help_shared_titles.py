import copy
import json
import struct
from pathlib import Path

import pytest

from dk4tool.patch.grand_race_help_release import compile_records as compile_help
from dk4tool.patch.grand_race_help_shared_titles import MENU, SHARED, validate_release_batch
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import apply_arm9_fixed_batches

VARIANT = Path('translations/grand_race_help_shared_menu_titles_v2.json')


@pytest.fixture(scope='module')
def inputs():
    source = NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin')
    japanese = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    manuscript = json.loads(Path('translations/grand_race_rules_manuscript_v2.json').read_text(encoding='utf-8'))
    batch = json.loads(VARIANT.read_text(encoding='utf-8'))
    return source, japanese, manuscript, batch


def test_all_nine_complete_help_pages_and_titles_survive_sharing(inputs):
    source, japanese, manuscript, batch = inputs
    rebuilt, _ = apply_arm9_fixed_batches([VARIANT, Path(MENU)], source)
    _, selections, used = compile_help(manuscript, source, japanese)
    assert used == 1794
    for row in selections:
        title, body = struct.unpack_from('<II', rebuilt, row['descriptor'])
        assert rebuilt[title - 0x02000000:].split(b'\0', 1)[0].decode('ascii') == row['title']
        assert rebuilt[body - 0x02000000:].split(b'\0', 1)[0] == bytes.fromhex(row['encoded_hex'])
    for descriptor, old, size, _, target in SHARED:
        assert struct.unpack_from('<I', rebuilt, descriptor)[0] == 0x02000000 + target
        assert rebuilt[old:old + size] == source[old:old + size]
        assert not any(r['offset'] < old + size and old < r['offset'] + len(bytes.fromhex(r['source_hex'])) for r in batch['records'])
    validate_release_batch(batch, source)


def test_sharing_without_complete_menu_dependency_is_rejected(inputs):
    source, _, _, _ = inputs
    with pytest.raises(ValueError, match='complete native menu batch'):
        apply_arm9_fixed_batches([VARIANT], source)


@pytest.mark.parametrize('dependency', ['help_batch', 'menu_batch'])
def test_stale_dependency_hash_is_rejected(inputs, dependency):
    source, _, _, batch = inputs
    changed = copy.deepcopy(batch)
    changed['native_shared_help_titles'][dependency + '_sha256'] = '0' * 64
    with pytest.raises(ValueError, match='missing or stale'):
        validate_release_batch(changed, source)


def test_dropped_help_page_is_rejected(inputs):
    source, _, _, batch = inputs
    changed = copy.deepcopy(batch)
    changed['records'].pop(0)
    with pytest.raises(ValueError, match='complete reviewed'):
        validate_release_batch(changed, source)


def test_wrong_shared_title_pointer_is_rejected(inputs):
    source, _, _, batch = inputs
    changed = copy.deepcopy(batch)
    changed['records'][-1]['replacement_hex'] = '00000000'
    with pytest.raises(ValueError, match='complete reviewed'):
        validate_release_batch(changed, source)
