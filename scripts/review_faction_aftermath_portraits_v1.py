"""Bind the defeat, succession and displaced-fleet portraits to dissolution."""

import inspect
from pathlib import Path

from scripts import review_diplomatic_letter_portraits_v1 as earlier
from scripts.register_diplomatic_letter_portraits_v1 import RELEASE
from scripts.source_locked_derivation_v5118 import checked_text


prior = earlier.prior
OUTPUT = earlier.OUTPUT.with_name('faction_aftermath_portraits_context_v1.json')
IDS = tuple(range(2690, 2711))
GROUPS = (
    (0x1170E0, 0x33EB0, ((0x33E70, 0x33E7C),), (2690, 2691, 2692, 2693, 2694, 2695, -1, 2696), (),
     'After the faction disbands, the game selects the defeated faction leader’s own fleet commander and plays a defiant reaction once. The speaker vows to recover from the defeat.'),
    (0x117160, 0x33EB4, ((0x33E78, 0x33E7C),), (2697, 2698, 2699, 2700, 2701, 2702, -1, 2703), (),
     'A different fleet’s commander vows to avenge or carry on the wishes of the fallen faction commander. This is an alternative to the faction leader speaking for themself.'),
    (0x1171E0, 0x33D58, ((0x33D34, 0x33D3C),), (2704, 2705, 2706, 2707, 2708, 2709, -1, 2710), (),
     'A displaced fleet commander reacts after the dissolution handler changes their affiliation. The speaker is considering their own next move.'),
)
SPANS = ((0x3A3DC, 0x3A494), (0x2C780, 0x2CAE0), (0x33CCC, 0x33EB8), (0x3697C, 0x369C8))
RESULT_IDS = (337, *range(2683, 2690))
DATA = {
    2690: ("It can't end here... I swear I'll avenge this defeat!",
           'Refuses to accept this as the end and swears to avenge the defeat.',
           'Keep the pause and the personal vow. Use ordinary I and make the determination the final beat.'),
    2691: ("Damn! It can't end here. I'll settle this score!",
           'Curses, refuses to let this be the end, and vows to settle the score.',
           'Retain the clipped curse and the firm two-part resolve.'),
    2692: ("Damn it! Still... I won't let this defeat go to waste!",
           'Swears in frustration, then insists on making something out of the setback.',
           'Retain the English idiom for gaining something from a fall. It preserves this voice’s pivot from frustration to resolve.'),
    2693: ('They got me... Just you wait!',
           'Admits to being beaten and warns the other side to wait and see.',
           'Retain the short admission and the sudden threat.'),
    2694: ("Like hell I'll die here! I'll pay you back for this!",
           'Roughly refuses to die here and vows to pay the other side back.',
           'Retain the rough register and the vow. The speaker is alive as they say it.'),
    2695: ("Blast it! It can't end here! I'll settle this score yet!",
           'Grunts in frustration, refuses to give up and vows to settle the grudge.',
           'Give the seasoned voice its own curse and cadence.'),
    2696: ("I won't let it end here! I'll teach you a lesson!",
           'Insists that this is no end for them and threatens to teach the other side a lesson.',
           'Retain the emphatic first-person threat and two complete sentences.'),
    2697: ("I'll avenge our commander!",
           'Vows to avenge the faction commander.',
           'Retain the concise vow and the established title.'),
    2698: ("I'll see our commander's last wishes carried out!",
           'Swears personally to carry on the faction commander’s dying wishes.',
           'Make the promise direct and retain this voice’s distinct reference to last wishes.'),
    2699: ("I'll make them pay for what they did to our commander!",
           'Personally vows to take vengeance against whoever wronged the faction commander.',
           'Give the younger voice a direct, emotional vow. Keep the commander and the object of revenge distinct.'),
    2700: ("I'll see our commander avenged!",
           'Vows to see the faction commander avenged.',
           'Retain the determined formality of the vow.'),
    2701: ("I'll avenge our commander myself!",
           'Insists on personally avenging the faction commander.',
           'Retain the blunt promise and the emphasis on personally acting.'),
    2702: ("I'll see to it myself. Our commander will be avenged!",
           'Personally promises to avenge the faction commander.',
           'Give this voice a deliberate first beat and a forceful second.'),
    2703: ("I shall see our commander avenged!",
           'Personally vows to avenge the faction commander in formal speech.',
           'Retain the formal shall and the clear vow.'),
    2704: ('Well, this is a problem. What am I to do now?',
           'Recognizes the difficult situation and wonders what to do next.',
           'Keep the reflective question and measured voice. The speaker is weighing their next move.'),
    2705: ('Am I just going to waste away...? No. There must be a place for me somewhere.',
           'Wonders whether they will just waste away, then decides there must be a place to live on.',
           'Keep the emotional turn from doubt to determination and the image of wasting away.'),
    2706: ("Aw, we lost. I'd better find someone else to work for, and fast.",
           'Reacts with dismay at the defeat and says they need to find a new employer quickly.',
           'Use ordinary spoken language for finding work and keep the urgency.'),
    2707: ('Well, this puts me in a spot. What am I supposed to do now...?',
           'Recognizes the trouble they are in and wonders what to do.',
           'Keep the hesitation at the end and use a conversational opening.'),
    2708: ("Tch. I'll go hungry at this rate. Now what...?",
           'Grumbles that their livelihood is in jeopardy and wonders what to do.',
           'Keep the livelihood idiom and the rough, short question.'),
    2709: ("Hmm... Isn't there someone out there who could use me?",
           'Wonders whether anyone somewhere might need them.',
           'Keep the quiet searching question and the uncertain pause.'),
    2710: ("Well, this is a bind. I'll have to consider my next move.",
           'Acknowledges the predicament and says they must consider what to do with themselves.',
           'Keep the speaker’s composed deliberation in idiomatic English.'),
}
SPEAKERS = {
    0x021170E0: 'Commander of the defeated faction leader’s fleet',
    0x02117160: 'Commander of another fleet in the defeated faction',
    0x021171E0: 'Displaced fleet commander',
}


def original_groups(runtime, clean):
    groups, rows = earlier.FunctionType(prior.original_groups.__code__, vars(prior) | {'GROUPS': GROUPS})(runtime, clean)
    for row in rows.values():
        row['speaker'] = SPEAKERS[row['original_table']]
    return groups, rows


def main():
    source = checked_text(inspect.getsource(earlier.main), {
        "    resolve_groups = FunctionType(prior.original_groups.__code__, vars(prior) | {'GROUPS': GROUPS})\n    groups, bindings = resolve_groups(runtime, clean)":
            '    groups, bindings = original_groups(runtime, clean)',
        "        if n == 2755:\n            # The original wrapper receives a faction argument this voice never interpolates.\n            row['unused_native_arguments'] = row['original_substitutions']\n            row['original_substitutions'] = ()\n": '',
        '    neighbors = [source_record(japanese, current, n) for n in range(2690, 2711)]\n': '',
        'previously_credited_neighbors=results, next_faction_defeat_and_succession_context=neighbors,':
            'previously_credited_neighbors=results,',
    })
    env = vars(earlier) | globals()
    exec(compile(source, __file__ + '::original-fleet-dissolution-portraits', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()

