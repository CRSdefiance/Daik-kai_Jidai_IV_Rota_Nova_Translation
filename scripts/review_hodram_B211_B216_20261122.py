"""Review Hodram's treasure rumors, Yukihisa's letter, and the swan sighting."""

from scripts import pair_hodram_B201_B220_20261122 as paired
from scripts import review_hodram_B208_B210_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = paired.base, paired.ROOT
OUTPUT = ROOT / "B211_B216_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    211: "Emilio wants the Minotaur Axe so he can grow stronger. Hodram teases him about food, agrees to look someday and reminds him that neither the search nor the reward is settled.",
    212: "An older man sees something of a formidable pirate in Cristina. Intrigued, she asks about the woman's treasured sword, which is said to have been lost during a battle in the Caribbean. The older man encourages her to look for it despite having only the story.",
    213: "Personality-dependent crew speakers report a letter from Yukihisa. Its formal language relates the effort to destroy Muramasa blades and the rumor of a hidden blade. The recipients react to Yukihisa's prose before Hodram considers the information.",
    214: "Al tells Hodram about a blood-red sword that a local lord is said to have sealed away. Al mocks the lord and proposes looking for the sword, while Hodram considers both the lord's reaction and the loss of an unusual weapon.",
    215: "Cristina sees a pair of swans in the square and speaks to them playfully. They fly away carrying an object. She tells Hodram what she saw and suggests looking near Amsterdam.",
    216: "An enthusiastic reader asks about Romance of the Three Kingdoms. A newcomer gets a reading recommendation. A fellow reader can choose a favorite commander, prompting different remarks. Zhao Yun prompts the rumor of a spear and a possible search.",
}
DECISIONS = {
    211: """
5|||Emilio draws out Admiral when he asks for a weapon. The opening pause suggests that he is asking a favor.
8|||Hodram reacts to the unexpected request with a short question. It gives Emilio room to explain.
12|||Emilio wants to get stronger too and asks for a weapon to do so. Keep the simple, eager explanation.
15|Something besides food? Now that's a surprise. What weapon?|besides food?;a surprise.|Hodram teases Emilio about his usual interests and asks what weapon he wants. The teasing belongs to Hodram's response.
18|||Emilio names the Minotaur Axe with enthusiasm. Keep the established item name.
22|||Hodram guesses that an axe like that would be enormous, then asks where to find it. Both parts fit his curiosity.
25|||Emilio knows only the story that the Minotaur once lived on the island. The uncertainty and the location stay explicit.
29|I see. We'll look for it sometime.|look for it sometime.|Hodram agrees to look at some point. His indefinite promise sets up the correction when Emilio gets excited.
32|||Emilio celebrates the possibility of looking for the axe. The short cheer comes before Hodram qualifies his promise.
36|Easy there. I said sometime.|I said sometime.|Hodram reins him in and repeats the indefinite time. The playful correction follows his cheer.
40|I know, but... hooray!||Emilio is still delighted despite the reminder. The syntax makes the repeated cheer sound like his own reaction.
44|And I never said I'd give it to you.|give it to you.|Hodram reminds him that looking for the axe does not guarantee he will let Emilio have it. The dry turn gets a disappointed response.
47|||Emilio deflates when he hears the second qualification. The short disappointed sound fits the comic ending.
""",
    212: """
5|You there, got a moment?|got a moment?|The older man calls Cristina over and asks to speak. His familiar greeting suits the open way he addresses her.
9|||Cristina checks whether she is the one being addressed. Her short question invites confirmation.
13|||The older man confirms that he means her. The repetition directly answers her question.
17|||Cristina asks what he wants. The direct reply fits her mild curiosity.
21|Looking at you reminds me of a pirate from years ago. She really was something. A formidable woman.|a pirate from years ago.;A formidable woman.|The older man remembers a woman pirate with striking strength. All three beats let his admiration come through in speech.
25|Really? Do I look like her?|Do I look like her?|Cristina wonders whether the resemblance is in her appearance. Her quick question lets him explain the resemblance.
28|||The older man explains the resemblance in manner and wonders whether it is her apparent strength. Keep his uncertain reading as his opinion.
32|You think so? Then I'd better get stronger and live up to her example.|You think so?;live up to her example.|Cristina is encouraged by the comparison and decides to grow stronger. Her resolve follows directly from the older man's compliment.
36|Want to get stronger, do you? Then how about looking for the treasured sword she carried?|get stronger, do you?;treasured sword;she carried?|The older man takes her goal seriously and suggests finding the pirate's treasured sword. The term gives Cristina something specific to ask about.
40|||Cristina echoes what the older man said about the pirate's sword. Her question gives him room to explain the story.
44|||He has heard she used it and is uncertain about its worth. The wording retains both qualifications.
48|Hmm. Now I'm curious. Where is it?|Now I'm curious.;Where is it?|Cristina shows genuine interest and asks where the sword can be found. The short question moves the story to the Caribbean.
51|||The older man gives the Caribbean Sea as the broad location. He has no exact coordinates.
55|||Cristina repeats the location as she weighs it. The pause leaves him the next turn.
59|She fought in a big sea battle there. The story goes she lost it in the fighting.|a big sea battle there.;The story goes;lost it in the fighting.|The older man relates the reported loss during a major battle in the Caribbean. The story remains hearsay.
62|||Cristina expects the older man to give her another clue. Her short prompt gives the next reply its effect.
66|That's all I know.|That's all I know.|The older man says he has reached the end of the story. The matter-of-fact response sets up her frustration.
70|||Cristina questions how she could find the sword with so little information. Her disbelief naturally follows the meager clue.
73|I'm afraid I couldn't tell you. I just have a feeling you'll find it.|couldn't tell you.;have a feeling;you'll find it.|The older man has no practical answer but thinks Cristina could succeed. Preserve the shift from ignorance to confidence.
76|||Cristina agrees to remember the clue. The reply leaves her free to decide what to do with it.
79|I do think you'll find it. Good luck.|you'll find it.;Good luck.|The older man reaffirms his belief and wishes her success. The encouragement belongs to him.
82|||Cristina thanks him before reflecting privately on the sword.
86|||Cristina wonders to herself about the legendary sword lost in the Caribbean. Its framing as a private thought and her wish to see it fit the closing beat.
90|||The notice identifies Cristina and an exact one-point Charm gain. Keep the approved name and compact stat format.
""",
    213: """
SC1_B213_STYLE_8_0|||This delivery announces a letter from Yukihisa plainly and addresses the captain as Admiral.
SC1_B213_STYLE_8_42|Admiral, correspondence has arrived from Yukihisa.|correspondence has arrived;from Yukihisa.|This formal voice uses a more ceremonial noun for the message and reports its arrival.
SC1_B213_STYLE_8_84|Admiral, there's a letter from Yukihisa.|there's a letter;from Yukihisa.|This alternative uses ordinary speech to announce the arrival. The address and sender stay exact.
SC1_B213_STYLE_8_122|||This courteous alternative puts the letter first and ends on the source address. The gentle delivery fits its voice.
SC1_B213_STYLE_8_168|Letter from Yukihisa for you, Admiral.|Letter from Yukihisa;for you, Admiral.|The rougher voice gives the same update in a brisk fragment. Its word order keeps it distinct.
SC1_B213_STYLE_8_206|Admiral, a letter's come from Yukihisa.|a letter's come;from Yukihisa.|This familiar delivery announces the arrival with a direct idiomatic construction.
SC1_B213_STYLE_8_244|||The eager call and second exclamation suit this voice. The speaker remains whoever the native personality slot selects.
27|Word has reached me of the Muramasa, the legendary cursed blade. It is a masterwork said to bode ill for Tokugawa, ruler of Japan. Efforts are being made to destroy every blade of its kind.|the legendary cursed blade.;bode ill for Tokugawa,;ruler of Japan.;destroy every blade|Yukihisa writes formally about the rumored cursed blade, its reputation for bringing Tokugawa misfortune and the attempt to destroy the blades. His formality sustains the reactions that follow the letter.
30|It appears that a clan with a grievance against Tokugawa has hidden one such blade somewhere in East Asia. For now, I write to inform you of this.|a grievance against Tokugawa;somewhere in East Asia.;inform you of this.|The second paragraph gives a possible hiding place and clan motive without claiming exact knowledge. Its formal close states why Yukihisa sent the letter.
33|||The final paragraph expresses certainty about the blade's identity and the length of his search. Preserve the established signature and its separate presentation.
SC1_B213_STYLE_702_0|That's hard to read. Sounds like Yukihisa, all right.|hard to read.;Sounds like Yukihisa,|The speaker remarks on the difficulty and cheerfully recognizes Yukihisa's style.
SC1_B213_STYLE_702_38|Rather difficult to read. Very like Yukihisa.|difficult to read.;Very like Yukihisa.|The formal voice gives a measured comment on the writing and recognizes the writer's usual manner.
SC1_B213_STYLE_702_70|That's quite a read. Those are Yukihisa's words, all right.|quite a read.;Yukihisa's words,|This speaker lightly remarks on the difficulty. Recognizing the writing is a reaction to style.
SC1_B213_STYLE_702_106|It's rather hard to follow. Just like Yukihisa.|hard to follow.;Just like Yukihisa.|The speaker observes how hard the prose is to follow and recognizes his manner. Keep her restrained delivery.
SC1_B213_STYLE_702_144|He sure makes it hard to read. That's Yukihisa for you.|hard to read.;Yukihisa for you.|The rougher voice complains that the prose is unnecessarily hard and attributes it directly to Yukihisa.
SC1_B213_STYLE_702_188|A hard bit of reading, that. Just like Yukihisa.|hard bit of reading,;Just like Yukihisa.|The older delivery uses familiar phrasing to comment on the difficult letter.
SC1_B213_STYLE_702_226|||This speaker simply cannot understand the hard writing. Preserve the absence of a comment on Yukihisa in this alternative.
SC1_B213_STYLE_702_270|Difficult reading indeed. Very much like Yukihisa.|Difficult reading indeed.;Very much like Yukihisa.|The measured tone preserves both the difficulty and the speaker's emphatic recognition.
65|He sure makes it hard to read. That's Yukihisa for you.|hard to read.;Yukihisa for you.|Jam finds the writing overly difficult and recognizes it as Yukihisa's usual manner. The words match the kind of remark he makes in the corresponding rough voice.
71|||Hodram takes the content seriously despite the other reader's reaction to the style. The pause and interest stay distinct.
""",
    214: """
5|Admiral, listen to this! I've got a good lead.|listen to this!;a good lead.|Al urgently calls for Hodram's attention because he picked up an interesting lead. The conversational opening fits his excitement.
8|||Al reports that a lord in the area apparently came into possession of a remarkably sharp sword. Keep it as information he picked up.
11|Oh? Go on.||Hodram invites him to continue. The initial reaction preserves his interest.
15|They say the blade has a faint red tinge, like it's drunk the blood of a lot of people.|a faint red tinge,;drunk the blood;of a lot of people.|Al relays the color and the impression it gives. The personification belongs to the rumor.
19|||Hodram finds the description unusual. His understated delivery contrasts with Al's lurid lead.
23|The lord thought it was creepy. He had it sealed away without ever using it, or so I heard. What a coward.|sealed away;without ever using it,;or so I heard.;What a coward.|Al says the lord found the blade sinister and sealed it unused. Al's own accusation remains his interpretation.
26|||Hodram thinks putting away a sword like that is a waste. The brief judgment sets up Al's harsher comment.
29|||Al calls the lord a fool and questions his idea of what a sword is for. His contempt stays in character.
33|Well, I can see why he'd feel that way. So what happened to the sword?|feel that way.;what happened to the sword?|Hodram can sympathize with the lord despite his own interest. His question returns them to the practical lead.
36|I couldn't find out where he hid it. Let's look for it if we get the chance.|where he hid it.;if we get the chance.|Al admits he lacks the location and proposes a future search. The qualification leaves the opportunity open.
""",
    215: """
5|What a pretty square... Oh? There's something in that little pond. Is that...?|What a pretty square...;in that little pond.;Is that...?|Cristina admires the square before noticing movement in the pond. Her unfinished thought leads into the first sound.
9|||The swan's first call interrupts Cristina. The single sound cue fits the recognition that follows.
13|A pair of swans! I didn't know they came here. Are you two traveling, too?|A pair of swans!;they came here.;you two traveling, too?|Cristina is surprised the pair comes this far and playfully asks if they are traveling. The birds get her attention as a pair.
17|||The calls alternate with the quieter calls. Keeping their sequence preserves the impression of the two swans responding.
21|Hee hee. Look how well you two get along. I'm jealous.|you two get along.;I'm jealous.|Cristina remarks on how close the swans seem and envies that closeness. Her warm laugh leaves their relationship at what she observes.
24|Flap, flap, flap!|Flap, flap, flap!|The quick repeated wingbeats cue the departure. Three beats reflect the source sound.
28|||Cristina wonders where the swans are going, then notices they are carrying something. The realization lands after the question.
32|||Cristina follows their direction as they fly off. Her unfinished observation is interrupted by Hodram.
36|||Hodram finds Cristina and calls her by the approved name. The simple greeting draws her away from watching the swans.
40|Oh, Admiral FI! I just saw a pair of swans!|a pair of swans!|Cristina quickly tells the admiral that two swans were there together. Preserve the native given-name substitution.
43|||Hodram echoes the animal's name and comments that swans are unusual this far into town. His remark responds to what she saw.
46|||Cristina describes what they carried, guesses they flew near Amsterdam and suggests looking. Her uncertainty stays attached to the destination.
""",
    216: """
5|||The reader greets the group and asks if they know Romance of the Three Kingdoms. Keep the established literary title.
SC1_B216_CHOICE_64_0|||Yes answers the knowledge question and opens the favorite-commander exchange.
SC1_B216_CHOICE_64_1|||No answers the same question and leads to a recommendation to read it.
22|||He encourages a newcomer to give the book a try because it is a good story. The friendly recommendation suits his enthusiasm.
32|You do? I'm so glad! Now who's your favorite commander?|I'm so glad!;your favorite commander?|The reader reacts happily to meeting someone familiar with the story and moves to his favorite subject. Avoid a literal third-person reference to himself.
SC1_B216_CHOICE_230_0|||Zhao Yun keeps the established name for the reader's own favorite and opens the spear rumor.
SC1_B216_CHOICE_230_1|||Guan Yu is the established name for the second military figure. Its distinct answer stays attached to the praise of his wisdom and bravery.
SC1_B216_CHOICE_230_2|||Zhuge Liang is the established name for the strategist. The answer has its own reaction about his memorial.
51|||The reader is delighted to share a favorite and thinks he and the player will get along. The answer fits his sudden familiarity.
54|||The reader recalls the scene at Changban Bridge in which Zhao Yun rides alone through Cao Cao's army with A Dou in his arms. His enthusiasm is part of recounting the story.
58|||The reader shares the rumor that a legendary spear said to be Zhao Yun's lies on a peninsula nearby. The qualifiers belong to a rumor with no precise location.
62|I wanted it myself. I looked everywhere and never found it. I thought you might have better luck.|I looked everywhere;never found it.;have better luck.|The reader searched in earnest without success and thinks this group might find the spear. Keep his personal stake and the failure explicit.
72|You like Guan Yu, the Lord of the Beautiful Beard? He isn't my favorite, but he's as wise as he is brave.|Lord of the Beautiful Beard?;he's as wise as he is brave.|The reader names Guan Yu's epithet and admires both wisdom and courage despite preferring another commander. Keep his appreciative tone.
78|Zhuge Liang, the brilliant strategist... Oh, that memorial he wrote before the campaign always brings tears to my eyes. He's probably my second favorite.|the brilliant strategist...;before the campaign;brings tears to my eyes.;my second favorite.|The reader praises the strategist, recalls his moving written memorial before the campaign and gives an approximate personal ranking. Preserve the cultural reference in ordinary speech.
""",
}

review = checked_text(previous.review, {"len(records) == 68": "len(records) == 93"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::treasure-rumors-and-letter", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
