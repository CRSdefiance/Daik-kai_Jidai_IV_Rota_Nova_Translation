"""Check Rafael's original sailing-lesson prerequisites on read-only snapshots."""

from argparse import ArgumentParser
from pathlib import Path
from struct import pack, unpack, unpack_from

from scripts import replay_rafael_sailing_from_lisbon_20261121 as replay
from scripts.prove_papal_trade_entries_v7628 import parse_events
from scripts.verify_personal_gameplay_v841 import get_machine


base, active = replay.base, replay.active
BASE, SCRATCH = 0x02000000, 0x02640000
Lisbon, lesson = 11, 128
PROOF = replay.BINDING.with_name('rafael_sailing_lisbon_eligibility_20261121_v1.json')
EVENT_IDS = (48, 128, 139)


def locate(archive, ram):
    at = ram.index(archive[:96])
    assert ram.find(archive[:96], at + 1) == -1
    return BASE + at - 0x34


def getters(arm, archive, ram):
    cpu, get = get_machine(arm, ram)
    owner = locate(archive, ram)
    assert get(0x7F244) == get(0x2E58C) == 0
    flags = {i: get(0x23840, owner + 4, i) for i in EVENT_IDS}
    fleet = get(0xCB1A8) + 4
    docked = get(0x34674, fleet)
    port_id = get(0xB65E4)
    point = None
    if docked == 0x73:
        ship = get(0x36C70, fleet + 12)
        point = unpack('<2i', cpu.mem_read(ship + 16, 8))
    port = get(0xCD6B8, Lisbon)
    target = [x * 128 for x in unpack('<2i', cpu.mem_read(port + 12, 8))]
    context = unpack('<3I', cpu.mem_read(owner + 0x2454, 12))
    assert bytes(cpu.mem_read(BASE, 0x400000)) == ram
    return dict(town=port_id, fleet_location_state=docked, ship_point=point, Lisbon_point=target,
                original_event_context=list(context), event_completion=flags)


def run_predicate(arm, archive, specs, snapshot, context, flip=None):
    cpu, get = get_machine(arm, snapshot)
    owner = locate(archive, snapshot)
    pointers = {}
    for i in EVENT_IDS:
        get(0x23888, SCRATCH, owner + 4, i)
        ptr, = unpack('<I', cpu.mem_read(SCRATCH, 4))
        assert ptr == owner + 0x34 + 96 + specs[i]['body_offset']
        runtime = bytes(cpu.mem_read(ptr, specs[i]['source_record_bytes']))
        assert runtime[4:] == bytes.fromhex(specs[i]['source_hex'])[4:]
        assert (unpack_from('<I', runtime)[0] ^ specs[i]['source_word0']) & ~0xC0008000 == 0
        pointers[i] = ptr
    cpu.mem_write(owner + 0x2454, pack('<3I', *context))
    if flip:
        before, = unpack('<I', cpu.mem_read(pointers[flip], 4))
        cpu.mem_write(pointers[flip], pack('<I', before ^ (1 << 30)))
    flags = {i: get(0x23840, owner + 4, i) for i in EVENT_IDS}
    get(0xCC9A8, SCRATCH + 0x80, get(0xCB1B4))
    before = bytes(cpu.mem_read(BASE, 0x400000))
    result = get(0x220D8, owner, pointers[lesson], SCRATCH + 0x80, 0)
    assert bytes(cpu.mem_read(BASE, 0x400000)) == before and result in (0, 1)
    return dict(offline_context=context, counterfactual_event_flag=flip, source_flag_values=flags,
                original_eligibility_result=result, original_predicate_left_ram_exact=True)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--inspect', type=Path, help='Read live emulator output without editing it.')
    args = parser.parse_args()
    release, binding = map(base.load, (active.RELEASE, replay.BINDING))
    assert base.digest(active.ROM) == release['candidate_sha256'] == binding['candidate_sha256']
    clean, current = map(base.NdsImage.open, (active.native.CLEAN, active.ROM))
    arm, clean_arm = [rom.read_file(active.native.ARM) for rom in (current, clean)]
    archive = current.read_file(binding['events_archive'])
    assert archive == clean.read_file(binding['events_archive'])
    assert active.native.digest(archive) == binding['events_archive_sha256']
    if args.inspect:
        print(getters(arm, archive, args.inspect.read_bytes()))
        return
    assert not PROOF.exists()
    spans = ((0x220D8, 0x22ECC), (0x23840, 0x238D8), (0x21EAC, 0x220D8))
    assert all(arm[a:b] == clean_arm[a:b] for a, b in spans)
    events = parse_events(archive)
    specs = {i: events[i] for i in EVENT_IDS}
    assert specs[lesson]['script_block'] == lesson and specs[lesson]['category'] == 6
    assert specs[lesson]['source_hex'] == binding['event_record_hex']
    assert specs[lesson]['must_be_completed'] == [139] and specs[lesson]['must_not_be_completed'] == [48]
    assert specs[48]['script_block'] == 48 and specs[139]['script_block'] == 139
    saved = binding['historical_arrival_observations'][-1]['snapshot']
    raw = Path(saved['path']).read_bytes()
    assert saved['read_only_export'] and base.digest(saved['path']) == saved['sha256']
    actual = getters(arm, archive, raw)
    assert actual['town'] == Lisbon and actual['original_event_context'] == [5, Lisbon, 0]
    assert actual['event_completion'] == {48: 0, 128: 0, 139: 1}
    cases = [
        run_predicate(arm, archive, specs, raw, [5, Lisbon, 0]),
        run_predicate(arm, archive, specs, raw, [6, Lisbon, 0]),
        run_predicate(arm, archive, specs, raw, [6, Lisbon + 1, 0]),
        run_predicate(arm, archive, specs, raw, [6, Lisbon, 0], 139),
        run_predicate(arm, archive, specs, raw, [6, Lisbon, 0], 48),
    ]
    assert [case['original_eligibility_result'] for case in cases] == [1, 1, 0, 0, 0]
    base.save(PROOF, dict(candidate_sha256=release['candidate_sha256'], original_entry_binding=str(replay.BINDING),
        original_entry_binding_sha256=base.digest(replay.BINDING), original_event_records=specs,
        historical_snapshot=saved, historical_state=actual, original_runtime_spans=[
            dict(offset=start, end_exclusive=end, sha256=active.native.digest(arm[start:end])) for start, end in spans],
        independent_offline_cases=cases, original_outer_category_selection_required=True,
        actual_gameplay=False, new_editorial_credit=0))
    print('The original predicate accepts Lisbon after event 139 and before event 48. The historical return already met both prerequisites.')


if __name__ == '__main__':
    main()
