"""Review city and ship outcomes with the original named-object substitutions."""

from collections import Counter
from hashlib import sha256
from pathlib import Path
from struct import unpack_from
from unicodedata import normalize

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import checkpoint_sea_event_review_v1 as prior
from scripts import register_fleet_reports_v1 as parent


BASE, ARM, COMMON, CLEAN = prior.BASE, prior.ARM, prior.COMMON, prior.CLEAN
OUTPUT = prior.ROOT / 'city_combat_notices_context_v1.json'
DIRECT = 0x53F0C
SHIP_NAME_LIMIT = Path('work/analysis/ship_name_bound_v1335b/original_ship_rename_capacity.json')
GROUPS = (
    (2580, 2584, 0x1183E0, 0x488B4, 0x488C8, 0x488D0, 0x48A40, 'town',
     'After an attack on a city, the captain reports that the named city surrendered. '
     'The original victory branch chooses this table when the opponent is the city.'),
    (2585, 2588, 0x118440, 0x48260, 0x48274, 0x4827C, 0x48A24, 'town',
     'The fleet captain reports that the named city opened fire on the fleet. '
     'This is the city-initiated branch.'),
    (2589, 2591, 0x118700, 0x48CF8, 0x48D0C, 0x48D14, 0x495A0, 'ship',
     'After resolving damage in the automated fleet battle, our captain reports sinking the named enemy ship.'),
    (2592, 2593, 0x1168A0, 0x48D38, 0x48D4C, 0x48D54, 0x495A4, 'ship',
     'The opposing side sank one of our ships. Our captain reports the loss using the affected ship’s name.'),
    (2594, 2596, 0x1168C0, 0x490D0, 0x490E4, 0x490EC, 0x495A8, 'ship',
     'Our captain reports capturing the named enemy ship in the automated fleet battle.'),
    (2597, 2598, 0x116900, 0x49110, 0x49124, 0x4912C, 0x495AC, 'ship',
     'Our captain reports that the opposing side captured our named ship. The ship has been taken.'),
    (2599, 2606, 0x116940, 0x49418, 0x49458, 0x49460, 0x495C0, 'gold',
     'After the battle outcome, the winning captain reports the gold value of the spoils. '
     'The original resolver passes the amount through the same number getter as the monthly fleet reports.'),
    (2607, 2614, 0x116980, 0x48318, 0x4832C, 0x48334, 0x48A28, 'town',
     'Our fleet captain reports that the fleet is starting its attack on the named city. '
     'The game sends this notice before resolving the outcome.'),
)

