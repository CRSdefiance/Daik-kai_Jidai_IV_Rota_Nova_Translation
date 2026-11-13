import json
from pathlib import Path

import pytest

from dk4tool.patch.damaged_save_release import (
    CAPACITY,
    ENGLISH,
    OFFSET,
    apply_release,
    formatted_suffix,
)
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage


def test_generated_word_layout_preserves_complete_meaning_and_owned_bytes():
    source = NdsImage.open('out/all_routes_combined_v144_candidate.nds').read_file('/__arm9__.bin')
    saved, report = apply_release(source, 'translations/damaged_save_release_v1.json')
    first, second = formatted_suffix().split('\n')
    assert ' '.join(formatted_suffix().split()) == ENGLISH
    assert second.startswith('  ')
    assert max(6 + len(first), len(second)) <= 38
    assert len(formatted_suffix().encode('ascii')) + 1 == CAPACITY
    restored = bytearray(saved)
    restored[OFFSET:OFFSET + CAPACITY] = source[OFFSET:OFFSET + CAPACITY]
    assert bytes(restored) == source
    assert report['runtime_verified'] is False


def test_unreviewed_formatting_cannot_be_relocked_into_release(tmp_path):
    source = NdsImage.open('out/all_routes_combined_v144_candidate.nds').read_file('/__arm9__.bin')
    config = json.loads(Path('translations/damaged_save_release_v1.json').read_text(encoding='utf-8'))
    document = json.loads(Path(config['manuscript']).read_text(encoding='utf-8'))
    document['records'][0]['review']['formatting'] = False
    manuscript = tmp_path / 'unreviewed.json'
    manuscript.write_text(json.dumps(document), encoding='utf-8')
    config['dependencies'].pop(config['manuscript'])
    config['manuscript'] = manuscript.as_posix()
    config['dependencies'][manuscript.as_posix()] = sha(manuscript.read_bytes())
    path = tmp_path / 'release.json'
    path.write_text(json.dumps(config), encoding='utf-8')
    with pytest.raises(ValueError, match='formatting review'):
        apply_release(source, path)


def test_older_renderer_stack_cannot_receive_damaged_save_release():
    source = NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin')
    with pytest.raises(ValueError, match='exact complete V144'):
        apply_release(source, 'translations/damaged_save_release_v1.json')
