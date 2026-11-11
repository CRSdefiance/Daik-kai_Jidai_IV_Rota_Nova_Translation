"""Bind shared item-use and crew-management replies to their original callers."""

from collections import Counter
from hashlib import sha256
from struct import unpack_from
from unicodedata import normalize

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import checkpoint_sea_event_review_v1 as prior
from scripts import register_sailing_reactions_v1 as parent


BASE, ARM, COMMON, CLEAN = prior.BASE, prior.ARM, prior.COMMON, prior.CLEAN
OUTPUT = prior.ROOT / 'crew_item_actions_context_v1.json'
DIRECT, QUEUED, CAPTAIN = 0x53F0C, 0x53D44, 0x53BD8
GROUPS = (
    (2500, 2504, 0x117320, ((0x406B0, 0x406B8, 0x406E0, DIRECT),),
     'When removing an item would leave a crew member unable to do their assigned work, '
     'that crew member objects to the admiral. The action is rejected.'),
    (2505, 2508, 0x117380, ((0x4BAA0, 0x4BAA8, 0x4BAB4, QUEUED), (0x4BDC4, 0x4BDCC, 0x4BDE8, QUEUED),
     (0x4BEAC, 0x4BEB4, 0x4BED0, QUEUED), (0x4BFB8, 0x4BFC0, 0x4BFE0, QUEUED),
     (0x4C17C, 0x4C184, 0x4C1A0, QUEUED)),
     'The player tries to use an item, but the current situation does not call for it. '
     'The role-1 crew reply explains why there is no need to use it now.'),
    (2509, 2511, 0x117520, ((0x4BF88, 0x4BF90, 0x4BFD8, DIRECT), (0x4C098, 0x4C0A0, 0x4C19C, DIRECT),
     (0x4C130, 0x4C138, 0x4C19C, DIRECT), (0x4C164, 0x4C16C, 0x4C19C, QUEUED)),
     'The successful item-use branch reports that the sailors received the selected remedy. '
     'The original caller supplies its catalogue name.'),
    (2512, 2515, 0x1175E0, ((0x4BE98, 0x4BEA0, 0x4BECC, QUEUED), (0x4BFA0, 0x4BFA8, 0x4BFDC, QUEUED)),
     'The item could help with the current condition, but the required crew member is unavailable. '
     'The role-1 reply says nobody knows how to use it.'),
    (2516, 2519, 0x117660, ((0x4BE38, 0x4BE48, 0x4BEC8, DIRECT),),
     'The assigned crew member voices a plea for divine anger to subside while using Hermes’ Prayer. '
     'The game then clears the fleet condition.'),
    (2520, 2523, 0x117700, ((0x4BD14, 0x4BD24, 0x4BDE4, DIRECT), (0x4BD8C, 0x4BD9C, 0x4BDE4, DIRECT),
     (0x4BDAC, 0x4BDB4, 0x4BDE4, QUEUED)),
     'The item action uses the Golden Cat. These lines announce that the cat took care of the rats. '
     'The direct and role-1 paths share the result table.'),
    (2524, 2528, 0x1177A0, ((0x1DCE4, 0x1DCEC, 0x1DD48, QUEUED),),
     'When dismissing all the sailors would leave the ship unable to sail, a role-1 crew reply warns the player. '
     'The branch rejects the action.'),
    (2529, 2532, 0x116740, ((0x406A4, 0x406A8, 0x406DC, CAPTAIN),),
     'The item-removal rejection uses this separate table when the person who needs the item is the player admiral. '
     'The speaker catches themself or states why they need to keep it.'),
)

