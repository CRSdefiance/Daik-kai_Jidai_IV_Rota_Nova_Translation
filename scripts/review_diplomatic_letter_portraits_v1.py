"""Review the original personal-letter, pact, war and submission exchanges."""

from hashlib import sha256
from pathlib import Path
from types import FunctionType

from scripts import review_rumor_and_cooperation_v1 as prior
from scripts.register_rumor_and_cooperation_v1 import RELEASE


OUTPUT = prior.ROOT / 'diplomatic_letter_portraits_context_v1.json'
IDS = tuple(range(2711, 2770))

GROUPS = (
    (0x117260, 0x93B90, ((0x939AC, 0x939B0),), (2711, 2712, 2713, 2714, -1, -1, -1, -1), ('sending faction',),
     'The faction leader hears who sent a personal letter and responds before deciding whether to accept it.'),
    (0x1172C0, 0x93B94, ((0x93A00, 0x93A04),), (2715, 2716, 2717, 2718, -1, -1, -1, -1), (),
     'The recipient rebuffs the letter, tells the attendant to return it, and the system reports the refusal.'),
    (0x1173A0, 0x93BA4, ((0x93AD0, 0x93AD4),), (2719, 2720, 2721, 2722, -1, -1, -1, -1), (),
     'The recipient accepts the personal letter. The system reports the change in relations when it rises.'),
    (0x117600, 0x938E8, ((0x93658, 0x9365C),), (2723, 2724, 2725, 2726, -1, -1, -1, -1), (),
     'The recipient considers a proposed pact after the receipt notice and before the native yes or no branch.'),
    (0x117720, 0x938EC, ((0x9368C, 0x93690),), (2727, 2728, 2729, 2730, 2731, -1, -1, -1), ('target faction',),
     'The recipient favors the pact and proposes action against the named third faction. The system reports the resulting alliance when applicable.'),
    (0x117880, 0x938F0, ((0x936BC, 0x936C0),), (2732, 2733, 2734, 2735, -1, -1, -1, -1), ('target faction',),
     'The recipient declines the pact because confronting the named third faction now would be unwise. The instruction is to turn down the proposal.'),
    (0x117A40, 0x93410, ((0x932C8, 0x932CC),), (2736, 2737, 2738, 2739, -1, 2740, -1, -1), ('sending captain',),
     'After the receipt notice, the other leader reacts to the player breaking their existing pact. The native caller uses the player captain’s name.'),
    (0x117C00, 0x931E8, ((0x92FF4, 0x92FF8),), (2741, 2742, 2743, 2744, -1, -1, -1, -1), (),
     'After receipt of the player’s letter, the leader reacts to the cease-fire proposal before the native decision.'),
    (0x117DA0, 0x931EC, ((0x9300C, 0x93010),), (2745, -1, 2746, 2747, 2748, -1, -1, -1), (),
     'The recipient agrees to the cease-fire because the fighting serves no purpose. The system reports agreement.'),
    (0x117FC0, 0x931F4, ((0x93050, 0x93054),), (2749, -1, 2750, 2751, 2752, -1, -1, -1), (),
     'The recipient refuses the cease-fire and tells the attendant to pass back a threat. The system then reports refusal.'),
    (0x118420, 0x92D8C, ((0x92C40, 0x92C44),), (2753, -1, 2754, 2755, 2756, -1, -1, -1), ('declaring faction',),
     'The other leader reacts to the player’s declaration of war before the original hostility change. Three voices name the declaring faction.'),
    (0x1187E0, 0x92B58, ((0x9298C, 0x92990),), (2757, 2758, 2759, 2760, -1, -1, -1, -1), ('demanding faction',),
     'The faction leader repeats the player’s demand for submission in disbelief. The game can proceed to acceptance, voiced rejection or ignoring the demand.'),
    (0x1168E0, 0x92B5C, ((0x929A4, 0x929A8),), (2761, 2762, 2763, 2764, 2765, -1, -1, -1), (),
     'The faction leader reluctantly agrees to come under the player’s authority. The system announces the result.'),
    (0x116960, 0x92B68, ((0x929F8, 0x929FC),), (2766, 2767, 2768, 2769, -1, -1, -1, -1), (),
     'The faction leader voices a dismissal before the system reports rejection. The separate ignore branch uses the previously reviewed forgery portraits and a distinct result.'),
)

