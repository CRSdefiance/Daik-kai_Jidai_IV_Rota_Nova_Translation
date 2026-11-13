"""Reject unreviewed prose, stale evidence and altered village dependencies."""

import json
from pathlib import Path

import pytest

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.village_promised_words_release import apply_release
from dk4tool.rom.nds import NdsImage


@pytest.fixture(scope='module')
def sources():
    return (NdsImage.open('out/all_routes_combined_v154_candidate.nds'),
            NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'))


def evidence_config(tmp_path, key, change, update_hash):
    config = json.loads(Path('translations/village_promised_words_release_v1.json').read_text(encoding='utf-8'))
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


def test_unreviewed_record_is_rejected_even_with_new_hash(tmp_path, sources):
    config = evidence_config(tmp_path, 'manuscript',
                             lambda p: p['records'][0]['review'].update({'formatting': False}), True)
    with pytest.raises(ValueError, match='per-record'):
        apply_release(*sources, config)


def test_changed_prose_is_rejected_even_with_new_hash(tmp_path, sources):
    config = evidence_config(tmp_path, 'manuscript',
                             lambda p: p['records'][0].update({'english': 'Different answer'}), True)
    with pytest.raises(ValueError, match='compiled-text'):
        apply_release(*sources, config)


def test_incomplete_keyboard_coverage_is_rejected(tmp_path, sources):
    config = evidence_config(tmp_path, 'keyboard_proof', lambda p: p['complete_answer_cases'].pop(), True)
    with pytest.raises(ValueError, match='coverage incomplete'):
        apply_release(*sources, config)


def test_stale_pixel_evidence_is_rejected(tmp_path, sources):
    config = evidence_config(tmp_path, 'title_proof', lambda p: p.update({'cases': []}), False)
    with pytest.raises(ValueError, match='evidence changed'):
        apply_release(*sources, config)
