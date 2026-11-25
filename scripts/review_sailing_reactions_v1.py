"""Review the returning wind, white-whale exchange and related sailing reactions."""

from collections import Counter
from hashlib import sha256
from struct import unpack_from
from unicodedata import normalize

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import checkpoint_sea_event_review_v1 as previous
from scripts import register_trade_good_descriptions_v1 as parent


BASE, ARM, COMMON, CLEAN = previous.BASE, previous.ARM, previous.COMMON, previous.CLEAN
OUTPUT = previous.ROOT / 'sailing_reactions_context_v1.json'
WHALE = 'After the white-whale encounter, the same lookout offers two reflections. '
GROUPS = (
    (2359, 2365, 0x116C00, 0x7AE78, 0x7A834, 0x7A83C, 0x53D44, 7,
     WHALE + 'First they consider whether the whale was gentle or meant no harm.'),
    (2454, 2461, 0x117180, 0x7AEB0, 0x7AE38, 0x7AE40, 0x53D44, 1,
     'When the dead calm ends, one crew voice notices the wind has returned. The speaker may be matter-of-fact, relieved or jubilant.'),
    (2462, 2468, 0x1171C0, 0x7AE7C, 0x7A840, 0x7A848, 0x53D44, 7,
     WHALE + 'Then they wonder whether people left it no choice but to fight and express sympathy.'),
    (2469, 2475, 0x117220, 0x71B0C, 0x71A94, 0x71A9C, 0x53D44, 7,
     'A lookout draws attention to an unidentified glint. The original discovery sequence follows the sighting.'),
    (2476, 2483, 0x117240, 0x73128, 0x72F64, 0x72F6C, 0x53F0C, None,
     'The reef branch reports that extra armor prevented damage. The adjacent native branch without this protection uses different dialogue.'),
    (2484, 2491, 0x117280, 0x73134, 0x73028, 0x73030, 0x53F0C, None,
     'The drift-ice branch reports that the ram broke the ice and the ship escaped damage. This is distinct from reef protection.'),
    (2492, 2499, 0x1172A0, 0x79FE4, 0x79DBC, 0x79DC4, 0x53D44, 7,
     'A lookout reacts to the treasure found by following the map. The item has already been discovered. The reactions range from appraisal to celebration.'),
)

