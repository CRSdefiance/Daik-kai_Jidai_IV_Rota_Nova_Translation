"""Reject lost reviews, incomplete native branches and stale movement evidence."""

import json
import struct
from pathlib import Path

import pytest

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.movement_notice_release import SHORTAGES, apply_release
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import (
    DIRECTORY_OFFSET,
    TABLE_OFFSET,
    common_message_entries,
)
from dk4tool.script.common_native_repack import repack_native_records
from scripts.execute_scene_caption_raster import execute
from scripts.probe_common_display_name_hook import branch_link
from scripts.verify_movement_notices_research import BASE, scope_case


@pytest.fixture(scope='module')
def sources():
    return NdsImage.open('out/all_routes_combined_v155_candidate.nds'), NdsImage.open('work/clean.nds')


def evidence_config(tmp_path, key, change, update_hash=True):
    config = json.loads(Path('translations/movement_notices_release_v1.json').read_text(encoding='utf-8'))
    evidence = json.loads(Path(config[key]).read_text(encoding='utf-8'))
    change(evidence)
    path = tmp_path / 'evidence.json'
    path.write_text(json.dumps(evidence), encoding='utf-8')
    config[key] = str(path)
    if update_hash:
        config[key + '_sha256'] = sha(path.read_bytes())
    path = tmp_path / 'config.json'
    path.write_text(json.dumps(config), encoding='utf-8')
    return path


def test_unreviewed_formatting_is_rejected(tmp_path, sources):
    config = evidence_config(tmp_path, 'manuscript', lambda p: p['records'][8]['review'].update({'formatting': False}))
    with pytest.raises(ValueError, match='per-record'):
        apply_release(*sources, config)


def test_changed_translation_is_rejected_with_updated_hash(tmp_path, sources):
    config = evidence_config(tmp_path, 'manuscript', lambda p: p['records'][5].update({'english': 'Nothing left.'}))
    with pytest.raises(ValueError, match='source/prose'):
        apply_release(*sources, config)


def test_missing_single_supply_branch_is_rejected(tmp_path, sources):
    config = evidence_config(tmp_path, 'native_proof', lambda p: p['native_preparation_cases'].pop())
    with pytest.raises(ValueError, match='coverage incomplete'):
        apply_release(*sources, config)


def test_stale_native_proof_is_rejected(tmp_path, sources):
    config = evidence_config(tmp_path, 'native_proof', lambda p: p.update({'paired_pixel_cases': []}), False)
    with pytest.raises(ValueError, match='evidence changed'):
        apply_release(*sources, config)


def packed_sources(image):
    common, arm9 = image.read_file('/COMMON/MESFILE.DK4'), image.read_file('/__arm9__.bin')
    entries = common_message_entries(common, arm9, clean=False)
    owners = {(entries[mid].block, entries[mid].record_index) for mid in SHORTAGES}
    blocks = IlnkContainer.parse(common).blocks
    prefixes = {owner: blocks[owner[0]].split(b'\0')[owner[1]][:next(e.start for e in entries if (e.block, e.record_index) == owner)]
                for owner in owners}
    return common, arm9, entries, prefixes


def test_unselected_padding_preserves_packed_neighbor_and_complete_prose(sources):
    common, arm9, entries, prefixes = packed_sources(sources[0])
    paragraphs = {mid: value[0].encode('ascii') for mid, value in SHORTAGES.items()}
    result = repack_native_records(common, arm9, paragraphs, prefixes,
                                   preserved_packed_neighbors={609: entries[609].text}, spare_padding_before_first_entry=True)
    assert result.entries[609].text == entries[609].text  # Includes original line breaks and its trailing space.
    assert all(result.entries[mid].text == text for mid, text in paragraphs.items())
    assert result.arm9[DIRECTORY_OFFSET:TABLE_OFFSET] == arm9[DIRECTORY_OFFSET:TABLE_OFFSET]
    old, new = IlnkContainer.parse(common).blocks, IlnkContainer.parse(result.common).blocks
    assert [(len(b), b.count(b'\0')) for b in old] == [(len(b), b.count(b'\0')) for b in new]
    assert all(before.text == after.text for before, after in zip(entries, result.entries, strict=True) if before.message_id not in SHORTAGES)


def test_preserved_neighbor_must_match_exact_bytes(sources):
    common, arm9, entries, prefixes = packed_sources(sources[0])
    with pytest.raises(ValueError, match='exact current'):
        repack_native_records(common, arm9, {mid: v[0].encode('ascii') for mid, v in SHORTAGES.items()}, prefixes,
                              preserved_packed_neighbors={609: entries[609].text.rstrip(b' ')})


def test_partial_packed_owner_is_rejected(sources):
    common, arm9, _entries, prefixes = packed_sources(sources[0])
    with pytest.raises(ValueError, match='every native entry'):
        repack_native_records(common, arm9, {mid: v[0].encode('ascii') for mid, v in SHORTAGES.items()}, prefixes)


def test_sailing_raster_rejects_inherited_tracking(sources):
    source = bytearray(Path('work/analysis/movement_notices_research_arm9.bin').read_bytes())
    struct.pack_into('<I', source, 0x6880C, branch_link(BASE + 0x6880C, BASE + 0xD5200))
    with pytest.raises(ValueError, match='sailing formatter'):
        execute(bytes(source), 'Auto Sail', sailing_status=True, surface_size=(256, 32),
                kanji_font=sources[0].read_file('/GRP/KANJI.FNT'))


def test_complete_template_guard_rejects_same_prefix(sources):
    source = Path('work/analysis/movement_notices_research_arm9.bin').read_bytes()
    scope_case(source, SHORTAGES[610][0] + 'x', BASE + 0x53DB8, BASE + 0x118580)
