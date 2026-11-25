"""Replay both original Palace quotes from the same isolated Istanbul save."""

import argparse
from pathlib import Path
import sys

from scripts import headless_desmume_v193 as harness
from scripts import native_condition_fixture_v520 as adapter
from scripts import replay_ruin_discovery_display_20261120 as istanbul
from scripts import stage_palace_contract_fee_20261120 as stage


def set_low_funds(arm, ram, request):
    assert request == {'mode': 'contract-insufficient-funds'} and len(ram) == 0x400000
    clean = stage.batch.NdsImage.open(stage.batch.CLEAN).read_file(stage.batch.ARM)
    assert arm[0x3CC80:0x3CCD0] == clean[0x3CC80:0x3CCD0]
    cpu, get = istanbul.get_machine(arm, ram)
    assert get(0xB65E4) == 22
    root, index = get(0xCB160), get(0x397D8)
    company = root + 4 + index * 76
    old = get(0x3CCC8, company)
    assert old == 8371
    get(0x3CC80, company, (1 - old) & 0xFFFFFFFF)
    assert get(0x3CCC8, company) == 1
    at = company + 12 - stage.ruin.BASE
    output = ram[:at] + bytes(cpu.mem_read(company + 12, 4)) + ram[at + 4:]
    changes = [dict(address=stage.ruin.BASE + i, before=ram[i], after=output[i])
               for i in range(at, at + 4) if ram[i] != output[i]]
    assert len(changes) == 2
    return output, dict(mode=request['mode'], original_funds=old, initialized_funds=1, changes=changes,
                        only_original_company_money_field_changed=True)


def main(which, output, journal):
    proof = stage.batch.load(stage.PROOF)
    rom = stage.parent.ROM if which == 'current' else stage.ROM
    assert stage.parent.base.digest(rom) == proof['parent_sha256' if which == 'current' else 'candidate_sha256']
    _, report, donor, _ = istanbul.source.history('epidemic')
    assert stage.parent.base.digest(donor) == report['battery_save_preloaded']['source_sha256']
    previous = adapter.set_condition, sys.stdin, sys.argv
    stream = istanbul.GrowingCommands(journal)
    try:
        adapter.set_condition, sys.stdin = set_low_funds, stream
        sys.argv = [harness.__file__, '--rom', str(rom), '--out', str(output), '--frames', '8000',
                    '--inputs-json', str(istanbul.INPUTS), '--battery-save', str(donor), '--touchscreen',
                    '--pause-at', '3200', '--allow-condition-fixtures', '--capture-every', '999999',
                    '--dump-pause-ram', '--dump-ram']
        harness.main()
    finally:
        adapter.set_condition, sys.stdin, sys.argv = previous
        stream.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('which', choices=('current', 'revised'))
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--journal', type=Path, required=True)
    options = parser.parse_args()
    main(options.which, options.output, options.journal)
