"""Review fleet encounters, battle outcomes and month-end finance reports."""

from collections import Counter
from hashlib import sha256
from struct import unpack_from
from unicodedata import normalize

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import checkpoint_sea_event_review_v1 as prior
from scripts import register_crew_item_actions_v1 as parent


BASE, ARM, COMMON, CLEAN = prior.BASE, prior.ARM, prior.COMMON, prior.CLEAN
OUTPUT = prior.ROOT / 'fleet_reports_context_v1.json'
DIRECT, QUEUED = 0x53F0C, 0x53D44
GROUPS = (
    (2533, 2536, 0x117940, 0x2E024, 0x2E03C, 0x2E044, 0x2E0C8, DIRECT, 'company',
     'The original encounter dispatcher reports that our side has spotted the opposing fleet and is going on the attack. '
     'The captain names its company. These lines introduce combat before there is a result.'),
    (2537, 2540, 0x117A00, 0x2E098, 0x2E0B0, 0x2E0B8, 0x2E0CC, DIRECT, 'company',
     'The counterpart encounter branch tells the player that the opposing fleet initiated the attack. '
     'The speaker reports its company name and the immediate danger.'),
    (2541, 2547, 0x117AE0, 0x492B0, 0x492E0, 0x492E4, 0x495B0, DIRECT, 'captain',
     'The winning captain reports the defeat of the opposing fleet and claims victory. '
     'The two fields name the same opposing captain, with the given name first.'),
    (2548, 2552, 0x117BC0, 0x492EC, 0x4931C, 0x49320, 0x495B4, DIRECT, 'captain',
     'The captain reports that the opposing fleet fled. The enemy captain name comes from the same two getters '
     'as the victory report. Flight is a distinct result from defeat.'),
    (2553, 2558, 0x117CE0, 0x49344, 0x49374, 0x49378, 0x495B8, DIRECT, 'captain',
     'The captain acknowledges their fleet was defeated. Both fields identify the opposing captain, '
     'with different reactions to the loss by voice class.'),
    (2559, 2564, 0x117D60, 0x49380, 0x493B0, 0x493B4, 0x495BC, DIRECT, 'captain',
     'The captain explains why their fleet withdrew. The opposing fleet proved unexpectedly tough '
     'or too strong. The outcome is a retreat.'),
    (2565, 2570, 0x117F20, 0x2DD48, 0x2DD5C, 0x2DD64, 0x2DEE4, DIRECT, 'gold',
     'At settlement, a subordinate fleet captain apologizes for a negative result. '
     'The original caller formats the positive magnitude of the loss in gold.'),
    (2571, 2574, 0x117FA0, 0x2DD24, 0x2DD38, 0x2DD40, 0x2DEE0, DIRECT, 'gold',
     'The nonnegative branch of the same settlement reports earnings in gold. '
     'The original caller supplies the displayed result, including zero when applicable.'),
    (2575, 2579, 0x118080, 0x2DD9C, 0x2DDF4, 0x2DDFC, 0x2DEE8, QUEUED, None,
     'When available cash falls short of fleet losses, the settlement exhausts available funds and carries the unpaid portion forward. '
     'After the fleet reports, the role-3 speaker explains the addition to next month’s expenses.'),
)

