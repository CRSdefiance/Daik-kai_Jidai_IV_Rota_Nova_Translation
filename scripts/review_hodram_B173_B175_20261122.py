"""Review the Proofs of Conquest, Yifa's demonstration and Sanghyeon's visit."""

from scripts import review_hodram_B171_B172_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT, paired = previous.base, previous.ROOT, previous.paired
OUTPUT = ROOT / "B173_B175_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    173: "Gerhard reluctantly turns to Mikhail for information about the Proofs of Conquest. Mikhail explains the treasures, the maps and how to look for clues. The crew needs the advice despite his tendency to turn the subject back to women.",
    174: "Yifa has slipped away from her master to train while traveling. She talks Hodram's crew into watching a demonstration and lunges while Gerhard is distracted. Hodram takes her skill seriously and asks if she will accept naval discipline.",
    175: "Sanghyeon visits Hodram in an apparent dream and explains why Yifa was expelled. They were raised like siblings and he still worries about her. Yifa senses that he visited and vows to keep training. Hodram reminds her that she has duties aboard.",
}
DECISIONS = {
    173: """
5|Something wrong, Gerhard?|Something wrong, Gerhard?|Hodram checks why Gerhard is troubled. Use a familiar, open question before he names the subject.
9|Ah, Admiral. I'd like to learn more about the Proofs of Conquest, but the man who knows about them is... Well...|the Proofs of Conquest,;the man who knows|Gerhard states the topic with its full title and hesitates over identifying the person who can answer. Mikhail interrupts before he says the name.
12|What is it?|What is it?|Hodram asks what is holding Gerhard back. The question gives Mikhail room to answer in his place.
16|||Mikhail takes obvious delight in revealing that he is the expert. The emphatic first-person answer suits him.
19|||Hodram understands Gerhard's hesitation as soon as Mikhail speaks. The separate beat lands before Gerhard resumes.
23|Yes. Of all the people it could have been...|all the people|Gerhard is dismayed that this particular man has the information he needs. The unfinished thought lets Mikhail challenge him.
26|Oh? Have something to say, Gerhard?|something to say, Gerhard?|Mikhail pointedly asks whether Gerhard wants to say something to him. The friendly address carries the challenge.
29|||Gerhard backs away, stammers and offers sincere respect for Mikhail's knowledge. The trailing qualification preserves his reservations about the man.
33|||Hodram puts the bickering aside and gives Mikhail the floor. The firm, simple instruction suits him.
36|||Mikhail laughs and asks if the admiral is interested in the Proofs. Keep the controlled familiar name and the light tone.
40|Spare me the lecture. I just want to know what they're for.|what they're for.|Hodram wants the purpose of the Proofs without unnecessary learning. The dry request makes Mikhail's throat-clearing comic.
44|||Mikhail starts his account with a ceremonial throat-clearing and explains the link between ruling a sea and obtaining its treasure. The claim stays attributed to legend.
48|||The old texts name seven treasures and the Seven Sages who marked their locations on different maps. The existing turn preserves all three facts.
51|Someday, whoever comes to rule one of those seas is destined to find its map. Or so the story goes.|to rule one of those seas;Or so the story goes.|Mikhail explains the predicted reward for mastering the sea. The destination is finding the map, and his closing qualification stays part of the account.
55|Just treasure? That's a little disappointing...|a little disappointing...|Hodram loses some interest when he hears the Proofs are treasures. The understatement leaves room for Gerhard to explain what they would mean to the fleet.
58|With respect, Admiral FI, those Proofs would let you call yourself master of the seas and mean it. Think what that would mean for us!|Admiral FI,;master of the seas;mean for us!|Gerhard argues that the Proofs would publicly establish mastery in fact as well as in title. Keep his excitement and the admiral's original name substitution.
61|||Hodram turns the political argument over in his mind. The brief echo makes his interest different from his first reaction to treasure.
65|Think of the people who follow you, Admiral FI. You'll see what I mean.|who follow you,;Admiral FI.|Gerhard asks Hodram to think of those who follow him. Retain the admiral's title and his controlled given name.
69|You're saying a clear goal would give them something to work toward?|a clear goal;something to work toward?|Hodram realizes that giving the crew a tangible goal could motivate them. The question lets Gerhard confirm that interpretation.
72|||Gerhard gives an unqualified assent. Keep it as its own turn before Mikhail interrupts.
76|What are you two whispering about? Impressed by how much I know?|you two whispering;how much I know?|Mikhail notices the private discussion and boasts that his knowledge has impressed them. The self-satisfaction suits his interruption.
80|W-we know how much you know. Just try not to cause a commotion aboard...|cause a commotion aboard...|Gerhard recognizes Mikhail's learning and asks him to behave aboard. The stammer shows that he is trying to be diplomatic.
83|||Mikhail waves away the concern and laughs. The existing reply fits his light attitude toward the warning.
87|||Hodram returns to business and asks how to find every Proof. Keep the individual Proofs distinct from their collective title.
91|||Mikhail explains that the crew must become the strongest power in a region and that influential people often know a clue. Preserve both the goal and the qualification.
95|||He says it may be necessary to overcome a wicked person who holds a clue. Keep that condition and its tentative force.
99|||Hodram waits through that part of the account. The independent silence precedes the next instruction.
103|||Mikhail directs them to the ruins hidden in cities and the mystery of the sealed Proof. Both stages matter to the explanation.
106|||Gerhard asks how they are supposed to locate those ruins. His plain question sets up Mikhail's less direct advice.
110|||Mikhail considers how he would do it. Preserve the delay before his one-word answer.
113|||Gerhard waits for that answer with a questioning reaction. The pause matters to the punch line.
117|||Mikhail answers women in a single word. The bluntness provokes Gerhard before he explains his reasoning.
121|||Gerhard draws out Mikhail's name in exasperation. Preserve the elongated call as a vocal effect rather than a different name.
125|||Mikhail tells Gerhard to calm down and points to large cities as sources of leads on nearby ruins. The practical advice follows the joke.
129|The women who work in taverns hear stories from sailors all over the world, every day. What they know is worth a fortune.|work in taverns;all over the world,;worth a fortune.|Mikhail explains why women who work in taverns hear valuable information. Keep the job context and avoid implying that every tavern worker has the same clues.
132|||He assumes information of that value will cost something. The phrasing leaves open what the woman would expect.
135|Hmm... So we'd have to offer something in return.|offer something in return.|Hodram interprets Mikhail's advice as an exchange. The wording lets him repeat the same idea in his later challenge.
138|||Mikhail distinguishes giving a gift from expecting a reward, then admits he wants to win someone's heart. Keep the contradiction because it sets up Hodram's joke.
141|...Isn't winning her heart something in return?|something in return?|Hodram calls out the contradiction in Mikhail's advice. Echo the same wording he just used about a transaction.
145|||Mikhail realizes he is getting carried away again. The abrupt retreat closes the joke.
""",
    174: """
7|||Yifa calls to Hodram with a teasing compliment. Handsome fits the familiar address without creating a relationship.
10|||Hodram does not answer the first call. Keep the silence before Yifa gets his attention.
14|Hey! I'm talking to you, handsome!|talking to you, handsome!|Yifa repeats the familiar address and makes it clear who she means. The added insistence reflects the Japanese repetition.
18|||Hodram checks whether he is the one being addressed. The short pause before the question fits his delayed reaction.
22|||Gerhard asks why Yifa is there. His formality is distinct from her teasing and identifies no relationship.
25|Shh! Keep your voice down. I'm in a little trouble.|Keep your voice down.;in a little trouble.|Yifa is hiding and asks for quiet before saying she has a problem. Trouble invites the question she gets from Hodram.
28|||Yifa guesses they are sailors and asks for passage. The short question tag and request express both thoughts directly.
32|What an odd young woman. That came out of nowhere.|came out of nowhere.|Gerhard reacts to the stranger and her sudden request. Preserve his surprise before Hodram asks for an explanation.
36|What kind of trouble? Why do you want to come aboard?|What kind of trouble?;come aboard?|Hodram follows up on her own description and asks for a practical reason. Both questions let her explain the need to leave.
39|||Yifa admits that she slipped away from her master and would be taken back if found. The worry stays about being discovered.
43|Slipping away like that sounds serious. What are you training in?|sounds serious.;training in?|Hodram recognizes the seriousness of her leaving and asks what she studies. The question follows her reference to a master.
46|||Yifa names her practice as Taoist arts. The cheerful pace conveys her confidence before she talks about skipping.
50|I don't mind studying the Taoist arts. It just gets old sometimes, you know?|the Taoist arts.;sometimes, you know?|Yifa likes the practice itself but gets bored at times. Keeping the name here makes the distinction between the arts and the routine clear.
54|||The master caught her skipping and scolded her. The stick-in-the-mud complaint belongs to Yifa's side of the story.
57|So here's my plan! I'll sail around the world and keep training. I'll show my master what I can do! Pretty great, huh?|sail around the world;Pretty great, huh?|Yifa decides to train while traveling and show her master how far she can get. Her self-praise suits the confidence that Gerhard immediately questions.
60|||Gerhard grumbles about young women today. The trailing complaint leaves Hodram to assess the plan seriously.
64|I admire your nerve. But how much do you actually know about these Taoist arts?|I admire your nerve.;these Taoist arts?|Hodram acknowledges her determination and asks about her skills. His practical interest invites the demonstration.
68|Heh. I could show you a little. Hey, old man. Get your sword ready!|Hey, old man.;Get your sword ready!|Yifa casually challenges Gerhard and calls him old. The age tease explains his startled response without asserting a relationship.
72|O-old man? You mean me?|O-old man?;You mean me?|Gerhard repeats Yifa's address in disbelief. Preserve the stammer and his surprise at being singled out.
75|That's right! Here I come. Get ready!|Here I come.;Get ready!|Yifa confirms that she means Gerhard and warns him she is about to begin. Her enthusiasm leads to the shout.
78|||Gerhard gives a brief sound as he prepares for the demonstration. The moment works in isolation.
82|||Yifa shouts with exertion. The drawn-out syllable preserves the demonstration without giving it a new name.
86|||Hodram silently wonders what is happening. The separate question prepares for Gerhard's private reaction.
90|||Gerhard thinks nothing happened. Keeping the observation private gives Yifa the surprise she needs.
93|||Yifa sees an opening and calls it out as she lunges. The short exclamation belongs to the timing of the trick.
98|||Gerhard is startled into a quick reaction. The existing exclamation fits the dodge Yifa immediately compliments.
102|Nice dodge! Well? That's my binding spell!|Nice dodge!;my binding spell!|Yifa praises the dodge and announces what she was using. Her satisfaction does not establish whether the magic actually worked.
106|||Gerhard repeats binding spell and remains unsure what he saw. His doubt gives Yifa the chance to tease him about its mystery.
109|||Yifa claims the Taoist arts are mysterious. The playful tag keeps her apparent satisfaction with the effect.
113|That isn't what I meant...|what I meant...|Gerhard tries to correct the way she understood his hesitation. The trailing reply leaves Hodram the next substantive assessment.
117|Closing in on Gerhard that fast is no small feat. You've got a good sense of an opponent's reach.|no small feat.;an opponent's reach.|Hodram is impressed that Yifa got within range so quickly against Gerhard. He praises her sense of distance, which she demonstrated during the lunge.
120|||Gerhard agrees there is evidence that she has trained. The short acknowledgment stays distinct from Hodram's description of her talent.
123|||Hodram recalls his own master telling him to go to sea and credits that advice for where he is now. Keep his personal comparison independent of any judgment about Yifa's master.
127|I don't approve of running off without a word, but I can see you've thought about what you're getting into. What's your name?|without a word,;What's your name?|Hodram still disapproves of the way she left but sees some resolve. His request for her name shows that he is taking the offer seriously.
131|||Yifa gives the approved name with her usual confidence. The terse introduction suits the energy of the exchange.
135|Yifa, this ship belongs to the navy. Do you still want to come aboard?|belongs to the navy.;come aboard?|Hodram points out the ship's naval role and gives Yifa a choice. Keep the warning about the setting he has actually named.
138|You're saying you're strict, too? Good. I like a challenge!|you're strict, too?;I like a challenge!|Yifa understands that navy life will also be strict and welcomes that prospect. Her cheerful acceptance answers his warning.
""",
    175: """
10|||The visitor starts with an indistinct polite address. The short fragment gives the dream encounter its slow opening.
14|||Hodram does not answer the indistinct call. Preserve his separate reaction before the visitor uses his name.
18|||The visitor calls the captain by his original controlled given name. The pause keeps his cautious approach.
22|||Hodram finally stirs with a quiet question. The short sound suits the uncertain state of the encounter.
26|||Sanghyeon apologizes for the unexpected visit and says he means no harm. His courtesy prepares the formal introduction.
29|It's an honor to meet you. My name is Sanghyeon. Yifa and I have the same master. I started training before she did.|My name is Sanghyeon.;the same master.|Sanghyeon introduces himself as the student senior to Yifa under their shared master. Seniority describes their training, and their personal closeness comes later.
33|I heard you've taken Yifa aboard. I came to introduce myself and pay my respects.|taken Yifa aboard.;pay my respects.|Sanghyeon explains why he approached Hodram and acknowledges the captain's responsibility for Yifa. Keep his visit brief and deferential.
37|Yifa's...?|Yifa's...?|Hodram starts to repeat the connection before Sanghyeon explains himself. The fragment clearly refers to Yifa.
41|||Sanghyeon is ashamed and blames himself for failing to guide Yifa. His description reflects his own sense of obligation.
44|||He says Yifa left the mountain without permission to escape her training and went abroad. Keep his explicit disapproval of both.
48|||He says Yifa may be unaware that people from their country are forbidden to go abroad. Preserve the prohibition and his uncertainty about her knowledge.
52|||Hodram suspects that he has come to take Yifa back. The question lets Sanghyeon explain why he cannot do that.
56|I couldn't take her back even if I wanted to. She broke a law of our country. It's a grave offense, and our school expelled her.|even if I wanted to.;our school expelled her.|Sanghyeon is unable to bring her back and attributes the expulsion to the gravity of breaking the ban. Preserve both the state restriction and the school's action.
59|That leaves me with no formal ties to her...|no formal ties to her...|Sanghyeon says the expulsion has formally severed his connection to Yifa. The following turn immediately distinguishes that from the affection he still feels.
62|||They grew up together as close as siblings. Keep the source comparison, which explains his concern without making them blood relatives.
65|||Sanghyeon worries that Yifa's inexperience could embarrass her in front of others. The concern belongs to his protective view.
69|I know I'm asking a great deal, but please guide her. I don't want her to lose her way.|asking a great deal,;lose her way.|Sanghyeon apologetically asks for guidance so Yifa continues on the right path. His concern here is how she lives as a person.
72|||He asks Hodram to remind her to train away from the mountain and heed the master's instructions. Keep both requests and his hesitation.
75|||Sanghyeon asks Hodram to take care of Yifa. The plain request closes his more formal speech.
78|||Hodram asks himself if it was a dream. The uncertainty is part of the transition to morning.
82|||Hodram comments on how vivid it felt. The existing fragment keeps his lingering uncertainty.
86|||Yifa bursts in with an eager morning greeting and starts to urge their departure. The drawn-out greeting stops on a new realization.
89|||Yifa breaks off in a silent exclamation. Keep the reaction separate from Hodram's question.
93|||Hodram asks what has happened. The short question gives Yifa room to explain what she sensed.
97|That presence... It's the senior student I trained with!|That presence...;I trained with!|Yifa identifies the presence of the person who trained ahead of her. She senses the connection before Hodram supplies his name.
101|Could it be...? Is the man you trained with named Sanghyeon?|named Sanghyeon?|Hodram recognizes a possible connection to his dream and asks Yifa to confirm the name. The question stays qualified.
105|||Yifa is startled and asks how he knows Sanghyeon's name. Her response makes the unexpected evidence clear.
109|So it really was him... A man in my dream gave me that name. He asked me to look after you.|A man in my dream;look after you.|Hodram takes her reaction as confirmation and explains both the introduction and Sanghyeon's request. The admitted dream preserves the uncertainty about the visit.
113|||Yifa softly says Sanghyeon's name. The familiarity conveys her affection without presenting him as a literal brother.
117|He used his arts to come all this way...|used his arts|Yifa realizes that Sanghyeon used the arts to visit. The route stays in her interpretation and no kind of spell is added.
121|||Hodram repeats arts in puzzlement and privately notes that it has come up again. Keep the aside distinct from his spoken question.
124|||Hodram passes along the request to follow her master's instructions away from the mountain. The advice reconnects Yifa with the training she decided to continue.
128|||Yifa fondly laughs that Sanghyeon never stops worrying. His name in familiar address is sufficient after the source establishes their sibling-like closeness.
132|||Hodram notices the change in Yifa and asks what it means. Keep the short question before her new promise.
135|||Yifa vows to train hard because she does not want to let Sanghyeon down. Her enthusiasm now follows responsibility as well as adventure.
139|Heh. Your training can't get in the way of your duties. I won't go easy on you just because you're a woman.|of your duties.;just because you're a woman.|Hodram reminds her that the ship's work still comes first and explicitly says he will hold her to the same standard. The laugh keeps his familiar tone.
142|||Yifa says she knows already. The repetition keeps her jaunty confidence after the warning.
""",
}
review = checked_text(previous.review, {"len(records) == 66": "len(records) == 114"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::proofs-and-yifa", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

