import pytest

from dk4tool.rom.nds import NdsImage
from scripts.prepare_fleet_names_v148_research import prepare
from scripts.probe_fleet_name_display_callers import execute


@pytest.fixture(scope='module')
def inputs():
    source, _ = prepare()
    return source, NdsImage.open('work/clean.nds').read_file('/GRP/KANJI.FNT')


@pytest.mark.parametrize('kind', ['fixed', 'centered'])
@pytest.mark.parametrize(('index', 'name', 'expected'), [
    (82, '', 'Pirate Square Shopkeeper'),
    (61, '', 'Pirate ヴェルス'),
    (0, 'A' * 16, 'Pirate ' + 'A' * 16),
    (208, '', 'Unidentified fleet'),
])
def test_actual_captain_selection_and_name_getter_pixels(inputs, kind, index, name, expected):
    source, font = inputs
    result, _ = execute(source, kind, name, raster=True, kanji_font=font,
                        captain_index=index, current_character=0)
    assert result['complete_text'] == expected
    assert result['native_captain_selector_and_name_dispatch_verified']
    assert result['full_glyph_order_bounds_and_independent_pixels_verified']


def test_uninitialized_captain_index_not_counted(inputs):
    with pytest.raises(ValueError, match='initialized ordinary'):
        execute(inputs[0], 'fixed', '', captain_index=207)


def test_overlong_player_field_not_counted(inputs):
    with pytest.raises(ValueError, match='sixteen-byte'):
        execute(inputs[0], 'fixed', 'A' * 17, captain_index=0)