# Each note refers to the clean line and its branch. A missing replacement retains the English prose.
DECISIONS = {
    2533: ("Fleet sighted! It's %s. We're moving in!", 'The speaker sights the named faction’s fleet and announces the attack.',
           'Keep the alert and immediate action. Let the company name stand alone so labels such as Bergstrom Fleet read naturally.'),
    2534: ("It's %s! We've got their fleet in sight. We're going in!", 'The speaker sights the faction’s fleet and announces the attack.',
           'Keep the rougher voice and both beats of the report. Use the company label without adding a possessive.'),
    2535: ("Fleet sighted! It's %s. Let's go after 'em!", 'The speaker sights the faction’s fleet and calls for an attack.',
           'Keep the decisive order in a plainspoken voice. The native argument is a company label.'),
    2536: ("That's %s out there! Let's attack!", 'The speaker points out the faction’s fleet and eagerly calls for an attack.',
           'Keep the quick sighting and the enthusiastic call to act.'),
    2537: ("We're under attack! It's %s!", 'The speaker reports that the named faction’s fleet initiated the attack.',
           'Open with the urgent report and let the company name identify the attackers.'),
    2538: ("So %s decided to attack us!", 'The speaker reacts with contempt to the opposing fleet initiating the attack.',
           'Make the indignation audible without changing who attacked first.'),
    2539: ("There they go! %s is attacking us!", 'The speaker calls attention to the opposing fleet’s attack.',
           'Preserve the exclamatory, plainspoken warning and the direction of the attack.'),
    2540: ("It's %s! They're attacking!", 'The speaker urgently reports that the named faction has attacked.',
           'Keep the alert brisk and use the native faction name as the identification.'),
    2541: ("We've defeated %s %s's fleet! The victory is ours!", 'The speaker announces the named captain’s fleet was defeated and claims victory.',
           'Give the formal victory report both beats and join the two captain name fields.'),
    2542: ("We defeated %s %s's fleet. We won.", 'The speaker reports the defeat of the named fleet and the victory in an even tone.',
           'Use a measured report that preserves both statements and the original subdued punctuation.'),
    2543: ("We beat %s %s's fleet! We did it!", 'The speaker celebrates their side defeating the named fleet.',
           'Render the source first-person plural naturally and join the given name and surname without a slash.'),
    2544: (None, 'The speaker reports that they defeated the named captain’s fleet and that they won.',
           'Retain the direct statement and the short, elated claim of victory.'),
    2545: ("We beat %s %s's fleet! Victory's ours!", 'The speaker boasts that their side defeated the named fleet and won.',
           'Keep the triumphant second beat and remove the separator between the two name fields.'),
    2546: ("We've beaten %s %s's fleet! The day is ours!", 'The speaker celebrates defeating the named fleet.',
           'Carry the older voice in the victory idiom and preserve the named captain.'),
    2547: ("We beat %s %s's fleet! We really won!", 'The speaker excitedly realizes their side defeated the named fleet and won.',
           'Preserve the younger voice’s emphatic second thought and keep the name intact.'),
    2548: ("%s %s's fleet has fled!", 'The speaker reports that the named captain’s fleet fled.',
           'Identify the captain with an ordinary full name and keep the clipped flight report.'),
    2549: (None, 'The speaker reports that the named captain’s fleet fled.',
           'Retain the even delivery and exact ownership of the fleet.'),
    2550: (None, 'The speaker exclaims that the named captain’s fleet ran away.',
           'Retain the blunt colloquial wording and the completed retreat.'),
    2551: ("%s %s's fleet turned tail!", 'The speaker exclaims that the named fleet fled.',
           'Use an older, plainspoken idiom without implying the fleet was destroyed.'),
    2552: (None, 'The speaker exclaims that the named captain’s fleet ran away.',
           'Retain the quick, excited report of the result.'),
    2553: (None, 'The speaker says their fleet was defeated by the named opposing captain’s fleet.',
           'Retain the formal acknowledgment and trailing disappointment.'),
    2554: ("We lost to %s %s's fleet...", 'The speaker acknowledges that their side was beaten by the named fleet.',
           'Render the first-person plural directly and preserve the deflated tone.'),
    2555: ("%s %s's fleet defeated us...", 'The speaker reports that the named captain’s fleet defeated them.',
           'Keep a direct admission of defeat and treat the two arguments as one name.'),
    2556: ("%s %s's fleet got the better of us...", 'The speaker ruefully reports defeat by the named fleet.',
           'Use a spoken admission while preserving that the opposing fleet prevailed.'),
    2557: ("%s %s's fleet has beaten us...", 'The speaker regrets their side’s defeat by the named fleet.',
           'Keep the subdued older voice and the opponent’s full name.'),
    2558: ("We got beaten by %s %s's fleet...", 'The speaker glumly admits the named fleet beat them.',
           'Keep the younger, informal voice and the named opponent.'),
    2559: ("%s %s's fleet was tougher than we expected. We had to retreat...",
           'The opposing fleet was tougher than expected, and the speaker’s side withdrew.',
           'Give the comparison and the withdrawal their own sentences and join the captain name fields.'),
    2560: ("%s %s's fleet was tougher than we thought. We pulled back...",
           'The opposing fleet was tougher than the speaker expected, and their side withdrew.',
           'Use a spoken report of their own retreat and keep the first-person plural.'),
    2561: ("%s %s's fleet was too strong for us. We pulled back...",
           'The opponent was very formidable, and the speaker’s fleet withdrew.',
           'Keep the strength judgment without inserting a comparison to expectations and restore the trailing tone.'),
    2562: ("%s %s's fleet put up more of a fight than we expected. We had to retreat...",
           'The opposing fleet was tougher than expected, and the speaker’s side withdrew.',
           'Keep the informal evaluation and the cause of the retreat.'),
    2563: ("%s %s's fleet was stronger than expected. We withdrew...",
           'The named fleet was stronger than anticipated, so the speaker’s fleet withdrew.',
           'Keep the measured phrasing and both beats without a slash in the name.'),
    2564: ("%s %s's fleet was stronger than we thought. We ran...",
           'The speaker says the opponent was stronger than expected and admits their fleet ran away.',
           'Keep the rueful admission of flight in the younger voice.'),
    2565: ("My apologies. We lost %s in gold.", 'The speaker formally apologizes for the stated loss in gold.',
           'Keep the apology and exact loss. The currency expression works with either one gold or a larger amount.'),
    2566: ("I'm sorry. We lost %s in gold.", 'The speaker apologizes that they lost the stated amount of gold.',
           'Retain the personal apology with an ASCII I and use a currency expression that also works for one.'),
    2567: (None, 'The speaker apologizes that they lost the stated amount of gold.',
           'Retain the short apology and established in-game currency wording.'),
    2568: ("Sorry about that. We lost %s gold.", 'The speaker apologizes for the loss of the stated amount.',
           'Keep the less formal cadence and the exact amount without requiring plural agreement.'),
    2569: ("I'm sorry about the loss. It cost us %s gold.", 'The speaker regrets the stated loss in gold.',
           'Replace the bureaucratic phrasing with a spoken regret and use the normal ASCII I.'),
    2570: ("Sorry! I cost you %s gold...", 'The speaker apologizes for causing the addressee a loss of that much gold.',
           'Keep the personal responsibility and the emphasis on what it cost the addressee.'),
    2571: ("We made %s in gold.", 'The speaker reports the exact amount earned in gold.',
           'Keep a straightforward financial report and the runtime amount, including zero.'),
    2572: (None, 'The speaker reports the amount earned in gold.',
           'Retain the short, matter-of-fact report and exact currency amount.'),
    2573: ("That earned us %s gold.", 'The speaker reports the amount they managed to earn.',
           'Keep a compact, plainspoken report in the older voice.'),
    2574: ("We made %s gold! Hehe!", 'The speaker excitedly reports the amount earned, then chuckles.',
           'Keep both the amount and the delighted laugh, with a currency expression that works for any amount.'),
    2575: ("We can't cover the loss with the money on hand. The balance will go into next month's expenses.",
           'Available cash cannot cover the loss, so the unpaid amount is carried into next month’s expenses.',
           'Keep the formal explanation, next-month timing and actual remainder.'),
    2576: ("We don't have enough cash to cover the loss. We'll carry the rest over to next month's expenses.",
           'There is not enough cash to settle the loss, so the remaining amount will count as an expense next month.',
           'Keep the explanatory tone and use a natural first-person commitment to carry it over.'),
    2577: ("We're short on gold. We'll put the rest down as an expense for next month.",
           'There is not enough gold to cover the loss, so the balance goes into next month’s expenses.',
           'Keep the blunt opening and the bookkeeping action.'),
    2578: ("We haven't enough gold to cover the loss. Best carry the balance over to next month's expenses.",
           'The speaker observes a shortfall and suggests carrying the unpaid loss into next month’s expenses.',
           'Keep the reflective older voice and the tentative decision.'),
    2579: ("We can't cover the loss. We'll add the rest to next month's expenses.",
           'The speaker says they cannot cover the loss and will record the unpaid amount for next month.',
           'Keep the colloquial delivery and make the unpaid remainder explicit.'),
}


