import json
from pathlib import Path

import pytest

from dk4tool.patch import common_blizzard_release as release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries


@pytest.fixture(scope='module')
def source():
    rom = NdsImage.open('out/all_routes_combined_v140_candidate.nds')
    return rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')


def config_copy(tmp_path):
    value = json.loads(Path('translations/common_blizzard_release_v1.json').read_text(encoding='utf-8'))
    path = tmp_path / 'config.json'
    path.write_text(json.dumps(value), encoding='utf-8')
    return path, value


def test_repair_preserves_every_other_selection_and_non_table_arm9_byte(source, tmp_path):
    path, _ = config_copy(tmp_path)
    common, arm9, report = release.apply_release(*source, path)
    before = common_message_entries(*source, clean=False)
    after = common_message_entries(common, arm9, clean=False)
    for old, new in zip(before, after, strict=True):
        expected = release.TEXT[new.message_id][0].encode('cp932') if new.message_id in release.TEXT else old.text.rstrip(b' ')
        assert new.text.rstrip(b' ') == expected
        assert (old.message_id, old.block, old.record_index) == (new.message_id, new.block, new.record_index)
    reconstructed = bytearray(source[1])
    for offset in report['changed_offsets']:
        reconstructed[offset:offset + 2] = arm9[offset:offset + 2]
    assert bytes(reconstructed) == arm9
    assert report['all_native_entries_compared'] == 3668


@pytest.mark.parametrize('component', [0, 1])
def test_changed_parent_is_rejected(source, tmp_path, component):
    path, _ = config_copy(tmp_path)
    changed = list(source)
    raw = bytearray(changed[component])
    raw[100] ^= 1
    changed[component] = bytes(raw)
    with pytest.raises(ValueError, match='parent differs'):
        release.apply_release(*changed, path)


def test_changed_output_hash_is_rejected(source, tmp_path):
    path, value = config_copy(tmp_path)
    value['target_arm9_sha256'] = '0' * 64
    path.write_text(json.dumps(value), encoding='utf-8')
    with pytest.raises(ValueError, match='output differs'):
        release.apply_release(*source, path)


@pytest.mark.parametrize('mutation', ['wording', 'owner', 'source', 'formatting'])
def test_changed_manuscript_cannot_inherit_approval(source, tmp_path, monkeypatch, mutation):
    path, config = config_copy(tmp_path)
    doc = json.loads(release.MANUSCRIPT.read_text(encoding='utf-8'))
    if mutation == 'wording':
        doc['records'][0]['english'] = 'A message about the story.{PAD}'
    elif mutation == 'owner':
        doc['records'].pop()
    elif mutation == 'source':
        doc['records'][0]['source_hex'] = '41'
    else:
        doc['records'][0]['review']['formatting'] = False
    manuscript = tmp_path / 'manuscript.json'
    manuscript.write_text(json.dumps(doc), encoding='utf-8')
    monkeypatch.setattr(release, 'MANUSCRIPT', manuscript)
    config['dependencies'][manuscript.as_posix()] = sha(manuscript.read_bytes())
    path.write_text(json.dumps(config), encoding='utf-8')
    with pytest.raises(ValueError):
        release.apply_release(*source, path)


def test_unreviewed_leading_glyphs_are_rejected(source, tmp_path, monkeypatch):
    path, config = config_copy(tmp_path)
    evidence = json.loads(release.EVIDENCE.read_text(encoding='utf-8'))
    evidence['entries'][0]['leading_and_final_glyphs_reviewed'] = False
    target = tmp_path / 'evidence.json'
    target.write_text(json.dumps(evidence), encoding='utf-8')
    monkeypatch.setattr(release, 'EVIDENCE', target)
    config['dependencies'][target.as_posix()] = sha(target.read_bytes())
    path.write_text(json.dumps(config), encoding='utf-8')
    with pytest.raises(ValueError, match='preview approval differs'):
        release.apply_release(*source, path)
