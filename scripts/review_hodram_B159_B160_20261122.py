"""Review Ian and Carlo's recruitment against the complete Japanese scenes."""

from scripts import review_hodram_B157_B158_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT, paired = previous.base, previous.ROOT, previous.paired
OUTPUT = ROOT / "B159_B160_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    159: "Ian is harassed while serving drinks, fired after defending himself, and ambushed outside. Hodram and his crew intervene. Hodram recruits Ian after seeing how he handles a sword, and Ian can finally return to sea.",
    160: "Carlo negotiates with Adil, notices he is ill, and sends him home. He gives the visiting party priority the next day. Hodram recruits him for his business experience and offers him a place with a crew after learning why he cannot return to Venice alone.",
}
DECISIONS = {
    159: """
6|||The barkeep asks Ian to carry something over. The easy request establishes Ian's work before customers start calling attention to him.
10|||Ian answers promptly and politely. His reserve will carry through all three errands.
15|||A customer points out Ian and admires his looks. The tentative question keeps the aside conversational.
19|||The other customer questions whether Ian is a man. Keep the blunt remark that the woman immediately tries to hush.
23|||She warns him that Ian might hear. The short rebuke comes too late for Ian.
27|||Ian is tired of being treated as a spectacle. The existing private thought carries his frustration before he goes back to work.
30|||The barkeep asks him to carry drinks too. The work keeps interrupting what Ian has to put up with.
34|||Ian answers again after a pause. The hesitation now signals that the attention has got to him.
38|Oh! Ian brought it over himself!|brought it over himself!|The customer is delighted to be served by Ian specifically. Restore her use of his name as part of the excitement.
41|What are you so happy about? Ugh. This is getting old.|you so happy about?;This is getting old.|The other customer is irritated by her excitement. The audible annoyance comes before the barkeep's next errand.
44|Ian! Take this to that table over there.|that table over there.|The barkeep calls Ian by name and directs him to another table. Over there preserves the gesture without assigning distance.
47|||Ian gives the same brief polite reply. The repetition contrasts with the next customer's behavior.
51|Hey, sweetheart. Pour me a drink. Heh.|Hey, sweetheart.;Pour me a drink.|The man calls Ian a feminizing pet name, demands a drink for himself, and leers. Keep the same address for when he corners Ian later.
54|||Ian gives the man no answer. The extended pause has a purpose between escalating remarks.
58|You're a pretty one, aren't you? Huh?|You're a pretty one, aren't you?|The heckler presses for a response after Ian says nothing. The repeated probing keeps the uncomfortable beat.
61|||Ian stays silent again. The renewed pause leads into the man's more explicit provocation and unwanted touch.
65|||The man questions Ian's sex again and uses his pale skin as an excuse to keep staring. The existing sneer comes through without additional abuse.
69|||Ian tells the man to stop touching him. Keep the unqualified command that triggers his reaction.
73|||The man cries out in pain. The quick repeated reaction suits the reversal.
77|||The man swears at Ian. The next thought belongs to Ian and gives the outburst room.
81|||Ian realizes he has put his job at risk. The brief private exclamation leaves the implication to what follows.
85|||The man sarcastically invokes how a customer should be treated. His self-importance explains why he later claims to have been humiliated.
89|...I beg your pardon, sir.|I beg your pardon, sir.|Ian answers with strained courtesy after defending himself. The deliberate pause makes the formality sound reluctant.
93|||Hodram intervenes for the moment by ordering a drink. Keep the short call to the barkeep before they speak separately.
97|||The barkeep answers Hodram, then asks Ian to talk. Keep the pause that separates the two audiences.
100|||The barkeep tells Ian that this work may be a bad fit for him. His tentative delivery leads into the firing.
104|||Ian addresses his employer respectfully before knowing the outcome. Sir reads naturally in that relationship.
108|I've had enough trouble. You can deal with a customer without drawing a sword.|deal with a customer;without drawing a sword.|The barkeep wants an end to the trouble and says a sword was avoidable. The direct second sentence reads as his judgment.
112|||The barkeep apologizes and lets Ian go. His wording stays quietly final.
116|||Ian acknowledges the decision after a pause. The answer stays controlled despite his private worry outside.
120|The way he moved... He's trained with a sword, and he's good. I should talk to him.|trained with a sword,;talk to him.|Hodram recognizes both training and ability from what he saw, then considers approaching Ian. Keep his practical interest before the ambush.
124|(Fired. No money. What am I supposed to do now?)|What am I supposed to do now?)|Ian states his predicament in clipped thoughts before asking himself what to do. Fired connects it directly to the conversation inside.
127|||Ian sees a ship offshore and wants to go back to sea. The private wish foreshadows the relief in his later acceptance.
131|Well, well, sweetheart! Running into you again already?|Running into you again already?|The man uses the same harassing address from the tavern and pretends the encounter is a coincidence.
134|||Ian reacts abruptly as the man appears. The single mark is its own beat.
138|||The man notices Ian is alone and calls his companions over. The existing mockery turns into an explicit threat.
142|||Ian takes in the threat without answering. Preserve the interval before the man explains his grievance.
146|You're not getting away. You made a fool of me back there!|made a fool of me|The man threatens Ian and claims Ian embarrassed him. The colloquial complaint fits his vindictiveness.
149|(There are too many. I can't take them all. I'll go for the one who looks like he's in charge!)|I can't take them all.;looks like he's in charge!)|Ian weighs the odds and singles out the apparent leader. He is making a tactical guess.
154|What's taking you so long? He's one man! Get on with it!|He's one man!;Get on with it!|The ringleader is angry that his group is taking so long against one person. The short orders fit an ongoing fight.
157|Heh heh. Pretty face and you can fight, too. Watching you fight is quite a turn-on.|Pretty face;quite a turn-on.|The accomplice makes a lewd appraisal of Ian even during the fight. Keep the menace focused on his conduct without adding a detail about Ian struggling.
161|Hah, hah... (I can't even get near him on my own!)|get near him|Ian is out of breath and realizes he cannot even reach the man alone. It shows that his original plan has failed.
164|Looks like you're about done. Finish him off!|Finish him off!|The ringleader thinks Ian is nearly beaten and orders the others to act. The command is cut short by the crew's arrival.
167|Wh-who are you?!|Wh-who are you?!|Hodram's intervention startles the ringleader into a stammer. It breaks the momentum of his orders.
171|Grown men, and it takes the lot of you to fight one? Shameful.|the lot of you;Shameful.|Hodram reproaches grown men for using numbers against a single opponent. His contempt comes through before the retreat.
174|||The man curses, admits he only starts fights he can win, and threatens revenge. His opportunism explains why he backs off now.
179|||Ian is silent after the attackers leave. Preserve this beat before Hodram speaks directly to him.
183|||Hodram understands the fuss the women were making at the tavern. Keep the observation that Ian immediately takes the wrong way.
187|...What does it matter how I look?|how I look?|Ian mutters that his appearance does not matter. The involuntary comment sets up his apology for speaking to himself.
190|||Hodram says Ian can think as he pleases. His disengaged answer gives Ian room to clarify.
193|I was talking to myself. Sorry... Thank you. You all saved my life.|talking to myself.;saved my life.|Ian apologizes for the aside and thanks the whole group for saving him. The sequence moves from defensiveness to gratitude.
197|No need to thank us. I saw what you can do with a sword, and I'd like to ask you a favor.|with a sword,;ask you a favor.|Hodram says thanks are unnecessary and makes Ian's swordsmanship the reason for his request. It leads into the offer on the next turns.
201|||Ian responds politely that he will help if he can. He has yet to learn what Hodram wants.
205|That was fine sword work back there. How'd you like to put it to the test out in the world?|fine sword work;out in the world?|Hodram praises Ian's swordsmanship directly and invites him to test it beyond this fight. The question leaves the offer initially unclear.
208|||Ian is puzzled and asks what Hodram means. The brief lead-in keeps the invitation and acceptance distinct.
211|||Hodram invites Ian aboard his ship, plainly and without trying to persuade him further.
215|||Ian checks that the offer is genuine and says he would gladly accept. The hesitation is about the timing, as he explains shortly afterward.
219|||Hodram takes Ian's hesitation as doubt and asks whether he sounds like he is joking. His matter-of-fact challenge suits the misunderstanding.
222|No, it's just... your timing couldn't be better.|couldn't be better.|Ian explains that the offer has arrived at an uncannily good moment. The hesitation gives way to relief.
225|||Hodram still does not understand the timing. The small reaction prompts Ian's final explanation.
229|I'm a navigator out of work. I'd be grateful for a place aboard your ship. Ian Dukov, at your service.|a navigator out of work.;Ian Dukov, at your service.|Ian identifies himself as an unemployed navigator, formally asks to join, and gives his established name. His courteous introduction follows the relief of finding a ship.
""",
    160: """
5|My usual amount of cinnamon, please.|My usual amount of cinnamon,|Carlo orders his customary quantity. The order establishes a regular customer with a basis for recognizing the higher price.
9|||Hodram realizes they have to wait for another customer. His quiet aside keeps him an observer while Carlo bargains.
13|Here you go. It'll come to this much.|come to this much.|Adil acknowledges the order and shows Carlo the total. His casual delivery leads to the price objection.
17|||Carlo notices that the price increased and sounds mildly surprised. Keep the observation before he calls Adil on it.
21|||Adil denies the increase and insists it is his usual price. The plain denial makes Carlo's answer effective.
24|||Carlo laughs and challenges Adil on his purchase cost. His teasing familiarity establishes that they know each other without implying a specific relationship.
27|Come on, now...|Come on, now...|Adil objects weakly after Carlo exposes the bluff. The trailing reply gives Carlo the floor again.
31|||Carlo cites the year's cinnamon crop and local demand as reasons for a better price. The existing succinct argument makes his negotiating skill evident.
35|||Carlo says he could buy elsewhere and owes no shop all his business. Keep the warning unstated as a threat.
39|Ugh... A-all right. I can't win with you.|I can't win with you.|Adil stammers as he concedes. The friendly frustration keeps the dispute good-natured before Carlo notices his condition.
43|||Carlo breaks off the bargaining when he notices Adil might have a fever. The short question does the work.
46|What now, Carlo? You still picking holes in how I do business?|What now, Carlo?;how I do business?|Adil thinks the fever question is just another complaint about his trade. Keep his exasperation and the misunderstanding.
49|||Carlo says Adil really has a fever and tells him to go to bed early. His direct concern replaces his bargaining voice.
52|||Adil starts to dismiss Carlo again, then realizes he has the chills. The established shift from disbelief to recognition works.
55|||Carlo tells Adil to close and says his purchases can wait until tomorrow. The reassuring order shows the concern is genuine.
58|||Adil accepts the advice and asks the waiting travelers to return tomorrow too. The awkward apology follows his concession naturally.
64|Sorry about that. You came here to trade, too, right?|to trade, too, right?|Carlo apologizes to the whole waiting party and checks why they came. The tag follows the question it qualifies.
67|||Hodram asks how Carlo knew the shopkeeper was ill. The question starts his assessment of Carlo beyond the bargaining.
71|He looked pale.|He looked pale.|Carlo points to Adil's complexion. The ordinary observation makes the next characters' disagreement about what they saw intelligible.
83|||The crew member claims Carlo is almost as observant as he is. The self-serving compliment keeps the joke between two sincere reactions.
89|||Hodram privately admits he saw no sign of illness. Retain the parenthetical reaction after the other crew member's boast.
93|||Carlo says most people would miss the sign and that he notices how others are feeling. The line hints at the personal reason without revealing it.
97|||Hodram quietly registers what Carlo tells him. The short aside leaves the explanation for later.
101|||Carlo invites them to return with him tomorrow morning and says he may make up for the inconvenience. Retain the time, place, and tentative offer.
104|Sure. I'll be there.|I'll be there.|Hodram agrees to come and gives his word. His assurance is warmer and more direct after Carlo's offer.
108|||Adil's wife greets Carlo with thanks the next day. The personal greeting begins the payoff to the previous scene.
112|||Carlo asks after Adil immediately. The question picks up his concern from yesterday.
116|||She says Adil is at home resting as a precaution. That accounts for her presence and sets up his unexpected entrance.
119|||Carlo hopes Adil recovers soon. Keep the plain wish before she explains why she is grateful.
123|That man never listens to me. If you hadn't said something yesterday...|never listens to me.;said something yesterday...|She complains fondly that Adil would not listen and begins to imagine what could have happened. The unfinished thought leads to her thanks.
127|||She catches herself going on and says Carlo saved Adil's life. The hyperbole is her grateful opinion.
131|||Carlo appreciates the thanks but directs her to the travelers who lost a day. The existing refusal is polite and gives his reason.
135|Oh, I'm sorry we kept you waiting. It isn't much, but... will you take this?|kept you waiting.;will you take this?|She apologizes for holding them up and offers a modest gift with a small hesitation. The established shorter version lost that warmth.
141|Thank you, ma'am. You folks are in a hurry, right? Go ahead and make your purchases.|in a hurry, right?;make your purchases.|Carlo thanks her and gives the travelers priority. The address suits the group without assuming how well he knows them.
145|||Adil arrives in high spirits and apologizes to Carlo. His energy abruptly contradicts the account of him resting.
148|Adil!|Adil!|She calls out to her husband in surprise. Using the name expresses that direct address without a literal and awkward you.
152|||Carlo answers Adil's surprise entrance by telling him he ought to be in bed. Keep the startled name.
155|||Adil cheerfully swears he is healthy and says such a good day for business is wasted in bed. The idiom and pacing suit his defiance.
159|||His wife calls him impossible. The familiar reproach plays off the stubbornness she described moments earlier.
163|Ha! Good to see you feeling better. Just don't overdo it today.|feeling better.;don't overdo it today.|Carlo is reassured by Adil's energy but still tells him to take care. Keep the laugh and the one-day qualification.
167|||Carlo says he will come back tomorrow and asks Adil to handle the travelers' business. The favor keeps his offer to compensate them.
170|Take care of your family and your health, folks. I'll be seeing you.|and your health, folks.;I'll be seeing you.|Carlo gives the strangers a personal reminder before he leaves. His emphasis on family and health prompts Hodram to stop him.
173|||Hodram pauses as Carlo says goodbye. Keep the interval before he decides to speak.
178|||Hodram calls Carlo back. The preceding hesitation makes the abrupt request believable.
182|||Carlo turns back with a questioning sound. It gives Hodram the next turn.
186|I was impressed with the way you bargained yesterday. I'd like you aboard my ship.|you bargained yesterday.;aboard my ship.|Hodram points to yesterday's bargaining and makes his offer explicit. This gives Carlo a clear reason to be surprised.
189|Hold on. Where'd that come from?|Where'd that come from?|Carlo is taken aback by the sudden offer. The quick questions match the familiar register heard with Adil.
193|||Hodram confirms that he is serious. His brief answer lets Carlo explain his objection.
197|||Carlo says he is a merchant with no claim to being a sailor. Keep the blunt description of himself.
200|||Hodram explains that work aboard a ship includes the important role of purser. Preserve the approved role and the distinction between trade and ship handling.
204|||Carlo falls silent after learning he has a place on a ship. The pause prompts Hodram to guess why he hesitates.
208|Do you mind leaving here? You don't want to leave your children?|leaving here?;leave your children?|Hodram guesses that Carlo may be unwilling to leave because he has children. The question stays a guess before Carlo corrects it.
211|I don't have a family... I lost them a year ago.|a year ago.|Carlo states the loss after a pause. His next turns explain who died and why he holds himself responsible.
214|||Hodram has no immediate reply. Keep the silence before Carlo tells the story.
219|My daughter was the first to catch it. There was an epidemic. I was so caught up in work... I didn't take proper care of her.|the first to catch it.;so caught up in work...;proper care of her.|Carlo recounts his daughter's illness and blames his absorption in work for not caring for her properly. The pause belongs to his reluctance to admit it.
222|We got help too late. My wife caught it, too... I lost them both.|My wife caught it, too...;I lost them both.|Carlo says treatment came too late and his wife contracted the illness. I lost them both completes his sense of responsibility without naming a disease.
226|||Hodram reacts softly to the loss. The subdued words leave Carlo space to say what changed for him.
230|...I'd neglected my family for my work, and in the end it felt empty. Ever since, I've cared more about people's health than about business.|neglected my family;in the end it felt empty.;than about business.|Carlo explains that the work he put before his family no longer meant anything. His concern for others follows directly from that loss.
233|||Hodram connects Carlo's explanation with his noticing that Adil was unwell. Keep the retrospective realization before he asks about home.
237|...Have you thought about going home?|thought about going home?|Hodram tentatively asks about Carlo's hometown. The hesitation belongs to a man choosing his words after hearing about the loss.
241|Venice? I've got too many happy memories there. I couldn't live there alone.|happy memories there.;live there alone.|Carlo names his hometown and says the happy memories make living there alone unbearable. His answer prepares Hodram's offer of company.
245|||Hodram considers Carlo's answer before pressing the offer. The separate silence keeps the change in tone unhurried.
249|Carlo, why don't you come with us? If you don't want to go back to Venice alone, that is.|come with us?;back to Venice alone,|Hodram offers Carlo a place with them. The qualification gives Carlo room to decide how much he wants company when he returns.
253|||Carlo is surprised by this renewed offer. Preserve the questioning beat before Hodram elaborates.
257|||Hodram describes shipmates living and working together and offers the crew as family. Keep the invitation in his voice without creating a legal or blood relationship.
260|You'd... be my new family?|be my new family?|Carlo asks whether Hodram and the crew mean to become his family. The hesitation carries his surprise and emotion.
264|That's right. And I can use a man with your skills. So... will you come?|a man with your skills.;will you come?|Hodram confirms the offer and says he values Carlo's skills too. The last question makes the choice Carlo's.
268|||Carlo thanks Hodram and gladly accepts after a pause. The brevity lets the decision speak for itself.
271|||Carlo gives his approved full name and formally introduces himself as their new shipmate. His courteous closing suits the quieter end to the exchange.
""",
}
review = checked_text(previous.review, {"len(records) == 73": "len(records) == 130"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::recruiting-Ian-and-Carlo", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

