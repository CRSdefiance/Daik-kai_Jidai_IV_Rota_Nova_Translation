import json
from pathlib import Path

import pytest

from dk4tool.patch.fleet_name_release import apply_release, transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage


@pytest.fixture(scope='module')
def source():
    return NdsImage.open('out/all_routes_combined_v148_candidate.nds').read_file('/__arm9__.bin')


def test_complete_registered_output_matches_native_research(source):
    saved, report = apply_release(source, 'translations/fleet_name_release_v1.json')
    assert saved == Path('work/analysis/fleet_names_v148_research_arm9.bin').read_bytes()
    assert report['runtime_verified'] is False


def test_changed_source_rejected(source):
    with pytest.raises(ValueError, match='exact complete V148'):
        transform(bytes([source[0] ^ 1]) + source[1:])


@pytest.mark.parametrize('rehash', [False, True])
def test_missing_name_coverage_rejected_even_with_updated_dependency(source, tmp_path, rehash):
    config = json.loads(Path('translations/fleet_name_release_v1.json').read_text(encoding='utf-8'))
    native = json.loads(Path(config['native_review']).read_text(encoding='utf-8'))
    native['cases'].pop(0)
    review_path = tmp_path / 'review.json'
    review_path.write_text(json.dumps(native), encoding='utf-8')
    old = config['native_review']
    config['native_review'] = str(review_path)
    digest = config['dependencies'].pop(old)
    config['dependencies'][str(review_path)] = sha(review_path.read_bytes()) if rehash else digest
    config_path = tmp_path / 'release.json'
    config_path.write_text(json.dumps(config), encoding='utf-8')
    with pytest.raises(ValueError, match='native fleet selection|dependency changed'):
        apply_release(source, config_path)
