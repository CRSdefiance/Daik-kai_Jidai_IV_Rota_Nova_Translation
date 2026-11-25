"""Local item raster success must not hide parent clipping of full English rows."""

from pathlib import Path

from dk4tool.patch.item_parent_layout_research import transform
from scripts.probe_item_parent_crops import verify
from scripts.verify_item_parent_layout import EXPECTED


def test_original_item_parent_full_rows_exceed_native_screen():
    result = verify(Path('work/analysis/item_interface_cache_research_arm9.bin').read_bytes())
    assert not result['destination_256x192_fit_at_native_zero_origin']
    assert result['requests'][2]['destination_origin'][0] + result['requests'][2]['size'][0] == 296


def test_four_position_fields_fix_native_parent_without_changing_source_crops_or_code():
    old = Path('work/analysis/item_interface_cache_research_arm9.bin').read_bytes()
    source, plan = transform(old)
    result = verify(source)
    assert result['destination_256x192_fit_at_native_zero_origin']
    assert [(r['source_origin'], r['size'], r['destination_origin']) for r in result['requests']] == EXPECTED
    assert len(plan['fields']) == 4 and plan['changed_byte_count'] == 4
