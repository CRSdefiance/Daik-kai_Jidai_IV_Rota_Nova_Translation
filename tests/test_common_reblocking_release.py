import copy
import hashlib
import json
from pathlib import Path

import pytest

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, common_message_entries
from dk4tool.script.common_reblocking_release import apply_common_reblocking
from scripts.audit_release_translation_integrity import build_report
from scripts.inventory_common_native_messages import inventory
from scripts.verify_common_native_items import verify as verify_items


@pytest.fixture(scope='module')
def release():
    rom = NdsImage.open('out/all_routes_combined_v119_candidate.nds')
    return rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')


def test_release_transform_reproduces_the_reviewed_map_and_locked_mapper(release):
    common, arm9, report = apply_common_reblocking(*release, Path('translations/common_native_reblocking_v120.json'))
    entries = common_message_entries(common, arm9, clean=False)
    assert len(entries) == 3668
    assert entries[1034].block == 13
    assert entries[1034].text.decode('cp932') == "Ｉ don't know whose fleet it is, but it's anchored at %s."
    assert report['all_unrelated_selected_text_unchanged']
    assert entries[469].text == b'?'
    assert len(report['authored_ids']) == 79


def test_clean_mode_and_unknown_directory_edits_still_fail(release):
    common, arm9, _ = apply_common_reblocking(*release, Path('translations/common_native_reblocking_v120.json'))
    with pytest.raises(ValueError, match='evidence mismatch'):
        common_message_entries(common, arm9, clean=True)
    bad = bytearray(arm9)
    bad[DIRECTORY_OFFSET + 12 * 4] ^= 1
    with pytest.raises(ValueError, match='evidence mismatch'):
        common_message_entries(common, bytes(bad), clean=False)


def test_release_transform_rejects_changed_parent_layers(release):
    common, arm9 = release
    corrupted = bytearray(common)
    corrupted[-1] ^= 1
    with pytest.raises(ValueError, match='parent layers differ'):
        apply_common_reblocking(bytes(corrupted), arm9, Path('translations/common_native_reblocking_v120.json'))


def test_release_transform_rejects_manuscript_hash_change(release, tmp_path):
    original = json.loads(Path('translations/common_native_reblocking_v120.json').read_text(encoding='utf-8'))
    config = copy.deepcopy(original)
    config['manuscripts'][0]['sha256'] = '0' * 64
    path = tmp_path / 'bad_config.json'
    path.write_text(json.dumps(config), encoding='utf-8')
    with pytest.raises(ValueError, match='manuscript hash differs'):
        apply_common_reblocking(*release, path)


def test_release_transform_rejects_incorrect_native_layout_even_with_updated_hash(release, tmp_path):
    config = json.loads(Path('translations/common_native_reblocking_v120.json').read_text(encoding='utf-8'))
    layout = json.loads(Path(config['layout_batch']).read_text(encoding='utf-8'))
    layout['records'][0]['entry_offsets'][0] += 1
    layout_path = tmp_path / 'bad_layout.json'
    layout_path.write_text(json.dumps(layout), encoding='utf-8')
    config['layout_batch'] = layout_path.as_posix()
    config['layout_batch_sha256'] = hashlib.sha256(layout_path.read_bytes()).hexdigest()
    path = tmp_path / 'bad_config.json'
    path.write_text(json.dumps(config), encoding='utf-8')
    with pytest.raises(ValueError, match='layout contradicts'):
        apply_common_reblocking(*release, path)


def test_saved_relocation_checks_every_item_and_all_visible_source_messages():
    candidate = Path('out/all_routes_combined_v120_candidate.nds')
    items = verify_items(candidate, 'all-routes-unified-v120', [29, 30, 31, 32])
    assert items['native_entry_count'] == 151
    assert items['relocated_complete_owners_verified']
    assert items['japanese_records_in_mapped_items'] == 0
    old = inventory(Path('out/all_routes_combined_v119_candidate.nds'), Path('work/clean.nds'))
    assert [e['message_id'] for e in old['blank_native_messages']] == [469]
    new = inventory(candidate, Path('work/clean.nds'))
    assert new['blank_native_message_count'] == 0
    assert new['leading_prefix_finding_count'] == 0
    integrity = build_report(candidate, Path('work/clean.nds'), 'all-routes-unified-v120')
    assert integrity['blocking_issue_count'] == 0
    assert integrity['common_native_relocation_layout_used']
    assert integrity['historical_common_coordinate_declarations_not_compared'] > 0
    assert integrity['audited_entry_count'] >= 3668
