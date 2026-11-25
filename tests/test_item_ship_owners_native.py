"""Native ship search/name consumers must retain complete names at bounds."""

import json
from pathlib import Path

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.verify_item_interface_research import verify_page


@pytest.fixture(scope='module')
def sources():
    image = NdsImage.open('out/all_routes_combined_v158_candidate.nds')
    return (Path('work/analysis/item_interface_cache_research_arm9.bin').read_bytes(),
            json.loads(Path('work/analysis/item_interface_plan.json').read_text(encoding='utf-8')),
            image.read_file('/GRP/KANJI.FNT'), image.read_file('/COMMON/MESFILE.DK4'))


@pytest.mark.parametrize('ship,name', [(50, None), (107, None), (153, None),
                                      (0, b'A'), (49, b'ABCDEFGHIJKLMNOPQR')])
def test_real_ship_initializer_search_name_and_field_boundaries(sources, ship, name):
    source, plan, font, common = sources
    result = verify_page(source, plan, 'main', (0, 3), font, 16, item_index=118,
                         common=common, ship_index=ship, ship_name=name)
    assert result['item_actual_owner_classifications'] == [[3, ship]]
    assert result['item_ship_owner_initialization']['native_fixed_source_names_checked'] == 104
    assert result['item_provider_contracts'] == ['item_art_provider_not_rendered']


def test_mutable_ship_name_overflow_is_rejected(sources):
    source, plan, font, common = sources
    with pytest.raises(ValueError, match='eighteen-byte editor capacity'):
        verify_page(source, plan, 'main', (0, 3), font, 16, item_index=118,
                    common=common, ship_index=0, ship_name=b'ABCDEFGHIJKLMNOPQRS')
