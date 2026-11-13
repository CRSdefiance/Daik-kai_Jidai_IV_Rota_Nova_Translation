"""Review pirate contact, battle outcomes and the follow-up port orders."""

from collections import Counter
from hashlib import sha256
from struct import unpack_from
from unicodedata import normalize

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.pirate_report_bearings_v1 import BEARINGS, CALL, TABLES, WRAPPER
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import checkpoint_sea_event_review_v1 as prior
from scripts import register_city_combat_notices_v1 as parent


BASE, ARM, COMMON, CLEAN = prior.BASE, prior.ARM, prior.COMMON, prior.CLEAN
OUTPUT = prior.ROOT / 'pirate_and_retreat_reports_context_v1.json'
DIRECT, QUEUED = 0x53F0C, 0x53D44
GROUPS = (
    (2615, 2620, 0x1169A0, ((0x77C50, 0x77C80, 0x77ECC, QUEUED),), 'bearing_and_pirate',
     'The lookout spots a pirate and identifies them by name. The direction is relative to the fleet. '
     'The first argument is the bearing, and the second is the pirate’s given name.'),
    (2621, 2626, 0x1169E0, ((0x2DFD8, 0x2DFE0, 0x2E0C0, DIRECT),), 'pirate',
     'The fleet captain reports that they obtained information about the named pirate. '
     'This report does not give the content of that information.'),
    (2627, 2630, 0x116A40, ((0x77C5C, 0x77C80, 0x77ED0, QUEUED),), 'bearing_and_pirate',
     'The lookout identifies the pirate and sounds the alarm that the pirate is attacking. '
     'The original first field is the bearing, and the second is the given name.'),
    (2631, 2637, 0x116A80, ((0x2E004, 0x2E00C, 0x2E0C4, DIRECT), (0x2E078, 0x2E080, 0x2E0C4, DIRECT)), 'pirate',
     'The fleet captain reports an encounter with the named pirate and says the fleet will fight. '
     'The voice-3 alternative explicitly says the pirate attacked first.'),
    (2638, 2644, 0x116AA0, ((0x488A4, 0x488AC, 0x48A3C, DIRECT),), None,
     'The fleet captain announces their side’s victory. This branch has no named opponent or captured-city argument.'),
    (2645, 2650, 0x116AE0, ((0x488E4, 0x488EC, 0x48A44, DIRECT),), None,
     'The fleet captain reports their own fleet’s defeat. The result does not specify whether any ship sank.'),
    (2651, 2656, 0x116B00, ((0x488F4, 0x488FC, 0x48A48, DIRECT),), None,
     'The fleet captain reports withdrawing. In the observed Hamburg sequence, the report follows the attack notice '
     'and leads to the decision to seek a nearby port.'),
    (2657, 2662, 0x116BA0, ((0x3561C, 0x35620, 0x35680, DIRECT), (0x357FC, 0x35800, 0x3586C, DIRECT)), None,
     'The game assigns a nearby port, and the fleet captain tells the player what they will do next. '
     'In the Hamburg replay, this follows the retreat. The formal voice also promises to wait for orders.'),
)

