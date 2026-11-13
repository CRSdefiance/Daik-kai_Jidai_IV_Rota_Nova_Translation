import json
from pathlib import Path

import pytest

from dk4tool.patch.deck_explanation_release import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage


def test_reviewed_release_matches_connected_native_research_exactly():
    source = NdsImage.open('out/all_routes_combined_v145_candidate.nds').read_file('/__arm9__.bin')
    saved, report = apply_release(source, 'translations/deck_explanation_release_v1.json')
    assert saved == Path('work/analysis/deck_explanations_pool_arm9.bin').read_bytes()
    assert report['inherited_owners_preserved'] == 27
    assert report['references_relocated'] == 31
    assert report['runtime_verified'] is False


def test_unreviewed_deck_prose_cannot_be_relocked_into_release(tmp_path):
    source = NdsImage.open('out/all_routes_combined_v145_candidate.nds').read_file('/__arm9__.bin')
    config = json.loads(Path('translations/deck_explanation_release_v1.json').read_text(encoding='utf-8'))
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


def test_older_stack_cannot_receive_relocated_deck_pool():
    source = NdsImage.open('out/all_routes_combined_v144_candidate.nds').read_file('/__arm9__.bin')
    with pytest.raises(ValueError, match='exact complete V145'):
        apply_release(source, 'translations/deck_explanation_release_v1.json')
