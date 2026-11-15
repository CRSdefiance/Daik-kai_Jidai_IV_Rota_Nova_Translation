"""Review captain reprimands and original shore-expedition outcomes."""

from collections import Counter
from hashlib import sha256
from struct import unpack_from
from unicodedata import normalize

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import checkpoint_sea_event_review_v1 as prior
from scripts import register_battle_commands_and_outcomes_v1 as parent


BASE, ARM, COMMON, CLEAN = prior.BASE, prior.ARM, prior.COMMON, prior.CLEAN
OUTPUT = prior.ROOT / 'crew_and_shore_reports_context_v1.json'
CAPTAIN, ROLE = 0x53BD8, 0x53D44
GROUPS = (
    (2193, 2196, 0x116720, 0x13A08, 0x13A0C, 0x13B74, CAPTAIN, None,
     'The captain reacts to noticing something off aboard ship. The original routine then inspects the crew slots '
     'and plays the crew interruption before the same captain speaks again.'),
    (2197, 2200, 0x116570, 0x13B60, 0x13B64, 0x13B8C, CAPTAIN, None,
     'The same captain calls out the crew for slacking. Preserve each protagonist’s reaction and reprimand as a pair, '
     'including the last captain’s irony rather than treating it as praise.'),
    (2222, 2228, 0x116EA0, 0x79D48, 0x79D50, 0x79FD4, ROLE, 7,
     'The lookout or original fallback announces the shore expedition’s find. The original item presentation follows '
     'and identifies it. This speech has no runtime item name.'),
    (2234, 2238, 0x116E60, 0x795E0, 0x795E8, 0x79698, ROLE, 1,
     'The First Mate or fallback passes on a friendly invitation from the local people and urges the captain to go. '
     'The original event can then show the separate gift of food and water.'),
    (2239, 2242, 0x116E40, 0x7960C, 0x79614, 0x7969C, ROLE, 1,
     'The officer reports that the local people shared food and water after the friendly welcome. Quantities and '
     'the replenishment belong to the original effect, outside the spoken report.'),
    (2243, 2249, 0x116E20, 0x7965C, 0x79664, 0x796A0, ROLE, 1,
     'A separate outcome reports that the expedition was attacked by local people. The original crew-loss routine '
     'may show a later count. The younger voice’s line about being eaten is their own dark joke.'),
    (2250, 2257, 0x116E00, 0x79530, 0x79538, 0x79598, ROLE, 1,
     'The empty search turns into a discovery that sailors have deserted. Some voices start preparing to leave, then '
     'interrupt themselves. The original crew-loss notice follows and does not specify a cause or death.'),
    (2258, 2263, 0x116920, 0x79424, 0x7942C, 0x79508, ROLE, 1,
     'The officer reports that wild animals attacked the shore expedition. Some voices relay the news or express '
     'uncertainty. A later original branch can report disease on board after the attack.'),
    (2264, 2268, 0x116DC0, 0x794C8, 0x794D0, 0x79518, ROLE, 7,
     'The lookout or fallback reports that disease has spread aboard the ship. The expedition’s earlier animal '
     'attack supplies the connection, with the level of certainty expressed by each voice.'),
    (2269, 2274, 0x116DA0, 0x793C8, 0x793D0, 0x793F8, ROLE, 1,
     'The officer reports that the expedition was caught in quicksand. The original loss effect follows separately. '
     'The spoken reports do not say the whole party sank or died.'),
)