DECISIONS = {
    2615: ("Pirate sighted %s! It's %s!", 'The speaker sights the pirate in the stated direction and names them.',
           'Use a lookout’s short alert and keep the two runtime fields in the original order.'),
    2616: ("We found a pirate %s. It's %s!", 'The speaker found the pirate in the stated direction.',
           'Use a conversational report with the identification as its own beat.'),
    2617: ("A pirate %s! It's %s!", 'The speaker excitedly identifies a pirate in the stated direction.',
           'Keep the brisk alert and place the name after the direction.'),
    2618: ("There's a pirate %s! That's %s!", 'The speaker calls out the sighting and identifies the pirate.',
           'Keep the plainspoken voice and the excited recognition.'),
    2619: ("Hey, there's a pirate %s! It's %s!", 'The speaker calls for attention and points out the pirate.',
           'Retain the young voice’s informal opening and both source facts.'),
    2620: ("We've spotted a pirate %s. It's %s!", 'The speaker announces the sighting and identifies the pirate.',
           'Use a measured sighting report and preserve the original direction and name.'),
    2621: ('We have word on the pirate %s.', 'The speaker reports getting information on the named pirate.',
           'Restore the speaker’s completed report in place of the fragment.'),
    2622: ("We've learned something about the pirate %s.", 'The speaker reports getting information on the named pirate.',
           'Keep the conversational voice and leave the content of the information open.'),
    2623: ('We got word about the pirate %s.', 'The speaker reports receiving information about the named pirate.',
           'Use a brief spoken report and keep the named subject.'),
    2624: ('We heard something about the pirate %s.', 'The speaker says they got information on the named pirate.',
           'Keep the plain delivery and the report’s unspecified content.'),
    2625: ('Ho ho ho! We have word on the pirate %s.', 'The older speaker chuckles, then reports getting information on the named pirate.',
           'Keep the audible chuckle and use a natural, complete report.'),
    2626: ('We got word on the pirate %s!', 'The speaker excitedly announces information on the named pirate.',
           'Keep the excitement and exact identity while making the phrasing more conversational.'),
    2627: ("A pirate %s! It's %s, and they're attacking!", 'The speaker recognizes the pirate in the stated direction and warns that the pirate attacked.',
           'Restore the bearing-first argument order and the urgent follow-up.'),
    2628: ("Hm! A pirate %s. It's %s! They're attacking!", 'The speaker spots the named pirate in the stated direction and angrily reports the attack.',
           'Restore the bearing-first order and the older voice’s exclamation.'),
    2629: ("Ah! A pirate %s is attacking us! It's %s!", 'The speaker reacts to the attack from the stated direction, then recognizes the pirate.',
           'Keep the alarm before the recognition and use the normal ASCII I.'),
    2630: ("A pirate %s! It's %s. We're under attack!", 'The speaker reports the named pirate appearing in the stated direction and attacking.',
           'Keep the sighting and immediate danger as separate beats.'),
    2631: (None, 'The captain reports encountering the named pirate and beginning combat.',
           'Retain the formal engagement report, including the immediate move into battle.'),
    2632: (None, 'The captain reports encountering the named pirate and says they will engage.',
           'Retain the measured report and the stated intention to fight.'),
    2633: ("There's the pirate %s! Let's fight!", 'The speaker recognizes the pirate and eagerly says they will fight.',
           'Keep the quick recognition and the young voice’s enthusiasm.'),
    2634: (None, 'The captain says the named pirate attacked them and their fleet will fight back.',
           'Retain the clear direction of the attack and the intent to respond.'),
    2635: ("We ran into the pirate %s! We're taking 'em on!", 'The speaker says they ran into the named pirate and will fight.',
           'Keep the accidental encounter and the rough voice’s resolve.'),
    2636: ("There's the pirate %s. We'll take them on!", 'The speaker reports encountering the pirate and declares that they will fight.',
           'Use a plainspoken recognition and a decisive reply.'),
    2637: ("Oh! It's the pirate %s! We're going to fight!", 'The speaker is surprised to run into the named pirate, then says they will fight.',
           'Restore the surprise without inventing fear or reluctance.'),
    2638: (None, 'The captain announces that their side has won.', 'Retain the formal exclamation.'),
    2639: (None, 'The captain states that their side has won.', 'Retain the composed report and quiet punctuation.'),
    2640: (None, 'The speaker exclaims that their side has won.', 'Retain the natural plural wording for the source pronoun.'),
    2641: (None, 'The speaker tells the player that their side has won.', 'Retain the composed voice’s pleased announcement.'),
    2642: (None, 'The speaker exclaims that their side won.', 'Retain the blunt, confident battle call.'),
    2643: ("The day is ours!", 'The speaker exclaims that their side won.',
           'Use a natural victory idiom for the older voice.'),
    2644: (None, 'The younger speaker exclaims that their side won.', 'Retain both beats of the excited realization.'),
    2645: (None, 'The captain reports the defeat of their fleet.', 'Retain the restrained report and trailing tone.'),
    2646: (None, 'The speaker ruefully reports that their fleet was defeated.',
           'Retain the contraction and natural plural possessive.'),
    2647: (None, 'The captain reports the defeat of their fleet.', 'Retain the formal report of defeat.'),
    2648: ('They beat our fleet...', 'The speaker ruefully reports their fleet’s defeat.',
           'Keep the rough, direct admission without implying that the fleet was destroyed.'),
    2649: ("Our fleet's been beaten...", 'The speaker regretfully reports the defeat of their fleet.',
           'Use a resigned, spoken report for the older voice.'),
    2650: (None, 'The younger speaker says their fleet was beaten.', 'Retain the informal phrasing and downbeat ending.'),
    2651: (None, 'The captain reports that their side has retreated.',
           'Retain the formal admission used after the Hamburg attack.'),
    2652: ('Our fleet pulled back...', 'The speaker reports that their fleet retreated.',
           'Keep the possessive sense of the first-person plural in a spoken report.'),
    2653: (None, 'The speaker says their fleet retreated.', 'Retain the full report in this more composed voice.'),
    2654: ('We pulled our fleet back...', 'The speaker reports that their fleet retreated.',
           'Use an active, plainspoken admission and preserve whose fleet withdrew.'),
    2655: ('Our fleet withdrew...', 'The speaker says their fleet retreated.',
           'Keep the older speaker’s measured delivery.'),
    2656: (None, 'The younger speaker says their fleet ran away.', 'Retain the frank admission of flight and its trailing tone.'),
    2657: ("We'll put into a nearby port and wait for orders.", 'The speaker will dock at a nearby port and await instructions.',
           'Keep the two parts of the captain’s response to the retreat. Use natural nautical wording and repair the midword break.'),
    2658: (None, 'The speaker will dock at a nearby town for now.', 'Retain the temporary plan and clear spoken delivery.'),
    2659: ("We'll dock at a nearby town for now.", 'The speaker says they will dock at a nearby town for the time being.',
           'Use the natural preposition for docking and keep the temporary qualification.'),
    2660: ("We'll put into a nearby port for now.", 'The speaker says their fleet will dock at a nearby town for now.',
           'Keep the practical plan and the time qualifier in a nautical voice.'),
    2661: ("Can't be helped. We'll put into a nearby port.", 'The speaker resigns themself to docking at a nearby town.',
           'Retain the resigned first beat and remove the redundant description of the port.'),
    2662: (None, 'The speaker says they will dock at a nearby town.', 'Retain the short, friendly report of the next action.'),
}


