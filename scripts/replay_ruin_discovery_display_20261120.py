"""Open the original undiscovered site from Istanbul in two equivalent replays."""

import argparse
from pathlib import Path
from struct import unpack_from
from types import FunctionType
import sys

from scripts import headless_desmume_v193 as harness
from scripts import native_condition_fixture_v520 as adapter
from scripts import native_ceremony_map_fixture_v814 as native_map
from scripts import replay_square_samples_wraps_20261115 as source
from scripts import stage_ruin_discovery_display_20261120 as stage
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.verify_personal_gameplay_v841 import get_machine


ROOT = stage.ROOT.parent
JOURNAL = ROOT / 'paired_discovery_commands.jsonl'
INPUTS = ROOT / 'istanbul_prefix.json'
LATE_DONOR = Path('E:/Rota Nova translations/Saves/Test fixtures/V813 Cappadocia rockfall cleared.dsv')
LATE_DONOR_SHA = '1de062be7b19a84c07e59a2ff5dad877afda81a3e9daa86e179c927be04aa2dc'
batch = stage.batch


def unlock_site(arm, raw, request):
    if request == {'mode': 'ceremony-Cappadocia-map'}:
        receipts = batch.load(stage.PROOF), batch.load(stage.parent.RELEASE)
        accepted = dict(zip(('source_arm9_sha256', 'target_arm9_sha256'),
                            (receipt['target_ARM9_sha256'] for receipt in receipts), strict=True))

        def release_identity(path):
            assert path == 'translations/ceremony_editorial_release_v1.json'
            return accepted

        transfer = FunctionType(native_map.set_condition.__code__,
                                native_map.set_condition.__globals__ | {'read': release_identity})
        updated, receipt = transfer(arm, raw, request)
        assert len(receipt['changes']) == 3
        return updated, receipt | request
    assert request in ({'mode': 'make-original-ruins-choice-available'}, {'mode': 'restore-first-discovery'})
    assert len(raw) == 0x400000
    clean = batch.NdsImage.open(batch.CLEAN).read_file(batch.ARM)
    assert all(clean[a:b] == arm[a:b] for a, b in ((0xB5050, 0xB50B8), (0xB5170, 0xB5188), (0x60DEC, 0x60E4C)))
    cpu, get = get_machine(arm, raw)
    town = get(0xB6618)
    assert get(0xB65E4) == 22 and get(0xB5170, town) == 8
    site = get(0xCB16C)+4+8*8
    if request['mode'] == 'restore-first-discovery':
        assert get(0xB507C, town, 11)
        at = site+4-stage.BASE
        value = raw[at]
        assert value & 1, 'Expected historical test donor with a preset discovery flag'
        after = bytes([value & ~1])
        return raw[:at]+after+raw[at+1:], dict(mode=request['mode'], town=22, first_discovery_ruin=8,
            only_existing_discovery_bit_reset=True, changes=[dict(address=site+4, before=value, after=after[0])])
    assert get(0xB50AC, town) == 0
    assert raw[site+4-stage.BASE] & 1 == 0
    at = town + 12 - stage.BASE
    original = unpack_from('<I', raw, at)[0]
    assert not original & (1<<11)
    get(0xB5050, town, 11, 1)
    new = bytes(cpu.mem_read(town+12, 4))
    assert int.from_bytes(new, 'little') == original | 1<<11
    assert get(0xB507C, town, 11) == 1<<11
    updated = raw[:at]+new+raw[at+4:]
    changes = [dict(address=stage.BASE+i,before=raw[i],after=updated[i]) for i in range(at, at+4) if raw[i] != updated[i]]
    assert len(changes) == 1
    return updated, dict(mode=request['mode'], town=22, first_discovery_ruin=8, original_facility_flags=original,
                         discovery_flag_unchanged=raw[site+4-stage.BASE], unlock_only=True, changes=changes)


def main(which, output, journal, frames, late_donor):
    staged = batch.load(stage.PROOF)
    rom = stage.parent.ROM if which == 'current' else stage.ROM
    expected = staged['parent_sha256'] if which == 'current' else staged['candidate_sha256']
    assert batch.digest(rom.read_bytes()) == expected
    _, original, donor, _ = source.history('epidemic')
    assert batch.load(INPUTS) == [row for row in original['scripted_input_schedule'] if row['start']<3200]
    assert batch.digest(donor.read_bytes()) == original['battery_save_preloaded']['source_sha256']
    if late_donor:
        donor = LATE_DONOR
        assert batch.digest(donor.read_bytes()) == LATE_DONOR_SHA
    stream = GrowingCommands(journal)
    old = adapter.set_condition, sys.stdin, sys.argv
    try:
        adapter.set_condition, sys.stdin = unlock_site, stream
        sys.argv = [harness.__file__, '--rom', str(rom), '--out', str(output), '--frames', str(frames),
                    '--inputs-json', str(INPUTS), '--battery-save', str(donor), '--touchscreen',
                    '--pause-at', '3200', '--allow-condition-fixtures', '--capture-every', '999999',
                    '--dump-pause-ram', '--dump-ram']
        harness.main()
    finally:
        adapter.set_condition, sys.stdin, sys.argv = old
        stream.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('which', choices=('current', 'revised'))
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--journal', type=Path, default=JOURNAL)
    parser.add_argument('--frames', type=int, default=18000)
    parser.add_argument('--late-donor', action='store_true')
    args = parser.parse_args()
    main(args.which, args.output, args.journal, args.frames, args.late_donor)
