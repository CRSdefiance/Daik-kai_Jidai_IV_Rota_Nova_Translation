import copy
import json

import pytest

from dk4tool.patch.golden_route_viewer_release import CONFIG, EVIDENCE, apply_release
from dk4tool.rom.nds import NdsImage
from scripts.approve_golden_route_viewer_formatting import approve
from scripts.prepare_golden_route_viewer import MANUSCRIPT


@pytest.fixture(scope='module')
def inputs():
    source = NdsImage.open('out/all_routes_combined_v138_candidate.nds').read_file('/__arm9__.bin')
    document = json.loads(MANUSCRIPT.read_text(encoding='utf-8'))
    evidence = json.loads(EVIDENCE.read_text(encoding='utf-8'))
    return source, document, evidence


def test_altered_parent_cannot_reuse_release(inputs):
    source = bytearray(inputs[0])
    source[0] ^= 1
    with pytest.raises(ValueError, match='V138 caption source'):
        apply_release(source, CONFIG)


@pytest.mark.parametrize('name', ['headings', 'footer', 'empty'])
def test_missing_native_coverage_cannot_approve_formatting(inputs, name):
    evidence = copy.deepcopy(inputs[2])
    evidence[name]['cases'].pop()
    with pytest.raises(ValueError):
        approve(inputs[1], evidence)


def test_nonzero_record_dispatch_to_empty_message_cannot_be_approved(inputs):
    evidence = copy.deepcopy(inputs[2])
    evidence['empty']['dispatches'][1]['empty_dialog_selected'] = True
    with pytest.raises(ValueError, match='dispatch coverage'):
        approve(inputs[1], evidence)


def test_failed_native_proof_cannot_be_approved(inputs):
    evidence = copy.deepcopy(inputs[2])
    evidence['footer']['status'] = 'failed'
    with pytest.raises(ValueError, match='did not pass'):
        approve(inputs[1], evidence)


def test_changed_manuscript_english_cannot_reuse_native_approval(inputs):
    document = copy.deepcopy(inputs[1])
    document['records'][0]['english'] = 'X' + document['records'][0]['english'][1:]
    with pytest.raises(ValueError, match='consumed labels'):
        approve(document, inputs[2])


def test_changed_evidence_dependency_is_rejected(inputs, tmp_path):
    config = json.loads(CONFIG.read_text())
    config['dependencies'][EVIDENCE.as_posix()] = '0' * 64
    path = tmp_path / 'bad-viewer-release.json'
    path.write_text(json.dumps(config))
    with pytest.raises(ValueError, match='evidence changed'):
        apply_release(inputs[0], path)