DECISIONS = {
    2359: ('Do you think it wants to get along with us? Maybe it is gentle after all.',
           'The speaker wonders whether the whale wants to be friendly and considers that it may be gentle.',
           'Keep the two tentative thoughts and lead naturally into the next reaction.'),
    2360: ('Maybe the white whale really is gentle.',
           'The white whale might actually be a gentle animal.',
           'Keep the reconsideration signaled by the source and name the whale.'),
    2361: (None, 'Maybe it is gentle and people have just decided to call it a monster.',
           'Retain the hesitant reconsideration and its link to the next remark about human treatment.'),
    2362: ("I'm starting to think the white whale doesn't really want to fight people.",
           'The speaker is starting to feel that the whale may not want to fight humans.',
           'Restore the change of heart and the specific doubt about fighting.'),
    2363: (None, 'Maybe the white whale never wanted to fight people in the first place.',
           'Retain the plainspoken qualification and the emphasis on the whale’s original intent.'),
    2364: ("Perhaps the white whale's gentler than we thought.",
           'The white whale may be surprisingly gentle.',
           'Keep the qualified judgment and surprise at the change in perspective.'),
    2365: ("Think it just wants to play with us? Maybe it's gentle after all.",
           'The speaker wonders whether the whale wants to play with them and might be gentle.',
           'Keep the playful question and the tentative discovery.'),
    2454: ('The wind has returned.', 'The wind has started blowing again.',
           'Restore the straightforward report after the calm.'),
    2455: ('Wind, at last...', 'At last there is wind, with a trailing expression of relief.',
           'Keep the brief relief and the original trailing thought.'),
    2456: (None, 'The speaker suddenly notices that the wind has started blowing.',
           'Retain the quick exclamation and the excited delivery.'),
    2457: ("Oh, I think the wind's picking up. What a relief!",
           'It seems the wind has begun blowing. The speaker is relieved.',
           'Keep the tentative observation and the emotional release.'),
    2458: ("Hey, the wind's back!", 'The speaker notices the wind starting up and calls out.',
           'Give the rougher voice a brisk call rather than sharing the other startled voice verbatim.'),
    2459: ("Ah! The wind seems to be picking up.", 'The speaker exclaims that the wind appears to have started blowing.',
           'Keep the measured certainty and normalize the full-width glyph.'),
    2460: ("Wind! Hooray! It's blowing again!", 'The speaker spots wind and celebrates that it has started blowing.',
           'Keep the childlike delight and its rhythm.'),
    2461: (None, 'The speaker politely confirms that the wind has started blowing.',
           'Retain the unhurried, complete report.'),
    2462: ('Perhaps it only fought because we humans were foolish enough to treat it like a monster...',
           'Perhaps foolish humans decided it was a monster and left it with no choice but to fight.',
           'Keep the criticism of people, the lack of choice and the hesitant conclusion.'),
    2463: ("Maybe it had no choice but to fight once people decided it was a monster. I feel sorry for it.",
           'People may have left the whale no choice but to fight by treating it as a monster. The speaker feels some sympathy.',
           'Keep the possible cause and allow the speaker to express personal sympathy.'),
    2464: (None, 'The speaker wonders if the whale is really to be pitied.',
           'Retain the inward, hesitant thought. Normalize the full-width I.'),
    2465: ("I wonder if it fights because people treat it like a monster. Maybe the poor thing never had a choice...",
           'Perhaps people call the animal a monster on their own authority and it fights because it has no choice. It may deserve sympathy.',
           'Keep the compassionate change of perspective and the speaker’s uncertainty.'),
    2466: ("Maybe it only fights because we decided it was a monster. I feel kind of sorry for it...",
           'Maybe it fights only because we people decided to treat it as a monster. The speaker feels somewhat sorry for it.',
           'Restore the self-implicating we and give the gruff voice its quieter finish.'),
    2467: ("Perhaps people left it no choice but to fight by treating it as a monster. I can't help feeling sorry for it...",
           'People may have called the whale a monster and left it no choice but to fight. The speaker pauses and feels pity.',
           'Restore the tentative inference and make the sympathy a separate thought.'),
    2468: ("Think it has to fight 'cause people call it a monster? Poor thing...",
           'The speaker wonders whether being called a monster leaves it no choice but to fight, then feels sorry for it.',
           'Preserve the wondering question and simple empathy in a young-sounding voice.'),
    2469: (None, 'The lookout calls to the admiral and points out a distant glint.',
           'Retain the precise address, direction and unknown object.'),
    2470: ('Admiral, over there! Something is shining!', 'The lookout asks the admiral to look over there and points out something shining.',
           'Keep the direct address and pointing cue in a slightly more deliberate voice.'),
    2471: ("Look over there, Admiral! Something's shining!", 'The speaker excitedly asks the admiral to look at something shining over there.',
           'Give the quick voice a natural sequence and retain the direction.'),
    2472: ("Admiral, look over there! See that glint?", 'The speaker calls for the admiral’s attention and points out something shining.',
           'Keep the conversational call for attention and the visible cue without identifying it.'),
    2473: (None, 'The rougher speaker calls to the admiral about something glittering over there.',
           'Retain the brisk voice, glitter and pointed direction.'),
    2474: ("Admiral! There's something shining over there!", 'The speaker calls to the admiral and points out a shining object over there.',
           'Restore where the glint is seen while keeping the emphatic opening.'),
    2475: (None, 'The speaker softly points and remarks on a sparkle.',
           'Retain the pause and excited discovery without adding an address.'),
    2476: ('Admiral, the extra armor kept the reef from damaging the ship!',
           'The speaker reports no reef damage thanks to extra armor.',
           'Restore the specific hazard and the result.'),
    2477: (None, 'The speaker tells the admiral that extra armor prevented damage.',
           'Retain the measured report and leave the hazard implicit as in this variant.'),
    2478: ("Admiral, we didn't take a scratch with that extra armor!",
           'The extra armor was fitted, so the ship is unscathed.',
           'Restore the result that the ship is completely undamaged.'),
    2479: ("No damage from the reef, Admiral! Good thing we had that extra armor.",
           'Thanks to the extra armor, the ship took no damage from the reef.',
           'Restore the reef and relief at being protected.'),
    2480: ("With that extra armor, we don't have to worry about reef damage!",
           'The speaker says the extra armor means there is no need to worry about reef damage.',
           'Preserve the confident reassurance rather than a generic report.'),
    2481: ("The extra armor kept the ship from taking a scratch. It pays to be prepared!",
           'With extra armor, the ship is unscathed. Preparation wards off trouble.',
           'Keep the no-damage result and use a natural equivalent for the proverb.'),
    2482: ("Reefs are no big deal with extra armor!", 'The speaker boasts that reefs are easy to handle with extra armor.',
           'Keep the jaunty reassurance about the equipment.'),
    2483: (None, 'The speaker respectfully reports that the extra armor prevented all reef damage.',
           'Retain the precise result, hazard and causal link.'),
    2484: (None, 'The ram shattered the drift ice and the ship sustained no damage.',
           'Retain the concise report and both facts. The hazard is already apparent in the scene.'),
    2485: ('Admiral, the ram broke up the drift ice. No damage!',
           'The speaker tells the admiral that the ram broke the drift ice and there was no damage.',
           'Restore the ram as the cause and complete the report in the original voice.'),
    2486: (None, 'The speaker exclaims at their good luck when the ram breaks the drift ice.',
           'Retain the delighted opening and the action just witnessed.'),
    2487: ("The ram shattered the ice, Admiral! What a relief.",
           'The speaker addresses the admiral, says the ram smashed the drift ice to pieces and expresses relief.',
           'Restore the address and the emotional reaction.'),
    2488: (None, 'The speaker announces that the ram smashed the floating ice.',
           'Retain the forceful verb and the plain description of the hazard.'),
    2489: ("The ram broke up the drift ice. We needn't worry about the ship now!",
           'The ram broke the drift ice, so there is no reason to worry about damage to the ship.',
           'Keep the equipment, hazard and reassuring second thought.'),
    2490: (None, 'The speaker reacts with excitement as the ram shatters the drift ice.',
           'Retain the energetic short report and complete hazard description.'),
    2491: ('Admiral, the ram shattered the drift ice before it could damage the ship!',
           'The ram shattered the drift ice and as a result the ship was not damaged.',
           'Keep the formal address and clear cause and effect.'),
    2492: ('Admiral, the map was right after all!',
           'The speaker realizes that what was written on the map was true.',
           'Restore the realization after seeing the result.'),
    2493: (None, 'The speaker realizes that what was written on the map was true.',
           'Retain the full reference to what the map said and the pleased surprise.'),
    2494: (None, 'The speaker is delighted by the good luck of finding something so impressive.',
           'Retain the spontaneous delight and the sense of a lucky find.'),
    2495: (None, 'The treasure looks expensive. The speaker wonders if it is worth what they paid for the map.',
           'Retain the practical comparison and the uncertain valuation.'),
    2496: ("Now that's something! How about a good meal later?",
           'The speaker is impressed and asks to be treated to something good to eat later.',
           'Keep the cheeky request without turning it into a demand or a promised feast.'),
    2497: ("S-so that's the hidden treasure... Pays to live a long life!",
           'The speaker stammers at the hidden treasure, then marvels that living long has let them see it.',
           'Restore the stammer and the older voice’s wry remark.'),
    2498: (None, 'The speaker joyfully anticipates a feast tonight.',
           'Retain the excited reaction and the time reference as the speaker’s expectation.'),
    2499: (None, 'The speaker did not expect treasure of this quality and credits the admiral.',
           'Retain the surprised admiration and attribution. Normalize both full-width I glyphs.'),
}