DECISIONS = {
    2193: (None, 'A puzzled pause as the captain notices something.', 'Keep the hesitant start leading into the sharp reprimand.'),
    2194: (None, 'The captain responds with a short, questioning grunt.', 'Keep the compact reaction before the stern follow-up.'),
    2195: (None, 'The captain cries out in recognition.', 'Keep the sudden, audible reaction before the rebuke.'),
    2196: (None, 'The captain reacts silently with visible puzzlement.', 'Keep the wordless pause before the dry sarcasm.'),
    2197: (None, 'The captain calls for attention and tells the crew to stop slacking.', 'Keep the natural shout and direct command.'),
    2198: ("Shouldn't you be working? There's no time to fool around.", 'The captain asks about the crew’s work and says there is no time to play.', 'Make the question a natural rebuke followed by the reason.'),
    2199: (None, 'The captain calls the crew out and asks what they are doing.', 'Keep the drawn-out protest’s emotional effect with a brisk exclamation.'),
    2200: ('My, you have time to spare. Must be nice.', 'The captain sarcastically remarks on their apparent leisure and privileged position.', 'Keep the polite opening and unmistakably dry follow-up.'),
    2222: (None, 'The lookout addresses the admiral and says the expedition found something.', 'Keep the clear introduction to the item that follows.'),
    2223: ('What a find! Look what the expedition turned up.', 'The lookout calls it a major discovery and draws attention to the find.', 'Use the language of a spoken announcement.'),
    2224: (None, 'The lookout is excited about what the expedition found.', 'Keep the immediate excitement and explicit finder.'),
    2225: ('Admiral, a big find! Look what the expedition found!', 'The lookout addresses the admiral and excitedly points out the expedition’s discovery.', 'Keep the quick, rough delivery and restore who found it.'),
    2226: ('Admiral, what a discovery! Look what the expedition found!', 'The lookout celebrates the expedition’s major find.', 'Restore the finder and use a complete older-voice exclamation.'),
    2227: ('Wow, what a find! Admiral, look what the expedition found!', 'The lookout excitedly addresses the admiral and shows the expedition’s find.', 'Use the youthful outburst and restore the expedition.'),
    2228: ('Wonderful! Look what the expedition found!', 'The lookout praises the expedition’s discovery.', 'Keep the measured exclamation and name the finder.'),
    2234: ("The locals sound friendly. They say we're welcome. Let's go, Admiral!", 'The officer has heard that the friendly local people will welcome them and urges the admiral to go.', 'Keep the reported welcome and make the invitation flow in speech.'),
    2235: ("I hear the locals are kind and want to welcome us. Come on, let's go!", 'The officer reports a welcome from kind local people and urges the others to go.', 'Use the ordinary dialogue I and a friendly spoken invitation.'),
    2236: (None, 'The officer passes on word of a friendly welcome and suggests going.', 'Keep the reported nature of the invitation and the direct address.'),
    2237: ("It seems the locals are friendly and will welcome us. Shall we go now, Admiral?", 'The officer thinks the friendly local people will receive them and suggests going at once.', 'Use ordinary ASCII and preserve the older voice’s suggestion.'),
    2238: ("The kind folks here invited us. Come on, Admiral, let's go!", 'The officer reports the kind local people’s invitation and urges the admiral to go now.', 'Use warm, eager speech without turning the people into a category label.'),
    2239: ('The locals shared food and water with us.', 'The officer reports the local people shared both food and water.', 'Use the same respectful description as the preceding welcome and name the recipients.'),
    2240: (None, 'The officer says the local people shared food and water with them.', 'Keep the natural, appreciative follow-up.'),
    2241: (None, 'The officer announces that the local people gave them food and water.', 'Keep the spoken gratitude and both kinds of supplies.'),
    2242: (None, 'The officer says the local people shared their food and water.', 'Keep the friendly report and the idea of sharing.'),
    2243: ('Bad news! The locals attacked our expedition!', 'The officer warns that local people attacked the expedition.', 'Use the formal alarm and keep the actors and target explicit.'),
    2244: ('The locals attacked the expedition!', 'The officer directly reports the attack.', 'Keep the terse delivery and the same descriptive wording as the welcome branch.'),
    2245: ('This is bad! They say the locals attacked the expedition!', 'The officer sounds alarmed and relays the reported attack.', 'Restore the warning and the fact that the officer heard the report.'),
    2246: ('Admiral, trouble! The locals attacked our party!', 'The officer calls out to the admiral and reports the expedition was attacked.', 'Preserve the immediate alarm in a rough, direct voice.'),
    2247: ('The locals attacked our expedition! The scoundrels!', 'The officer reports the attack and angrily condemns the attackers.', 'Keep the speaker’s anger aimed at the people who attacked the party.'),
    2248: ('They say the locals attacked our party! At least nobody got eaten!', 'The officer relays the attack and blurts out relief that nobody was eaten.', 'Restore the reported attack and keep the youthful dark joke as speech.'),
    2249: (None, 'The officer reports the local people attacked their expedition.', 'Keep the formal and complete warning.'),
    2250: ("Looks like the expedition found nothing. Wait! Admiral, some of our sailors have deserted!", 'The officer says the search appears fruitless, then notices some sailors deserted.', 'Restore the abrupt interruption and use a consistent English glyph for the opening.'),
    2251: ('No discoveries. Prepare to leave... What?! Admiral, some sailors have deserted!', 'The officer gives departure orders, then informs the admiral that some sailors deserted.', 'Keep the terse order and restore the direct address.'),
    2252: ('Looks like they found nothing. Wait! Sailors are missing! They deserted!', 'The officer first sees no discoveries, then notices missing sailors and declares desertion.', 'Preserve the moment when missing crew becomes the explanation.'),
    2253: ("Looks like they found nothing. Shall we go, then? Wait! I think some of the sailors deserted!", 'The officer suggests leaving, then realizes some sailors seem to have deserted.', 'Keep the tentative realization and an audible change of subject.'),
    2254: (None, 'The officer says the search apparently found nothing, orders departure and reports some sailors ran off.', 'Keep the rough “ran off,” the interrupted order and the direct address.'),
    2255: (None, 'The officer says the search seems empty and some sailors appear to have deserted.', 'Keep the measured uncertainty and the sudden change from departure to desertion.'),
    2256: ("They say they found nothing. Let's go... Wait! We're short some sailors! They ran off!", 'The officer relays the empty search, then notices the smaller crew and says the missing sailors deserted.', 'Restore the evidence the young speaker notices before drawing the conclusion.'),
    2257: ("The expedition seems to have found nothing. Well, let's be off... What?! Some sailors have deserted!", 'The officer suggests departure after the empty search, then reports desertion.', 'Keep the formal lead-in and the contrast with the sudden alarm.'),
    2258: ('It looks like wild animals attacked the expedition!', 'The officer says the expedition appears to have been attacked by wild animals.', 'Restore the uncertainty in a complete spoken warning.'),
    2259: ('Wild animals attacked our party!', 'The officer exclaims that wild animals attacked the expedition.', 'Use the urgent spoken report with a clear subject.'),
    2260: ('Admiral! It looks like wild animals attacked our party!', 'The officer warns the admiral of an apparent attack by wild animals.', 'Restore the direct address and uncertainty.'),
    2261: ('Admiral! Wild animals attacked our party!', 'The officer calls to the admiral and reports the attack.', 'Restore the alarm and the rough voice’s directness.'),
    2262: ('Admiral! They say wild animals attacked our party!', 'The officer relays the report of an attack by wild animals.', 'Keep the direct address and the hearsay.'),
    2263: (None, 'The officer states that wild beasts attacked the expedition.', 'Keep the emphatic and complete report in the older formal voice.'),
    2264: ('Admiral, disease is spreading through the ship! It seems the expedition caught it when the animals attacked!', 'The officer reports shipwide disease and suspects the party caught it during the attack.', 'Use standard-width English glyphs and preserve the tentative source of the disease.'),
    2265: ('Admiral, sickness is spreading all over the ship! Looks like the party caught it when those animals attacked!', 'The officer says the disease is widespread and apparently came from the attacked party.', 'Keep the familiar delivery and the uncertainty.'),
    2266: ('Disease has spread all through the ship! Looks like the expedition caught it when those beasts attacked!', 'The officer says the disease has spread throughout the ship and the expedition apparently caught it in the attack.', 'Keep the emphatic report and the tentative explanation.'),
    2267: ('This is bad! People are sick all over the ship! They say it spread from the party the animals attacked!', 'The officer reports shipwide disease and relays that it came from the attacked party.', 'Restore the urgency, the spread aboard ship and the reported cause.'),
    2268: ('This is serious! Disease has spread throughout the ship! It came from the expedition the beasts attacked!', 'The officer says the shipwide disease spread from the expedition after it was attacked.', 'Restore the full report and keep this voice’s confidence in the connection.'),
    2269: ('The expedition was caught in quicksand!', 'The officer says the expedition was caught in quicksand.', 'Keep the danger without implying that the whole party sank.'),
    2270: (None, 'The officer says the expedition seems to be trapped in quicksand.', 'Keep the native report’s uncertainty.'),
    2271: (None, 'The officer calls to the admiral and says the party is in quicksand.', 'Keep the natural urgency and full address.'),
    2272: (None, 'The officer urgently reports the party is in quicksand.', 'Keep the rough voice’s short, direct warning.'),
    2273: (None, 'The officer exclaims that the party is in quicksand.', 'Keep the plain report without inventing an outcome.'),
    2274: ('Oh no! The expedition got caught in quicksand!', 'The officer cries out that the expedition got caught in quicksand.', 'Restore the younger voice’s alarm and retain the danger without implying death.'),
}


