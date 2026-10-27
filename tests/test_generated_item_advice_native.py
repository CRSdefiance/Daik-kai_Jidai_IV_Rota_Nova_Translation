"""Generated maps retain complete names and one terminated description."""

import json
from pathlib import Path

import pytest
from ndspy.code import MainCodeFile

from dk4tool.rom.nds import NdsImage
from scripts.execute_scene_caption_raster import execute
from scripts.probe_item_parent_crops import verify as parent_crops
from scripts.probe_promotional_item_full import verify as full_promotional
from scripts.verify_item_interface_research import verify_page
from scripts.verify_item_parent_layout import compose


@pytest.fixture(scope='module')
def resources():
    image = NdsImage.open('out/all_routes_combined_v158_candidate.nds')
    return (Path('work/analysis/generated_item_advice_research_arm9.bin').read_bytes(),
            json.loads(Path('work/analysis/generated_item_advice_plan.json').read_text(encoding='utf-8')),
            image.read_file('/GRP/KANJI.FNT'), image.read_file('/COMMON/MESFILE.DK4'))


@pytest.mark.parametrize('seed', (0, 0xFFFFFFFF))
def test_full_initializer_complete_names_terminators_metadata_and_return(resources, seed):
    source, _, _, _ = resources
    result = full_promotional(source, seed)
    assert len(result['names']) == 30
    assert len(set(result['selected_default_indices'])) == 5
    assert max(r['name_byte_length'] for r in result['names']) <= 31
    assert result['native_callee_saved_registers_and_stack_preserved']


@pytest.mark.parametrize(('index', 'page', 'mode'), ((198, 'main', 4), (217, 'main', 16),
                                                  (198, 'standalone', 16), (217, 'standalone', 4)))
def test_native_generated_maps_whole_name_description_and_parent_pixels(resources, index, page, mode):
    source, plan, font, common = resources
    result = verify_page(source, plan, page, (0, 4 if page == 'main' else 1), font, mode,
                         item_index=index, common=common)
    assert result['item_draws'][-1]['text'] == 'Map fragment. Collect all four.'
    assert result['item_draws'][-1]['y'] == (36 if page == 'main' else 24)
    assert result['item_native_object_metadata_initialization']['index'] == index
    if page == 'main':
        _, cells = compose(result, parent_crops(source)['requests'])
        assert len(cells) == len(result['glyph_events'])


def test_prior_single_string_fallback_reads_extra_continuations(resources):
    _, _, font, common = resources
    old = Path('work/analysis/item_parent_layout_research_arm9.bin').read_bytes()
    result = execute(old, 'fixture', item_page='main', item_case=(0, 4), surface_size=(240, 96),
                     kanji_font=font, item_resource_index=198, item_common=common)
    body = [r for r in result['item_draws'] if 36 <= r['y'] < 84]
    assert len(body) > 1
    assert any(ord(c) > 126 for r in body for c in r['text'])


def test_missing_first_generated_description_letter_is_rejected(resources):
    source, plan, font, common = resources
    code = MainCodeFile(source, 0x02000000)
    pointer = plan['item_advice_projection'][198]['pointer']
    code.sections[3].data[pointer - 0x02387A20] = 32
    with pytest.raises(ValueError, match='complete prose'):
        verify_page(bytes(code.save()), plan, 'main', (0, 4), font, 16, item_index=198, common=common)
