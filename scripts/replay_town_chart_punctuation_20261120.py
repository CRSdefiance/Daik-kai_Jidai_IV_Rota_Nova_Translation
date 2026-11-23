"""Replay the Lisbon route chart with its original known and unknown branches."""

from argparse import ArgumentParser
from pathlib import Path
from struct import unpack_from
import sys

from scripts import headless_desmume_v193 as harness
from scripts import native_condition_fixture_v520 as adapter
from scripts import replay_forces_relationships_20261115 as history
from scripts import stage_town_chart_punctuation_20261120 as stage
from scripts.replay_ruin_discovery_display_20261120 import GrowingCommands


BASE = stage.runtime.BASE
FIRST, JRN = 12280, stage.ROOT.parent / 'paired_journal.jsonl'


def setter(arm, clean):
    def apply(actual, raw, request):
        assert actual == arm and len(raw) == 0x400000
        assert raw[0xB50B8:0xB50E4] == arm[0xB50B8:0xB50E4] == clean[0xB50B8:0xB50E4]
        assert request == {'mode': 'conceal'} or request == {'mode': 'restore'}
        known = int(request['mode'] == 'restore')
        cpu, get = history.get_machine(arm, raw)
        assert get(0xB65E4) == 11
        town = get(0xB6618)
        assert get(0xB50D8, town) == (1 - known) * 2
        get(0xB50B8, town, known)
        assert get(0xB50D8, town) == known * 2
        offset = town + 8 - BASE
        before, = unpack_from('<H', raw, offset)
        after = bytes(cpu.mem_read(town + 8, 2))
        assert (int.from_bytes(after, 'little') ^ before) == 2
        result = raw[:offset] + after + raw[offset + 2:]
        return result, dict(mode=request['mode'], town_ID=11, original_knowledge_setter=0x020B50B8,
            changes=[dict(address=town + 8, before=raw[offset], after=after[0])],
            only_original_information_condition_changed=True)
    return apply


def main(side, out, journal):
    assert not out.exists()
    proof = stage.batch.load(stage.PROOF)
    rom = stage.parent.ROM if side == 'current' else stage.ROM
    assert stage.parent.base.digest(rom) == proof['parent_sha256' if side == 'current' else 'candidate_sha256']
    earlier = stage.batch.load(history.REFERENCE)
    donor = earlier['battery_save_preloaded']
    assert stage.parent.base.digest(donor['source']) == donor['source_sha256']
    inputs = [r for r in earlier['scripted_input_schedule'] if r['start'] < FIRST]
    out.mkdir(parents=True)
    schedule = out / 'inputs.json'
    stage.batch.write(schedule, inputs)
    clean, arm = [stage.batch.NdsImage.open(p).read_file(stage.batch.ARM) for p in (stage.batch.CLEAN, rom)]
    previous = adapter.set_condition, sys.stdin, sys.argv
    stream = GrowingCommands(journal)
    try:
        adapter.set_condition, sys.stdin = setter(arm, clean), stream
        sys.argv = [harness.__file__, '--rom', str(rom), '--out', str(out/'capture'), '--frames', '16500',
            '--inputs-json', str(schedule), '--press-start', '-1', '--capture-every', '999999',
            '--battery-save', donor['source'], '--touchscreen', '--pause-at', str(FIRST), '--dump-pause-ram',
            '--allow-condition-fixtures']
        harness.main()
    finally:
        adapter.set_condition, sys.stdin, sys.argv = previous
        stream.close()


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('side', choices=('current', 'revised'))
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--journal', type=Path, default=JRN)
    args = parser.parse_args()
    main(args.side, args.out, args.journal)
