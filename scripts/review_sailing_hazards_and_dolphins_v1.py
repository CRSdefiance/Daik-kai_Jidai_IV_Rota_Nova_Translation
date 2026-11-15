"""Review the dolphin log exchange and the original sailing hazard reactions."""

from inspect import getsource

from scripts import register_oasis_and_whale_reports_v1 as parent
from scripts import review_crew_and_shore_reports_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


prior = previous.prior
BASE, ARM, COMMON, CLEAN = previous.BASE, previous.ARM, previous.COMMON, previous.CLEAN
OUTPUT = prior.ROOT / 'sailing_hazards_and_dolphins_context_v1.json'
CAPTAIN, ROLE, DIRECT = previous.CAPTAIN, previous.ROLE, 0x53F0C
GROUPS = (
    (2366, 2372, 0x116BE0, 0x7AB6C, 0x7AB74, 0x7AE98, ROLE, 7,
     'The lookout spots the dolphins and asks to record the encounter in the ship’s log. The next original call supplies the captain’s approval, and the farewell comes later.'),
    (2373, 2376, 0x116790, 0x7AB78, 0x7AB7C, 0x7AE9C, CAPTAIN, None,
     'Rafael, Hodram, Lil or Maria answers the lookout’s request according to the original four-captain table. Each agrees, with a different degree of formality.'),
    (2377, 2384, 0x116B80, 0x7ABC0, 0x7ABD4, 0x7AEA4, ROLE, 7,
     'The dolphins swim away after the log exchange. The lookout enjoys or reflects on the moment of peace. This is the closing beat of the encounter.'),
    (2385, 2390, 0x116BC0, 0x7AA50, 0x7AA58, 0x7AE90, ROLE, 15,
     'The original Sirens event has progressed from unfamiliar singing to a voice that overwhelms the sailor. The original role selector chooses the speaker or fallback. The lines express distress or fear of losing one’s mind.'),
    (2391, 2396, 0x116CE0, 0x72DDC, 0x72DE0, 0x73114, DIRECT, None,
     'After the Strange Bubbles sighting, warning and order to evade, the hazard is engulfing the ship. The original hazard dispatch applies damage after this report.'),
    (2397, 2398, 0x116F20, 0x65CA8, 0x65CB4, 0x65D40, DIRECT, None,
     'A crew member voices the cold in the original ship condition check. The lines express discomfort, with a shiver or stammer.'),
    (2399, 2403, 0x116F40, 0x65930, 0x65938, 0x65964, DIRECT, None,
     'A crew member cries out at lightning. The immediate reaction ranges from a clipped warning to a frightened stammer.'),
    (2404, 2408, 0x116FA0, 0x72E4C, 0x72E50, 0x73118, DIRECT, None,
     'The original tornado hazard has caught the ship. Some voices name it, while others react to being caught in it.'),
    (2409, 2412, 0x116FE0, 0x72ED4, 0x72ED8, 0x7311C, DIRECT, None,
     'The ship is caught in the whirlpool. The crew reacts to the current danger, ranging from alarm to the youthful image of being eaten.'),
    (2413, 2418, 0x117040, 0x72F74, 0x72F7C, 0x7312C, DIRECT, None,
     'The ship reaches the reef without the protection that selects the earlier extra-armor dialogue. The report announces the reef or the contact before the original damage is applied.'),
    (2419, 2424, 0x117060, 0x73038, 0x73040, 0x73138, DIRECT, None,
     'The ship encounters drift ice without the ram that selects the earlier protection dialogue. The officer reacts to steering or turning too late before the original damage is applied.'),
)

