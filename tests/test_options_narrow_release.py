import json
from pathlib import Path

import pytest

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.options_narrow_release import SLOTS, apply_release
from dk4tool.rom.nds import NdsImage


def test_complete_source_locked_options_release_preserves_all_other_bytes():
    source = NdsImage.open('out/all_routes_combined_v143_candidate.nds').read_file('/__arm9__.bin')
    saved, report = apply_release(source, 'translations/options_narrow_release_v1.json')
    restored = bytearray(saved)
    for at, (capacity, _, english) in SLOTS.items():
        assert saved[at:at + capacity].split(b'\0', 1)[0].decode('ascii') == english
        restored[at:at + capacity] = source[at:at + capacity]
    assert bytes(restored) == source
    assert report['runtime_verified'] is False


def test_older_parent_cannot_receive_narrow_prompts():
    source = NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin')
    with pytest.raises(ValueError, match='exact complete V143'):
        apply_release(source, 'translations/options_narrow_release_v1.json')


def test_incomplete_formatting_review_cannot_be_relocked_into_release(tmp_path):
    source = NdsImage.open('out/all_routes_combined_v143_candidate.nds').read_file('/__arm9__.bin')
    config = json.loads(Path('translations/options_narrow_release_v1.json').read_text(encoding='utf-8'))
    document = json.loads(Path(config['manuscript']).read_text(encoding='utf-8'))
    document['records'][0]['review']['formatting'] = False
    manuscript = tmp_path / 'unreviewed.json'
    manuscript.write_text(json.dumps(document), encoding='utf-8')
    old = config['manuscript']
    config['manuscript'] = manuscript.as_posix()
    config['dependencies'].pop(old)
    config['dependencies'][manuscript.as_posix()] = sha(manuscript.read_bytes())
    path = tmp_path / 'config.json'
    path.write_text(json.dumps(config), encoding='utf-8')
    with pytest.raises(ValueError, match='formatting review'):
        apply_release(source, path)
