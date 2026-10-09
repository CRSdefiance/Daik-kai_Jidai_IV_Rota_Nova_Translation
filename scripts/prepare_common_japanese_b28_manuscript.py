"""Prepare clean-source pirate encounters, ship losses and diplomatic reactions."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

TEXT = {
    2629: ("Ah! We're under attack from %s! It's the pirate %s!", 'Youthful startled report of an attack from the first location, identifying the pirate by the second argument.'),
    2630: ("At %s, the pirate %s has appeared! We're under attack!", 'Formal older report of the pirate appearing at the first location and attacking us.'),
    2631: ("We've encountered the pirate %s! We're engaging!", 'Reports encountering the named pirate and beginning combat.'),
    2632: ("We've encountered the pirate %s. We'll engage.", 'Formal concise report of encountering the named pirate and engaging in combat.'),
    2633: ("There's the pirate %s! We're going to fight!", 'Youthful sighting of the named pirate and decision to fight.'),
    2634: ("The pirate %s attacked us! We're fighting back!", 'Feminine report of being attacked by the named pirate and engaging in combat.'),
    2635: ("We ran into the pirate %s! We're fighting!", 'Rough report of encountering the named pirate and engaging.'),
    2636: ("We've encountered the pirate %s! We'll fight!", 'Older report of encountering the named pirate and engaging.'),
    2637: ("We ran into the pirate %s! We're going to fight!", 'Youthful report of encountering the named pirate and fighting.'),
    2638: ('Victory is ours!', 'Emphatic report of our victory.'),
    2639: ('Victory is ours.', 'Formal report of our victory.'),
    2657: ("We'll call at a nearby town and await orders.", 'Plans to dock in a nearby town and wait for instructions.'),
    2658: ("We'll dock at a nearby town for now.", 'Informal interim plan to dock in a nearby town.'),
    2659: ("We'll dock in a nearby town for now.", 'Feminine interim plan to dock in a nearby town.'),
    2660: ("We'll dock at a nearby town for now.", 'Rough interim plan to dock in a nearby town.'),
    2661: ("We have no choice. We'll put into port at a nearby town.", 'Older resigned decision to dock in a nearby town.'),
    2662: ("We'll dock at a nearby town.", 'Youthful announcement of docking at a nearby town.'),
    2663: ('%s has sunk!', 'Confirms that the named ship has sunk.'),
    2671: ('There are no sailors aboard %s!', 'Reports that the substituted ship has no sailors aboard.'),
    2673: ('Not one sailor is aboard %s!', 'Rough emphatic report that the substituted ship has no sailors at all.'),
    2677: ("Are you sure? We'll abandon %s.", 'Confirms the order before abandoning the substituted ship.'),
    2678: ("We have no choice... We'll abandon %s, then.", 'Resigned announcement of abandoning the substituted ship.'),
    2679: ('Are we really abandoning %s?', 'Informal question confirming abandonment of the substituted ship.'),
    2680: ("So, we're abandoning %s, right?", 'Rough question confirming abandonment of the substituted ship.'),
    2681: ("No choice... We'll abandon %s.", 'Older resigned announcement of abandoning the substituted ship.'),
    2682: ("Then we'll abandon %s, okay?", 'Youthful announcement and confirmation of the ship-abandonment decision.'),
    2683: ("Our flagship's out of action! We're retreating to %s!", 'Reports the flagship defeated and retreating to the substituted destination; no invented sinking.'),
    2684: ("Our flagship's out of action! Retreat to %s!", 'Formal urgent report of flagship defeat and an order to retreat to the substituted destination.'),
    2685: ("Our flagship's out of action! Fall back to %s!", 'Youthful urgent report of flagship defeat and retreat to the substituted destination.'),
    2686: ("Our flagship's out of action! We're falling back to %s!", 'Rough report of flagship defeat and retreat to the substituted destination.'),
    2687: ("Our flagship's out of action! Retreat to %s!", 'Older urgent report of flagship defeat and retreat to the substituted destination.'),
    2688: ("Our flagship's out of action! We're retreating to %s!", 'Youthful alarm over flagship defeat and announcement of retreat to the substituted destination.'),
    2689: ("Our flagship's out of action! Let's retreat to %s!", 'Formal older report of flagship defeat and proposal to retreat to the substituted destination.'),
    2690: ("It can't end here... I'll have my revenge for this defeat!", 'Refuses to let things end here and vows to avenge the humiliation of defeat.'),
    2691: ("Damn! It can't end here. I'll settle this score!", 'Angry refusal to let things end here and vow to settle the grudge.'),
    2692: ("Damn it! Still... I won't let this defeat go to waste!", 'Angry but resilient vow to gain something despite falling; localizes the idiom without inventing a specific reward.'),
    2694: ("Like hell I'll die here! I'll pay you back for this!", 'Rough refusal to die here and vow to repay the enemy for the defeat.'),
    2695: ("Damn! It can't end here! I'll settle this score!", 'Older angry refusal to let things end here and vow to settle the grudge.'),
    2696: ("I won't let it end here! I'll teach you a lesson!", "Defiant declaration that the speaker's story will not end here and threatens retaliation."),
    2697: ("I'll avenge our commander!", "Vows personally to redress the commander's unfulfilled grievance; no explicit added cause of death."),
    2698: ("Our commander's last wishes are mine to fulfill!", "Emphatic vow personally to carry forward the commander's last wishes."),
    2699: ("I'll avenge our commander!", 'Youthful vow to avenge the commander.'),
    2700: ("I'll see our commander avenged!", "Feminine vow personally to redress the commander's grievance."),
    2701: ("I'll avenge our commander myself!", "Rough emphatic personal vow to redress the commander's grievance."),
    2702: ("I'll avenge our commander myself!", "Older emphatic personal vow to redress the commander's grievance."),
    2703: ('I shall see our commander avenged!', "Formal personal vow to redress the commander's grievance."),
    2704: ('Well, this is a problem. What on earth should we do now...', 'Troubled consideration of what to do from this point onward.'),
    2705: ('Will I just waste away like this... No, there must still be somewhere I can make a life.', 'Worries about wasting away, then rejects despair and believes there is still a place to live and make a life.'),
    2706: ("Aw, we lost. I'd better find a new employer soon.", 'Disappointment at defeat and urgent need to find a new employer.'),
    2707: ('This is a problem. Whatever should I do next...', 'Feminine troubled uncertainty about what to do next.'),
    2708: ("Tch! I can't make a living like this. Now, what should I do...", 'Rough worry about losing the ability to make a living and deliberation about what to do.'),
    2709: ("Hmm... Isn't there anyone out there who needs me...", 'Older worried search for someone somewhere who needs the speaker.'),
    2710: ('This is a predicament. I must think about what to do next...', "Formal older admission of difficulty and need to consider the speaker's future."),
    2711: ('A personal letter from %s?', 'Surprised question about a personal diplomatic letter from the substituted sender.'),
    2713: ('A personal letter from %s?', 'Question about a personal diplomatic letter from the substituted sender.'),
    2714: ('%s sent a personal letter?', 'Feminine surprised question about the sender sending a personal diplomatic letter.'),
    2715: ('I have no reason to accept that thing. Send it back!', 'Formal dismissive refusal to receive the letter and order to return it.'),
    2716: ("There's no reason to accept that thing. Send it back!", 'Stern refusal to receive the letter and order to return it.'),
    2717: ('I have no reason to accept that. Send it back.', 'Informal dismissive refusal to receive the letter and instruction to return it.'),
    2718: ('What are they thinking? Send that thing back, please.', "Feminine question about the sender's intent and dismissive request to return the letter."),
    2719: ("Hmm. I'll accept it.", 'Thoughtful acceptance of the letter.'),
    2720: ("Very well, I'll accept it.", 'Formal decision to accept the letter.'),
    2721: ("Hmm... I'll accept it, then.", 'Informal contemplative decision to accept the letter.'),
    2722: ("I'll accept it.", 'Feminine decision to accept the letter.'),
    2723: ('Hmm. A pact?', 'Thoughtful reaction to a proposed pact.'),
    2724: ('A pact...', 'Contemplative reaction to a proposed pact.'),
    2725: ('A pact...', 'Informal contemplative reaction to a proposed pact.'),
    2726: ('A pact, hmm...', 'Feminine contemplative reaction to a proposed pact.'),
    2727: ("Very well. Let's take this opportunity to strike at %s.", 'Formal agreement and proposal to use this opportunity to attack the substituted target.'),
    2728: ('Hmm... This could be a good opportunity to strike at %s.', 'Thoughtful judgment that attacking the substituted target on this occasion may be worthwhile.'),
    2729: ('Yes, this would be a good opportunity to strike at %s.', 'Informal agreement that this occasion is a useful opportunity to attack the target.'),
    2730: ("All right. Let's use this opportunity to strike at %s.", 'Feminine agreement and proposal to attack the target on this occasion.'),
    2731: ("Yes, striking at %s now wouldn't be a bad idea.", 'Qualified agreement that attacking the substituted target on this occasion is not a bad idea.'),
    2732: ('Opposing %s now would be unwise. Decline the offer as you see fit.', 'Judges opposing the target now strategically unwise and instructs an appropriate refusal of the offer.'),
    2733: ('Opposing %s now would be unwise... Find a way to decline.', 'Judges current opposition to the target bad and instructs refusal somehow.'),
    2734: ("We shouldn't oppose %s right now... Please work out how to decline.", 'Informal judgment that current opposition to the target is inadvisable and request to arrange refusal.'),
    2735: ("We shouldn't oppose %s right now... Decline the offer.", 'Feminine judgment that current opposition to the target is undesirable and instruction to decline.'),
    2736: ('Breaking the pact?! What the hell is %s thinking?!', "Angry shocked report of pact termination and question about the named party's intent."),
    2738: ('Breaking the pact?! What the hell is %s thinking?!', "Informal angry shock at pact termination and question about the named party's intent."),
    2739: ('Breaking the pact...?! %s... What are they thinking?!', "Feminine shocked reaction to pact termination and question about the named party's intent."),
    2740: ('What?! Breaking the pact?! Curse %s... What are they thinking?', 'Older angry shock at pact termination, disparages the named party and questions intent.'),
    2741: ('They want a cease-fire?', 'Surprised question about a request for cessation of hostilities.'),
    2742: ('A cease-fire?', 'Short surprised question about cessation of hostilities.'),
    2743: ('They want a cease-fire?', 'Informal surprised question about a request for cessation of hostilities.'),
    2744: ("They're telling us to cease fire?", 'Feminine surprised question about being told to cease hostilities.'),
}


def main():
    clean = NdsImage.open('work/clean.nds')
    entries = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),
                                     clean.read_file('/__arm9__.bin'))
    owners = {(entries[i].block, entries[i].record_index) for i in TEXT}
    selected = [e for e in entries if (e.block, e.record_index) in owners]
    assert {e.message_id for e in selected} == set(TEXT)
    rows = []
    for e in selected:
        english, meaning = TEXT[e.message_id]
        rows.append({
            'id': f'COMMON_MESSAGE_{e.message_id}', 'message_id': e.message_id,
            'block': e.block, 'record': e.record_index,
            'source_hex': e.text.hex().upper(), 'japanese': e.text.decode('cp932'),
            'previous_japanese': entries[e.message_id - 1].text.decode('cp932'),
            'next_japanese': entries[e.message_id + 1].text.decode('cp932'),
            'english': english.replace('I', 'Ｉ').replace('F', 'Ｆ') + '{PAD}',
            'source_meaning': meaning,
            'speaker': 'Crew report, faction leader or retainer voice variant',
            'context': (f'Independent native message {e.message_id}, clean COMMON B28 '
                        f'R{e.record_index}; pirate encounters, ship losses and diplomatic reactions. '
                        'All native selections in each selected source owner are included.'),
            'localization_note': ('Fresh clean-source American English preserves encounter versus enemy attack, '
                                  'combat and victory, nearby-port calls and waiting for orders, confirmed '
                                  'sinking versus flagship defeat, sailor absence, ship-abandonment confirmation, '
                                  'defiance, revenge, last wishes, livelihood uncertainty, personal letters, '
                                  'pact offers and refusals, strategic reasons and cease-fire requests versus '
                                  'demands. No invented ship sinking, destination type or relationship. '
                                  'The defeat-go-to-waste idiom preserves resilience without inventing a reward. '
                                  'Location and pirate arguments remain in source order. One paragraph; '
                                  'safe full-width I/F. Exact-font previews await review.'),
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': False},
        })
    payload = {'format': 'dk4-common-entry-manuscript-v1',
               'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
               'encoder': 'dialogue-fixed-v1',
               'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
               'status': 'draft-awaiting-reblocking-and-formatting-review', 'records': rows}
    Path('translations/common_japanese_b28_manuscript_v1.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Prepared {len(rows)} clean-source native messages')


if __name__ == '__main__':
    main()
