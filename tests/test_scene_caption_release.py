import copy
import json

import pytest

from dk4tool.patch.scene_caption_release import (
    CONFIG,
    EVIDENCE,
    MANUSCRIPT,
    apply_release,
    compile_release,
)
from dk4tool.rom.nds import NdsImage
from scripts.approve_scene_caption_formatting import approve


@pytest.fixture(scope='module')
def inputs():
    source = NdsImage.open('out/all_routes_combined_v137_candidate.nds').read_file('/__arm9__.bin')
    document = json.loads(MANUSCRIPT.read_text(encoding='utf-8'))
    evidence = json.loads(EVIDENCE.read_text(encoding='utf-8'))
    return source, document, evidence


def test_changed_post_common_parent_is_rejected(inputs):
    source = bytearray(inputs[0])
    source[0] ^= 1
    with pytest.raises(ValueError, match='complete V137'):
        compile_release(source, *inputs[1:])


def test_missing_editorial_gate_is_rejected(inputs):
    document = copy.deepcopy(inputs[1])
    document['records'][0]['review']['formatting'] = False
    with pytest.raises(ValueError, match='gates'):
        compile_release(inputs[0], document, inputs[2])


@pytest.mark.parametrize('kind', ['missing-case', 'cleanup', 'pixels'])
def test_native_formatting_approval_rejects_incomplete_evidence(inputs, kind):
    evidence = copy.deepcopy(inputs[2])
    if kind == 'missing-case':
        evidence['wrappers']['cases'].pop()
    elif kind == 'cleanup':
        evidence['wrappers']['cases'][0]['native_cleanup_executed'] = False
    else:
        evidence['wrappers']['cases'][0]['pixels_sha256'] = '0' * 64
    with pytest.raises(ValueError):
        approve(inputs[1], evidence['raster'], evidence['wrappers'])


def test_same_length_english_mutation_cannot_reuse_native_approval(inputs):
    document = copy.deepcopy(inputs[1])
    document['records'][0]['english'] = 'X' + document['records'][0]['english'][1:]
    with pytest.raises(ValueError, match='target is not reproduced'):
        compile_release(inputs[0], document, inputs[2])


def test_dependency_hash_changes_rejected(inputs, tmp_path):
    config = json.loads(CONFIG.read_text())
    config['dependencies'][EVIDENCE.as_posix()] = '0' * 64
    path = tmp_path / 'bad-caption-release.json'
    path.write_text(json.dumps(config))
    with pytest.raises(ValueError, match='evidence changed'):
        apply_release(inputs[0], path)
