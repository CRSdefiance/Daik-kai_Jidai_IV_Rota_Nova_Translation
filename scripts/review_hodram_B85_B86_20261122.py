"""Review Cristina's recruitment and the complete Mivor rescue exchange."""

from scripts import review_hodram_B81_B84_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT, paired = previous.base, previous.ROOT, previous.paired
OUTPUT = ROOT / "B85_B86_contextual_v3.json"
GLYPHS = set()
CONTEXTS = {
    85: "Cristina has had enough of Mivor following her over the engagement their parents arranged. She recognizes her grandfather Julio, who offers her the chance to sail and train. Mivor's protests end in an ill-judged sword challenge.",
    86: "Cristina revisits London and tells Mivor she has not come back for him. She tries to rescue a boy and is herself in danger. Mivor overcomes his fear in the moment. She thanks him after hearing the mother confirm what happened, and keeps her own position about him.",
}

DECISIONS = {
    85: """
5|||Cristina is exasperated because Mivor keeps following her. The short opening and question tag sound like a real outburst.
8|||Mivor uses florid affection and asks why she is cold toward him. The existing voice characterizes his expectations alone.
11|What's wrong with you? Why keep following someone who can't stand you?|What's wrong with you?;who can't stand you?|Cristina directly challenges him for following someone who strongly dislikes it. The exasperation follows his self-pity.
14|||Mivor mistakes her irritation for shyness. Keep the joke in his misreading rather than changing her meaning.
18|Ugh, I've had it. Our parents arranged the engagement without asking me. I'm not getting married. Period!|I've had it.;without asking me.;I'm not getting married.|Cristina says the parents acted without her consent and emphatically rejects marriage.
21|The sound of your voice is all I need to be happy!|The sound of your voice;to be happy!|Mivor ignores what she is saying and declares that just hearing her makes him happy. The theatrical sentiment is his.
24|||Cristina calls him a fool outright when he misses the point. The single insult keeps the comic timing.
28|||Hodram hesitantly asks Julio if she is the person they came to meet. The brief question keeps his uncertainty.
32|||Julio confirms it plainly and sees no reason to wait.
36|She looks a little busy at the moment...|a little busy;at the moment...|Hodram diplomatically points out the commotion around Cristina. The understatement fits his hesitation.
39|||Julio says it is no trouble and calls out to Cristina. The greeting changes the direction of the argument.
43|||Julio calls Cristina by name again and asks how she has been. Keep his warmth.
47|||Cristina calls him Grandpa and asks when he reached London. This relationship is explicit in the exchange.
51|||Julio says he has just arrived and is going to sea again. The two short statements fit his offhand delivery.
54|||Cristina reacts to the repeat and says both parents will try to stop him. Keep her genuine surprise.
57|They won't find out if you don't tell them. Ho ho!|won't find out;if you don't tell them.|Julio says his plans can stay a secret if she says nothing. The laugh makes it conspiratorial.
60|||Cristina starts to object to his evasion. The unfinished complaint leads into his invitation.
64|Anyway, how about going to sea with me?|going to sea with me?|Julio turns from the parents to his offer that Cristina come sailing with him.
67|||Mivor responds in horror and objects at once. His abrupt interruption fits the scene.
70|||Julio asks who Mivor is in plain language. He neither knows him nor owes him a title.
73|||Cristina identifies him as the son of one of her father's friends and genuinely cannot recall his name. The existing question makes her indifference clear.
76|||Mivor again calls her shy, then checks whether Julio is her grandfather. The question leaves him to introduce himself next.
80|||Mivor introduces himself with the approved Mivor Genz and repeats the given name as a flourish. The formal greeting suits his performance.
83|Right, that's the name. Before I knew it, Dad and the others had made the whole arrangement without me.|that's the name.;Dad and the others;without me.|Cristina recognizes his name and reiterates that her father and the others acted on their own.
87|||Cristina says she is supposedly engaged to him and struggles for a dismissive noun. The existing hesitation fits her disbelief.
90|||Julio calmly takes in the information. His brief reaction gives Cristina something specific to object to.
94|||Cristina repeats Julio's words to reject his casual response. The quoted phrase preserves the call and response.
98|Hmm. This pale fellow, is it...|This pale fellow|Julio takes stock of Mivor using his physical description. His trailing thought invites Mivor to speak.
101|I-it isn't just because our parents said so. I really do care for Miss Cristina...|isn't just because;care for Miss Cristina...|Mivor says his feelings are sincere apart from the arrangement. His polite address and incomplete thought stay his alone.
108|||Julio says it sounds like Harald and jokes that he may have raised him badly. Keep his self-directed joke and the approved name.
111|||Mivor hesitates and tries to speak again before Cristina cuts him off.
115|You be quiet! Now, Grandpa, what were you saying about a ship?|You be quiet!;saying about a ship?|Cristina tells Mivor to be quiet and turns back to Julio's unfinished invitation.
119|Oh, right! I thought you might like to come with me.|I thought you might like;come with me.|Julio remembers his point and repeats that he wants her to come with him.
123|Julio says you're quite a swordswoman. Pardon me for asking out of the blue, but will you come aboard my ship?|quite a swordswoman.;out of the blue,;come aboard my ship?|Hodram repeats Julio's assessment of her swordsmanship, acknowledges the sudden request, and invites her aboard.
126|||Cristina turns to Julio to ask who the strangers are. Her abrupt question follows the sudden invitation.
129|Well... (So much to explain.) First, meet Admiral FI FA.|So much to explain.|Julio thinks privately about all the explaining, then introduces the admiral by both controlled names. The formatter can keep the full substituted name together on the next line.
132|||Cristina marvels at how young the admiral is. The existing direct observation keeps her personality.
136|You said it's hard for women to challenge other schools. Why not travel the world and train with your sword?|challenge other schools.;travel the world;train with your sword?|Julio recalls her difficulty challenging other schools as a woman and suggests training abroad as an opportunity.
139|||Mivor objects loudly. The repeated rejection suits his renewed interruption.
143|Hmm... That sounds good to me. I'll go.|sounds good to me.;I'll go.|Cristina considers the idea and decides for herself to accept.
146|||Mivor repeats his objection more forcefully as she ignores it.
150|||Hodram asks what to do about the other man. The brief question does not give Mivor a role on the ship.
154|||Cristina dismisses the distraction and urges them to act now. The existing English proverb serves the same purpose as hers.
157|That's my granddaughter! You've got the right idea.|That's my granddaughter!;the right idea.|Julio commends his granddaughter for grasping the point. His pride and the stated relationship remain.
160|||Hodram checks Mivor's name and offers him the same chance to come along. The offer is genuine even though it leads to more comedy.
164|||Mivor stammers instead of answering the invitation. Keep that hesitation.
168|||Cristina says he cannot swim, is terrified of water and therefore cannot follow. The taunting question fits her certainty.
171|||Mivor sees no other way out and challenges someone to a contest with swords. The stammer preserves the contrast with his theatrical resolve.
174|||Hodram reacts with a wordless jolt as the challenge starts. Keep the two exclamation marks.
178|||Cristina says he never learns and lets out a fighting cry. No account of what the blow does is added.
182|||Mivor gives a howl and cries out in pain. The existing short exclamations fit.
186|With a stance like that, you couldn't beat a child.|With a stance like that,;couldn't beat a child.|Cristina mocks his poor stance and says even a child could beat him. The insult stays aimed at his swordsmanship.
189|||Julio recognizes her skill and says it has not dulled. His approval follows the sudden exchange of blows.
192|||Mivor exclaims over his rapier and says his father bought it. Keep the commotion without specifying how the rapier was damaged.
196|Come on, let's go! I'm looking forward to the sword matches, but the voyage sounds fun too!|I'm looking forward;the sword matches,;the voyage sounds fun too!|Cristina is eager to leave and looks forward to the ship voyage as well as the sword matches.
""",
    86: """
5|||Cristina welcomes the air back home in London. Her comfortable tone sets the scene before the interruption.
8|You're home. Take some time to unwind.|Take some time to unwind.|Hodram encourages Cristina to take it easy while she is back in her hometown.
12|Thanks. I'll take a walk around the harbor. I've always liked it there.|take a walk around the harbor.;I've always liked it there.|Cristina says she will walk around the harbor, something she has long enjoyed. The English avoids repeating the walking phrase.
16|||Hodram says the rest of them will be at the inn. The concise reply gives Cristina room to leave.
19|||Cristina notices the harbor feels unchanged and enjoys it. Her pauses carry that brief calm.
22|Oooooh! It's a miracle! This is love! Cri-sti-naaa!|It's a miracle!;This is love!|Mivor stretches his exclamation and Cristina's name as he declares the meeting a miracle of love. The romantic reading is his.
26|||Cristina realizes who it is and reacts with alarm. Keep the compact exclamation.
30|||Mivor repeats his relief before stammering that he knew his love would reach her. The sentence trails off as he starts crying.
34|||Cristina asks him not to cry in public. The stammer and the reason already sound natural.
40|||Mivor is confused by her explanation that this is only a temporary stop.
44|||Cristina emphasizes she did not return for him. The spoken repetition gives Mivor no grounds to misread her purpose.
47|And I haven't given marrying you a thought. Not one little thought.|marrying you a thought.;Not one little thought.|Cristina emphatically says she has spent no time considering marriage to him. Her emphasis stays firm.
51|B-but... what is it you don't like about me?|don't like about me?|Mivor takes the refusal personally and anxiously asks what she dislikes.
54|||Cristina explains that she is not considering marriage yet and tells him to let it go. Her wording does not encourage him to wait for consent.
58|...I understand. I'll give up, yes... Ahh... So ends my love...|I'll give up, yes...;So ends my love...|Mivor gives in and narrates the end of his own love in a theatrical sigh.
62|Whew... Now he can stop chasing me.|stop chasing me.|Cristina is relieved that his pursuit may finally stop. The compact response preserves her relief without guaranteeing his behavior.
66|||Cristina is suddenly alarmed by something else. Keep the punctuation beat distinct from Mivor's.
70|||Mivor changes from a sigh to surprise. His two reactions lead toward the commotion.
74|Oh, my boy!|my boy!|The mother cries out to the child. The brief exclamation fits the immediate danger.
78|||Cristina asks what happened before anyone has explained the danger.
83|||The mother says her son fell into the sea and calls for someone to save him. Keep the urgency and stated relationship.
87|Hang on! I'll get him!|I'll get him!|Cristina urgently tells the mother to wait and commits to rescuing the boy.
91|||Cristina tells the boy to hold on because she is on her way. The promise of imminent help suits the action.
95|||Mivor calls Cristina's name in surprise as she rushes to help. Keep the hesitation.
100|||Cristina reassures the boy that she's here and he is safe. The English avoids turning the familiar older-sister form into a relationship.
103|||The Boy panel carries the child's first repeated cry of fear. The exact label and speakerless presentation remain appropriate.
106|||Cristina says again that he is safe. Her short reassurance fits his fear.
110|||Cristina asks the boy to release her neck because she cannot breathe. Her stammer conveys strain.
113|||The second Boy panel repeats the fear as the boy clings to her. Its words and label work in the exchange.
116|||Cristina realizes both could drown if this continues. The existing sentence expresses the shared danger plainly.
119|||The third Boy panel adds a cry before saying he is scared. Keep it distinct from the two preceding panels.
122|||Cristina stammers that she is drowning. The fragmented delivery suits the moment.
126|||The mother cries out for someone to help. Keep the urgency without inventing who is nearby.
132|||Mivor asks whether anyone can help before he has resolved to enter the water.
136|||Mivor repeats Cristina's name, only to be checked by his fear of the sea and water. The fragments keep his indecision.
139|||The repeated fear and the greater-than sign make his first internal comparison legible. Preserve the source joke and its initial direction.
142|||Mivor's two attempts to object give way to a roar. The sound conveys the turn before the second comparison.
145|||Use the same words as the first comparison with the sign reversed. The reversal shows his resolve winning out in this moment.
148|||Mivor says Cristina's name three times. Retain the repetition building to the next shout.
151|||Mivor yells her name emphatically. The existing capitals and punctuation give the peak of the sequence a distinct voice.
155|||Mivor announces himself in the third person as he sets off. The existing wording keeps his odd self-encouragement.
159|||He tells Cristina he's coming to save her. The earlier Japanese leading layout spacing is already absent from the current prose.
165|Cough... Cough... Mivor? Where am I? What happened to me?|Where am I?;What happened to me?|Cristina coughs awake, recognizes Mivor uncertainly, and asks where she is and what happened.
169|||Mivor's familiar florid address returns as he realizes she has woken. It does not establish how she feels.
172|||Cristina remembers drowning, then asks if the boy is safe. The question follows the alarm on waking.
176|Yes, he's fine. His mother said thank you.|he's fine.;His mother said thank you.|Mivor confirms the boy is safe and says the woman thanked him. The prior cries and their later return establish that she is the boy's mother.
180|Then someone must've saved us. I should thank them. Where are they?|someone must've saved us.;I should thank them.|Cristina infers that someone saved them and asks where to find her rescuer.
184|||Mivor hesitantly indicates that the rescuer is right there. His indirectness leads to her confusion.
187|||Cristina's small surprised question asks him to clarify.
191|Well, you see... I... I saved you.|I saved you.|Mivor reluctantly gets the words out that he saved her. Restore his repeated first-person hesitation.
194|||Cristina is incredulous because Mivor is afraid of water. Her trailing question fits.
198|||Mivor acknowledges the fear and explains that his thoughts changed when he had to rescue her. Keep his inability to finish the thought.
202|||He says he somehow swam and cannot believe it himself. The existing words preserve surprise without claiming a permanent change.
205|||Cristina asks whether he really did it and says she can't believe it. The quiet disbelief precedes her excuse to go.
208|||Cristina falters and says she has to get to the inn. Her stammer fits the awkwardness.
212|||Mivor asks whether she is all right. The simple concern does not press her further.
216|||Cristina says she can go on her own. Her straightforward answer keeps that boundary.
220|||Mivor takes his leave quietly. The pause fits the change from excitement to uncertainty.
225|||The boy recognizes Cristina when he returns. His familiar address is naturally conveyed without suggesting she is his sister.
229|||Cristina checks whether the boy is all right. The informal question fits her concern.
233|||The boy thanks her and asks after the man who saved them. The English avoids an invented kinship.
237|||The mother thanks Cristina and asks where her companion has gone. The existing wording stays polite.
240|||Cristina asks again whether Mivor truly jumped into the sea. She is verifying what sounded impossible to her.
244|||The mother confirms that he leaped in while making a strange yell. The existing sentence recalls his unusual entrance.
247|||The mother reads the leap as proof of how much he loves Cristina. Keep it as the mother's interpretation.
250|||Cristina accepts that the rescue really happened. The pause gives the realization space.
254|||The mother offers something in thanks and asks Cristina to accept it. The identity of the gift is not stated here.
259|||Cristina is surprised and thanks her. The small pause suits the gesture.
263|||The mother says they are leaving and thanks Cristina once more.
266|||The child gives a simple goodbye. The English needs no kinship label.
272|||Cristina concludes her account to Hodram. The existing phrase picks up after her explanation.
276|||Hodram is surprised Mivor did it and grants him credit. His two brief reactions fit.
279|||Cristina still cannot quite accept it, even after the witness confirmed it.
283|||Hodram sees Mivor while they are discussing him. The existing proverb conveys the comic timing.
287|||Cristina recognizes Mivor and pauses before she thanks him.
291|||Mivor answers quietly with her name. Keep the hesitation before her admission.
295|I didn't thank you properly before. Thank you, Mivor. You were... pretty dashing.|thank you properly;Thank you, Mivor.;pretty dashing.|Cristina gives overdue thanks and hesitantly compliments Mivor for his rescue. Her later warning limits how he should read it.
299|||Mivor is wildly surprised by the compliment. The drawn-out question fits his disbelief.
303|||He echoes the compliment in surprise and repeats how happy he is. His excitement is about what he thinks she said.
307|||Cristina tells Mivor not to get the wrong idea. The brief warning stays firm.
311|||Mivor remains delighted regardless. Keep his repetitions and return to calling her name.
315|Oh, will you be quiet? Let's sail already. He's driving me crazy!|will you be quiet?;Let's sail already.;driving me crazy!|Cristina reacts to the renewed commotion and wants the ship to leave. The relief and gratitude did not end her irritation.
319|||Mivor calls after her that he will always wait. His promise is unilateral.
322|Heh. You two are quite a pair.|quite a pair.|Hodram teases them as a pair after the argument. The banter leaves the relationship to them.
""",
}

review = checked_text(previous.review, {"len(records) == 76": "len(records) == 139"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::contextual-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