DECISIONS = {
    2500: ("Admiral, I can't do my job if you take that away.",
           'The speaker tells the admiral that taking the item will prevent them from doing their work.',
           'Keep the direct address and replace the vague “my work is done for” with the practical consequence.'),
    2501: (None, 'The speaker tells the admiral they will be unable to do their job if the item is taken.',
           'Retain the clear condition and polite phrasing. Render the pronoun with the normal ASCII glyph.'),
    2502: ("Admiral, I can't do my job without that.",
           'The speaker bluntly tells the admiral that they cannot work if the item is taken.',
           'Restore the address and keep the objection blunt.'),
    2503: ("Hm? I can't do my job if you take that away.",
           'The speaker reacts with a puzzled sound, then says they cannot work if the item is taken.',
           'Restore the puzzled opening and use a plainspoken conditional.'),
    2504: ("Admiral, I won't be able to do my job if you take that!",
           'The speaker protests that they will not be able to work if the admiral takes the item.',
           'Keep the personal protest and restore who is taking the item.'),
    2505: (None, 'The speaker sees no apparent need to use the item right now.',
           'Retain the tentative judgment and the immediate time frame.'),
    2506: (None, 'The speaker asks whether they can do without using the item for now.',
           'Retain the inclusive, conversational question and its short tag.'),
    2507: ('No need to use it just yet.', 'The speaker judges that it is fine to leave the item unused for now.',
           'Keep the unhurried voice and make the temporary judgment concise.'),
    2508: ("Doesn't look like we need it right now, though...",
           'The speaker tentatively points out that the item seems unnecessary right now.',
           'Restore the crew’s perspective. The source does not identify an outside group that might need it.'),
    2509: (None, 'The speaker reports having given the named item to the sailors.',
           'Retain the straightforward report and the exact runtime item slot.'),
    2510: (None, 'The speaker reports having given the named item to the sailors.',
           'Retain the short report with the item as the direct object and the sailors as recipients.'),
    2511: ('We gave the sailors %s!', 'The speaker lets the player know the sailors received the named item.',
           'Keep the simple report and let the delivery sound brighter than the formal variant.'),
    2512: (None, 'The speaker says nobody knows how to use the item.',
           'Retain the unambiguous explanation.'),
    2513: ('How do you use this? Looks like nobody knows.',
           'The speaker asks how to use it, then observes that nobody seems to know.',
           'Keep the question and reply as two spoken thoughts. Remove the abstract reference to an answer.'),
    2514: ("What's that? Seems no one knows how to use it.",
           'The speaker asks what the item is and observes that nobody seems to know how to use it.',
           'Keep the opening surprise and the separate uncertainty about using the item.'),
    2515: ('How does it work? Nobody seems to know.',
           'The speaker asks how to use the item and concludes that nobody seems to know.',
           'Keep the light spoken question and the tentative follow-up.'),
    2516: ('O God, please let your anger pass!',
           'The speaker calls on God and begs for divine anger to subside.',
           'Keep the solemn invocation and make the plea speakable.'),
    2517: ('Please, God, let your anger pass!',
           'The speaker addresses God directly and asks for the anger to subside.',
           'Make this a direct prayer. “Please be calm” reads like advice to a person.'),
    2518: ('O God, let your anger pass, I beg you!',
           'The speaker implores God to quiet divine anger in an old-fashioned register.',
           'Use a solemn cadence and a personal plea to carry the older voice.'),
    2519: ("Please, God! Don't be angry!",
           'The speaker begs God not to be angry.',
           'Retain the plain, urgent plea in two short spoken beats.'),
    2520: (None, 'The speaker reports that the cat got rid of the rats for them.',
           'Retain the clear result and both animals.'),
    2521: ('The cat took care of the rats!', 'The speaker announces that the cat got rid of the rats.',
           'Keep the result and give the announcement a livelier voice.'),
    2522: (None, 'The speaker reports that they had the cat get rid of the rats.',
           'Retain the crew’s agency in putting the cat to work.'),
    2523: ('The cat got those rats!', 'The speaker announces that the cat beat the rats.',
           'Keep the excited result without specifying how the cat dispatched them.'),
    2524: ("If you dismiss all the sailors, we can't sail!",
           'The speaker warns that dismissing the entire crew would leave the ship unable to sail.',
           'Restore the proposed action and make the practical consequence explicit.'),
    2525: ("Admiral! If you fire every sailor, we can't sail!",
           'The speaker protests to the admiral that firing all the sailors would make sailing impossible.',
           'Preserve the alarm and use “fire” for the colloquial dismissal verb.'),
    2526: (None, 'The speaker tells the admiral that dismissing every sailor will make it impossible to sail the ship.',
           'Retain the full warning and direct address. Use the native layout to place the breaks.'),
    2527: ("Hold on. If you dismiss all the sailors, the ship won't go anywhere!",
           'The speaker interrupts to warn that the ship cannot move if all the sailors are dismissed.',
           'Keep the cautionary interruption and the ship as the subject of the consequence.'),
    2528: ("Who's gonna sail if you let everyone go? I can't do it alone!",
           'The speaker asks who would sail the ship and protests that they cannot do it on their own.',
           'Restore the speaker’s inability to sail alone and preserve the informal voice.'),
    2529: ('Wait... I need this to do my job.',
           'The speaker catches themself and remembers that they need the item to work.',
           'Retain the moment of recognition and restore the speaker’s pronoun.'),
    2530: (None, 'The speaker says they cannot do their job without the item.',
           'Retain the direct statement. Render the pronoun with the normal ASCII glyph.'),
    2531: ('Oh, right. I need this to do my job.',
           'The speaker catches themself and remembers they need the item to do their work.',
           'Let the opening convey a reminder in the speaker’s own voice.'),
    2532: ("I can't do my job without this.",
           'The speaker says they cannot do their job without the item.',
           'Restore the subject and keep the matter-of-fact statement.'),
}


