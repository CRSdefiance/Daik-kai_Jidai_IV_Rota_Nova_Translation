"""Seal complete-exchange English drafts before consulting these records' current English."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.gloss_hodram_B311_B324_clean_v1 import ROOT

MEANINGS = ROOT / 'all400_clean_meanings_before_English_v1.json'
OUT = Path('translations/hodram_B311_B324_clean_drafts_v1.json')

ORDINARY = {
311: {
84: 'Hm?', 113: 'Aaaah!', 117: 'Everyone, run!',
156: 'Dive into the brush!', 172: '...', 176: 'Is everyone all right?!',
180: 'Yeah!', 185: '...', 189: 'Is everyone all right?!', 193: 'Yeah!',
239: 'What is it?!', 270: 'Aaaah! Run!', 274: 'Hah... hah...',
278: "I've had enough!", 284: 'The sailors seem fatigued.',
290: 'Not much farther. Keep it together.', 323: 'We made it.',
327: 'Whew! That gave me a fright.'},
312: {
6: 'Oh, {MACRO:FI}! There was something I meant to tell you, but it completely slipped my mind.',
10: "I heard someone recently found an ancient pictorial map. Apparently, it shows the ruins of an old kingdom near this town.",
13: 'Oh? And where is this map?',
16: "Sorry, I don't know that much. If you're interested, why not go look for it?"},
313: {
65: "It's a desert. Of course it's hot. We press on.", 68: 'W-whoa!!',
92: 'Calm down.', 96: 'B-but... What are you going to do?',
115: 'Leave it to me. Hah!', 139: "Leave it to me. I'll drive them off.",
162: 'Gah!', 189: 'Damn! I let my guard down.',
228: '{MACRO:FI} was injured. You spend a day here for treatment.',
236: 'Sorry. I am all right now.',
242: 'We retreat quietly. Do not provoke them.', 275: 'Thud!',
279: 'Oops! There goes our gear!', 303: 'Aaagh!',
331: 'Run through! Hurry!', 336: 'A sailor seems to have been injured.',
355: "Oh! Looks like we've arrived!"},
314: {
6: 'Welcome!',
10: "Say, {MACRO:FI}, have you heard of the Goryeo Incense Burner? It's made of celadon. Apparently, it's somewhere in East Asia.",
14: "They say it makes your fortune-telling much more accurate. Oh, I'd love to try it just once...",
30: 'Oh, really?', 35: 'Oh, that reminds me!',
39: "It sounds like pirates have been causing trouble around here lately. You'd better make sure you're properly equipped.",
43: "Really? That sounds dangerous... Thanks. I'll be careful.",
47: 'See you around!'},
315: {
6: 'Oh, welcome back!',
10: "My readings have been much more accurate since you gave me that incense burner. Let me tell your fortune to thank you.",
14: 'Here, have a seat.', 18: '...', 22: '...',
26: "Far inland from this town, deep in the desert, there are ruins. I'm sure you'll find what you're looking for there."},
316: {
104: "Let's try pressing on for now.",
144: "We'll cut through the trees if we have to. Keep going.",
174: 'The sailors seem fatigued.', 179: "We'll find a way around.",
214: "It is dangerous to move in this. We'd better wait for the fog to clear.",
243: '...', 247: '......', 254: 'One day passed.',
258: "It seems to have cleared. Let's go."},
317: {
63: 'Whew. It is humid here. I am concerned about how exhausted the party is getting...',
89: 'It is darker than I expected...', 93: 'Admiral...',
108: 'Never mind. We press on.', 113: 'Hm? This feels like...',
116: 'Admiral! A huge snake! Ah! One of the party...!',
127: 'Aaaah! An Indian python!! (I think?)',
133: 'This is bad! Everyone, fall back!',
141: 'A sailor seems to have been injured.', 147: '...Where are we?',
176: "All right. Let's light a fire...",
180: "Ugh! Bats?! That's quite a swarm...",
206: 'Ignore them. Keep moving.', 214: 'The sailors seem fatigued.'},
318: {
12: 'First, please get a map to the ruins.',
44: "Actually... According to this map, the ruins don't seem to be on this island.",
48: 'What?', 54: "...We'll need to cross the sea.",
59: 'Then we should return to port.',
63: "No, I've prepared a small boat. We'll continue in that.",
66: "You are the only ones qualified. I'd like you to keep the location of the ruins from the sailors.",
75: 'One day passed.',
79: "We've arrived. We'll go overland from here.", 82: 'Oh? Huh?',
94: 'You are... Rafael of the Castor Company, correct? What are you doing here?',
100: '...Who are you?',
109: 'Your guide asked me to look for the ruins. I got lost along the way...',
114: 'So you were among those "strong-looking people" asked at random, too.',
117: "I'm sorry. There was no word from any of the searchers, so I finally decided to come along myself.",
121: "No, it's my fault. I should have done better...",
125: 'Well, no matter. We can search together.', 128: 'Yes.',
132: "You're right. Let's look together.", 136: 'Oh! There they are! We found them!',
165: 'Coming.'},
319: {
5: 'Oh, welcome!',
9: 'Say, have you ever been to that village far to the north in the New World?',
13: 'A customer told me about a respected monk from this town who traveled to the northern continent to spread his faith long ago.',
17: 'They say he found that village, then went missing. I wonder what happened to him.',
21: "Couldn't say.",
25: 'He was apparently a very virtuous man. I hope the people he went to preach to grew fond of him.',
28: 'If you ever head north, ask around about what became of him, would you?'},
320: {
5: "You don't look familiar. Where are you from?",
8: 'Sweden, in northern Europe.',
12: 'Hm? Never heard of it. You must have come a very long way.',
16: "Ah, I see! You must have one of those handy devices called a sextant, don't you?",
20: 'What?',
24: "I've heard about them. Something about knowing where you are at sea, even when there are no landmarks.",
28: "Well? Would you give us that sextant? I'll give you something good in return.",
31: 'Something good?', 35: "Bring it here, and you'll find out."},
321: {
6: "Oh, you brought it? Here, take this in exchange.",
14: 'You handed over the Sextant.'},
322: {
71: 'You provided all your money for initial expenses.',
76: 'You provided 1,000 gold coins for initial expenses.',
83: "We'll begin the investigation now. Please report to the Sofala guild."},
323: {
6: 'Is this what you came looking for?',
10: 'It has been so long... At last, the day has come.',
13: 'We will place our trust in you. Please, take it.'},
324: {
5: 'Oh! You know of the monk!', 9: 'You knew him?',
13: "He couldn't bear to see us suffering from that illness. He cared for us tirelessly. Thanks to him, our village wasn't wiped out.",
16: 'His medicine brought relief almost at once. It was a miracle.',
20: 'Did he know medicine?',
24: 'No, he called it alchemy. Something about removing the mineral poison that had gotten into our drinking water...',
28: 'Here, he wrote this book.', 39: 'Wait! Could this be...?!',
58: 'This is the book Charles mentioned! We finally found it!',
65: "The Alchemy Book?! I-I never thought we'd find it here!",
69: '...What is it, Charles?',
73: 'Not long ago, I heard a rumor that a new experimental material had been discovered in the New World!',
77: 'I learned that this Alchemy Book was needed to obtain it, but...',
81: "There is no doubt it holds a clue to some precious metal! Now, if I can just work out how to use it... Hmm...",
84: '...Sorry, but I do not have time for an explanation now.',
90: 'So, where is the monk now?', 94: '...', 98: 'Hm?',
102: "He drank the water here and came down with the same illness we had...",
105: 'But he kept it to himself and gave every last bit of the medicine he made to the villagers!',
109: "And in the end, he died...! He truly was a messenger of God...",
112: '...', 116: '...May we entrust this book to you?', 119: 'Entrust it to us?',
123: 'It holds the secrets of an ore no one has ever seen before.',
126: 'Surely there must be deposits of it somewhere in the world.',
129: "We seek someone to carry on the monk's research. Would you find that ore for us?",
133: '...You have my word. We will find it.',
144: "Of course! I'll investigate it thoroughly!",
148: "...All right, all right. Find this new ore, and I'll put you in command of a fleet in that region. You can research to your heart's content."},
}

# Each list follows the ordered physical offsets, not eight duplicate alias slots.
STYLE = {
(311,24): [
"Admiral, we cannot go any farther without a map.",
"Admiral, going on without a map would be reckless.",
"Admiral, without a map, we won't know where to go.",
"Admiral, how are we supposed to get anywhere without a map?",
"Admiral, we can't go on without a map.",
"Admiral, without a map, we won't know which way to go.",
"Admiral, we need a map! We won't know where to go!",
"Admiral, advancing without a map is impossible."],
(311,436): [
"It is very dark in this forest.", "Such a dense forest...",
"It's so dark in here, even in the daytime!", "It really is dark in here, isn't it?",
"It's a dark forest, all right.", "A dense forest, this...",
"It's pitch-black in here! Like nighttime!", "Quite a dense forest..."],
(311,654): [
"Admiral... Do you hear something?", "Admiral... Can you hear that?",
"Admiral... I can hear something. Can you?", "Admiral... I hear something!",
"Admiral... Do you hear that?", "Admiral... I can hear something..."],
(311,838): [
"Whoa! A rock coming from behind us!!", "Whoa! Behind us!!",
"Whoa! There's a huge rock behind us!!", "Aaaah! Behind us!!",
"Whoa! A rock behind us!!", "B-behind us!!",
"A rock is falling toward us from behind!!"],
(311,1124): [
"It's a dead end!", "Whoa! A dead end!", "No! It's a dead end!",
"Dead end!", "This is bad! A dead end!", "It's a dead end! Oh, no!"],
(311,1460): ['Hm?', 'Oh?'],
(311,1500): ['Aaaaaah!!', 'Eeeeeek!!'],
(311,1578): [
"A-a snake!!", "A huge snake!!", "A-a snake!", "Th-there's a snake!!",
"S-snake!!", "A-a snake!!", "S-snaaake!!", "Now it's a snake!!"],
(311,1918): [
"Oh! It rolled down the left path!", "The rock rolled down the left path!",
"Lucky us! The rock rolled off to the left!", "The rock went down the left path!",
"The rock rolled off to the left!", "Ah! It rolled down the left path!",
"The rock went down the left path!"],
(311,2220): [
"Admiral! Look, over there!", "Admiral! Look! There!",
"Admiral! Look over there!", "Admiral! Look, look! Over there!"],
(313,24): [
"Admiral, we will lose our way without a map.",
"Admiral, without a map, we'll get lost.",
"Admiral, we'll end up lost without a map!",
"Admiral, we're going to get lost without a map.",
"Admiral, we'll get ourselves lost without a map.",
"Admiral, we'll lose our way without a map.",
"Admiral, we'll get looost without a map!",
"Admiral, we shall lose our way without a map."],
(313,376): [
"It really is hot here.", "Whew, it's hot!", "It sure is hot...",
"Hot, isn't it?", "Ugh. It's so hot!"],
(313,546): [
"A-Admiral! A swarm of scorpions!", "Whoa! A swarm of scorpions!",
"Eek! S-scorpions!!", "A-Admiral! Look at all those scorpions!",
"A-Admiral! A whole swarm of scorpions!", "Aaaah! Scorpions!"],
(313,856): [
"Oh, they've fled! We can always count on you, Admiral.",
"Oh, they ran away! Well done, Admiral.",
"Oh, they ran off! We sure can count on you, Admiral!",
"Hey, they ran off! We can count on you, Admiral!",
"Ah, they've fled! A fine job, Admiral. We can count on you.",
"Oh, they ran away! Admiraaal, you're amazing!",
"Ah, they've fled! As expected, Admiral. Most reassuring."],
(313,1252): [
"Oh, they've fled! We can always count on you, Admiral.",
"Oh, they ran away! Well done, Admiral.",
"Oh, they ran off! We sure can count on you, Admiral!",
"Hey, they ran off! We can count on you, Admiral!",
"Ah, they've fled! A fine job, Admiral. We can count on you.",
"Oh, they ran away! Admiraaal, you're amazing!",
"Ah, they've fled! As expected, Admiral. Most reassuring."],
(313,1624): [
"Admiral! Are you all right?!", "Admiral! Are you okay?!",
"Admiral! You all right?!", "Admiraaal!"],
(313,1756): [
"He needs treatment immediately!", "We have to treat him, quickly!",
"Oh, no! We must treat him right away!", "We've got to treat him, quick!",
"He needs urgent treatment!", "He needs treatment at once!"],
(313,2118): [
"Come along, everyone. Quietly... Very quietly...",
"Everyone, let's go. Quietly now. Quietly...",
"Come on, everyone. Nice and quiet... Nice and quiet...",
"Let's go, everyone. Quietly... Very quietly...",
"Time to go, everyone. Quietly now. Quietly...",
"Come on, everybody! Quietly... Nice and quiet..."],
(313,2472): ['Oh, no!', 'Ah!', "We're in trouble!", 'Oh, no!'],
(313,2556): [
"A-are you all right?! Hang in there!", "Are you all right?! Hold on!",
"A-are you okay?! Hang in there!", "Hey! You all right?! Hang in there!",
"A-are you all right?! Hold on!", "A-are you all right? Stay with us!"],
(316,24): [
"Admiral, we are likely to get lost without a map.",
"Admiral, we will get lost without a map.",
"Admiral, we'll end up lost without a map!",
"Admiral, I think we'll get lost without a map.",
"Admiral, we're going to get ourselves lost without a map.",
"Admiral, we'll lose our way without a map.",
"Admiral, get us a map!", "Admiral, we shall lose our way without a map."],
(316,348): [
"Then let us set out.", "Shall we get going?", "Come on, let's go!",
"Well, let's head out.", "Right, let's get going!", "Come on, now! Off we go!",
"Ready, set... Let's go!"],
(316,520): [
"Fog is rolling in.", "The fog is rolling in, I see.", "It's getting foggy.",
"Oh, it's turned foggy.", "That's some thick fog.", "Fog's coming in, I see.",
"Wow, it's really foggy!"],
(316,754): [
"It appears to be a dead end.", "A dead end...", "Oh, great. A dead end.",
"It's a dead end...", "Looks like a dead end.", "Aww. It's a dead end!",
"Well, well. A dead end."],
(316,1010): [
"I'll try.", "Let us give it a try.", "This is ridiculous... I'll try, though.",
"I'll give it a try.", "All right! We're going all the way!",
"You ask a lot of us. Well, I'll give it a try.",
"This is crazy! All right... Here we go!"],
(316,1310): [
"Admiral, we found a fork in the path!", "Admiral, there is a fork in the path.",
"Admiral, look closely! There's a fork in the path!", "Admiral, there's a path this way!",
"Admiral, there's a path over here!", "Admiral, it looks like we can go this way!",
"Admiral! Over here! This way!", "Why, there is a path here!"],
(316,1634): [
"That seems the better choice.", "That's a good idea.", "Yes, that's best.",
"Yeah. Let's do that.", "Doesn't seem we have much choice.",
"Yeah, let's do that!", "That would be safer."],
(316,1916): [
"It is coming into view.", "I can see it now!", "It's coming into view!",
"Oh? Is that it?"],
(317,24): [
"Admiral, it is dangerous to wander aimlessly through a jungle like this.",
"Admiral, we can't just wander through a jungle like this with no idea where we're going!",
"Admiral, wandering through this jungle without a direction is dangerous.",
"Admiral, I'm not wandering around a jungle like this with no idea where to go.",
"Admiral, it's dangerous to wander aimlessly through such a jungle.",
"Admiral, it's dangerous to walk through a jungle like this without even a map!",
"Admiral, wandering aimlessly through this jungle would be dangerous."],
(317,446): [
"Well, shall we go?", "Let us go, then.", "Come on! Let's get going!",
"Well, let's go.", "Right, let's move.", "Well, off we go."],
(317,654): ["A cave, here of all places...", "Huh? There's a cave!"],
(317,1114): [
"...I'm not certain, but we seem to be near the ruins.",
"...We appear to be near the ruins.",
"Here? Um... I'm not sure, but aren't we near the ruins?",
"Um... Hm? It looks as though we're near the ruins.",
"Whoa! ...Aren't we near the ruins?!",
"Where are we?! ...Hmm. Looks like we've come out near the ruins.",
"Here? Um... Huh? I'm not really sure, but I think we're near the ruins! Lucky us!",
"Hmm... We seem to be near the ruins."],
(317,1648): [
"There are too many!", "There are way too many!",
"Aaaah! Admiral, there shouldn't be this many!", "There's too many of 'em!",
"Admiral! We cannot get through while fighting off this many bats!",
"Aaaah! Bats! They're so creepy!"],
(317,1974): [
"We did it, Admiral! We made it out of the jungle!", "We're out of the jungle!",
"We did it, Admiral! We're out of the jungle!", "What a relief! We're out of the jungle!",
"We did it, Admiral! We're clear of the jungle!", "We did it! Out of the jungle at last!",
"Well done, Admiral! We have made it out of the jungle!"],
(317,2252): [
"Admiral, we seem to have reached the ruins.", "Admiral, these are the ruins, aren't they?",
"Admiral, here are the ruins.", "Admiral, this is the place, then.",
"Admiral, looks like we've reached the ruins.", "Admiral! These are the ruins, huh?",
"Admiral, we have reached the ruins at last."],
(318,96): [
"It is hard to believe an ancient city once stood in a place like this...",
"An ancient city once stood here...",
"So there used to be an ancient city here!",
"An ancient city once stood here, of all places...",
"An ancient city, in a place like this...",
"Hard to believe an ancient city once stood in a place like this.",
"There used to be a town even way out here!",
"So an ancient city once stood in a place like this..."],
(318,1420): [
"Admiral, we have found the ruins.", "Admiral, we found the ruins!",
"Admiral, those are the ruins over there.", "Admiral, looks like we've found the ruins.",
"Admiral, seems we've found the ruins.", "Admiral! Those are the ruins, right?",
"Admiral, it appears we have found the ruins."],
(322,8): [
"We will put the survey party ashore now.", "We're putting the survey party ashore.",
"We'll put the survey party ashore.", "Let's get the survey party ashore.",
"Survey party going ashooore!", "We shall now put the survey party ashore."],
}

CAPTIONS = {
(311,1086): ['Go left', 'Go right'],
(311,1306): ['Left-hand brush', 'Right-hand brush'],
(313,782): ['Fight', 'Drive them off', 'Run'],
(316,674): ['Keep going', 'Wait for the fog to clear'],
(316,934): ['Press on anyway', 'Find a way around'],
(317,764): ['Feel our way forward', 'Light a fire'],
}

VOICE = {
0: 'Rafael is polite and youthful; preserve source actor0, without importing Hodram into his turns.',
1: 'Hodram is practical, restrained and decisive. Preserve concern, dry humor and source-supported courtesy without adding an office or relationship.',
2: 'Lil reacts with excited recognition; retain Charles as the existing given-name reference and do not assume both conditional reactions occur in sequence.',
18: 'Charles is enthusiastic and scholarly; the Alchemy Book and rumored material excite him, but neither proves a particular ore or confirmed discovery.',
22: 'Samwell panics and then doubts his own species identification. Keep that small self-undercutting joke.',
151: 'The sailor uses casual, immediate reactions; preserve the generic role without inventing a named participant.',
161: 'The resident is curious or solemn according to the exchange; age-coded Japanese register does not create a chief title or kinship.',
179: 'The source Villager label is contextual; do not infer that the guide and every village witness are the same individual.',
204: 'Verisa is warm and conversational. Her fortune-telling is her claim, not a new narrator-certified magical effect.',
205: 'Silvia is friendly and apologetic about forgotten information; keep the map lead as hearsay.',
206: 'Isabel is conversational and concerned about the missing monk, without inventing a religious order or personal relationship.',
207: 'Preserve the source captain-role selector and its own brief reaction; final runtime binding remains pending.',
208: 'Preserve the source companion selector without assigning an invented identity.',
214: 'Preserve the dynamic companion reaction as breath sounds rather than a spoken stage direction or medical diagnosis.',
254: 'The native status panel preserves the precise time, funding direction, apparent condition or source pause.',
}

SPECIAL = {
(311,180): 'A casual affirmative answers the urgent welfare question, not a greeting; no artificial elongated spelling is needed.',
(311,193): 'The alternate welfare check gets the same informal affirmative.',
(311,290): 'Keep the stern encouragement idiomatic without adding distance or an insult.',
(311,323): 'This expresses relief at survival; it does not credit an unstated rescuer.',
(312,10): 'Pictorial describes the map; do not identify it as a particular catalogue item from this generic description.',
(313,162): 'A pained sound does not introduce profanity.',
(313,189): 'The source explicitly curses here, unlike the earlier pained sound.',
(313,228): 'FI names the injured captain; one day is for treatment, without a promise of complete recovery.',
(313,279): 'Baggage falls; no quantity or permanent cargo loss is asserted.',
(314,10): 'Reuse the existing Goryeo Incense Burner item title and retain the celadon material explicitly in the dialogue.',
(316,243): 'The first wordless system pause is shorter than the following one; use ASCII punctuation to avoid mixed glyphs.',
(316,247): 'Retain a longer wordless pause than the preceding notice, without authored line breaks.',
(317,116): 'Leave the party-member alarm unfinished; do not invent a bite, swallowed victim or death.',
(317,127): 'The Indian-python identification is followed by Samwell doubting it, rather than a substitute joke.',
(318,109): 'Guide describes the person currently accompanying Hodram; no gender, friendship or kinship is added.',
(318,114): 'This recalls clean B287R104 asking strong-looking people indiscriminately; preserve the callback without claiming a deliberate qualification test.',
(321,14): 'The Sextant is handed over, not acquired.',
(322,71): 'The player supplies all money for initial expenses; this is not income.',
(322,76): 'Exactly 1,000 gold coins are supplied for initial expenses, not received.',
(324,24): 'Preserve the witness’s vague account of alchemy and mineral poison, without a named toxin or medical explanation.',
(324,109): 'Render the euphemism as death; preserve praise as God’s messenger without a canonized title.',
(324,148): 'The Japanese explicitly offers regional fleet command and freedom to research; retain the dry joke without assigning a modern formal admiral rank.',
}

def main():
    assert not OUT.exists()
    meanings = load(MEANINGS)
    assert meanings['records_count'] == meanings['source_meanings'] == 400
    assert meanings['English_drafts'] == meanings['current_story_English_compared'] == 0
    names = load(ROOT / 'draft_name_reference_v1.json')
    items = load(ROOT / 'draft_item_reference_v1.json')
    assert names['source_meanings_sha256'] == digest(MEANINGS)
    assert {x['source_Japanese']: x['current_English'] for x in items['records']} == {
        '高麗青磁の香炉': 'Goryeo Incense Burner', '六分儀': 'Sextant', '錬金術の書': 'Alchemy Book'}
    style_groups = {}
    for row in meanings['records']:
        if row.get('kind') == 'actor-style-alternative':
            key = (row['block'], row['source_command_offset'])
            style_groups.setdefault(key, []).append(row)
    assert set(style_groups) == set(STYLE)
    style_english = {}
    for key, rows in style_groups.items():
        rows = sorted(rows, key=lambda x: x['source_reference']['offset'])
        assert len(rows) == len(STYLE[key]), (key, len(rows), len(STYLE[key]))
        assert sorted(i for row in rows for i in row['source_style_indices']) == list(range(8))
        style_english.update({row['id']: english for row, english in zip(rows, STYLE[key], strict=True)})
    rows = []
    for original in meanings['records']:
        row = deepcopy(original)
        block = row['block']
        if row.get('kind') == 'actor-style-alternative':
            english = style_english[row['id']]
            speaker = 'Native companion role ' + str(row['source_selector'])
            note = row['source_meaning'] + ' Keep this register and every physical alias; do not assign an age, gender, kinship or named participant.'
        elif row.get('kind') == 'typed-choice-label':
            english = CAPTIONS[(block, row['source_command_offset'])][row['source_index']]
            speaker = 'Choice caption'
            note = row['source_meaning'] + ' Preserve the original branch order and complete-exchange action.'
        else:
            index = row['source_reference']['record_index']
            english = ORDINARY[block][index]
            speaker = 'Native system panel' if row['source_selector'] == 254 else 'Source actor ' + str(row['source_selector'])
            note = row['source_meaning'] + ' ' + VOICE[row['source_selector']]
            if (block, index) in SPECIAL:
                note += ' ' + SPECIAL[(block, index)]
        english.encode('ascii')
        assert english.strip() == english and '\n' not in english and '\r' not in english
        assert not any(token in english for token in ['{LB', '{ALIGN', '{PAD}', '%'])
        assert all(english.count('{MACRO:' + macro + '}') == row.get('source_macros', {}).get(macro, 0)
                   for macro in ['FI', 'FA', 'FO']), (row['id'], english)
        row.update(english=english, speaker=speaker, context=row['exchange_context'], localization_note=note,
                   review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False),
                   clean_first_draft_not_final_comparison_approval=True, current_English_conversation_comparison_pending=True,
                   source_names_terms_anddisplay_still_require_scoped_current_binding=True, new_credit=0)
        rows.append(row)
    assert len(rows) == 400 and len({row['id'] for row in rows}) == 400
    assert sum(row.get('kind') == 'actor-style-alternative' for row in rows) == 236
    assert sum(row.get('kind') == 'typed-choice-label' for row in rows) == 13
    ordinary_keys = {(row['block'], row['source_reference']['record_index']) for row in rows if row['id'].startswith('DK4_')}
    assert ordinary_keys == {(block, index) for block, values in ORDINARY.items() for index in values}
    save(OUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
                  review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'], records=rows,
                  records_count=400, ordinary_drafts=151, physical_style_drafts=236, typed_caption_drafts=13,
                  complete_exchange_blocks=list(range(311, 325)), source_meanings=str(MEANINGS), source_meanings_sha256=digest(MEANINGS),
                  all400_logical_drafts_written_before_current_ROM_story_English_intake=True,
                  prior_names_andnonstory_terms_consulted_as_references=True, no_blanket_claim_of_no_historical_English_exposure=True,
                  linked_clean_B287_recruitment_context_read=True, current_English_comparisons=0,
                  current_comparison_name_term_formatting_andrelease_gates_pending=True,
                  no_ordinary_manual_breaks_padding_alignment_ornew_story_fact=True,
                  full_goal_complete=False, new_credit=0, guide_photos=False,
                  evidence={str(path): digest(path) for path in [MEANINGS, ROOT / 'draft_name_reference_v1.json',
                      ROOT / 'draft_item_reference_v1.json', ROOT / 'linked_clean_recruitment_context_v1.json', Path(__file__)]}))
    print('Sealed400 source-first logical drafts. Current comparisons, scoped names/terms and all display checks remain.')

if __name__ == '__main__':
    main()
