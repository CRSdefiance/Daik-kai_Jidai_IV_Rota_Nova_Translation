"""Review Hodram's B224 through B229 conversations from the clean Japanese."""

from scripts import pair_hodram_B221_B240_20261122 as paired
from scripts import review_hodram_B221_B223_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = paired.base, paired.ROOT
OUTPUT = ROOT / "B224_B229_contextual_v1.json"
GLYPHS = {"DK4_MES_B225_R0005", "DK4_MES_B227_R0011"}
CONTEXTS = {
    224: "A merchant challenges the heroic account of the Crusades. Al shares his own account of the invaders and explains why he admires Saladin. He suggests looking for armor Saladin wore.",
    225: "Hodram finds Gerhard watching the sunset. Gerhard recounts Noritsune's last battle and is unusually moved. Hodram responds to his account and quietly returns to the detail about the armor.",
    226: "A native crew voice announces Ian's letter. Ian relates a book's story about Timur and the mail stolen from his grave. Cesare suggests why Ian might have an interest in the subject.",
    227: "Julian compares Safia's gaze to Medusa's after hearing a rumor about the shield. Safia teases him about the comparison, while Julian turns it into a romantic fantasy. Safia admits to herself that it did affect her.",
    228: "Hodram watches children play at being Charles Martel. Gerhard explains the importance that he attributes to Martel's victory and wonders how future generations will remember Hodram.",
    229: "Hodram and Gerhard meet Manuel in the square. Manuel talks about Attila's challenge to the Roman empires before explaining the rumor he heard about armor carried northwest after Attila's death.",
}
DECISIONS = {
    224: """
5|Hey, you! You can't just walk through our square without stopping!|through our square;without stopping!|The merchant calls out to a passerby and gives him a reason to stop.
8|||Hodram asks what makes the town worth his attention. The question follows the interruption.
12|Ever hear of the Crusades?|hear of the Crusades?|The merchant tests whether Hodram knows the subject. His plainspoken question invites either menu response.
SC1_B224_CHOICE_138_0|||Yes confirms familiarity and lets the merchant challenge the familiar account.
SC1_B224_CHOICE_138_1|||No leads to his explanation of the version told in Europe.
28|Hmph. I bet you heard they were chivalrous soldiers who fought to take back the Holy Land.|chivalrous soldiers;the Holy Land.|The merchant assumes the player knows the chivalric account and repeats it with audible skepticism.
34|Hmph. In Europe, they tell it as a story about chivalrous soldiers fighting to take back the Holy Land...|chivalrous soldiers;the Holy Land...|On the other branch he attributes the same account to Europe before challenging it.
40|That's a lie that suits them. People in this town know what the Crusaders were really like.|a lie that suits them.;what the Crusaders|The merchant rejects that account and asserts the townspeople's knowledge in his own voice.
43|Oh? What really happened?|What really happened?|Hodram invites him to explain the truth he claims to know.
47|I've heard a little myself. They were after the wealth of this region, weren't they? They looted and killed as they went. Anything went.|the wealth of this region,;weren't they?;looted and killed|Al agrees with the merchant's account of motive and adds the violence he has heard about.
50|I can't stand the way they've twisted history to suit themselves! Saladin was our real hero!|twisted history;our real hero!|The merchant objects to the retelling and openly takes pride in Saladin. The contrast with the Crusaders is clear from the preceding turns.
53|||Hodram asks who Saladin was, giving Al the chance to explain.
57|His name still lives on in Islamic history. Driving back the Crusaders was only part of what made him great.|in Islamic history.;Driving back the Crusaders|Al distinguishes Saladin's historical stature from the single military achievement.
61|He fought humanely, treated prisoners and ordinary people with decency, and offered fair terms for peace. A fine man. He never stooped to dirty tricks.|treated prisoners;ordinary people;terms for peace.;dirty tricks.|Al's admiration covers conduct in war, treatment of captives and civilians, and peace terms. The final judgment belongs to him.
64|||Hodram sums up the qualities Al and the merchant admire in a short acknowledgment.
68|Come to think of it, I heard some armor Saladin wore went missing... If you'd like to take after him, why not look for it?|armor Saladin wore;went missing...;why not look for it?|Al remembers a rumor about the armor and proposes a search. His suggestion follows their praise of Saladin.
""",
    225: """
5|......||Preserve the long silent pause with two native ASCII ellipses before Hodram speaks.
9|What's the matter, Gerhard? Watching the sunset... Something on your mind?|What's the matter, Gerhard?;on your mind?|Hodram notices Gerhard looking at the sunset and asks about his distraction.
12|Admiral... I heard about a man here in Japan. I don't usually let a story get to me like this...|here in Japan.;get to me like this...|Gerhard admits he is unusually moved by a story he heard in Japan.
16|Oh? Who was it about?|Who was it about?|Hodram asks about the person in the story with interest.
20|||Gerhard names the warrior Noritsune and places him centuries in the past.
23|||Hodram asks what the man did, inviting Gerhard to tell the whole story.
27|He belonged to a clan that had once been powerful. After defeat upon defeat at the hands of a rival, the clan was driven to ruin.|once been powerful.;defeat upon defeat;driven to ruin.|Gerhard describes both Noritsune's affiliation and the repeated defeats that brought the clan down.
30|As his fainthearted kin were cut down one by one, he alone had the courage to stand and fight...|one by one,;stand and fight...|Gerhard judges the fallen kin harshly and singles out Noritsune's courage.
33|||The reported feat keeps the final sea battle, seven ships and the enemy commander's ship distinct.
37|||The old account keeps both soldiers, his failing strength, the strait and the brilliant armor. The pause preserves Gerhard's tone.
40|To think a man of such courage came from this small country in the East... I feel as though I've glimpsed the spirit of its people.|a man of such courage;in the East...;the spirit of its people.|Gerhard relates his impression of Noritsune and the East in his own awed voice.
44|A fearsome way to die... He must have been a true warrior.|A fearsome way to die...;a true warrior.|Hodram reacts to the terrible death and offers his own judgment of Noritsune.
47|||Gerhard's short agreement lets Hodram respond to his unusual emotion.
51|Gerhard, I can see how much that story meant to you.|how much that story;meant to you.|Hodram acknowledges Gerhard's feeling before returning to the armor clue.
54|||Hodram echoes the last detail about the strait and the armor. Keep his thought unfinished.
57|I've gone on longer than I meant to. Shall we get back to work?|longer than I meant to.;back to work?|Gerhard notes he got carried away and gently turns the conversation back to work.
""",
    226: """
SC1_B226_STYLE_8_0|||The plain delivery announces that Ian's letter has arrived and keeps the admiral's address.
SC1_B226_STYLE_8_40|Admiral, correspondence has arrived from Ian.|correspondence has arrived;from Ian.|The formal voice uses the same register as for Yukihisa's and Janus's letters.
SC1_B226_STYLE_8_80|||The direct contraction gives this announcement an easy tone.
SC1_B226_STYLE_8_116|||The courteous alternative puts the letter before the address to the admiral.
SC1_B226_STYLE_8_156|||The brisk fragment suits the familiar crew voice, and Ian remains the sender.
SC1_B226_STYLE_8_192|||Here retains the immediacy of this voice's announcement.
SC1_B226_STYLE_8_228|||The drawn-out call is expressed by two short exclamations in the eager voice.
28|The other day, I found an interesting book in an antique shop.|an interesting book;in an antique shop.|Ian starts his letter with the source of the story and the time of his discovery.
31|It was about Timur. Some two hundred years ago, he carried on the line of the declining Mongol Empire and built a vast empire from Central to Western Asia.|Some two hundred years ago,;the declining Mongol Empire;a vast empire;Central to Western Asia.|Ian recounts the book's account of Timur, the dynastic claim, span of territory and approximate date.
34|The book says he wore such sturdy mail that arrows bounced off it and the blades of swords and spears chipped against it.|such sturdy mail;arrows bounced off it;swords and spears|Ian attributes the mail's remarkable strength to the account he read.
37|||Ian says that the mail was buried with Timur and stolen decades later along with other grave goods. The chronology is clear.
40|||The passage keeps the thieves' motive, their desert route and how close they were to seeing the sea.
44|||Ian records that the story went unknown for a long time and that the mail remains undiscovered.
48|If you're interested, it might be worth looking into. Ian Dukov|it might be worth looking into.;Ian Dukov|Ian closes with a polite suggestion. Preserve the approved signature and give it a distinct final row.
56|Oh? Ian's interested in Asian history?|interested in Asian history?|Hodram is surprised by Ian's interest rather than stating a new biographical fact.
67|||Cesare links Ian's likely interest to the empire's rule over the Russian people and years of conflict. The explanation remains conjecture.
70|||Hodram acknowledges the explanation without stating that he agrees.
""",
    227: """
5|||Julian greets Safia and compliments her eyes. Mysterious sets up his reference to Medusa.
8|||Safia welcomes Julian by name in a warm, brief reply.
11|...||Use the ordinary English ellipsis for Julian's silent stare before Safia asks about it.
15|||Safia wonders whether something is on her face. The familiar question suits the pause.
18|No... When you look at me like that, I feel like I could fall right into those eyes. Is that what turning to stone feels like?|fall right into those eyes.;turning to stone|Julian is drawn in by Safia's gaze and makes the playful leap to being turned to stone.
22|||Safia is confused by the comparison and invites him to explain.
26|I had a story on my mind about the Medusa Shield. They say it's in the Tasman Sea. Seeing your eyes reminded me of it.|the Medusa Shield.;the Tasman Sea.;reminded me of it.|Julian explains the rumor and why he made the comparison.
29|||Safia recognizes the monster with snakes for hair and challenges the unflattering implications of the comparison.
32|What are you talking about? You could keep your hair covered and still catch me with those beautiful eyes alone.|keep your hair covered;those beautiful eyes alone.|Julian brushes off her concern and returns to his compliment. He refers to her covered hair without adding a reason.
35|||Safia dismisses his flattery as more teasing. Keep her quick, familiar response.
39|You'd turn me to stone, and I'd stay by your side forever in the moonlight... Ah, how romantic.|turn me to stone,;by your side forever;how romantic.|Julian indulges the fantasy in his own theatrical voice.
43|||Safia promptly says she would not look after him, undercutting his romantic fantasy.
46|You're cold to me, aren't you? But that coolness is part of your charm... Well, I'd better go. See you.|cold to me, aren't you?;part of your charm...;I'd better go.|Julian calls her coolness charming and turns abruptly to his farewell.
50|||Safia returns the farewell before her quieter private reaction.
54|What an odd comparison... Still, it made my heart skip a beat.|an odd comparison...;heart skip a beat.|Safia finds the comparison odd but admits to a small thrill. The idiom conveys the playful feeling of the source musical cue.
""",
    228: """
5|Prepare yourself, heathen! I, Charles Martel, will defeat you!|Prepare yourself, heathen!;Charles Martel,|The child grandly plays the part of Martel. The period insult belongs to the role-play.
9|||The other child cries out, surrenders and stammers through the retreat command.
12|||Hodram asks what the children are doing. His question introduces Gerhard's explanation.
16|They're playing heroes. Children in every country look up to their own heroes.|playing heroes.;their own heroes.|Gerhard recognizes the game and connects it to children admiring heroes from their own country.
20|So the local hero is Charles... What was his name again?|the local hero;his name again?|Hodram recalls only the given name he heard in the game.
23|||Gerhard supplies Martel's full name and places him more than eight hundred years earlier.
26|||Gerhard's account keeps Tours and Poitiers, the northward advance and the Iberian Peninsula.
29|Winning a battle is an achievement. Calling him a hero just for that seems a little much.|Winning a battle;seems a little much.|Hodram questions whether the victory by itself explains heroic status.
33|What matters is what the victory meant.|the victory meant.|Gerhard distinguishes the significance of this victory from simply winning a battle.
37|||Gerhard gives his own counterfactual view of Europe's religious and historical future. Preserve it as his speech.
41|||Hodram connects possible historical change to the children's idea of Martel as a defender.
45|Your deeds are no less worthy than his, Admiral.|no less worthy;his, Admiral.|Gerhard compares Hodram's own accomplishments to Martel's and keeps his respectful address.
49|||Gerhard wonders how Hodram will be remembered. His interest brings the conversation back to the way children learn about heroes.
""",
    229: """
5|||Manuel recognizes and greets the admiral in the square.
8|||Hodram recognizes Manuel in turn. The brief reply suits their familiarity.
12|||Manuel asks whether Hodram is checking trade trends and gently remarks on the demands of his work.
15|Partly. It's also a chance to take a breather.|take a breather.|Hodram describes the stroll as both work and a chance to relax.
18|I see.||Manuel acknowledges the explanation before Gerhard asks why he is there.
22|What brings you to the square, Manuel?|to the square, Manuel?|Gerhard asks what business brought him to the square in the first place.
25|Same as the admiral. I thought I'd take a walk and pick up a bit of news while I was at it.|take a walk;pick up a bit of news;while I was at it.|Manuel sees his visit as serving the same two purposes and introduces what he heard.
28|||Manuel asks whether the admiral knows of Attila and supplies his title and people.
32|||Hodram recognizes the name but leaves room for Manuel to explain.
36|||Manuel gives the story's account of the Huns' origin and says Attila threatened both halves of the Roman Empire.
40|To put that kind of pressure on Rome... He must have been a formidable man.|that kind of pressure;formidable man.|Gerhard is struck by the scale of the threat to Rome and infers Attila's stature.
44|History shows that even the mightiest empire will meet a stronger foe someday. No power lasts forever, I suppose.|the mightiest empire;meet a stronger foe;No power lasts forever,|Manuel draws a historical lesson from Attila's threat and qualifies his conclusion.
47|That's a stern lesson. You're saying we should stay on our guard?|a stern lesson.;stay on our guard?|Hodram applies Manuel's observation to their own situation.
50|||Manuel agrees and says the outcome depends on continued effort.
53|||Hodram agrees, then asks why Manuel brought up Attila in this conversation.
57|I just heard a story about some armor connected to Attila. It's only a rumor, mind you.|armor connected to Attila.;a rumor, mind you.|Manuel explains why the subject arose. The armor's link stays hearsay.
61|||Hodram echoes the word armor and leaves Manuel the next turn.
65|||Manuel reports that someone reportedly carried the armor northwest after Attila's death.
69|A king's armor carried northwest... Anyone who could threaten Rome must have struck fear into people.|armor carried northwest...;could threaten Rome;struck fear into people.|Gerhard considers the direction and the reputation of someone who could threaten Rome.
73|||Manuel guesses that northwest may indicate northern Europe. Preserve the uncertainty rather than naming a destination.
""",
}

review = checked_text(previous.review, {"len(records) == 30": "len(records) == 97"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::saladin-noritsune-and-town-leads", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