DECISIONS = {
    2580: (None, 'The named city has surrendered.', 'Retain the decisive report and the city’s own action.'),
    2581: (None, 'The speaker boasts that their side forced the city to surrender.',
           'Retain the proud, active wording. This source voice explicitly takes credit.'),
    2582: (None, 'The speaker says the named city has surrendered.',
           'Retain the even delivery and completed result.'),
    2583: (None, 'The speaker excitedly reports that the city surrendered.',
           'Retain the quick announcement and its lift.'),
    2584: (None, 'The speaker tells the player that the named city has surrendered.',
           'Retain the composed report and the exclamation that marks the result.'),
    2585: (None, 'The named city opened fire on the fleet.',
           'Retain the alert, the attacking city and the target.'),
    2586: ('%s just opened fire on us!', 'The speaker reports that the city has opened fire on them.',
           'Keep the urgent, colloquial report in the moment the fire starts.'),
    2587: ('%s has started firing on us!', 'The speaker exclaims that the city fired on their fleet.',
           'Keep the blunt warning and the direction of the bombardment.'),
    2588: (None, 'The named city is firing its cannons at the fleet.',
           'Retain the young voice’s direct account of the cannon fire.'),
    2589: ('Enemy ship %s sunk!', 'The speaker reports that the named enemy ship was sunk.',
           'Keep the clipped battle call and make the ship designation explicit.'),
    2590: ('Enemy ship %s sunk.', 'The speaker reports the sinking of the named enemy ship.',
           'Restore the enemy identification and retain the original matter-of-fact delivery.'),
    2591: ('We sank the enemy ship %s!', 'The speaker exclaims that their side sank the named enemy ship.',
           'Keep the youthful excitement and the sense that this was their side’s action.'),
    2592: (None, 'The named ship on our side was sunk.',
           'Retain the restrained report and its trailing disappointment.'),
    2593: (None, 'The speaker reacts sadly to the named ship going down.',
           'Retain the simple past and subdued reaction.'),
    2594: ('Enemy ship %s captured!', 'The speaker reports capture of the named enemy ship.',
           'Keep the clipped battle report and restore the explicit enemy designation.'),
    2595: ('Enemy ship %s captured.', 'The speaker reports capture of the named enemy ship.',
           'Keep the measured result and restore the enemy designation.'),
    2596: ('We took the enemy ship %s!', 'The speaker exclaims that their side captured the named enemy ship.',
           'Use the familiar naval sense of taking a ship. Keep the side that acted and the target.'),
    2597: (None, 'The named ship on our side was captured.',
           'Retain the restrained passive report and trailing disappointment.'),
    2598: ('They captured %s...', 'The speaker reacts to losing the named ship to capture.',
           'Keep the younger speaker’s plain admission and the distinction from sinking.'),
    2599: ('We took spoils worth %s gold!', 'The winning side obtained spoils worth the stated amount of gold.',
           'Make clear that the amount measures the value of the spoils.'),
    2600: ('We secured spoils worth %s gold.', 'The speaker formally reports the value of the recovered spoils.',
           'Keep the measured delivery and state the value without implying all proceeds were coins.'),
    2601: ("We grabbed %s gold's worth of loot!", 'The speaker tells the player how much the captured loot was worth.',
           'Use the informal “grabbed” and “loot” for this voice.'),
    2602: ("We've taken spoils worth %s gold!", 'The speaker excitedly reports the value of what their side took.',
           'Preserve the excitement and exact amount as a valuation.'),
    2603: ("We took %s gold's worth of loot!", 'The speaker boasts about the value of what their side seized.',
           'Use a quick, rough report that leaves the nature of the spoils open.'),
    2604: ('We took loot worth %s gold!', 'The speaker announces the value of the spoils their side seized.',
           'Keep the older voice plainspoken and give the amount a natural currency unit.'),
    2605: ('We got loot worth %s gold!', 'The speaker excitedly reports the value of the captured loot.',
           'Keep the younger speaker’s simple choice of verb and the excited cadence.'),
    2606: ("We've secured spoils worth %s gold!", 'The speaker formally announces the value of the spoils captured.',
           'Keep a fuller report for this voice and state the valuation explicitly.'),
    2607: (None, 'The speaker announces the start of an attack on the named city.',
           'Retain the brief report, immediate action and target.'),
    2608: (None, 'The speaker announces the start of an attack on the named city.',
           'Retain the measured delivery and the stated target.'),
    2609: (None, 'The speaker reports that their side is attacking the named city.',
           'Retain the direct present-progressive report.'),
    2610: (None, 'The speaker declares that their side will attack the named city.',
           'Retain the composed declaration and the target.'),
    2611: ("We're going after %s!", 'The speaker declares that their side is launching an attack on the named city.',
           'Restore the speaker’s declaration of what the fleet will do.'),
    2612: (None, 'The speaker declares that their side will attack the named city.',
           'Retain the decisive spoken announcement.'),
    2613: (None, 'The speaker says their side is attacking the named city now.',
           'Retain the immediate timing and eager voice.'),
    2614: ("All right. We'll begin the attack on %s.", 'The speaker turns to the next action and announces the start of the attack.',
           'Restore the transition and keep the formal report easy to say.'),
}


def argument_samples(runtime, source):
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    for start, end in ((0x49808, 0x4993C), (0xABF50, 0xABFCC), (0xB5630, 0xB5640)):
        assert source[start:end] == runtime.arm[start:end]

    def word(address):
        return unpack_from('<I', cpu.mem_read(address, 4))[0]

    def string(pointer):
        assert BASE <= pointer <= BASE + 0x400000 - 64
        return bytes(cpu.mem_read(pointer, 64)).split(b'\0', 1)[0]

    towns = []
    root = get(0xCB178) + 4
    for index in range(114):
        town = root + index * 108
        getter = word(word(town) + 8)
        assert getter == BASE + 0xB5630
        name = string(get(getter - BASE, town))
        assert name and name.isascii()
        towns.append(dict(town_index=index, getter=getter, arguments=[name.hex()]))
    assert any(row['arguments'] == [b'Hamburg'.hex()] for row in towns)
    ships = []
    fleet_root, scratch = get(0xCB1A8) + 4, 0x02460000
    for index in (0, 1, 2, 3, 8, 57):
        fleet = fleet_root + index * 132
        assert get(0x49808, scratch, fleet) == scratch
        for slot in range(5):
            ship = scratch + slot * 24
            if word(ship + 4) == 155:
                continue
            getter = word(word(ship) + 4)
            assert getter == BASE + 0x49908
            name = string(get(getter - BASE, ship))
            assert name and name.isascii()
            ships.append(dict(fleet_index=index, slot=slot, getter=getter, arguments=[name.hex()]))
    assert any(row['arguments'] == [b'Arnhem'.hex()] for row in ships)
    limit = prior.load(SHIP_NAME_LIMIT)
    assert limit['max_name_bytes_excluding_NUL'] == 18
    stress = b'Northern Star Wind'
    assert len(stress) == limit['max_name_bytes_excluding_NUL']
    ships.append(dict(offline_boundary_input=True, arguments=[stress.hex()],
                      limit_evidence=str(SHIP_NAME_LIMIT), limit_evidence_sha256=prior.digest(SHIP_NAME_LIMIT)))
    amounts = []
    for value in (1, 90000, 0x7FFFFFFF):
        text = string(get(0xABF50, value))
        assert normalize('NFKC', text.decode('cp932')) == str(value)
        amounts.append(dict(value=value, getter=BASE + 0xABF50, arguments=[text.hex()]))
    runtime.calls.clear()
    return dict(town=towns, ship=ships, gold=amounts)


