"""Reject changes to verified persistent-name allocation and its source."""

import copy
import json
from pathlib import Path

import pytest
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.persistent_name_release import BASE, TARGET, apply_release, transform
from dk4tool.rom.nds import NdsImage


@pytest.fixture(scope='module')
def inputs():
    source = NdsImage.open('out/all_routes_combined_v147_candidate.nds').read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    allocation = json.loads(Path('translations/persistent_name_allocation_v1.json').read_text(encoding='utf-8'))
    return source, allocation, bytes(MainCodeFile(clean, BASE).sections[2].data)


def test_release_reproduces_reviewed_bytes(inputs):
    saved, report = apply_release(inputs[0], 'translations/persistent_name_release_v1.json')
    assert sha(saved) == TARGET
    assert saved == Path('work/analysis/persistent_name_section_arm9.bin').read_bytes()
    assert report['runtime_verified'] is False


def test_reject_changed_source(inputs):
    source, allocation, dtcm = inputs
    with pytest.raises(ValueError, match='exact complete V147'):
        transform(bytes([source[0] ^ 1]) + source[1:], allocation, dtcm)


@pytest.mark.parametrize('change', ['padding', 'heap', 'missing_reference', 'pointer', 'source_lock', 'dtcm'])
def test_reject_unreviewed_allocation(inputs, change):
    source, allocation, dtcm = inputs
    allocation = copy.deepcopy(allocation)
    if change == 'padding':
        allocation['payload_hex'] = allocation['payload_hex'][:-2] + '01'
    elif change == 'heap':
        allocation['heap_low'] += 32
    elif change == 'missing_reference':
        allocation['moves'].pop()
    elif change == 'pointer':
        allocation['moves'][0]['runtime_pointer'] += 1
    elif change == 'source_lock':
        allocation['moves'][0]['source_hex'] = '00000000'
    else:
        dtcm = dtcm[:-1] + bytes([dtcm[-1] ^ 1])
    with pytest.raises(ValueError):
        transform(source, allocation, dtcm)
