import copy
import json

import pytest

from scripts.approve_grand_race_result_formatting import MANUSCRIPT, PROOFS, approve


@pytest.fixture
def inputs():
    return (json.loads(MANUSCRIPT.read_text(encoding='utf-8')),
            {key: json.loads(path.read_text()) for key, path in PROOFS.items()})


def test_all_native_reviews_preserve_runtime_limit(inputs):
    result = approve(*inputs)
    assert result['reviewed_record_counts']['native_text_formatting'] == 51
    assert result['pending_formatting_records'] == []
    assert all(all(row['review'].values()) for row in result['records'])
    assert any('cold-boot' in blocker for blocker in result['integration_blockers'])
    assert result['status'].endswith('runtime-pending')


def test_incomplete_frame_cases_rejected(inputs):
    document, proofs = inputs
    proofs = copy.deepcopy(proofs)
    proofs['frame']['cases'].pop()
    with pytest.raises(ValueError, match='Complete native printf/frame'):
        approve(document, proofs)


def test_other_unreviewed_text_cannot_be_marked_complete(inputs):
    document, proofs = inputs
    document = copy.deepcopy(document)
    next(row for row in document['records'] if row['id'].endswith('_ROLES'))['review']['formatting'] = False
    with pytest.raises(ValueError, match='All fifty-one reviewed'):
        approve(document, proofs)
