import copy
import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.execute_golden_route_heading import execute
from scripts.prepare_golden_route_viewer import compile_allocation, compile_manuscript


@pytest.fixture(scope='module')
def inputs():
    sources = [NdsImage.open(path).read_file('/__arm9__.bin') for path in (
        'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds',
        'out/all_routes_combined_v138_candidate.nds')]
    document = compile_manuscript(*sources)
    proposal, report = compile_allocation(document, sources[-1])
    return sources, document, proposal, report


def test_all_six_complete_labels_fit_with_shared_accepted_strings(inputs):
    _, document, proposal, report = inputs
    assert len(document['records']) == 6
    assert report['owned_bytes'] == 88 and report['unused_bytes'] == 13
    assert report['code_changed'] is False
    assert all(row['review']['formatting'] is False for row in document['records'])
    for selection in report['selections']:
        pointer = struct.unpack_from('<I', proposal, selection['pointer_field'])[0]
        assert pointer == 0x02000000 + selection['offset']
        start = selection['offset']
        assert proposal[start:proposal.index(0, start)] == selection['english'].encode('ascii')


@pytest.mark.parametrize('selection,english,x', [(0, 'Golden Route Found!', 71),
                                                (1, 'Golden Route Records', 68)])
def test_actual_title_lookup_strlen_and_printf_keep_full_text(inputs, selection, english, x):
    result = execute(inputs[2], selection)
    assert bytes.fromhex(result['full_text_hex']) == english.encode('ascii') + b'\0'
    assert result['x'] == x and result['y'] == 12
    assert result['native_strlen_printf_executed']


def test_unowned_padding_is_rejected(inputs):
    clean = bytearray(inputs[0][0])
    clean[0x16A1A7] = 1
    with pytest.raises(ValueError, match='padding ownership'):
        compile_manuscript(clean, *inputs[0][1:])


def test_changed_canonical_shared_english_is_rejected(inputs):
    canonical = bytearray(inputs[0][1])
    canonical[0x11B53C] = ord('X')
    with pytest.raises(ValueError, match='shared English'):
        compile_manuscript(inputs[0][0], canonical, inputs[0][2])


def test_missing_label_or_changed_consumer_scope_is_rejected(inputs):
    document = copy.deepcopy(inputs[1])
    document['records'].pop()
    with pytest.raises(ValueError):
        compile_allocation(document, inputs[0][-1])
    document = copy.deepcopy(inputs[1])
    document['records'][0]['pointer_field'] += 4
    with pytest.raises(ValueError, match='consumer scope'):
        compile_allocation(document, inputs[0][-1])


@pytest.mark.parametrize('english', ['Bad\nlabel', '%s', ' Label'])
def test_unreviewed_control_or_format_string_is_rejected(inputs, english):
    document = copy.deepcopy(inputs[1])
    document['records'][0]['english'] = english
    with pytest.raises(ValueError, match='literal English'):
        compile_allocation(document, inputs[0][-1])