DATA = {
    2711: ('A personal letter from %s?', 'Asks in surprise whether the named faction sent a personal letter.', 'Retain the short question before the reply.'),
    2712: ('%s sent us a personal letter?', 'Repeats in disbelief that the named faction sent a personal letter.', 'Retain the emphasis on the sender and the implied recipients.'),
    2713: ('A personal letter from %s?', 'Asks whether the named faction sent a personal letter.', 'Retain the simple surprise. The voice follows through in the answer.'),
    2714: ('%s sent a personal letter?', 'Asks whether the named faction sent a personal letter.', 'Retain the natural rising question and sender-first phrasing.'),
    2715: ('I see no reason to accept it. Send it back!', 'Sees no reason to accept the letter and orders it sent back.', 'The preceding question identifies the letter. Keep the composed judgment and emphatic order.'),
    2716: ("There's no reason to take it. Send it back!", 'Says there is no reason to accept and gives a blunt order to send the letter back.', 'Use a short first clause to match the sharper command.'),
    2717: ('I see no reason to take it. Send it back.', 'Sees no reason to accept the letter and tells the attendant to return it.', 'Keep the delivery matter-of-fact with a flat ending.'),
    2718: ('What are they thinking? Send it back, please.', 'Questions the sender’s intent and asks the attendant to return the letter.', 'Keep the irritated question and courteous form of the instruction.'),
    2719: ("Hmm. I'll accept it.", 'Considers the letter briefly and agrees to accept it.', 'Retain the measured pause and plain decision.'),
    2720: ("Very well, I'll accept it.", 'Decides to accept the letter.', 'Retain the formal assent in this voice.'),
    2721: ("Hmm... All right, I'll take it.", 'Thinks for a moment and agrees to accept the letter.', 'Keep the slight hesitation and casual assent together.'),
    2722: ("I'll accept it.", 'Says she will accept the letter.', 'Retain the concise agreement.'),
    2723: ('Hmm. A pact?', 'Considers the proposal for a pact.', 'Retain the short, thoughtful question.'),
    2724: ('A pact...', 'Mulls over the proposed pact.', 'Retain the brief pause before the leader’s response.'),
    2725: ('A pact...', 'Considers the proposed pact.', 'Retain the spare repetition, with the next turn carrying the decision.'),
    2726: ('A pact, hmm...', 'Reflects aloud on the proposal with a drawn-out ending.', 'Retain the audible musing before either response.'),
    2727: ("Very well. Let's take this opportunity to strike at %s.", 'Agrees and proposes using the opportunity to strike at the named faction.', 'Retain the formal assent, shared proposal and specific target.'),
    2728: ('Hmm... This could be a good opportunity to strike at %s.', 'Reflects and considers striking the named faction while there is an opportunity.', 'Retain the deliberation and conditional phrasing.'),
    2729: ('Good point. This could be our chance to strike at %s.', 'Agrees with the idea and sees merit in striking at the named faction now.', 'Give the agreement a conversational beat before the practical conclusion.'),
    2730: ("All right. Let's use this opportunity to strike at %s.", 'Agrees and proposes taking the chance to strike at the named faction.', 'Retain the decisive, collaborative delivery.'),
    2731: ("Yes, striking at %s now wouldn't be a bad idea.", 'Agrees that taking this chance to attack the named faction could be worthwhile.', 'Retain the qualified approval of this voice.'),
    2732: ("It would be unwise to take on %s now. Find a way to turn them down.", 'Judges confrontation with the named faction unwise and delegates declining the proposal.', 'Let the second clause speak to the attendant and keep the third faction in the first clause.'),
    2733: ("We can't afford to take on %s now... Find a way to decline.", 'Thinks opposing the named faction now would be a bad move and orders a refusal.', 'Keep the pause and the short order. “Can’t afford” expresses the strategic risk.'),
    2734: ("We shouldn't take on %s right now... See if you can turn them down.", 'Thinks opposing the named faction now is a bad idea and asks the attendant to decline the proposal.', 'Keep the softened instruction in the speaker’s voice.'),
    2735: ("This is no time to take on %s... Decline the offer.", 'Finds it undesirable to oppose the named faction now and tells the attendant to decline.', 'Keep the strategic judgment and the composed order.'),
    2736: ('Breaking the pact?! What is %s playing at?', 'Reacts angrily to the pact being broken and questions the named captain’s intent.', 'Use a sharp question to convey the contempt in the Japanese form of address.'),
    2737: ('They ended the pact?! What is %s thinking?', 'Reacts to the pact being broken and questions what the named captain intends.', 'Retain the startled question and the natural second sentence.'),
    2738: ('Break the pact?! What does %s think this is?!', 'Reacts with agitation and demands to know what the named captain is thinking.', 'Keep the two outbursts and the speaker’s indignation.'),
    2739: ('Breaking the pact...?! %s... What are they thinking?!', 'Reacts to the broken pact, pauses on the named captain and questions their intent.', 'Retain the pauses and the more reflective delivery.'),
    2740: ('What?! Ending the pact, are they? Curse %s... What are they up to?', 'Expresses shock at the broken pact, curses the named captain and questions their intentions.', 'Use a rhetorical tag for this voice and keep the curse and suspicion.'),
    2741: ('They want a cease-fire?', 'Asks whether the other side wants a cease-fire.', 'Retain the short question.'),
    2742: ('A cease-fire?', 'Repeats the cease-fire proposal in surprise.', 'Retain the terse echo.'),
    2743: ('They want a cease-fire?', 'Asks in surprise if the other side wants a cease-fire.', 'Retain the natural phrasing and let the reply distinguish the voice.'),
    2744: ("They're telling us to cease fire?", 'Reacts to what the speaker frames as an instruction to cease fire.', 'Retain the pointed wording of this voice.'),
    2745: ('...Very well. We have no wish to fight a pointless war either.', 'Agrees after a pause and says their side also has no desire for futile fighting.', 'Use measured language and keep the pause ahead of assent.'),
    2746: ("All right. We don't want a pointless fight either.", 'Agrees and says their side has no desire for a pointless fight.', 'Retain the practical and conversational agreement.'),
    2747: ("...All right. We don't want to fight needlessly either.", 'Agrees after a pause and says their side also has no desire for needless fighting.', 'Place the pause before the decision as in the original.'),
    2748: ('All right. Pointless fighting does nobody any good.', 'Agrees because there is nothing to gain from futile fighting.', 'Retain the blunt practical reason.'),
    2749: ('How dare they! Tell them to prepare for death!', 'Takes offense and tells the attendant to relay a threat of death.', 'Retain the imperious threat. The Japanese neck-washing idiom warns the other side to prepare to die.'),
    2750: ('What are they talking about...? Tell them to brace themselves!', 'Dismisses the proposal in disbelief and tells the attendant to warn the other side to steel themselves.', 'Retain the bemused pause and the warning to brace for what comes.'),
    2751: ('What nonsense... Tell them to get ready to die!', 'Dismisses the cease-fire as foolish and tells the attendant to pass on a threat of death.', 'Retain the pause and the force of the threat.'),
    2752: ("They've got some nerve. Tell them to get ready to die!", 'Takes the proposal as outrageous and orders the attendant to relay a death threat.', 'Use a rough expression of outrage to lead into the threat.'),
    2753: ("What?! Damn %s... They've got nerve! I'll teach them a lesson!", 'Curses the declaring faction, acknowledges their audacity and vows to make them regret it.', 'Retain the mounting anger and vow. Use the ordinary capital I.'),
    2754: ('What?! You looking for trouble, %s? You asked for it!', 'Reacts to the declaration, addresses the faction and threatens consequences.', 'Address the faction directly and keep the retort sharp.'),
    2755: ("If that's how you want it, I've got a few ideas of my own. Just you wait!", 'Says she has a response of her own and warns the other side to wait and see.', 'Avoid repeating “plan” and keep the controlled threat.'),
    2756: ('What?! So they want trouble... %s had better watch out!', 'Reacts in anger, says the declaring faction seems to want trouble and warns them to be ready.', 'Keep the rough move from disbelief to a named threat.'),
    2757: ("They're telling us to submit to %s?", 'Repeats the demand to come under the named faction’s authority.', 'Retain the pointed emphasis on the demand.'),
    2758: ('They want us to submit to %s?', 'Asks in disbelief if they are expected to submit to the named faction.', 'Retain the direct question and the faction substitution.'),
    2759: ('They say we should submit to %s?', 'Repeats in disbelief that they are being told to submit to the named faction.', 'Retain the conversational phrasing before the decision.'),
    2760: ('They expect us to submit to %s?', 'Asks incredulously if they are expected to come under the named faction’s authority.', 'Use “expect” for the questioning tone of this voice.'),
    2761: ('Grr... We have no choice.', 'Grumbles and accepts submission as unavoidable.', 'Retain the audible frustration and reluctant conclusion.'),
    2762: ('We have no choice...', 'Reluctantly acknowledges that they have no alternative.', 'Retain the terse resignation.'),
    2763: ('Fine... I guess we have no choice.', 'Gives in and reluctantly acknowledges that there is no alternative.', 'Keep the informal concession and hesitation without trailing off twice.'),
    2764: ("So... there's no other way.", 'Concludes reluctantly that there is no other course.', 'Retain the reflective pause and understated conclusion.'),
    2765: ('We have no choice...', 'Accepts submission as unavoidable.', 'Retain the short resigned answer.'),
    2766: ('What nonsense! We need not dignify such a ridiculous demand with an answer.', 'Dismisses the demand as foolish and declares it unworthy of attention.', 'Use formal disdain for the speaker and identify the demand heard in the preceding turn.'),
    2767: ("So that's what this is about... I won't give such a ridiculous demand the time of day!", 'Realizes what the other side is after and refuses to entertain the demand.', 'Keep the dismissive realization and give the refusal a spoken idiom.'),
    2768: ("So that's it, huh? I'm not going along with a ridiculous demand like that!", 'Recognizes the other side’s purpose and rejects the demand out of hand.', 'Keep the conversational opening and a more direct refusal.'),
    2769: ("So that's what they wanted... I have no time for such nonsense!", 'Recognizes what the other side is asking for and says she has no time for it.', 'Keep the realization and the brisk dismissal.'),
}


