import copy
import json
from pathlib import Path

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.prepare_grand_race_complete_ui_review import DRAFT, review


@pytest.fixture
def inputs():
    return (json.loads(DRAFT.read_text(encoding='utf-8')),
            NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'),
            json.loads(Path('work/analysis/grand_race_ui_coverage_v136.json').read_text()),
            json.loads(Path('work/analysis/grand_race_ui_allocation_v136/report.json').read_text()))


def test_conditional_rows_keep_formatting_gate_closed(inputs):
    result = review(*inputs)
    assert result['reviewed_record_counts'] == {'source_context_localization_naturalness': 51,
                                               'native_text_formatting': 43, 'formatting_pending': 8}
    for row in result['records']:
        assert row['english'] == next(r['english'] for r in inputs[0]['records'] if r['id'] == row['id'])
        assert row['review']['formatting'] == (row['id'] not in result['pending_formatting_records'])


def test_missing_context_evidence_rejected(inputs):
    draft, clean, coverage, allocation = inputs
    coverage = copy.deepcopy(coverage)
    coverage['records'][0]['consumer_evidence'] = []
    with pytest.raises(ValueError, match='mapped consumer evidence'):
        review(draft, clean, coverage, allocation)


def test_different_source_record_rejected(inputs):
    draft, clean, coverage, allocation = inputs
    draft = copy.deepcopy(draft)
    draft['records'][0]['source_parts_in_reading_order'][0]['offset'] += 1
    with pytest.raises(ValueError, match='Japanese or padding differs'):
        review(draft, clean, coverage, allocation)


def test_shortened_allocated_prose_rejected(inputs):
    draft, clean, coverage, allocation = inputs
    allocation = copy.deepcopy(allocation)
    row = allocation['selections'][0]
    row['line'] = row['line'][1:]
    row['raw_hex'] = (row['line'].encode('ascii') + b'\0').hex()
    with pytest.raises(ValueError, match='Complete prose'):
        review(draft, clean, coverage, allocation)
