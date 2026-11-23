"""Review Fernando's tavern wager and Julio's two recruitment paths."""

from scripts import review_hodram_B167_B168_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT, paired = previous.base, previous.ROOT, previous.paired
OUTPUT = ROOT / "B169_B170_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    169: "Fernando offers a coin game for a drink and then explains his skill at reading other people. He correctly predicts a nearby couple will split up. Hodram offers him a place aboard, and Fernando lets a coin flip decide whether to trust him.",
    170: "Julio denounces the tavern's bad drink and asks Hodram for something better. He can talk trading and respond to a sincere question or a test, or react to Hodram's planned search. He invites himself aboard in both paths before Hodram has said yes.",
}
DECISIONS = {
    169: """
11|Now that you're here, you've got to play me!|got to play me!|Fernando presses a returning visitor to accept his challenge. He does not explain the coin game again on this path.
16|Well, a new face! Want to play for a drink? It's a simple little game.|Want to play for a drink?;a simple little game.|Fernando greets a new face, wagers one drink and reassures the visitor that the game is simple.
20|||Fernando points out the coins and says to take turns removing one to three. The existing instructions leave the choice to each player.
24|||Fernando explains that taking the last coin loses, then calls the rule simple and invites play. The existing pacing makes the stakes clear before the menu.
SC1_B169_CHOICE_356_0|||Play directly accepts the wager, in the vocabulary Fernando just used. The short caption fits alongside Pass.
SC1_B169_CHOICE_356_1|||Pass declines the game. It preserves the route to conversation without implying a loss or accepting the stake.
47|||When Fernando wins, he asks for his drink. The brief line works as the agreed reward.
51|||Fernando takes a sip, compliments the drink and thanks the player before saying goodbye. The easy farewell suits his informal voice.
60|||Fernando acknowledges the loss with a grudging sound and says it has been a while since he was beaten. The handover completes the wager.
70|I'll pass for now. Tell me, are you always this sure of yourself when you gamble?|I'll pass for now.;when you gamble?|Hodram declines the immediate offer and asks about Fernando's confidence in gambling. Keep the question about his general confidence, which prompts his explanation.
74|||Fernando says sharp observation and luck are what matter. The two skills set up his claim and demonstration.
77|||Fernando boasts that he has both qualities and was born to gamble. Keep it as a playful claim he makes for himself.
81|||Hodram doubts that Fernando can read people. The terse challenge gives Fernando room to demonstrate the skill.
85|||Fernando advises Hodram against judging by appearances. The familiar wording directly answers his skepticism.
89|||Fernando points out the couple and asks Hodram to guess what they are talking about from a distance. The existing turn explicitly bars overhearing.
92|He's trying to win her over, I'd guess.|win her over, I'd guess.|Hodram assumes the man is courting her and says so as a guess. This supplies the error Fernando can correct.
96|||Fernando dismisses the guess as an easy mistake and says they're breaking up. The confident answer sets up the shift to the couple themselves.
100|||Hodram is puzzled. The isolated reaction preserves his distance from Fernando's certainty.
104|||Fernando tells him to keep watching. The spare instruction starts the demonstration.
108|I've been listening to you, and I've had enough. I can't go along with this anymore. Why does everything have to be about you?|I've had enough.;everything have to be about you?|The woman has been listening and now openly disagrees. Her accusation of selfishness motivates her next decision without supplying an invented grievance.
111|Think what you like. If you ask me, you're the selfish one.|Think what you like.;the selfish one.|The man says she can think as she pleases and calls her selfish in return. The matched accusation keeps the escalation between them clear.
114|||She takes his response as a reason to stop seeing each other. The established phrasing conveys a breakup without assigning marriage or a past history.
117|||He agrees that if they both feel the same way, the relationship is over. The finality makes Fernando's observation testable.
120|||Hodram pauses when the prediction comes true. Keep the beat before Fernando asks what Hodram thought.
124|||Fernando says he called it. The short colloquial boast fits his voice and the demonstration he has just completed.
128|You got it right... How'd you know?|How'd you know?|Hodram is surprised and asks Fernando to explain. The question shows genuine curiosity instead of continuing his skepticism.
132|Did you see her clench her fist under the table? She was trying to keep her temper. That's hardly sweet talk.|clench her fist;keep her temper.;hardly sweet talk.|Fernando describes the concealed gesture and interprets it as suppressed anger. This is the first of the two pieces of evidence he gives.
136|||Fernando points out that the man never looked at her and asks if that is what love would look like. Keep the question as his inference, apart from the observed gesture.
140|||Hodram acknowledges what Fernando saw and credits his sharp eye. The concession is his change of mind before the offer.
143|||Fernando explains how a sharp eye lets him read an opponent's moves. The application to gambling follows the example naturally.
146|||Fernando says his luck supplies the other part of winning. Keep the claim in his own confident voice.
149|It'd be a shame to use that talent just for gambling. Want to join my crew?|just for gambling.;Want to join my crew?|Hodram thinks the talent has a better use and offers a place aboard. The direct question matches Fernando's surprise at a sudden offer.
153|||Fernando is startled by the offer. His short remark lets him consider it on his own terms.
157|||Fernando has time to spare and offers to go if the coin lands heads. The condition stays explicit before outcome branches.
163|Forget the drink. Come aboard.|Forget the drink.;Come aboard.|Hodram turns down the drink and repeats the invitation on the alternate route. Both parts of his answer matter here.
167|||Fernando recognizes the repeated offer and decides to ask the coin again. His running joke stays consistent across visits.
192|||On the unlucky result, Fernando says he will not put his life in unlucky hands and takes his leave. The line keeps his reasoning explicit.
208|||On the favorable result, Fernando says the matter is decided and wagers his life on Hodram. The figurative wager completes the way he approached recruitment.
211|Name's Fernando Dias! Guess that's luck for you!|Name's Fernando Dias!;luck for you!|Fernando gives his approved full name and uses the coin's decision as a final joke about luck.
214|||Hodram tells Fernando he is counting on his skill. The quiet answer balances Fernando's emphasis on luck.
228|||Fernando mutters about the recent dry spell. The short frustrated aside makes no new claim about who caused it.
""",
    170: """
5|||Julio suddenly objects before the others know what is wrong. The brief outburst comes before Hodram's puzzled reaction.
9|||Hodram questions the outburst silently. Preserve the beat before Julio repeats it at greater length.
13|No, no, no! Ab-so-lutely not!|Ab-so-lutely not!|Julio repeats his objection and stretches out the final word for comic effect. The phrasing makes his loud tone clear before Hodram realizes he is drunk.
16|(Is he drunk...?)|Is he drunk...?|Hodram privately guesses the speaker is drunk. The uncertainty preserves the immediate reaction without stating a fact aloud.
21|||Julio singles out the people he is addressing. The abrupt call comes before the admonition.
25|||Hodram stays quiet instead of answering the call. The pause gives Julio the floor.
29|||Julio begins the familiar complaint about young people. The line sets up Hodram's private joke before the actual subject turns out to be the drink.
33|(...Here comes the lecture about young people.)|lecture about young people.|Hodram privately recognizes the familiar opening of an older man's lecture. The joke in English leaves Julio room to surprise him.
37|||Julio scolds them for drinking such bad liquor. The vulgar swill and formal objection carry his comic change of subject.
40|(Here we go...)|Here we go...|Hodram privately reacts with dismay at being drawn into the rant. The short aside leaves Julio to notice his expression.
44|||Julio notices Hodram's expression and asks about it. The question takes the disagreement from an aside to direct speech.
48|||Hodram asks why Julio would keep drinking liquor he dislikes. The plain question makes the contradiction clear.
51|When a man needs a drink, he makes do with what he's got.|makes do with what he's got.|Julio answers with the idea that necessity leaves him no choice. It keeps his excuse conversational and gives Gerhard a reason to tell him to be quiet.
54|||Gerhard tells him to drink quietly out of consideration for everyone else. The measured rebuke suits him.
57|I may have to settle for swill and gripe about it, but...|settle for swill;gripe about it, but...|Julio acknowledges his own grumbling while setting up what he would prefer. Preserve the unfinished sentence across the two spoken turns.
61|What I really want is a good drink. Say... could you get me one?|really want is a good drink.;could you get me one?|Julio says he would rather drink something good and turns that wish into a request. The invitation sounds personal without naming a drink the Japanese leaves open.
65|||Julio offers to quiet down if Hodram gives him something decent to drink. The conditional bargain preserves his comic audacity.
68|(Good grief...)|Good grief...|Hodram has a weary private response to Julio's proposed bargain. Keep it short before the demands continue.
72|Come on, don't keep me waiting. I have a feeling you've got something good to drink.|don't keep me waiting.;something good to drink.|Julio urges Hodram to hurry and trusts his intuition that Hodram already has a good drink. It leads into the choices about whether there is any.
SC1_B170_CHOICE_894_0|||Yes answers Julio's assumption and its trailing pause gives Hodram's assent the source hesitation.
SC1_B170_CHOICE_894_1|||No answers the same question with the direct denial in the source, leading to Julio's challenge about what Hodram is planning.
86|Really? Good for you!|Good for you!|Julio is surprised and praises Hodram for having a drink. The second short beat lets Hodram qualify his knowledge of liquor.
90|||Hodram says he only knows the market value of liquor and disclaims deeper expertise. This introduces trade without making him claim to be an expert.
94|Trade, you say? Now there's something I know a bit about.|Trade, you say?;a bit about.|Julio perks up at the subject of trade and says he has some experience. The understatement lets Hodram ask how he traded.
98|Did you do your trading by sea?|your trading by sea?|Hodram courteously asks if Julio traded aboard a ship. The full question takes Julio's experience seriously.
101|Aye. Call me an old hand.|an old hand.|Julio agrees and tells Hodram to call him experienced. The nautical English idiom suits the sailor without adding a military title.
105|||Hodram takes that answer seriously enough to ask permission to pose a question. The hesitation gives the player a reason to choose the approach.
109|Hm? What do you want to know?|What do you want to know?|Julio asks what Hodram wants to hear about. The simple question is the lead-in to the choices.
SC1_B170_CHOICE_1314_0|||Ask what you don't know states that Hodram will ask sincerely about unfamiliar material. Its voice is the menu's direct instruction to the player.
SC1_B170_CHOICE_1314_1|||Test him on what you know distinguishes challenging Julio with a known answer from trying to learn. Retain the explicit distinction between branches.
125|Straightforward of you. Good attitude to have.|Good attitude to have.|Julio approves of a sincere approach. His gruff compliment contrasts with the response when Hodram tests him.
128|||Julio immediately asks where the ship is. His assumption that they are leaving together comes before any agreement.
133|||Julio recognizes a test and refuses to play along. His short teasing reply sets up the promise of instruction.
136|||Julio considers the test contrary and promises an education that begins with identifying a good drink. Keep his comic return to the subject.
139|Well, don't just stand there. Show me to your ship.|don't just stand there.;Show me to your ship.|Julio tells his hosts to stop staring and show him where their ship is. His taking command follows his own offer to teach.
145|||Hodram still has no idea why Julio assumes he is coming. The single sound is a natural reaction.
149|You're taking me along, aren't you? I've got plenty to teach you. It'd take more than a day or two.|You're taking me along, aren't you?;more than a day or two.|Julio presumes he is joining and says he needs more than a day or two to tell them all he knows. The question tag keeps the presumptive tone.
153|||Hodram lets the presumption stand without answering yet. The silence leads to Julio giving his name.
157|||Julio formally gives his approved name after announcing that he is coming. The short introduction lands as if they had agreed already.
160|||Hodram answers the introduction politely after a pause. The qualified greeting fits his surprise.
164|Hold on! The admiral never said you could come aboard...|Hold on!;come aboard...|Gerhard stops Julio to point out that Hodram has never agreed. Keep the title for Hodram and the protest separate from Hodram's answer.
168|||Hodram gives his agreement after the protest. His brief concession completes the recruitment.
172|Back to sea at last! I can hardly wait!|Back to sea at last!;I can hardly wait!|Julio says he has been away from the sea for a long time and is thrilled to return. The lift contrasts with his first complaint.
181|||After Hodram denies having a drink, Julio calls it a lie and says his age is no reason to play dumb with him. The insistence prompts an explanation.
184|Well... we were going to look for some while we're out sailing.|look for some;while we're out sailing.|Hodram says they are about to search for better drink along the way. The mention of sailing is what suddenly interests Julio.
188|You're going to sea? Well, that's splendid! I'll come with you, then.|You're going to sea?;I'll come with you, then.|Julio seizes on the voyage and announces he is coming. His sudden enthusiasm belongs to the same man who was demanding a drink.
192|||Hodram reacts in surprise before Julio explains that he is an active sailor. Keep the surprised beat separate.
196|||Julio laughs and says he is a seafaring man still going strong. His old-fashioned laugh keeps his voice distinct.
200|I may be old, but I can still make myself useful.|make myself useful.|Julio acknowledges his age and says he can be of help. Keep that offer as his assertion before Gerhard objects.
203|Hold on! The admiral never said you could come aboard...|Hold on!;come aboard...|Gerhard repeats the same source interruption in the other branch. It has the same audience and role as in the first recruitment path.
207|||Hodram agrees to let Julio join. His brief consent answers Gerhard and concludes the alternate recruitment.
211|||Julio gives his approved name and offers a friendly closing suited to joining a crew. His prospect of sailing fits the accepted invitation.
""",
}
review = checked_text(previous.review, {"len(records) == 76": "len(records) == 93"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::the-wager-and-the-old-hand", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

