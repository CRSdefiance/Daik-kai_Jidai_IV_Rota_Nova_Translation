"""Reject missing Gallery review, captain cases and incomplete primary crops."""

import json
from pathlib import Path

import pytest

from dk4tool.patch.gallery_description_release import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage


@pytest.fixture(scope='module')
def sources():
    return NdsImage.open('out/all_routes_combined_v157_candidate.nds'), NdsImage.open('work/clean.nds')


def evidence_config(tmp_path, key, change, update_hash=True):
    config = json.loads(Path('translations/gallery_description_release_v1.json').read_text(encoding='utf-8'))
    evidence = json.loads(Path(config[key]).read_text(encoding='utf-8'))
    change(evidence)
    path = tmp_path / 'evidence.json'
    path.write_text(json.dumps(evidence), encoding='utf-8')
    config[key] = str(path)
    if update_hash:
        config[key + '_sha256'] = sha(path.read_bytes())
    path = tmp_path / 'config.json'
    path.write_text(json.dumps(config), encoding='utf-8')
    return path


def test_missing_formatting_review_is_rejected(tmp_path, sources):
    config = evidence_config(tmp_path, 'manuscript', lambda p: p['records'][0]['review'].update({'formatting': False}))
    with pytest.raises(ValueError, match='per-record'):
        apply_release(*sources, config)


def test_missing_captain_pixel_case_is_rejected(tmp_path, sources):
    config = evidence_config(tmp_path, 'native_proof', lambda p: p['native_pixel_cases'].pop(8))
    with pytest.raises(ValueError, match='coverage incomplete'):
        apply_release(*sources, config)


def test_cropped_primary_canvas_is_rejected_with_updated_hash(tmp_path, sources):
    config = evidence_config(tmp_path, 'native_proof',
                             lambda p: p['native_parent_composition']['draw_requests'][0].update({'size': [128, 192]}))
    with pytest.raises(ValueError, match='complete primary composition'):
        apply_release(*sources, config)


def test_unlocked_evidence_change_is_rejected(tmp_path, sources):
    config = evidence_config(tmp_path, 'native_proof', lambda p: p.update({'native_pixel_cases': []}), False)
    with pytest.raises(ValueError, match='evidence changed'):
        apply_release(*sources, config)