def item_arguments(runtime, clean):
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    root = get(0xCB190) + 4
    result = []
    for slot, expected in ((21, 'Lime Drops'), (23, "Hua Tuo's Tonic")):
        item = root + 20 * slot
        vtable = unpack_from('<I', cpu.mem_read(item, 4))[0]
        getter = unpack_from('<I', cpu.mem_read(vtable + 8, 4))[0]
        assert getter == BASE + 0x4A53C
        assert clean[0x4A53C:0x4A548] == runtime.arm[0x4A53C:0x4A548]
        pointer = get(getter - BASE, item)
        value = bytes(cpu.mem_read(pointer, 64)).split(b'\0', 1)[0]
        assert value.decode('ascii') == expected
        result.append(dict(slot=slot, item_name=expected, getter=getter, value_hex=value.hex()))
    runtime.calls.clear()
    return result


def main():
    assert not OUTPUT.exists()
    release = prior.load(parent.RELEASE)
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
    assert set(DECISIONS) == set(range(2500, 2533))
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    roster = {i: runtime.actor_root + (0x19E4 if i == 3 else 4 + 32 * i) for i in range(207)}
    voices = {i: get(0x7E988, actor) for i, actor in roster.items()}
    arguments = item_arguments(runtime, arm)
    groups, records = [], []
    for start, end, table, callers, context in GROUPS:
        bindings = [prior.caller_binding(arm, runtime.arm, load, call, pool, BASE + table, wrapper)
                    for load, call, pool, wrapper in callers]
        captain = callers[0][3] == CAPTAIN
        count = 4 if captain else 8
        raw = arm[table:table + 4 * count]
        assert raw == runtime.arm[table:table + 4 * count]
        slots = unpack_from(f'<{count}i', raw)
        assert set(slots) - {-1} == set(range(start, end + 1))
        selections = []
        if captain:
            assert get(0x53C6C, BASE + table) == slots[3]
        else:
            for i, actor in roster.items():
                expected = start if slots[voices[i]] == -1 else slots[voices[i]]
                assert get(0x53F4C, actor, BASE + table) == expected
                selections.append((i, voices[i], expected))
        substitutions = arguments if start == 2509 else []
        groups.append(dict(first_ID=start, last_ID=end, table=BASE + table, slots=slots,
            native_callers=bindings, original_voice_choices=selections, current_captain_selection=slots[3] if captain else None,
            runtime_item_name_inputs=substitutions, context=context))
        for number in range(start, end + 1):
            jp, old = source[number], current[number]
            old_text = old.text.decode('cp932')
            paragraph = ' '.join(normalize('NFKC', old_text).split())
            revision, meaning, note = DECISIONS[number]
            english = revision or paragraph
            assert english.isascii() and english == ' '.join(english.split())
            assert bool(revision) == (english != paragraph)
            assert jp.text.count(b'%s') == old.text.count(b'%s') == english.count('%s') == bool(substitutions)
            assert '%' not in english.replace('%s', '')
            records.append(dict(id=f'COMMON_MESSAGE_{number}', message_ID=number, file_path=COMMON,
                source_reference=prior.reference(jp), current_reference=prior.reference(old),
                source_hex=jp.text.hex(), current_hex=old.text.hex(), source_Japanese=jp.text.decode('cp932'),
                current_English=old_text, english=english, context=context, native_group_first_ID=start,
                original_slots=[i for i, selected in enumerate(slots) if number == selected],
                speaker='Player admiral' if captain else 'Crew member selected by the original caller',
                source_meaning=meaning, localization_note=note, decision='revision' if revision else 'retention',
                inherited_fullwidth_Latin=prior.wide_letters(old_text), original_substitution_count=int(bool(substitutions)),
                review={gate: gate != 'formatting' for gate in prior.GATES}))
    assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    assert [row['message_ID'] for row in records] == list(range(2500, 2533))
    counts = Counter(row['decision'] for row in records)
    prior.save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=prior.GATES, records=records,
        registered_input=runtime.receipt(), source_ROM_sha256=release['clean_input_sha256'], native_context=groups,
        original_offline_actor_selections=sum(len(group['original_voice_choices']) for group in groups),
        counts=dict(counts), formatting_pending=True, gameplay_pending=True, new_credit=0, full_goal_complete=False))
    print(f'{len(records)} editorial decisions {dict(counts)} across {len(groups)} original tables.')


if __name__ == '__main__':
    main()