def argument_samples(runtime, source):
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    for start, end in ((0x352F4, 0x35320), (0x3697C, 0x369AC), (0xABF50, 0xABFCC)):
        assert source[start:end] == runtime.arm[start:end]

    def word(address):
        return unpack_from('<I', cpu.mem_read(address, 4))[0]

    def string(pointer):
        if not pointer:
            return b''
        assert BASE <= pointer <= BASE + 0x400000 - 64
        return bytes(cpu.mem_read(pointer, 64)).split(b'\0', 1)[0]

    def field(obj, slot):
        getter = word(word(obj) + slot)
        return getter, string(get(getter - BASE, obj))

    owners, captains, amounts = [], [], []
    root = get(0xCB1A8) + 4
    for index in range(63):
        fleet = root + index * 132
        company = get(0x352F4, fleet)
        if company:
            getter, text = field(company, 8)
            if text:
                owners.append(dict(fleet_index=index, getter=getter, arguments=[text.hex()]))
        actor = get(0x3697C, fleet)
        if actor:
            given, family = field(actor, 0x20), field(actor, 0x24)
            if given[1] and family[1]:
                captains.append(dict(fleet_index=index, getters=[given[0], family[0]],
                                     arguments=[given[1].hex(), family[1].hex()]))
    for value in (0, 1, 10, 10000, 99999999, 0x7FFFFFFF):
        text = string(get(0xABF50, value))
        assert normalize('NFKC', text.decode('cp932')) == str(value)
        amounts.append(dict(value=value, getter=BASE + 0xABF50, arguments=[text.hex()]))
    assert any(row['arguments'] == [b'Bergstrom Fleet'.hex()] for row in owners)
    assert any(row['arguments'] == [b'Maria'.hex(), b'Li'.hex()] for row in captains)
    runtime.calls.clear()
    return dict(company=owners, captain=captains, gold=amounts)


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
    assert set(DECISIONS) == set(range(2533, 2580))
    arguments = argument_samples(runtime, arm)
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    roster = {i: runtime.actor_root + (0x19E4 if i == 3 else 4 + 32 * i) for i in range(207)}
    voices = {i: get(0x7E988, actor) for i, actor in roster.items()}
    groups, records = [], []
    for start, end, table, prefix, load, call, pool, wrapper, kind, context in GROUPS:
        binding = prior.caller_binding(arm, runtime.arm, load, call, pool, BASE + table, wrapper)
        assert arm[prefix:call + 4] == runtime.arm[prefix:call + 4]
        assert arm[table:table + 32] == runtime.arm[table:table + 32]
        slots = unpack_from('<8i', arm, table)
        assert set(slots) - {-1} == set(range(start, end + 1))
        selections = []
        for i, actor in roster.items():
            expected = start if slots[voices[i]] == -1 else slots[voices[i]]
            assert get(0x53F4C, actor, BASE + table) == expected
            selections.append((i, voices[i], expected))
        substitutions = 2 if kind == 'captain' else int(bool(kind))
        groups.append(dict(first_ID=start, last_ID=end, table=BASE + table, slots=slots,
            native_callers=[binding], original_voice_choices=selections, argument_kind=kind,
            original_role_argument=3 if wrapper == QUEUED else None,
            argument_prefix=dict(start=BASE + prefix, exact_hex=arm[prefix:call + 4].hex()), context=context))
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
                speaker='Crew member selected by the original accounting role' if wrapper == QUEUED else
                        'Fleet captain selected by the original dispatcher',
                source_meaning=meaning, localization_note=note, decision='revision' if revision else 'retention',
                inherited_fullwidth_Latin=prior.wide_letters(text), original_substitution_count=substitutions,
                source_first_person_macro_localized_as_plural=b'IC' in jp.text,
                review={gate: gate != 'formatting' for gate in prior.GATES}))
    assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    assert [row['message_ID'] for row in records] == list(range(2533, 2580))
    assert {row['message_ID'] for row in records if row['source_first_person_macro_localized_as_plural']} == {2543, 2554, 2560}
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
