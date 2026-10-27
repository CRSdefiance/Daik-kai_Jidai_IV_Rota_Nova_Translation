import copy
import json
import struct
from pathlib import Path

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.compile_grand_race_complete_ui_proposal import compile_ui
from scripts.plan_grand_race_ui_allocation_v136 import CANDIDATE


@pytest.fixture
def inputs():
    return (NdsImage.open(CANDIDATE).read_file('/__arm9__.bin'),
            json.loads(Path('work/analysis/grand_race_ui_allocation_v136/report.json').read_text()),
            json.loads(Path('translations/grand_race_remaining_ui_manuscript_v2.json').read_text(encoding='utf-8')))


def test_complete_combined_proposal(inputs):
    source, allocation, manuscript = inputs
    proposed, report = compile_ui(source, allocation, manuscript)
    assert report['message_count'] == 51
    assert report['saved_string_count'] == 60
    assert len(report['name_append_cases']) == 34
    assert report['waiting_widget_execution']['stack_balanced']
    assert struct.unpack_from('<I', proposed, 0x12ED04)[0] == 180
    for lo, hi in allocation['inherited_reserved_spans']:
        assert proposed[lo:hi] == source[lo:hi]


def test_dropped_leading_character_cannot_compile(inputs):
    source, allocation, manuscript = inputs
    allocation = copy.deepcopy(allocation)
    row = allocation['selections'][0]
    row['line'] = row['line'][1:]
    row['raw_hex'] = (row['line'].encode('ascii') + b'\0').hex()
    with pytest.raises(ValueError, match='prose was shortened'):
        compile_ui(source, allocation, manuscript)


def test_unowned_text_destination_cannot_compile(inputs):
    source, allocation, manuscript = inputs
    allocation = copy.deepcopy(allocation)
    allocation['selections'][0]['offset'] = 0x100
    with pytest.raises(ValueError, match='outside unchanged source'):
        compile_ui(source, allocation, manuscript)


def test_missing_message_cannot_compile(inputs):
    source, allocation, manuscript = inputs
    manuscript = copy.deepcopy(manuscript)
    manuscript['records'].pop()
    with pytest.raises(ValueError, match='Full scoped text'):
        compile_ui(source, allocation, manuscript)


def test_arbitrary_pointer_field_cannot_compile(inputs):
    source, allocation, manuscript = inputs
    allocation = copy.deepcopy(allocation)
    allocation['selections'][0]['pointer_fields'].append(0x100)
    with pytest.raises(ValueError, match='original mapped consumer'):
        compile_ui(source, allocation, manuscript)
