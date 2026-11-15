"""Review Rafael's quest assignments, leads, and hidden village exchanges."""

import argparse
from pathlib import Path
from types import FunctionType

from scripts import register_rafael_history_wraps_20261114 as parent
from scripts import stage_rafael_history_wraps_20261114 as previous


base, sha, prior = previous.base, previous.sha, previous.prior
FILE, ARM, CLEAN, IlnkContainer = previous.FILE, previous.ARM, previous.CLEAN, previous.IlnkContainer
ROOT = Path('work/rafael_quest_wraps_20261114_v1')
CAPTURE = ROOT / 'rafael_startup/capture_report.json'
RUNTIME = ROOT / 'rafael_native_context.json'
REVIEW = parent.TRIAGE.with_name('rafael_quest_wraps_context_v1.json')
PROOF = ROOT / 'stored_and_native.json'

FEVER = "I think he'll be all right now. His fever seems to be down, too."
GRATITUDE = "You're a good man. I'll never forget what you did. Anything you want to know about this town, just ask."
GRATITUDE_MEANING = 'The guildmaster says he will always remember Rafael’s kindness and offers to answer any questions about the town.'
FEVER_MEANING = 'Rafael thinks the boy will now be all right and says his fever seems to have eased.'

DECISIONS = {
    (254, 149): ('Priest', "The figure seems to accept you.",
        'The priest says it appears that the figure has recognized the group as worthy.',
        'Maintain his cautious judgment after the ordeal. Julio calls it luck, and the priest rejects the need for modesty.',
        ('seems to accept you.',)),
    (255, 19): ('Margrete', "A sailor who went to the New World told me there's a river with gold dust flowing through it.",
        'Margrete heard from a sailor who had been to the New World that a river there carries gold dust.',
        'Attribute the claim to the sailor and keep the image of gold in motion before Margrete calls the sight romantic.',
        ('to the New World', "told me there's a river", 'gold dust flowing through it.')),
    (258, 7): ('Nelly', "Have you seen the pyramid yet?",
        'Nelly opens by asking whether Rafael has already visited the pyramid.',
        'Keep a friendly opening question. She offers directions once Rafael says he has yet to go.',
        ('seen the pyramid yet?',)),
    (260, 9): ('Rafael', "Well... There's something strange about this statue. I can feel something coming from it. Almost like compassion...",
        'The statue feels strange to Rafael, as though he senses compassion coming from it.',
        'Preserve the hesitation and tentative feeling. Cesare cannot see the statue at first and asks where it is.',
        ('something strange', 'about this statue.', 'coming from it.', 'Almost like compassion...')),
    (261, 6): ('Fernando', "Over here, Admiral! There's writing on the wall!",
        'Fernando calls the admiral over to look at an inscription on the wall.',
        'Use the brisk summons and keep the wall writing clear just before the inscription appears.',
        ('Over here, Admiral!', "There's writing on the wall!")),
    (266, 8): ('Sailor', "(Always bossing me around. Who does he think he is?)",
        'The sailor thinks Jean always acts superior and resents the way he speaks.',
        'Keep the private complaint in parentheses. Jean immediately tells him to obey.',
        ('Who does he think he is?', 'bossing me around.')),
    (266, 53): ('Jean', "L-look, I don't smuggle anything. Ha ha, honest! It isn't smuggling. You can take my word for it. That's right.",
        'Jean stammers and laughs, keeps denying that he smuggles, then appeals to his own reliability and agrees with himself.',
        'Keep the repetition and nervous laugh so Rafael’s remark about his loss of nerve makes sense.',
        ("I don't smuggle anything.", 'Ha ha, honest!', "It isn't smuggling.", 'my word for it.', "That's right.")),
    (266, 56): ('Rafael', "You were talking big a minute ago. Look at you now... Come on. We're going to the guild in Sofala.",
        'Rafael remarks how pitiable Jean seems compared to earlier, then takes him to the Sofala guild.',
        'Preserve Rafael’s judgment and the destination while moving briskly from Jean’s denial to the escort.',
        ('talking big a minute ago.', 'Look at you now...', "We're going", 'the guild in Sofala.')),
    (269, 14): ('Guildmaster', "Catch a smuggler for me, will you? His name's Jacob Portunto. He's a slippery one. Nothing but trouble.",
        'The guildmaster asks Rafael to catch the cunning smuggler Jacob Portunto, who has been a major nuisance.',
        'Keep the full name, the smuggling and the guildmaster’s irritation before his East Africa lead.',
        ('a smuggler', "His name's Jacob Portunto.", "He's a slippery one.", 'Nothing but trouble.')),
    (272, 19): ('Guildmaster', "Looking for Jacob? Heard he's based in Mozambique.",
        'The guildmaster asks if Rafael is looking for Jacob and says he has heard Jacob uses Mozambique as his base.',
        'Keep the familiar question and the hearsay qualifier. Put the location and what it means together.',
        ('Looking for Jacob?', "heard he's based in Mozambique.")),
    (273, 11): ('Guildmaster', "Stole our guild's client list. Fled with it to the Netherlands.",
        'Jacks stole the guild’s client list and took it with him when fleeing to the Netherlands.',
        'Keep the object and first destination. The following speech distinguishes that from the later rumor he went to Africa.',
        ("our guild's client list", 'fled with it', 'to the Netherlands.')),
    (277, 6): ('Guildmaster', "I think you're up to this. I need you to take down a man.",
        'The guildmaster has selected Rafael as someone he can rely on to take down the target.',
        'Keep the personal confidence supporting the request before the name and treason allegation.',
        ("I think you're up to this.", 'to take down a man.')),
    (280, 13): ('Guildmaster', "The outlaw is Plett Perrault. You'll help her, right?",
        'The guildmaster names Plett Perrault and asks Rafael to agree to help the bereaved woman.',
        'Keep the approved name and the direct appeal for help. She intends to avenge her father herself.',
        ('Plett Perrault.', "You'll help her, right?")),
    (281, 72): ('Guildmaster', "Ever been to the Forbidden City? It's worth seeing at least once. It's a bit of a trip from here.",
        'The guildmaster asks if Rafael has been to the Forbidden City and says it is worth seeing despite the distance.',
        'Keep the Forbidden City and the casual aside after the reward. The next line asks Rafael to keep the recommendation quiet.',
        ('the Forbidden City?', 'worth seeing at least once.', 'a bit of a trip from here.')),
    (283, 11): ('Guildmaster', "They say he leads a squadron that roams these waters. Here's your advance. The rest comes when you finish.",
        'The guildmaster has heard that Peralonso commands a mobile squadron in the area. He pays an advance and promises the balance on completion.',
        'Keep the squadron, the performance condition and the advance handed over in the following notice.',
        ('leads a squadron', 'roams these waters.', "Here's your advance.", 'The rest comes when you finish.')),
    (284, 5): ('Rafael', "I've brought Peralonso in.",
        'Rafael reports that he caught Peralonso and brought him back.',
        'Use a simple delivery report. Both the waiting guildmaster and the embarrassed captive respond.',
        ("I've brought Peralonso in.",)),
    (284, 74): ('Guildmaster', "Word is an ancient kingdom's ruins still stand intact in the jungle far inland from here.",
        'The guildmaster has heard that the ancient kingdom’s ruins remain intact in jungle far inland from town.',
        'Keep the distance and condition of the ruins as claims. The guildmaster next says nobody has confirmed them.',
        ("an ancient kingdom's ruins", 'still stand intact', 'in the jungle', 'far inland from here.')),
    (286, 11): ('Guildmaster', None,
        'The guildmaster has intelligence that Clive is headed for Havana, requests Rafael’s help and gives him an advance.',
        'Keep the reported destination and lay out the trust and payment as separate beats before the amount appears.',
        ("he's headed for Havana.", "I'm counting on you.", "Here's your advance.")),
    (286, 26): ('Guildmaster', "One thing I forgot to mention earlier. I hear he's dangerous. Strong doesn't cover it... You'll see when you meet him. I'm counting on you.",
        'The guildmaster adds that Clive is reportedly very dangerous, that mere strength does not explain it, and that Rafael will understand once they meet.',
        'Retain the uneasy qualification, the absence of specifics and the renewed request as the last beat.',
        ('forgot to mention earlier.', "I hear he's dangerous.", "Strong doesn't cover it...", "You'll see when you meet him.", "I'm counting on you.")),
    (295, 49): ('Guildmaster', "Yeah, that's it! You came prepared. Looks like this job's in good hands. I'm counting on you.",
        'The guildmaster confirms the map, praises Rafael’s preparedness and feels confident entrusting him with the job.',
        'Keep the three beats after the player already has the correct map. The guildmaster’s reaction should sound familiar and approving.',
        ("Yeah, that's it!", 'You came prepared.', "job's in good hands.", "I'm counting on you.")),
    (299, 77): ('Claudio', "Hold on. What's going on here? Were they really looking for this?!",
        'Claudio is astonished that the search seems to have been for this blank scrap.',
        'Keep his surprise after the scrap and blankness are revealed. Rafael answers with the practical decision to leave.',
        ("What's going on here?", 'looking for this?!')),
    (301, 80): ('Arcadius', "...Can you slow down a little? It's too dark to see where I'm stepping.",
        'Arcadius politely asks the others to slow down because he cannot see where he is putting his feet.',
        'Keep the discomfort and physical reason after Rafael says they should hurry. The growl interrupts the exchange.',
        ('slow down a little?', "It's too dark to see", "where I'm stepping.")),
    (302, 20): ('Lucia', "...It won't be that easy! The forest outside town is thick, and it's full of dangerous animals.",
        'Lucia warns the crew that the ruins will be hard to find, with dense forest and dangerous animals beyond the town.',
        'Keep the warning in response to the prospect of being first. Her next line offers directions and insists on a map.',
        ("It won't be that easy!", 'The forest outside town', 'full of dangerous animals.')),
    (303, 31): ('Rafael', "The Indian Ocean's Proof comes first, then!",
        'Rafael realizes they must find the Indian Ocean’s Proof first.',
        'Keep the order of discovery and use the established shorthand from the preceding lines.',
        ("The Indian Ocean's Proof", 'comes first, then!')),
    (305, 69): ('Rafael', "Whew! We're finally at the top!",
        'Rafael exhales with relief as the group finally reaches the top.',
        'Keep the spoken breath and relief before the guide says goodbye.',
        ("We're finally at the top!",)),
    (305, 97): ('Claudio', "It's a hidden village, right? I bet they still tell stories from way back!",
        'Claudio guesses that a hidden village would still have old legends.',
        'Let his excitement cut through the fear of the forest without making the legends a certainty. Rafael then connects them to the Proof.',
        ('a hidden village, right?', 'stories from way back!')),
    (305, 194): ('Janus', "We really have to cross there...?",
        'Janus asks uneasily whether they are really to cross in such a place.',
        'Keep his hesitation at the log bridge. Claudio teases him and urges him to cross.',
        ('have to cross there...?',)),
    (306, 31): ('Guildmaster', "...The boy's seriously ill.",
        'The guildmaster hesitates, then admits the boy has become gravely ill.',
        'Keep the difficulty of admitting the illness before Rafael asks for details and the father gives the bleak prognosis.',
        ("The boy's seriously ill.",)),
    (306, 112): ('Rafael', FEVER, FEVER_MEANING,
        'He responds to the returning color and the reduced cough with measured reassurance. The same recovery is shown via B308.',
        ("he'll be all right now.", 'His fever seems to be down, too.')),
    (306, 142): ('Guildmaster', GRATITUDE, GRATITUDE_MEANING,
        'Keep the father’s gratitude and concrete offer before Rafael says goodbye. Use the same wording in the alternate encounter.',
        ("I'll never forget what you did.", 'about this town, just ask.')),
    (308, 30): ('Rafael', FEVER, FEVER_MEANING,
        'Keep the same reassurance as B306 when the father sees the medicine work in this alternate path.',
        ("he'll be all right now.", 'His fever seems to be down, too.')),
    (308, 60): ('Guildmaster', GRATITUDE, GRATITUDE_MEANING,
        'Keep the same gratitude as B306. Here it leads into the guildmaster answering the question about ruins.',
        ("I'll never forget what you did.", 'about this town, just ask.')),
    (309, 30): ('Guildmaster', "If you're set on going, try climbing the cliff. It's a little risky.",
        'The guildmaster offers climbing the cliff as an option for someone determined to go and warns of the danger.',
        'Keep the option conditional and the warning mild. Rafael then checks that he really means climbing.',
        ("If you're set on going,", 'try climbing the cliff.', "It's a little risky.")),
    (309, 50): ('Guildmaster', "Sure, I'll take you to the cliff. Bring a map and meet me back here.",
        'The guildmaster agrees to guide them to the cliff and tells them to bring a map when they meet him here.',
        'Keep the promise, meeting point and map requirement together before Rafael asks why a map is needed.',
        ("I'll take you to the cliff.", 'meet me back here.')),
    (309, 59): ('Guildmaster', "Yes, it's a hidden village. Its people are Christians. Even I don't know the exact way once you're up the cliff. You can probably find a map in a Mediterranean town.",
        'He says it is a hidden Christian village, admits he does not know the route beyond the climb, and suggests a town in the Mediterranean might sell a map.',
        'Keep the reason for needing the map and the uncertain regional lead. The climb and the route afterward are distinct.',
        ('a hidden village.', 'Its people are Christians.', "don't know the exact way", "once you're up the cliff.", 'in a Mediterranean town.')),
}


get_exchanges = FunctionType(previous.get_exchanges.__code__, previous.get_exchanges.__globals__ | globals())
compile_rows = FunctionType(previous.compile_rows.__code__, previous.compile_rows.__globals__ | globals()
                            | {'previous': previous.compile_rows.__globals__['previous']})
bind_runtime = FunctionType(previous.bind_runtime.__code__, previous.bind_runtime.__globals__ | globals())
main = FunctionType(previous.main.__code__, previous.main.__globals__ | globals())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', action='store_true')
    main(parser.parse_args().preview)
