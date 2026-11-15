import copy
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
from threading import Barrier

import pytest

from historical_fixture_support import historical_rom, load_recipe, materialize, reconstruct
import historical_fixture_support as support
from scripts.build_integrated_release import load_release_stack, resolve_release_batches

NAME = 'all_routes_combined_v117_candidate'


def test_archival_input_matches_original_manifest_without_a_release_filename():
    path = historical_rom(NAME)
    _,recipe = load_recipe(NAME)
    assert path.suffix == '.romfixture'
    assert hashlib.sha256(path.read_bytes()).hexdigest() == recipe['expected_ROM_sha256']
    manifest = json.loads(Path(recipe['original_manifest']).read_text())
    assert recipe['expected_ROM_sha256'] == manifest['candidate_sha256']
    assert recipe['historical_profile_status'] == 'revoked'


def test_changed_cached_input_is_rejected(tmp_path):
    _,recipe = load_recipe(NAME)
    (support.cache_location(tmp_path)/(recipe['expected_ROM_sha256']+'.romfixture')).write_bytes(b'altered historical bytes')
    with pytest.raises(ValueError,match='cache hash differs'):
        materialize(NAME,tmp_path)


@pytest.mark.parametrize('name',['hodram_deep_route_v32_candidate','raphael_deep_route_v93_candidate'])
def test_early_route_fixture_preserves_original_arm9_record_scope_and_rom_hash(name):
    document,recipe = load_recipe(name)
    manifest = json.loads((support.ROOT/recipe['original_manifest']).read_text())
    arm9_ids = []
    for batch in recipe['batches']:
        header = json.loads((support.ROOT/batch).read_text(encoding='utf-8'))
        if header['file_path'] == '/__arm9__.bin':
            arm9_ids.extend(row['id'] for row in header['records'])
    assert sorted(arm9_ids) == sorted(manifest['changed_records']['/__arm9__.bin'])
    assert hashlib.sha256(historical_rom(name).read_bytes()).hexdigest() == manifest['candidate_sha256']


def test_unknown_historical_identity_is_rejected():
    with pytest.raises(ValueError,match='explicit original identity'):
        load_recipe('unregistered-current-ROM-substitution')


def test_changed_canonical_input_is_rejected():
    document,recipe = load_recipe(NAME)
    recipe = dict(recipe,base_sha256='0'*64)
    with pytest.raises(ValueError,match='canonical source hash differs'):
        reconstruct(document,recipe)


def test_changed_historical_batch_lock_is_rejected():
    document,recipe = load_recipe(NAME)
    document = copy.deepcopy(document)
    document['input_sha256'][recipe['batches'][0]] = '0'*64
    with pytest.raises(ValueError,match='batch hash differs'):
        reconstruct(document,recipe)


def test_concurrent_materialization_publishes_only_complete_verified_bytes(tmp_path,monkeypatch):
    payload = b'isolated cache publication test'*10000
    recipe = dict(expected_ROM_sha256=hashlib.sha256(payload).hexdigest(),
        original_manifest='synthetic-test',original_manifest_sha256='synthetic-test',
        historical_profile_status='test-only')
    barrier = Barrier(2)
    def prepared(_document,_recipe):
        barrier.wait(timeout=10)
        return payload
    monkeypatch.setattr(support,'load_recipe',lambda _name:({},recipe))
    monkeypatch.setattr(support,'reconstruct',prepared)
    with ThreadPoolExecutor(max_workers=2) as workers:
        paths = list(workers.map(lambda _: materialize('synthetic',tmp_path),range(2)))
    assert paths[0] == paths[1]
    assert paths[0].read_bytes() == payload
    assert not list(support.cache_location(tmp_path).glob('*.partial'))


@pytest.mark.parametrize('profile',[f'all-routes-unified-v{version}' for version in (117,119,120,122,128,134)])
def test_archival_fixture_does_not_allow_revoked_playable_profile(profile):
    stack = load_release_stack()
    assert stack['profiles'][profile]['status'] == 'revoked'
    with pytest.raises(ValueError,match='revoked and cannot be built'):
        resolve_release_batches(profile,[],stack)
