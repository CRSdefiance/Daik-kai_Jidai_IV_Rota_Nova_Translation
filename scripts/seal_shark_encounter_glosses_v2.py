"""Seal the individual clean-source glosses without changing the reviewed English."""

from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.review_shark_encounter_v1 import OUTPUT as INITIAL
from scripts.stage_shark_encounter_v1 import PROOF


OUTPUT = INITIAL.with_name('shark_encounter_context_v2.json')
MEANINGS = {
    2425: 'Al remarks that the creature they just fought was quite formidable.',
    2426: 'Rafael agrees readily with Al’s assessment of the fight.',
    2427: 'Hodram agrees with Al in a short, matter-of-fact response.',
    2428: 'Maria agrees with Al’s assessment of the fight.',
    2429: 'Lil agrees with Al’s assessment of the fight.',
    2430: 'Al asks the admiral what they should do with the shark.',
    2431: 'Even granting that a shark is a monster, Rafael hesitates to kill one this small.',
    2432: 'Even with a shark, Hodram is reluctant to kill a creature that is this small.',
    2433: 'Lil points out how small the shark is and says killing it would be pitiless.',
    2434: 'Even though it is a shark, Maria cannot bear to take the life of such a small creature.',
    2435: 'Al protests the idea of letting it go back into the sea and asks the admiral to consider what might happen when it grows up.',
    2436: 'Al reacts with drawn-out shock and asks whether the admiral is serious.',
    2437: 'Rafael confirms the decision and looks forward to finding out what happens.',
    2438: 'Hodram confirms he is serious.',
    2439: 'Lil agrees but trails off because she does not know how it will turn out.',
    2440: 'Maria gives a complete affirmative answer.',
    2441: 'Al disclaims responsibility for whatever happens later, then mutters in displeasure.',
    2442: 'Al says this is the best course for the future and that pity is unnecessary.',
    2443: 'Samwell asks casually for a moment to speak.',
    2444: 'Rafael asks what Samwell wants to say.',
    2445: 'Hodram tersely asks what Samwell wants.',
    2446: 'Lil asks informally what Samwell wants.',
    2447: 'Maria asks what Samwell wants to say.',
    2448: 'Samwell has a hunch that sharks may be edible and could become a new trade good.',
    2449: 'Samwell suggests keeping and raising this one as a way to test his idea.',
    2450: 'Al challenges what Samwell is saying and tells him he does not know how frightening sharks are.',
    2451: 'Al says the best course when a shark is caught is to kill it. He urges the admiral to set Samwell’s suggestion aside and kill the shark at once.',
    2452: 'Samwell enthusiastically approves and says he is excited and looking forward to it.',
    2453: 'Samwell sighs about losing the makings of a feast and says it is a waste.',
}


def main():
    assert not OUTPUT.exists()
    initial, proof = map(load, (INITIAL, PROOF))
    assert digest(INITIAL) == proof['evidence'][str(INITIAL)]
    assert tuple(MEANINGS) == tuple(row['message_ID'] for row in initial['records'])
    result = initial | dict(records=[row | {'source_meaning': MEANINGS[row['message_ID']]} for row in initial['records']],
        initial_manuscript=str(INITIAL), initial_manuscript_sha256=digest(INITIAL),
        individual_clean_glosses_producer=str(Path(__file__)), individual_clean_glosses_producer_sha256=digest(__file__))
    save(OUTPUT, result)


if __name__ == '__main__':
    main()