def main():
    assert not OUTPUT.exists()
    release = prior.load(parent.RELEASE)
    assert parent.base.digest(parent.base.REGISTRY) == release['registry_sha256']
    assert prior.digest(CLEAN) == release['clean_input_sha256']
    runtime = prior.RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    clean = parent.base.NdsImage.open(CLEAN)
    arm = clean.read_file(ARM)
    source = common_message_entries(clean.read_file(COMMON), arm)
    directory = sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    current = owned_entries(runtime.common, runtime.arm, directory)
    ledger = prior.load(parent.base.LEDGER)
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    credited = {row['id'] for row in ledger[parent.base.CONTEXT]['integrated_record_keys'] if row['file_path'] == COMMON}
    assert not credited.intersection(f'COMMON_MESSAGE_{n}' for n in DECISIONS)
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    roster = {i: runtime.actor_root + (0x19E4 if i == 3 else 4 + 32 * i) for i in range(207)}
    voices = {i: get(0x7E988, actor) for i, actor in roster.items()}
    groups, records = [], []
    for start, end, table, load, call, pool, wrapper, role, context in GROUPS:
        binding = prior.caller_binding(arm, runtime.arm, load, call, pool, BASE + table, wrapper)
        size = 4 if wrapper == CAPTAIN else 8
        assert arm[table:table + 4 * size] == runtime.arm[table:table + 4 * size]
        slots = unpack_from(f'<{size}i', arm, table)
        assert set(slots) - {-1} == set(range(start, end + 1))
        if wrapper == CAPTAIN:
            selections = [(i, None, slots[i]) for i in range(4)]
        else:
            selections = [(i, voices[i], get(0x53F4C, actor, BASE + table)) for i, actor in roster.items()]
            assert all(number == (slots[voice] if slots[voice] >= 0 else slots[0]) for _, voice, number in selections)
        groups.append(dict(first_ID=start, last_ID=end, table=BASE + table, slots=slots,
            native_callers=[binding], original_voice_choices=selections, original_role_argument=role,
            argument_kind=None, context=context))
        for n in range(start, end + 1):
            jp, old = source[n], current[n]
            text = old.text.decode('cp932')
            paragraph = ' '.join(normalize('NFKC', text).split())
            revision, meaning, note = DECISIONS[n]
            english = revision or paragraph
            assert english.isascii() and english == ' '.join(english.split())
            assert bool(revision) == (english != paragraph)
            assert b'%' not in jp.text and b'%' not in old.text and '%' not in english
            records.append(dict(id=f'COMMON_MESSAGE_{n}', message_ID=n, file_path=COMMON,
                source_reference=prior.reference(jp), current_reference=prior.reference(old),
                source_hex=jp.text.hex(), current_hex=old.text.hex(), source_Japanese=jp.text.decode('cp932'),
                current_English=text, english=english, context=context, native_group_first_ID=start,
                original_slots=[i for i, selected in enumerate(slots) if n == selected],
                speaker='Storyline captain' if role is None else ('Original lookout or fallback' if role == 7 else 'Original First Mate or fallback'),
                source_meaning=meaning, localization_note=note, decision='revision' if revision else 'retention',
                inherited_fullwidth_Latin=prior.wide_letters(text), original_substitution_count=0,
                review={gate: gate != 'formatting' for gate in prior.GATES}))
    assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    assert [row['message_ID'] for row in records] == sorted(DECISIONS) and len(records) == 56
    linked = []
    for n in [*range(2217, 2222), *range(2229, 2234), 312]:
        assert f'COMMON_MESSAGE_{n}' in credited
        jp, old = source[n], current[n]
        linked.append(dict(message_ID=n, source_reference=prior.reference(jp), current_reference=prior.reference(old),
            source_hex=jp.text.hex(), current_hex=old.text.hex(), source_Japanese=jp.text.decode('cp932'),
            current_English=old.text.decode('cp932'), new_credit=0))
    counts = Counter(row['decision'] for row in records)
    prior.save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=prior.GATES, records=records,
        registered_input=runtime.receipt(), source_ROM_sha256=release['clean_input_sha256'],
        native_context=groups, initialized_argument_samples={}, linked_credited_context=linked,
        original_offline_actor_selections=sum(len(group['original_voice_choices']) for group in groups),
        counts=dict(counts), formatting_pending=True, gameplay_pending=True, new_credit=0, full_goal_complete=False))
    print(f'{len(records)} decisions {dict(counts)} across {len(groups)} original tables.')


if __name__ == '__main__':
    main()
