import copy
import json
import struct
from pathlib import Path

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.compile_scene_caption_allocation import (
    BRANCH,
    POOL_END,
    POOL_START,
    compile_allocation,
)
from scripts.compile_scene_caption_tracking import compile_tracking
from scripts.execute_scene_caption_selection import execute


@pytest.fixture(scope='module')
def inputs():
    document = json.loads(Path('translations/scene_caption_manuscript_v2.json').read_text(encoding='utf-8'))
    sources = [NdsImage.open(path).read_file('/__arm9__.bin') for path in (
        'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds',
        'out/all_routes_combined_v137_candidate.nds')]
    allocation, report = compile_allocation(document, *sources)
    tracking, proof = compile_tracking(allocation, document)
    return document, sources, allocation, report, tracking, proof


def test_complete_allocation_preserves_widgets_and_all_text(inputs):
    _, _, _, report, _, proof = inputs
    assert report['caption_count'] == len(report['complete_selections']) == 164
    assert sum(hi - lo for lo, hi in report['unused_ranges']) == 2
    assert report['retired_Ironclad_source_slot_unchanged']
    assert report['waiting_widget_before']['steps'] - report['waiting_widget_after']['steps'] == 16
    assert proof['case_count'] == 164 and proof['max_width'] == 220
    assert all(case['right_edge'] <= 256 for case in proof['cases'])
    assert proof['font_sixth_column_empty_for_all_caption_characters']


@pytest.mark.parametrize('clear', [0, 1])
def test_original_mode_one_wrapper_keeps_ink_context_and_clear_behavior(inputs, clear):
    _, sources, _, _, tracking, _ = inputs
    before = execute(sources[2], 0x115A04, 24, 41, wrapper_only=True, clear=clear)
    after = execute(tracking, 0x115A04, 24, 41, wrapper_only=True, clear=clear)
    for key in ('pointer', 'full_text_hex', 'x', 'y', 'style', 'tracking', 'clear_calls', 'stack_and_registers_preserved'):
        assert before[key] == after[key]


def test_data_island_with_a_literal_pointer_consumer_is_rejected(inputs):
    document, sources, *_ = inputs
    current = bytearray(sources[2])
    struct.pack_into('<I', current, 0x100, 0x02000000 + POOL_START)
    with pytest.raises(ValueError, match='another literal pointer consumer'):
        compile_allocation(document, *sources[:2], current)


def test_data_island_with_direct_branch_entrance_is_rejected(inputs):
    document, sources, *_ = inputs
    current = bytearray(sources[2])
    displacement = (POOL_START - 0x100 - 8) // 4
    struct.pack_into('<I', current, 0x100, 0xEA000000 | displacement)
    with pytest.raises(ValueError, match='direct branch entrance'):
        compile_allocation(document, *sources[:2], current)


def test_initializer_setup_cannot_be_reclaimed_as_data(inputs):
    document, sources, *_ = inputs
    current = bytearray(sources[2])
    struct.pack_into('<I', current, BRANCH, 0xE3A00001)
    with pytest.raises(ValueError, match='exact redundant initializer NOPs'):
        compile_allocation(document, *sources[:2], current)


def test_missing_complete_caption_is_rejected(inputs):
    document, sources, *_ = inputs
    changed = copy.deepcopy(document)
    changed['records'].pop()
    with pytest.raises(ValueError, match='Every complete caption'):
        compile_allocation(changed, *sources)


def test_tracking_proposal_keeps_branch_over_the_entire_text_island(inputs):
    tracking = inputs[4]
    instruction = struct.unpack_from('<I', tracking, BRANCH)[0]
    assert BRANCH + 8 + (instruction & 0xFFFFFF) * 4 == POOL_END
