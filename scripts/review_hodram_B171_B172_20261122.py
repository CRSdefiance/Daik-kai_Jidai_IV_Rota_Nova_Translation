"""Review the sailing lesson choices and Mikhail's recruitment and tutorial."""

from scripts import pair_hodram_B171_B180_20261122 as paired
from scripts import review_hodram_B169_B170_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = paired.base, paired.ROOT
OUTPUT = ROOT / "B171_B172_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    171: "A bored sailor offers an optional lesson on sails and wind. The choice takes the lesson or declines it politely. The 27 speech decisions are already bound to their exact earlier review.",
    172: "A local sends Hodram to the scholar Mikhail and hints that he behaves badly around women. He is knowledgeable enough for the crew to consider inviting him, but only shows interest once he sees Sera or Cristina. Their reactions and the officers' objections make his conduct the problem. Julio directly identifies Cristina as his granddaughter. The tutorial then explains Mikhail's separate role and how to open his item details.",
}
DECISIONS = {
    171: """
SC1_B171_CHOICE_154_0|||Listen accepts the sailor's invitation and suits the short menu. The retained speech leads into the distinct sail geometry and wind lesson.
SC1_B171_CHOICE_154_1|||No thanks gives the polite refusal in the Japanese. The crew can comment on the lesson before the sailor waits for a less experienced guest.
""",
    172: """
5|You folks here to see Mikhail, too?|see Mikhail, too?|The local assumes the visitors have come to see the well-known older man. Keep the familiar name without suggesting he is related to either the speaker or the crew.
8|Mikhail?|Mikhail?|Hodram repeats the unfamiliar name in a question. He has not yet been told how the local knows him.
20|W-what? Mikhail?! No, no, you can't go see him! FI, stay away!|you can't go see him!;stay away!|Julio recognizes the name and urgently tells Hodram not to meet him. Keep the stammer, insistent repetition and controlled given-name address.
26|Oh, that's not why you're here? People around here know him for his learning.|why you're here?;for his learning.|The local corrects the assumption and explains Mikhail's reputation. The description is about knowledge, without inventing a profession before the game names it.
30|Huh... Let's go meet him.|Let's go meet him.|Hodram considers the local's description and decides to see Mikhail. His interest is still tentative before the warning.
34|||The local urges them to think twice if a woman is with them. The trailing warning withholds the reason until they see Mikhail for themselves.
45|||Julio promptly supports the warning. His unusually forceful agreement echoes his first reaction.
51|||Hodram reacts with a question when the warning and Julio's agreement leave him puzzled. Keep the beat before he sees Mikhail.
55|||Hodram identifies the man before the strangers start talking to him. The name alone is enough after the conversation about his reputation.
59|||The woman gushes about Mikhail. Her praise is familiar and enthusiastic without treating the casual older-man address as a family relationship.
63|Oh, I know! Ho ho ho!|Oh, I know!|Mikhail agrees eagerly with her praise instead of modestly brushing it aside. His recurring laugh is part of his voice.
66|||Another onlooker asks what the object is. The short excited question lets his explanation take the next turn.
70|||Mikhail identifies a peppercorn, gives its tropical origin and explains that grinding it makes a spice. Keep those details in his voiced explanation before he realizes he was mistaken.
74|It ought to grow well around Brunei. I bet it'd make a valuable trade good.|around Brunei.;a valuable trade good.|He predicts it will grow near Brunei and have trading value. The statement remains an opinion and sets up the abrupt reversal.
78|Wait a second... These are rabbit droppings! Ugh!|rabbit droppings!|Mikhail looks again and realizes what he is holding. The pause makes the new information a comic correction rather than a competing item description.
82|||The onlooker recoils and asks him to throw it away. The brief protest follows the discovery naturally.
86|All right, all right. Away it goes!|Away it goes!|Mikhail agrees and tosses it away. The repeated assent keeps his easy delivery after the onlooker's disgust.
90|||The woman marvels at how much he knows and asks how he learned it. The existing response leaves the personal address playful and the next remark his own.
94|Well, I am a genius. Hardly anyone knows more than I do. I could even guess your bust size, my dear!|knows more than I do.;your bust size, my dear!|Mikhail boasts about his knowledge and makes an unsolicited remark about the woman's body. Keep the impropriety with him and the overfamiliar address free of a claimed relationship.
98|||The woman calls him a dirty old man after his intrusive remark. The startled exclamation makes her own immediate reaction clear.
102|||Mikhail laughs in reply. The existing recurring laugh conveys that he takes her rebuke as part of the joke.
106|He certainly knows a lot. I'm less sure about his manners...|less sure about his manners...|Hodram acknowledges the knowledge but doubts Mikhail's behavior. The concern sets up Gerhard's practical answer.
110|Still, what he knows would come in handy. I think it's worth asking him to join us.|come in handy.;asking him to join us.|Gerhard expects Mikhail's knowledge to help and recommends inviting him. His own later objections show that this judgment is provisional.
114|||Hodram accepts the recommendation after a pause. Keep the decision before the invitation, separate from Mikhail's reply.
118|||Mikhail stammers as he notices the new visitors. The question makes his surprise audible.
122|You know quite a bit, Mikhail. I'm FI FA, admiral of this fleet.|quite a bit, Mikhail.;FI FA,|Hodram acknowledges Mikhail's knowledge and introduces himself with both original names and the military role he states in the Japanese.
126|||Hodram asks if Mikhail will put his knowledge to work for them. The turn lets Mikhail respond to the offer directly.
129|||Mikhail refuses to leave the town or accept an invitation from men. The two reasons set up how quickly his attitude changes when he notices the woman with them.
133|||Gerhard asks him to reconsider and addresses him politely. The request implies respect for an older person without assigning a rank or kinship.
137|Well, even if you ask me again... Oh!|ask me again...|Mikhail starts to resist again, then notices one of the women. The gap in his reply belongs to the sudden shift in attention.
140|Oh! You there, miss. What's your name?|What's your name?|Mikhail asks the woman accompanying them for her name. Use a familiar form of address without assigning an age or relationship.
149|||Sera says nothing when he asks for her name. The separate silence precedes Hodram's explanation that she cannot understand him.
153|||Hodram explains that Sera cannot understand their language and gives her name. The existing hesitation leaves Mikhail to respond to the name.
158|||On the alternate path, Cristina gives her own name in a stammer. Her reply stays separate from Sera's silence and Hodram's introduction.
171|||Mikhail repeats Sera's name while assessing his options. His own later drawn-out call supplies the intrusion.
177|||Mikhail repeats Cristina's name on her alternate path. The same kind of response stays tied to the woman present.
184|||Mikhail repeats how pleased he is. The remark prompts Hodram's confusion and his own sudden agreement to go.
188|||Hodram cannot follow the change of attitude. The question mark is a separate reaction before Mikhail makes his decision explicit.
192|||Mikhail declares that he has decided to come. The repetition makes his self-invitation emphatic.
201|||Mikhail drags out Sera's name while calling after her. The unusual spelling reflects the voice, and the approved name remains recognizable.
207|||Mikhail draws out Cristina's name on the alternate path. Keep the parallel with his call to Sera and the correct character.
214|||Mikhail announces he will follow her anywhere. His conduct and the next responses make this an unwelcome declaration.
224|||Sera reacts without speech. The sharp punctuation gives Gerhard a reason to intervene on her path.
228|FI! Call this off! Sera isn't safe with him!|Call this off!;Sera isn't safe with him!|Gerhard urges Hodram to withdraw the invitation because he fears for Sera. Preserve the original given-name control and his direct concern.
233|Wh-who is this man? Eek! Stay away from me!|Stay away from me!|Cristina is startled by Mikhail and directly tells him to keep away. Her stammer and exclamation preserve the abrupt reaction.
244|Mikhail! Still alive, you dirty old man? Stay away from my granddaughter!|you dirty old man?;my granddaughter!|Julio recognizes him, insults him for his behavior and demands that he stay away from Cristina. Granddaughter is the relationship Julio explicitly states.
248|Julio! It's been a long time! You're still hanging on, too. I'm not taking old-man jokes from another old man!|It's been a long time!;from another old man!|Mikhail recognizes an old acquaintance, returns the joke about his age and objects to being called old by someone in his own age group.
254|FI, we can't take him with us!|take him with us!|Gerhard asks Hodram to abandon the idea of recruiting Mikhail. The captain's original runtime name stays in his address.
260|No, no! I've made up my mind. I'm coming! I'll put what I know to good use, don't you worry.|I've made up my mind.;put what I know to good use,|Mikhail refuses to reconsider, insists he is coming and promises his knowledge will help. His assurance answers the objections raised around him.
263|...All right, you can come. But...|you can come.|Hodram grants permission after the arguing, then starts to qualify it. The unfinished part leads to a warning.
272|Lay a hand on Sera and I'll cut you down, however old you are!|Lay a hand on Sera;however old you are!|Gerhard warns that he will use his sword if Mikhail touches Sera even though he is elderly. The threat shows the depth of his concern.
275|||Mikhail calls Sera's name again immediately after the warning. The repeated drawn-out address shows that he is ignoring Gerhard.
279|S-sir, I was speaking to you...|I was speaking to you...|Gerhard stammers while trying to make Mikhail listen. The deferential address keeps both his restraint and his exasperation.
283|||Hodram's silence gives space to the alternate reactions. It makes no new claim about his judgment.
288|Touch me and I'll run you through with this sword!|I'll run you through|Cristina threatens to defend herself if Mikhail touches her. Her anger is her own direct answer, separate from Gerhard's defense of Sera.
291|||Mikhail immediately repeats Cristina's drawn-out name. The exact character and repeated timing matter in the alternate path.
295|Ugh, I've had enough!|I've had enough!|Cristina exclaims that she cannot stand it. Her frustration follows Mikhail ignoring her warning.
307|||Julio again calls Mikhail a dirty old man and says to stay away from his granddaughter. The familiar phrasing preserves the repeated protective instruction.
311|||Mikhail claims he can love whomever he pleases, then says it is fortunate Cristina takes after someone other than Julio. Keep the liberties as his words and the insult aimed at Julio.
315|Oh, shut up!|shut up!|Julio angrily cuts Mikhail off after the comment about Cristina. The short retort fits the quarrel before the game explains Mikhail's actual function.
329|||The notice identifies Mikhail as a scholar and explains that he cannot fill a deck position because he is not a navigator. Keep the reason and the restriction together in the speakerless tutorial.
333|||The notice says that with Mikhail aboard, the player can see more detailed information about items. The unlocked function is distinct from the button instruction.
336|Press X while item info is shown.|Press X;item info is shown.|The speakerless notice tells the player to press X when item information is on screen. Use the established way of naming the button and preserve the prerequisite.
339|I can't help sail the ship, but I'm glad to be aboard. If you want to know more about an item, just call me over!|glad to be aboard.;call me over!|Mikhail acknowledges that he cannot do the ship's work and invites the crew to call him for item information. The personal offer follows the neutral tutorial notices.
""",
}
review = checked_text(previous.review, {"len(records) == 93": "len(records) == 66"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::sail-lesson-and-mikhail", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