# Each entry records the localized wording when revised, the clean Japanese
# meaning, and the reason for the specific wording choice.
DECISIONS = {
    2366: (None, 'The lookout spots dolphins and asks permission to log the sighting.', 'Keep the quick recognition and clear question using ship’s log.'),
    2367: ("Admiral, look! A pod of dolphins! May I put this in the ship's log?", 'The lookout calls to the admiral, points out a pod and asks permission to record it.', 'Give the sighting its own beat and use the established ship’s log wording and standard I.'),
    2368: ("Wow, a pod of dolphins over there! Can I put this in the ship's log?", 'The excited lookout points out a pod and asks to record the sighting.', 'Keep the open delight and use a less formal request for this voice.'),
    2369: ("Admiral, look over there! Dolphins! May I write about them in the ship's log?", 'The lookout gets the admiral’s attention, points out the dolphins and asks to write about them.', 'Restore the act of pointing them out and phrase the request as recording a sighting.'),
    2370: (None, 'The lookout is amazed by the dolphins and casually asks to put the sighting in the log.', 'Keep the rough voice’s two bursts of excitement and conversational question.'),
    2371: ("Oh, a pod of dolphins! What a sight! May I make a note in the ship's log?", 'The older lookout calls the pod a splendid sight and then asks to record it.', 'Give the sight its own exclamation and preserve the more measured request.'),
    2372: ("Wow! So many dolphins! I'd love to put this in the ship's log. Can I, Admiral?", 'The youthful lookout marvels at how many dolphins there are, wants to write about them and asks the admiral.', 'Give the eagerness its own sentence and keep the direct appeal.'),
    2373: ('Sure, write it down.', 'Rafael agrees and asks the lookout to write it down.', 'Use Rafael’s easy assent and the simple action requested.'),
    2374: (None, 'Hodram formally grants permission.', 'Keep the deliberate permission in the captain’s formal voice.'),
    2375: ('Sure. Put it in the log.', 'Lil agrees and directs that the sighting be recorded.', 'Keep the two brisk beats and a natural spoken directive.'),
    2376: (None, 'Maria agrees and asks politely for it to be written down.', 'Keep the courteous request and concise assent.'),
    2377: ("There go the dolphins. That was soothing, wasn't it?", 'The lookout notes the dolphins leaving and shares a feeling of calm.', 'Preserve the warm invitation to share the reaction.'),
    2378: ('The dolphins have gone. What a peaceful sight.', 'The lookout first notices the departure, then reflects on the soothing sight.', 'Restore the sequence and the particular feeling the sight evoked.'),
    2379: (None, 'The lookout regrets that the dolphins have left and casually reflects on the pleasant feeling.', 'Keep the trailing pause and understated, conversational reaction.'),
    2380: ("There go the dolphins... It's nice to have a quiet moment now and then.", 'The lookout says the dolphins have gone and appreciates the occasional peaceful mood.', 'Restore the thought about how welcome an occasional quiet moment is.'),
    2381: ('There go the dolphins... That sure was peaceful.', 'The rough-voiced lookout sees the dolphins leave and feels serene.', 'Bring out the informal voice while keeping the calm.'),
    2382: ('So the dolphins have gone... That put me at ease.', 'The older lookout notices they have left and reflects on the calm they brought.', 'Retain the older speaker’s reflective opening and personal response.'),
    2383: (None, 'The youthful lookout bids the dolphins goodbye and savors the calm feeling.', 'Keep the direct goodbye and the relaxed, childlike afterthought.'),
    2384: ('Well, the dolphins are gone. That was a welcome little break...', 'The older lookout calls the time with the dolphins a brief rest.', 'Restore the brevity and give the measured farewell a natural cadence.'),
    2385: ("M-my head! I feel like I'm losing my mind!", 'The sailor stammers and fears the voice is driving them out of their mind.', 'Keep the broken opening and state the fear as a complete spoken thought.'),
    2386: ("Aah! What's that voice? I'm losing my mind!", 'The startled sailor hears a voice and feels they are going mad.', 'Restore the voice and mental distress where the earlier line described a headache.'),
    2387: ("Aah! M-my head! I feel like I'm going mad!", 'The sailor screams and fears their mind is giving way.', 'Preserve the cry and stammer with idiomatic spoken English.'),
    2388: ("H-help me! M-my head! I feel like I'm going mad!", 'The older sailor stammers for help and fears they are going mad.', 'Restore the panicked plea and broken delivery.'),
    2389: ('Aah! What a weird voice!', 'The youthful sailor cries out at the strange voice.', 'Keep the immediate fright and the specific voice.'),
    2390: ("Aah! I feel like I'm going mad!", 'The sailor cries out and fears losing their mind.', 'Use the speaker’s immediate fear of going mad.'),
    2391: ('The bubbles are swallowing the ship!', 'The bubbles are engulfing the ship.', 'Use the term established by the Strange Bubbles encounter and preserve the threat.'),
    2392: ('These bubbles are swallowing the ship!', 'The sailor says these bubbles are engulfing the ship.', 'Keep the immediacy of these and the present danger.'),
    2393: ('The bubbles are going to swallow our ship!', 'The sailor fears the ship is about to be engulfed by bubbles.', 'Keep the personal urgency and the sense of what is about to happen.'),
    2394: ("The bubbles are swallowing our ship!", 'The rough voice says the ship is being engulfed.', 'Keep the familiar reference to the ship and use the encounter’s hazard term.'),
    2395: ('Those bubbles are swallowing the ship!', 'The older voice sounds the alarm as bubbles engulf the ship.', 'Keep the pointed warning and the ongoing action.'),
    2396: ('The bubbles are eating our ship!', 'The youthful sailor imagines the ship being eaten by bubbles.', 'Restore the youthful image in a full spoken exclamation.'),
    2397: (None, 'The sailor groans and stammers from the cold.', 'Keep the natural shiver, stammer and pause.'),
    2398: (None, 'The younger sailor shivers and complains of the cold.', 'Keep the expressive shiver and complaint with a standard-width I.'),
    2399: (None, 'The frightened sailor exclaims and stammers over lightning.', 'Keep the startled opening and three-part stammer.'),
    2400: (None, 'The sailor briefly exclaims at lightning.', 'Keep the clipped warning.'),
    2401: (None, 'The startled sailor stammers the word lightning.', 'Keep the short warning and native character of the stammer.'),
    2402: (None, 'The frightened sailor stammers the word lightning.', 'Keep the abrupt cry without adding an explanation.'),
    2403: (None, 'The young voice cries out that there is lightning.', 'Keep the scream and quick recognition.'),
    2404: (None, 'The sailor realizes with dismay that the tornado has caught them.', 'Keep the blunt reaction and the reference to the visible danger.'),
    2405: ("This is bad! We're caught in the tornado!", 'The sailor sounds the alarm that they are caught in the tornado.', 'Express the present danger in two natural beats.'),
    2406: ("Aah! The ship's caught in the tornado!", 'The sailor screams that the ship is caught in the tornado.', 'Restore the trapped state and keep the ship as the subject.'),
    2407: ("This is bad! The ship's being pulled in!", 'The older sailor reacts to the ship being caught.', 'Retain the ongoing motion and the immediate warning.'),
    2408: (None, 'The youthful voice cries out that the tornado is swallowing them.', 'Keep the vivid image and the youthful alarm.'),
    2409: ('Whoa! The whirlpool caught us!', 'The sailor yells as they are caught in the whirlpool.', 'Restore the sudden alarm before the report.'),
    2410: ("We're in trouble! The whirlpool's got us!", 'The sailor urgently says they are caught in the whirlpool.', 'Use an immediate spoken warning and the whirlpool in view.'),
    2411: (None, 'The older sailor warns that they are being drawn into a whirlpool.', 'Keep the sense of motion and the explicit danger.'),
    2412: (None, 'The youthful sailor imagines the whirlpool eating the ship.', 'Keep the playful image within a real warning.'),
    2413: (None, 'The sailor realizes with dismay that there is a submerged reef.', 'Keep the surprise and the concealed hazard.'),
    2414: ("We've hit a reef!", 'The sailor reports that the ship is in contact with a reef.', 'Make the immediate collision clear without inventing damage.'),
    2415: (None, 'The sailor warns that the ship is in trouble because of a reef.', 'Keep the two short alarm beats.'),
    2416: ('Look out! A reef!', 'The sailor cries out in alarm at the reef.', 'Use a natural urgent warning in place of an abstract cry of trouble.'),
    2417: (None, 'The sailor urgently identifies a submerged reef.', 'Keep the explicit warning and the nature of the hazard.'),
    2418: (None, 'The young sailor stammers in fright and identifies a reef.', 'Keep the youthful cry and simple identification.'),
    2419: ("No! The rudder... We can't turn in time!", 'The sailor trails off about the rudder, then says there is no time to turn.', 'Restore the hesitation and preserve the urgent conclusion.'),
    2420: ("It's too late! We can't turn in time!", 'The sailor fears that it is already too late to steer clear.', 'Restore the stronger first beat and the reason for the panic.'),
    2421: ("No! The rudder... We won't turn in time!", 'The sailor cries out, hesitates over the rudder and says it is too late to turn.', 'Keep the interrupted thought and the officer’s own phrasing.'),
    2422: ("No good! We can't turn in time!", 'The older sailor says that there is no time to steer clear.', 'Keep the terse older voice and the urgency of the two thoughts.'),
    2423: (None, 'The youthful sailor cries out that they cannot steer.', 'Keep the specific loss of steering and the alarm.'),
    2424: ("This is bad! We won't turn in time!", 'The sailor warns in dismay that the ship will not turn soon enough.', 'Preserve the distinct warning and the timing of the danger.'),
}


def main():
    source = checked_text(getsource(previous.main), {
        "speaker='Storyline captain' if role is None else ('Original lookout or fallback' if role == 7 else 'Original First Mate or fallback')":
            "speaker=(('Rafael', 'Hodram', 'Lil', 'Maria')[slots.index(n)] if wrapper == CAPTAIN\n"
            "                    else 'Original lookout or fallback' if role == 7\n"
            "                    else 'Original role-selected sailor or fallback' if role == 15 else 'Original ship-duty officer')",
        'len(records) == 56': 'len(records) == 59',
        '[*range(2217, 2222), *range(2229, 2234), 312]': '[*range(436, 441), *range(457, 481), *range(2476, 2492)]',
    })
    env = vars(previous) | globals()
    exec(compile(source, __file__ + '::sailing-hazards-and-dolphins-source-review', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
