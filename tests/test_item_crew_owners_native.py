"""Ownership/name getters must execute and retain leading characters at bounds."""

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


@pytest.mark.parametrize('item,crew,mutable', [(24, 0, None), (49, 206, None),
                                             (24, 206, b'A'), (24, 0, b'ABCDEFGHIJKLMNOPQR')])
def test_real_crew_search_and_name_boundaries(sources, item, crew, mutable):
    source, plan, font, common = sources
    result = verify_page(source, plan, 'main', (0, 2), font, 16, item_index=item,
                         common=common, crew_index=crew, player_name=mutable)
    assert result['item_actual_owner_classifications'] == [[2, crew]]
    assert result['item_provider_contracts'] == ['item_art_provider_not_rendered']


def test_mutable_owner_name_exceeding_editor_limit_is_rejected(sources):
    source, plan, font, common = sources
    with pytest.raises(ValueError, match='eighteen-byte editor capacity'):
        verify_page(source, plan, 'main', (0, 2), font, 16, item_index=24,
                    common=common, crew_index=0, player_name=b'ABCDEFGHIJKLMNOPQRS')
