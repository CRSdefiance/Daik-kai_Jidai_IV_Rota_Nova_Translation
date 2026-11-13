"""Item integration rejects missing text reviews, clipped rows and stale evidence."""

import json
from pathlib import Path

import pytest

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.item_interface_release import TARGET, apply_release
from dk4tool.rom.nds import NdsImage


@pytest.fixture(scope='module')
def sources():
    return NdsImage.open('out/all_routes_combined_v158_candidate.nds'), NdsImage.open('work/clean.nds')


def evidence_config(tmp_path, key, change, lock=True):
    config = json.loads(Path('translations/item_interface_release_v1.json').read_text(encoding='utf-8'))
    evidence = json.loads(Path(config[key]).read_text(encoding='utf-8'))
    change(evidence)
    path = tmp_path / 'evidence.json'
    path.write_text(json.dumps(evidence), encoding='utf-8')
    config[key] = str(path)
    if lock:
        config[key + '_sha256'] = sha(path.read_bytes())
    path = tmp_path / 'config.json'
    path.write_text(json.dumps(config), encoding='utf-8')
    return path


def test_full_source_locked_item_release(sources):
    data, report = apply_release(*sources, 'translations/item_interface_release_v1.json')
    assert sha(data) == TARGET
    assert report['visible_localized_logical_records'] == 34
    assert report['nonvisible_source_references'] == ['ITEM_USE']
    assert not report['physical_gameplay_verified']


def test_missing_visible_review_is_rejected(tmp_path, sources):
    config = evidence_config(tmp_path, 'manuscript', lambda p: p['records'][0]['review'].update(formatting=False))
    with pytest.raises(ValueError, match='per-record'):
        apply_release(*sources, config)


def test_changed_first_label_letter_is_rejected(tmp_path, sources):
    config = evidence_config(tmp_path, 'manuscript', lambda p: p['records'][0].update(english='tems Acquired %d/%d'))
    with pytest.raises(ValueError, match='source/prose/compiled'):
        apply_release(*sources, config)


@pytest.mark.parametrize(('key', 'change', 'message'), (
    ('generated_proof', lambda p: p['generated_rasters'].pop(), 'coverage incomplete'),
    ('generated_proof', lambda p: p['parent']['requests'][2].update(destination_origin=[56, 40]), 'parent crops'),
    ('generated_proof', lambda p: p['boot']['late_copy_cache_model'].update(
        worst_case_dirty_data_and_stale_instruction_model_visible=False), 'startup/cache'),
    ('role_proof', lambda p: p['cases'].pop(), 'Role eligibility'),
    ('role_proof', lambda p: p['cases'][2].update(owner_name_color=1), 'Role eligibility'),
    ('inherited_proof', lambda p: p['shared_name_owners'].pop(), 'Inherited native'),
    ('role_proof', lambda p: p['visual_review'].update(complete=False), 'visual review'),
    ('generated_proof', lambda p: p['verification_script_snapshot_sha256'].update(
        {'scripts/execute_scene_caption_raster.py': '0' * 64}), 'verification script changed'),
))
def test_incomplete_or_incorrect_evidence_is_rejected(tmp_path, sources, key, change, message):
    config = evidence_config(tmp_path, key, change)
    with pytest.raises(ValueError, match=message):
        apply_release(*sources, config)


def test_unlocked_evidence_change_is_rejected(tmp_path, sources):
    config = evidence_config(tmp_path, 'role_proof', lambda p: p.update(cases=[]), lock=False)
    with pytest.raises(ValueError, match='evidence changed'):
        apply_release(*sources, config)