def argument_samples(runtime, clean):
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    assert clean[0x6567C:0x6576C] == runtime.arm[0x6567C:0x6576C]
    assert clean[0x77B94:0x77BA8] == runtime.arm[0x77B94:0x77BA8]
    assert clean[CALL - BASE - 4:CALL - BASE + 4] == runtime.arm[CALL - BASE - 4:CALL - BASE + 4]
    for pointer, stored, _ in BEARINGS:
        assert bytes(cpu.mem_read(pointer, len(stored) + 1)) == stored + b'\0'

    def word(address):
        return unpack_from('<I', cpu.mem_read(address, 4))[0]

    names = []
    fleet_root = get(0xCB1A8) + 4
    for index in range(41, 53):
        fleet = fleet_root + index * 132
        if get(0x35320, fleet) != 21:
            continue
        assert cpu.mem_read(fleet + 0x3E, 1) == b'\x08'
        actor = get(0x3697C, fleet)
        getter = word(word(actor) + 0x20)
        pointer = get(getter - BASE, actor)
        name = bytes(cpu.mem_read(pointer, 64)).split(b'\0', 1)[0]
        assert name and name.isascii()
        names.append(dict(fleet_index=index, getter=getter, arguments=[name.hex()]))
    assert any(row['arguments'] == [b'Peralonso'.hex()] for row in names)
    runtime.calls.clear()
    return dict(pirate=names, bearings=[dict(source_pointer=pointer, original_hex=old.hex(),
        localized_hex=english.hex()) for pointer, old, english in BEARINGS])


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
    assert set(DECISIONS) == set(range(2615, 2663))
    arguments = argument_samples(runtime, arm)
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    roster = {i: runtime.actor_root + (0x19E4 if i == 3 else 4 + 32 * i) for i in range(207)}
    voices = {i: get(0x7E988, actor) for i, actor in roster.items()}
    groups, records = [], []
    for start, end, table, callers, kind, context in GROUPS:
        bindings = [prior.caller_binding(arm, runtime.arm, load, call, pool, BASE + table, wrapper)
                    for load, call, pool, wrapper in callers]
        queued = callers[0][3] == QUEUED
        if queued:
            assert BASE + table in TABLES and BASE + QUEUED == WRAPPER
        assert arm[table:table + 32] == runtime.arm[table:table + 32]
        slots = unpack_from('<8i', arm, table)
        assert set(slots) - {-1} == set(range(start, end + 1))
        selections = []
        for i, actor in roster.items():
            expected = start if slots[voices[i]] == -1 else slots[voices[i]]
            assert get(0x53F4C, actor, BASE + table) == expected
            selections.append((i, voices[i], expected))
        substitutions = 2 if queued else int(bool(kind))
        groups.append(dict(first_ID=start, last_ID=end, table=BASE + table, slots=slots, native_callers=bindings,
            original_voice_choices=selections, argument_kind=kind, original_role_argument=7 if queued else None,
            context=context))
        for n in range(start, end + 1):
            jp, old = source[n], current[n]
            text = old.text.decode('cp932')
            paragraph = ' '.join(normalize('NFKC', text).split())
            revision, meaning, note = DECISIONS[n]
            english = revision or paragraph
            assert english.isascii() and english == ' '.join(english.split()) and bool(revision) == (english != paragraph)
            assert jp.text.count(b'%s') == old.text.count(b'%s') == english.count('%s') == substitutions
            assert '%' not in english.replace('%s', '')
            records.append(dict(id=f'COMMON_MESSAGE_{n}', message_ID=n, file_path=COMMON,
                source_reference=prior.reference(jp), current_reference=prior.reference(old),
                source_hex=jp.text.hex(), current_hex=old.text.hex(), source_Japanese=jp.text.decode('cp932'),
                current_English=text, english=english, context=context, native_group_first_ID=start,
                original_slots=[i for i, selected in enumerate(slots) if n == selected],
                speaker='Lookout' if queued else 'Fleet captain selected by the original caller',
                source_meaning=meaning, localization_note=note, decision='revision' if revision else 'retention',
                inherited_fullwidth_Latin=prior.wide_letters(text), original_substitution_count=substitutions,
                source_first_person_macro_localized_as_plural=b'IC' in jp.text,
                review={gate: gate != 'formatting' for gate in prior.GATES}))
    assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    assert [row['message_ID'] for row in records] == list(range(2615, 2663))
    assert {row['message_ID'] for row in records if row['source_first_person_macro_localized_as_plural']} == {2640, 2646, 2652}
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