def main():
    load, save = previous.load, previous.save
    assert not OUTPUT.exists()
    release = load(parent.RELEASE)
    runtime = previous.RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    assert previous.digest(CLEAN) == release['clean_input_sha256']
    image = NdsImage.open(CLEAN)
    arm = image.read_file(ARM)
    source = common_message_entries(image.read_file(COMMON), arm)
    directory = sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    current = owned_entries(runtime.common, runtime.arm, directory)
    ledger = load(parent.base.LEDGER)
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    credited = {row['id'] for row in ledger[parent.base.CONTEXT]['integrated_record_keys'] if row['file_path'] == COMMON}
    assert not credited.intersection(f'COMMON_MESSAGE_{n}' for n in DECISIONS)
    assert set(DECISIONS) == {n for start, end, *_ in GROUPS for n in range(start, end + 1)}
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    actors = {i: runtime.actor_root + (0x19E4 if i == 3 else 4 + 32 * i) for i in range(207)}
    voices = {i: get(0x7E988, obj) for i, obj in actors.items()}
    groups, records = [], []
    for start, end, table, pool, pc, call, wrapper, role, context in GROUPS:
        binding = previous.caller_binding(arm, runtime.arm, pc, call, pool, BASE + table, wrapper)
        if role is not None:
            assert unpack_from('<I', arm, pc + 4)[0] == 0xE3A00000 | role
        else:
            assert unpack_from('<I', arm, pc + 4)[0] == 0xE1A00006
        assert arm[table:table + 32] == runtime.arm[table:table + 32]
        slots = unpack_from('<8i', arm, table)
        assert set(slots) - {-1} == set(range(start, end + 1))
        selections = []
        for i, actor in actors.items():
            selected = get(0x53F4C, actor, BASE + table)
            slot = slots[voices[i]]
            assert selected == (start if slot == -1 else slot)
            selections.append([i, voices[i], selected])
        groups.append(dict(first_ID=start, last_ID=end, table=BASE + table, slots=slots,
            consumer=wrapper, original_role_argument=role, original_source_caller=binding,
            original_voice_choices=selections, context=context))
        for n in range(start, end + 1):
            jp, old = source[n], current[n]
            text = old.text.decode('cp932')
            revision, meaning, note = DECISIONS[n]
            paragraph = ' '.join(normalize('NFKC', text).split())
            english = revision or paragraph
            assert english.isascii() and english == ' '.join(english.split()) and '%' not in english
            assert b'%' not in jp.text and bool(revision) == (english != paragraph)
            records.append(dict(id=f'COMMON_MESSAGE_{n}', message_ID=n, file_path=COMMON,
                source_reference=previous.reference(jp), current_reference=previous.reference(old),
                source_hex=jp.text.hex(), current_hex=old.text.hex(), source_Japanese=jp.text.decode('cp932'),
                current_English=text, english=english, speaker='Crew member selected by the original voice class',
                native_group_first_ID=start, original_slots=[i for i, key in enumerate(slots) if key == n],
                source_meaning=meaning, context=context, localization_note=note,
                decision='revision' if revision else 'retention', inherited_fullwidth_Latin=previous.wide_letters(text),
                original_substitution_count=0, review={gate: gate != 'formatting' for gate in previous.GATES}))
    assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    counts = Counter(row['decision'] for row in records)
    save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=previous.GATES, records=records,
        registered_input=runtime.receipt(), clean_input_sha256=release['clean_input_sha256'],
        native_context=groups, original_offline_actor_selections=len(groups) * len(actors), counts=dict(counts),
        formatting_pending=True, new_credit=0, full_goal_complete=False))
    print(f'{len(records)} prose decisions {dict(counts)}, {len(groups)} exact source voice tables.')


if __name__ == '__main__':
    main()
