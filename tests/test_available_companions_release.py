import json
from pathlib import Path

import pytest

from dk4tool.patch.available_companions_release import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage


def source():
    return NdsImage.open('out/all_routes_combined_v146_candidate.nds').read_file('/__arm9__.bin')


def relock(tmp_path, key, change):
    config = json.loads(Path('translations/available_companions_release_v1.json').read_text(encoding='utf-8'))
    document = json.loads(Path(config[key]).read_text(encoding='utf-8'))
    change(document)
    path = tmp_path / (key + '.json')
    path.write_text(json.dumps(document), encoding='utf-8')
    config['dependencies'].pop(config[key])
    config[key] = path.as_posix()
    config['dependencies'][path.as_posix()] = sha(path.read_bytes())
    destination = tmp_path / 'config.json'
    destination.write_text(json.dumps(config), encoding='utf-8')
    return destination


def test_release_matches_reviewed_native_bytes_and_preserves_all_neighbors():
    saved, report = apply_release(source(), 'translations/available_companions_release_v1.json')
    assert saved == Path('work/analysis/available_companions_arm9.bin').read_bytes()
    assert report['inherited_owners_preserved'] == 3
    assert report['references_relocated'] == 4
    assert report['runtime_verified'] is False


def test_unreviewed_formatting_cannot_be_relocked_into_release(tmp_path):
    path = relock(tmp_path, 'manuscript',
                  lambda d: d['records'][0]['review'].__setitem__('formatting', False))
    with pytest.raises(ValueError, match='formatting review'):
        apply_release(source(), path)


def test_altered_neighbor_cannot_be_relocked_into_release(tmp_path):
    path = relock(tmp_path, 'pool',
                  lambda d: d['moves'][2].__setitem__('complete_text', '(%s)'))
    with pytest.raises(ValueError, match='neighboring wording'):
        apply_release(source(), path)


def test_older_stack_cannot_receive_release():
    older = NdsImage.open('out/all_routes_combined_v145_candidate.nds').read_file('/__arm9__.bin')
    with pytest.raises(ValueError, match='exact complete V146'):
        apply_release(older, 'translations/available_companions_release_v1.json')


def test_native_error_options_and_name_format_preserved_by_production():
    from scripts.probe_available_companions import empty_branch, parenthesized_format
    from scripts.probe_options_narrow_prompts import execute, respond

    saved, _ = apply_release(source(), 'translations/available_companions_release_v1.json')
    empty_branch(saved)
    for kind in ('sailing', 'reports'):
        for flags in (0, 1, 2, 3, 255):
            execute(saved, kind, flags)
            for accepted in (False, True):
                respond(saved, kind, flags, accepted)
    for name in ('', 'A', 'Even', 'Fleet', '海', 'Indigo海'):
        parenthesized_format(saved, name)