# Each span covers a whole decision block and its source table literals.
SPANS = ((0x927F0, 0x92B78), (0x92B78, 0x92D9C), (0x92D9C, 0x931FC),
         (0x931FC, 0x93424), (0x93424, 0x93900), (0x93900, 0x93BAC))
RESULT_IDS = (346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357,
              358, 359, 360, 361, 362, 363, 381, 382, 2791, 2792, 2793, 2794, 2795)
WIDE_ASCII = str.maketrans({chr(i + 0xFEE0): chr(i) for i in range(0x21, 0x7F)})


def source_record(japanese, current, n):
    a, b = japanese[n], current[n]
    return dict(id=f'COMMON_MESSAGE_{n}', file_path=prior.COMMON, message_ID=n,
                source_reference=prior.reference(a), current_reference=prior.reference(b),
                source_hex=a.text.hex(), current_hex=b.text.hex(),
                clean_Japanese=a.text.decode('cp932'), current_English=b.text.decode('cp932'))


def main():
    assert not OUTPUT.exists()
    release = prior.load(RELEASE)
    runtime = prior.RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    source = prior.NdsImage.open(prior.CLEAN)
    clean, arm = source.read_file(prior.ARM), runtime.arm
    assert prior.digest(prior.CLEAN) == release['clean_input_sha256']
    assert all(clean[lo:hi] == arm[lo:hi] for lo, hi in SPANS)
    japanese = prior.common_message_entries(source.read_file(prior.COMMON), clean)
    directory = sha256(arm[prior.DIRECTORY_OFFSET:prior.TABLE_OFFSET]).hexdigest()
    current = prior.owned_entries(runtime.common, arm, directory)
    resolve_groups = FunctionType(prior.original_groups.__code__, vars(prior) | {'GROUPS': GROUPS})
    groups, bindings = resolve_groups(runtime, clean)
    assert tuple(DATA) == IDS == tuple(bindings)
    ledger = prior.load(prior.LEDGER)
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    credited = {(row['file_path'], row['id']) for row in ledger[prior.CONTEXT]['integrated_record_keys']}

    records = []
    for n, (english, meaning, note) in DATA.items():
        row = source_record(japanese, current, n) | bindings[n]
        if n == 2755:
            # The original wrapper receives a faction argument this voice never interpolates.
            row['unused_native_arguments'] = row['original_substitutions']
            row['original_substitutions'] = ()
        assert (prior.COMMON, row['id']) not in credited
        assert english.count('%s') == row['clean_Japanese'].count('%s') == len(row['original_substitutions'])
        old = ' '.join(row['current_English'].translate(WIDE_ASCII).split())
        records.append(row | dict(english=english, source_meaning=meaning, localization_note=note,
            decision='retention' if english == old else 'revision',
            current_wide_glyphs=prior.wide_letters(row['current_English']),
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)))

    results = [source_record(japanese, current, n) for n in RESULT_IDS]
    assert all((prior.COMMON, row['id']) in credited for row in results)
    neighbors = [source_record(japanese, current, n) for n in range(2690, 2711)]
    prior.save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'],
        records=records, registered_input=runtime.receipt(), original_portrait_tables=groups,
        previously_credited_neighbors=results, next_faction_defeat_and_succession_context=neighbors,
        exact_native_handlers=[dict(start=prior.BASE + lo, end=prior.BASE + hi,
                                    clean_current_sha256=sha256(clean[lo:hi]).hexdigest()) for lo, hi in SPANS],
        source_rom_sha256=release['clean_input_sha256'], new_completion_credit=0, full_goal_complete=False,
        evidence={str(path): prior.digest(path) for path in (RELEASE, Path(__file__))}))
    counts = {key: sum(row['decision'] == key for row in records) for key in ('revision','retention')}
    print(f'Reviewed {len(records)} clean-source portraits across {len(groups)} voice tables: {counts}.')


if __name__ == '__main__':
    main()

