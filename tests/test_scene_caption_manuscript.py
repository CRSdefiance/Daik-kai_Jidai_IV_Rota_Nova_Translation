import copy
import json
from pathlib import Path

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.plan_scene_caption_source_pool import inspect_pool
from scripts.prepare_scene_caption_manuscript import compile_manuscript


@pytest.fixture(scope='module')
def inputs():
    inventory = json.loads(Path('work/analysis/common_scene_caption_duplicates_v137.json').read_text(encoding='utf-8'))
    document = compile_manuscript(inventory)
    sources = [NdsImage.open(path).read_file('/__arm9__.bin') for path in (
        'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds',
        'out/all_routes_combined_v137_candidate.nds')]
    return inventory, document, sources


def test_complete_prose_is_kept_when_capacity_and_width_are_insufficient(inputs):
    _, document, sources = inputs
    plan = inspect_pool(document, *sources)
    assert len(document['records']) == 164
    assert all(row['review']['formatting'] is False for row in document['records'])
    assert plan['owned_capacity'] == 3232
    assert plan['complete_unique_english_bytes_with_nul'] == 3324
    assert plan['raw_capacity_deficit_before_external_sharing'] == 92
    assert plan['over_screen_width'] == [{'id': 'SCENE_CAPTION_ROUTE_3_35',
        'english': 'Maria and Her Companions at the Grand Review', 'width_pixels': 264}]
    assert len(plan['mapped_caption_pointer_fields']) == 163
    assert plan['additional_literal_pointer_fields_requiring_consumer_review'] == {}


def test_changed_japanese_cannot_receive_source_approval(inputs):
    inventory = copy.deepcopy(inputs[0])
    inventory['captions'][0]['japanese'] = '別の場面'
    with pytest.raises(ValueError, match='Japanese source or native ownership'):
        compile_manuscript(inventory)


def test_missing_caption_variant_is_rejected(inputs):
    inventory = copy.deepcopy(inputs[0])
    inventory['captions'].pop()
    with pytest.raises(ValueError, match='Complete unique caption scope'):
        compile_manuscript(inventory)


def test_unowned_source_padding_cannot_be_reclaimed(inputs):
    _, document, sources = inputs
    clean = bytearray(sources[0])
    row = document['records'][0]
    clean[row['source_offset'] + len(bytes.fromhex(row['source_hex'])) + 1] = 1
    with pytest.raises(ValueError, match='source/padding ownership'):
        inspect_pool(document, clean, *sources[1:])


def test_inherited_ironclad_keeps_its_complete_terminated_name(inputs):
    _, document, sources = inputs
    plan = inspect_pool(document, *sources)
    reserved = [row for row in plan['slots'] if row['reserved_inherited_name']]
    assert len(reserved) == 1
    assert reserved[0]['id'] == 'SCENE_CAPTION_ROUTE_1_24'
    assert not any(lo <= reserved[0]['start'] < hi for lo, hi in plan['owned_ranges'])
