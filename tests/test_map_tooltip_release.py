import copy
import json

import pytest

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.map_tooltip_release import CONFIG, EVIDENCE, MANUSCRIPTS, apply_release
from dk4tool.rom.nds import NdsImage
from scripts.approve_map_tooltip_formatting import TARGET_SHA, approve


@pytest.fixture(scope='module')
def inputs():
    source = NdsImage.open('out/all_routes_combined_v139_candidate.nds').read_file('/__arm9__.bin')
    documents = [json.loads(path.read_text(encoding='utf-8')) for path in MANUSCRIPTS]
    evidence = json.loads(EVIDENCE.read_text(encoding='utf-8'))
    return source, documents, evidence


def test_strict_release_reproduces_exact_verified_target(inputs):
    proposed, report = apply_release(inputs[0], CONFIG)
    assert sha(proposed) == TARGET_SHA
    assert report['message_count'] == 9
    assert report['inherited_caption_count'] == 164
    assert not report['runtime_verified']


def test_changed_parent_rejects(inputs):
    source = bytearray(inputs[0])
    source[0] ^= 1
    with pytest.raises(ValueError, match='V139 parent'):
        apply_release(source, CONFIG)


@pytest.mark.parametrize('name,field', [('complete', 'tooltip_cases'), ('factions', 'fixed_name_rasters'),
                                      ('numeric', 'percentage_cases'), ('player', 'cases'), ('pixels', 'cases')])
def test_missing_native_coverage_rejects(inputs, name, field):
    evidence = copy.deepcopy(inputs[2])
    evidence[name][field].pop()
    with pytest.raises(ValueError):
        approve(inputs[1], evidence)


def test_dropped_leading_class_cannot_reuse_approval(inputs):
    evidence = copy.deepcopy(inputs[2])
    evidence['complete']['tooltip_cases'][0]['second_row_first_glyph_x'] = 0
    with pytest.raises(ValueError, match='leading glyph'):
        approve(inputs[1], evidence)


def test_changed_english_cannot_reuse_native_evidence(inputs):
    documents = copy.deepcopy(inputs[1])
    documents[1]['records'][0]['english'] = 'Fish'
    with pytest.raises(ValueError, match='consumed wording'):
        approve(documents, inputs[2])


def test_failed_real_itcm_pixels_cannot_reuse_approval(inputs):
    evidence = copy.deepcopy(inputs[2])
    evidence['pixels']['cases'][0]['independent_full_buffer_pixels_match'] = False
    with pytest.raises(ValueError, match='ITCM pixel'):
        approve(inputs[1], evidence)


def test_changed_evidence_dependency_rejects(inputs, tmp_path):
    config = json.loads(CONFIG.read_text())
    config['dependencies'][EVIDENCE.as_posix()] = '0' * 64
    path = tmp_path / 'invalid.json'
    path.write_text(json.dumps(config))
    with pytest.raises(ValueError, match='evidence changed'):
        apply_release(inputs[0], path)