def main():
    assert not OUTPUT.exists()
    release = prior.load(parent.RELEASE)
    assert parent.base.digest(parent.base.REGISTRY) == release['registry_sha256']
    runtime = prior.RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    clean = NdsImage.open(CLEAN)
    arm = clean.read_file(ARM)
    assert prior.digest(CLEAN) == release['clean_input_sha256']
    source = common_message_entries(clean.read_file(COMMON), arm)
    directory = sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    current = owned_entries(runtime.common, runtime.arm, directory)
    ledger = prior.load(parent.base.LEDGER)
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    credited = {row['id'] for row in ledger[parent.base.CONTEXT]['integrated_record_keys'] if row['file_path'] == COMMON}
    assert not credited.intersection(f'COMMON_MESSAGE_{n}' for n in DECISIONS)
    assert set(DECISIONS) == set(range(2580, 2615))
    arguments = argument_samples(runtime, arm)
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    roster = {i: runtime.actor_root + (0x19E4 if i == 3 else 4 + 32 * i) for i in range(207)}
    voices = {i: get(0x7E988, actor) for i, actor in roster.items()}
    groups, records = [], []
    for start, end, table, prefix, load, call, pool, kind, context in GROUPS:
        binding = prior.caller_binding(arm, runtime.arm, load, call, pool, BASE + table, DIRECT)
        assert arm[prefix:call + 4] == runtime.arm[prefix:call + 4]
        assert arm[table:table + 32] == runtime.arm[table:table + 32]
        slots = unpack_from('<8i', arm, table)
        assert set(slots) - {-1} == set(range(start, end + 1))
        selections = []
        for i, actor in roster.items():
            expected = start if slots[voices[i]] == -1 else slots[voices[i]]
            assert get(0x53F4C, actor, BASE + table) == expected
            selections.append((i, voices[i], expected))
        groups.append(dict(first_ID=start, last_ID=end, table=BASE + table, slots=slots, native_callers=[binding],
            original_voice_choices=selections, argument_kind=kind, original_role_argument=None,
            argument_prefix=dict(start=BASE + prefix, exact_hex=arm[prefix:call + 4].hex()), context=context))
        for n in range(start, end + 1):
            jp, old = source[n], current[n]
            text = old.text.decode('cp932')
            paragraph = ' '.join(normalize('NFKC', text).split())
            revision, meaning, note = DECISIONS[n]
            english = revision or paragraph
            assert english.isascii() and english == ' '.join(english.split()) and bool(revision) == (english != paragraph)
            assert jp.text.count(b'%s') == old.text.count(b'%s') == english.count('%s') == 1
            assert '%' not in english.replace('%s', '')
            records.append(dict(id=f'COMMON_MESSAGE_{n}', message_ID=n, file_path=COMMON,
                source_reference=prior.reference(jp), current_reference=prior.reference(old),
                source_hex=jp.text.hex(), current_hex=old.text.hex(), source_Japanese=jp.text.decode('cp932'),
                current_English=text, english=english, context=context, native_group_first_ID=start,
                original_slots=[i for i, selected in enumerate(slots) if n == selected],
                speaker='Fleet captain selected by the original battle dispatcher',
                source_meaning=meaning, localization_note=note, decision='revision' if revision else 'retention',
                inherited_fullwidth_Latin=prior.wide_letters(text), original_substitution_count=1,
                review={gate: gate != 'formatting' for gate in prior.GATES}))
    assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    assert [row['message_ID'] for row in records] == list(range(2580, 2615))
    counts = Counter(row['decision'] for row in records)
    prior.save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=prior.GATES, records=records,
        registered_input=runtime.receipt(), source_ROM_sha256=release['clean_input_sha256'],
        native_context=groups, initialized_argument_samples=arguments,
        original_offline_actor_selections=sum(len(group['original_voice_choices']) for group in groups),
        counts=dict(counts), formatting_pending=True, gameplay_pending=True, new_credit=0, full_goal_complete=False))
    print(f'{len(records)} decisions {dict(counts)} across {len(groups)} original tables.')


if __name__ == '__main__':
    main()
