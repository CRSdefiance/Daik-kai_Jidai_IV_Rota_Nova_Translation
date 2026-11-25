"""Review the Silla Gold Crown, the pirate encounter and the banana forecast."""

from scripts import review_hodram_B173_B175_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT, paired = previous.base, previous.ROOT, previous.paired
OUTPUT = ROOT / "B176_B180_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    176: "Julian finds that his usual flattery cannot distract Mihwa from the Silla Gold Crown. He rushes off to find it. Hodram, who overheard them, asks about the crown but makes no promise to her.",
    177: "A tavern worker in Seoul knows a likely location for the crown. Her account of the previous visitor's flattery leads Hodram to suspect Julian went to the tomb first.",
    178: "Julian gives Mihwa the crown and insists on crediting Hodram. Hodram recognizes his adventurous spirit and loyalty. Julian asks to join, and Hodram agrees on condition that Julian does his duties.",
    179: "A pirate recognizes the fleet and jokes with Gerhard. She rebukes Angel for trying to intimidate the officers and insists on settling the matter at sea. Hodram notices the way she commands her crew.",
    180: "A woman predicts that bananas will catch on and orders a skeptical companion to buy as many as possible. The independent game notice leaves the expected result in Seville tentative.",
}
DECISIONS = {
    176: """
7|||Julian declares that he lives to see Mihwa's smile. His deliberate excess sets up Hodram's dry aside.
11|||Mihwa responds familiarly to the compliment. The brief acknowledgment gives Julian room to notice what is different about her reaction.
15|Good grief, that's sweet enough to hurt.|sweet enough to hurt.|Hodram finds the compliment painfully cloying. The dry aside keeps the tooth-related joke without interrupting Julian.
19|Huh? That usually makes you smile. You haven't gone off me, have you?|usually makes you smile.;gone off me, have you?|Julian notices that his usual line has failed and worries that Mihwa no longer likes him. His question stays in his own anxious voice.
23|No, that's not it. You usually cheer me up, but...|cheer me up, but...|Mihwa reassures him, then explains that the usual flattery cannot lift her mood today. Keep the trailing answer for her disclosure.
27|||Mihwa says she badly wants something and cannot get it out of her mind day or night. The familiar idiom preserves the intensity.
31|Oh, Mihwa. It hurts to see you looking so glum. What is it you want so badly?|looking so glum.;want so badly?|Julian finds her expression out of place and wants to know what has caused it. His concern comes through his characteristic exaggeration.
35|||Mihwa names the Silla Gold Crown and says she has heard that it is valuable. The question about its name keeps the attraction personal.
39|||Julian assumes the crown will be expensive and wonders whether he can afford it. His question about a shop sets up her correction.
42|That's the thing. Shops don't sell it. I heard it's somewhere in Seoul.|Shops don't sell it.;somewhere in Seoul.|Mihwa says the crown cannot be purchased in a shop and repeats the lead about Seoul. Her wording still conveys that she only heard the location.
45|No one sells it? ...Of course! I know where to look!|No one sells it?;I know where to look!|Julian repeats the surprising fact before deciding where to look. He has a candidate location before he has actually found the crown.
48|||Mihwa asks if he knows where to go. The quick question follows his realization.
52|Leave it to me! I'll find the Silla Gold Crown as fast as I can and put that smile back on your face!|the Silla Gold Crown;back on your face!|Julian says he will get the named crown as quickly as possible and cheer her up. His enthusiasm connects it to his first compliment.
56|That smile of yours keeps me going! And if I find the Silla Gold Crown, you'll go out with me, right?|keeps me going!;the Silla Gold Crown,;with me, right?|Julian returns to how much Mihwa's smile means to him and asks for a date as a condition. The tag brings out his eagerness and leaves her free to answer.
59|||Mihwa says he is getting ahead of himself and only agrees to think about it. The limit matters because Julian immediately treats it as a promise.
63|||Julian celebrates the promise he thinks he heard, tells her to remember it and sets out for Seoul. Keep his overinterpretation in his own words.
66|I'm counting on you... Oh. He's gone already.|I'm counting on you...;He's gone already.|Mihwa tries to express her expectation only to realize Julian has already left. Keep the comic interruption.
69|||Hodram stays silent before Mihwa notices him. The separate beat lets the scene change addressee.
73|Oh, I'm sorry. I didn't see you there. Welcome.|didn't see you there.|Mihwa apologizes for failing to notice Hodram and greets him as a customer. Preserve the missed greeting as the reason for her apology.
76|||Hodram asks about the conversation he just heard. The trailing opening gives Mihwa room to realize he was listening.
80|||Mihwa checks whether Hodram heard what she said. The brief question lets him name the subject.
84|||Hodram asks about the named crown. Keeping the full item title clear connects his question to Julian's search.
88|||Mihwa admits that she knows little and says she has heard that the crown is beautiful. The limitation matters to Hodram's next question.
91|||Hodram considers how little she knows. Preserve the quiet beat before she comments on his appearance.
95|You look like a military man. I didn't think you'd be interested in something like that.|look like a military man.;something like that.|Mihwa judges by his appearance and is surprised by his interest. Keep the military role as her observation rather than a formal introduction.
98|||Hodram checks that he heard Seoul correctly. The brief question sticks to the only actionable clue.
102|||Mihwa confirms the city and admits she knows nothing else. Keep the limits of the lead explicit.
105|||Hodram has enough to start looking and expects to learn more once he arrives. The next step stays his decision.
108|If you find it, would you give it to me?|give it to me?|Mihwa asks for the crown only if Hodram finds it. The condition leaves him free to answer without making a promise.
112|||Hodram says he will consider it. The noncommittal answer preserves his reserve at the end of the encounter.
""",
    177: """
6|||Hodram thinks somebody in town might know about the Silla Gold Crown. The thought gives him a reason to talk to the tavern worker.
9|||The tavern worker welcomes him and offers a drink. The ordinary greeting leaves him room to bring up the crown himself.
13|||Hodram accepts the drink, then introduces the real subject with the full item title. The two parts make it a recognizable tavern exchange.
17|||She asks what he wants to know. The brief offer lets Hodram say that he needs the location.
21|||Hodram asks where the crown might be. The short follow-up reflects what the worker just asked.
24|||The worker names the Tomb of King Muryeong as the likely location but admits she does not know how to get the crown. Preserve both uncertainties.
28|||Hodram repeats the tomb's name as he takes in the lead. The established title stays consistent with the previous turn.
32|Funny thing is, someone asked me that same question earlier.|that same question earlier.|The tavern worker mentions a prior visitor and identifies the question as the same. Her casual surprise invites Hodram to make the connection.
35|The same thing? Of course... Was the man who asked named Julian?|Was the man who asked;named Julian?|Hodram realizes the visitor might have been Julian and asks for confirmation. The question allows the worker to recognize his habits without remembering his name.
39|I don't remember his name. First thing he said was, 'Your lips are like rose petals.' He's had plenty of practice flirting.|I don't remember his name.;are like rose petals.';practice flirting.|The worker cannot recall the name but quotes the exact kind of compliment and comments on his practiced flirting. Keep the rose-petal comparison as his words.
42|||Hodram takes the flattery as a recognizable clue. The source leaves his reaction wordless.
46|||Hodram asks if that means Julian went straight to the tomb. The question remains an inference from the report.
49|||She thinks he probably went there. The uncertainty stays intact before Hodram leaves.
53|I see. I'd better be on my way.|be on my way.|Hodram acknowledges the information and makes up his mind to go. The plain farewell closes the conversation.
""",
    178: """
6|Oh, it's you. Thanks for your help earlier.|for your help earlier.|Julian recognizes Hodram and thanks him. He does not yet explain what happened to Mihwa.
10|||Mihwa realizes that Julian and Hodram already know each other. The question leaves Julian room to present the crown first.
14|Anyway, here's your Silla Gold Crown, just like I promised!|Silla Gold Crown,;just like I promised!|Julian turns the conversation back to Mihwa and gives her the crown as promised. The present-tense handover keeps his excitement.
18|||Mihwa recognizes the crown, admires it and thanks him. Her promise to treasure it suits the excitement of finally seeing it.
22|Looks like it all worked out...|all worked out...|Hodram notes that Julian's gesture has gone well. The restrained observation starts his exchange with Gerhard.
26|||Gerhard agrees quietly. The spare echo keeps their reaction apart from Mihwa's celebration.
30|Then we'd better leave them to it...|leave them to it...|Hodram suggests withdrawing now that the gift has been given. His quiet exit is interrupted by Julian.
34|||Julian asks them to wait. The quick interruption gives him the chance to give Hodram credit.
38|||Hodram pauses in surprise instead of answering Julian immediately. Keep the short reaction between their exchanges.
42|Mihwa, actually, FI here is the one who found the Silla Gold Crown.|FI here;the Silla Gold Crown.|Julian tells Mihwa who really found the named item. Preserve the captain's controlled name and the original distinction between finding and giving.
46|||Mihwa reacts in surprise and checks that it is true. The two short beats keep her attention on Julian's disclosure.
50|||Julian explains that he asked Hodram for the crown and that Hodram let him have it. The request preserves the distinction between his part and Hodram's.
53|I thought I'd told you to keep that to yourself...|keep that to yourself...|Hodram reminds Julian that he asked him not to mention it. His subdued response keeps the credit issue from becoming a rebuke.
56|I couldn't do that. I'll find a proper way to thank you later.|I couldn't do that.;thank you later.|Julian feels obliged to be open about it and insists on thanking Hodram later. His loyalty is what Hodram notices.
59|||Mihwa says Julian's name softly after hearing the truth. Leave her precise feeling to the scene rather than adding one.
63|There's no need. But I like your spirit of adventure, and I respect the way you repay a kindness.|spirit of adventure,;repay a kindness.|Hodram declines a reward but takes an interest in Julian's adventurousness and loyalty. Both qualities motivate the recruitment that follows.
67|||Julian asks to join and promises to work hard. The direct use of the captain's controlled name keeps the invitation specific.
70|||Gerhard takes note of the offer without deciding for Hodram. The formal observation gives Julian a chance to explain.
74|My grandfather sailed all over the world. Every time I heard one of his stories, I wanted to see more of it myself...|sailed all over the world.;one of his stories,|Julian says his actual grandfather traveled widely and that his stories awakened his interest. Keep the emphasis on the effect of hearing them.
78|||Julian explicitly wants to be an adventurer like his grandfather. The enthusiastic line concludes his explanation.
82|||Hodram turns over Julian's desire to follow his grandfather's example. The separate echo fits his pause before describing life on his ship.
86|Adventure isn't what my ship is for. But we do sail all over the world.|what my ship is for.;all over the world.|Hodram explains that adventure is not their mission, but they do travel the world. The qualification keeps Julian's eventual duties in view.
90|If you can do the work I expect of you, you can come aboard.|work I expect of you,;come aboard.|Hodram agrees to take him on condition that he can do the work. The direct language keeps the agreement.
93|||Julian celebrates and takes the matter as settled. The emphatic response answers the conditional invitation in his voice.
""",
    179: """
6|Hm... That woman...|That woman...|Hodram recognizes the woman before she speaks. The unfinished thought gives her a natural opening.
10|||The pirate recognizes the fleet through its original company substitution and says their meeting is unexpected. Retain the source-owned modal layout and runtime substitution.
13|Why have you been following our fleet?!|following our fleet?!|Gerhard asks about repeated pursuit. The direct accusation sets up her accusation that he is no fun.
17|My, my. Straight to business. Aren't you a dull one?|Straight to business.;Aren't you a dull one?|The pirate teases Gerhard for bringing up the accusation immediately. The joke is about his manner and invents no title.
21|||She says she had hoped to spend some pleasant time together. The ironical offer keeps the tension before Gerhard answers.
24|...What's with this woman?!|What's with this woman?!|Gerhard is frustrated by her attempt to make light of his question. His aside comes before she calls him stiff.
28|Heh heh. You're every bit the stiff military man. You can't even take a joke.|military man.;can't even take a joke.|The pirate laughs and calls Gerhard a stiff military man who cannot take a joke. Keep the complaint in her provocative voice.
32|||Gerhard suspects that she laid an ambush to assassinate them. The accusation remains his theory rather than an objective description of her intentions.
35|||Hodram waits silently while Gerhard confronts her. The pause gives Angel space to intrude.
39|Do the math. Two of you, dozens of us!|Two of you, dozens of us!|Angel boasts about their numerical advantage. Keeping the two quantities together makes the threat clear before the pirate shuts him down.
43|That's cowardly...|That's cowardly...|Gerhard condemns the threat of using numbers against them. The trailing thought lets the pirate turn on Angel.
47|...Angel. Since when do you speak for me?|Since when do you speak for me?|She rebukes Angel for acting as if he has the authority to intervene. His name and the rhetorical question show who commands the exchange.
51|||Angel stammers once he is called out. The halted defense keeps his sudden loss of confidence.
55|I don't need you butting in. Back off!|butting in.;Back off!|She tells Angel to stop talking out of turn and stand back. The short order makes her authority apparent.
58|||Angel obeys with a stammer. Keep his brief assent separate from her response to Gerhard.
62|Hmph... Get one thing straight.|Get one thing straight.|She turns from Angel back to the officers to correct their assumption. The warning introduces the reason she will not attack them here.
65|I've got too much pride to kill you here!|to kill you here!|The pirate says her pride will not allow her to kill the officers in this situation. Her own rule sets up Hodram's surprise.
68|||Hodram is surprised that pirates claim to have pride. The challenge gives her a reason to explain what she means.
72|Pirates have our own code of honor. You're a man of the sea. You know what I mean. We'll settle this at sea!|code of honor.;a man of the sea.;settle this at sea!|The pirate appeals to a seafarer's pride and insists on settling the dispute at sea. She describes a sense of honor, without adding any named rules.
76|I'll be ready when the time comes.|when the time comes.|Hodram accepts her challenge for that time and place. The measured reply suits his willingness to face her later.
80|Then get ready to meet your end! ...Huh?|meet your end!|The pirate threatens Hodram, then notices something. The altered idiom preserves the threat and the following surprise.
83|||Hodram asks what she noticed. The brief question invites her comment on his sword.
87|...That's a fine sword you've got.|a fine sword|The pirate pauses and praises Hodram's sword. Her attention is specific to the object before she reveals she has been wondering about it.
91|||She is surprised that Hodram has the sword and says she will make it hers someday. Keep her laughter and the unexplained significance of the sword.
95|I have no idea what you're talking about.|what you're talking about.|Hodram says he does not understand her meaning. His plain reply preserves the mystery.
99|You'll find out someday. Come on, boys. We're leaving!|You'll find out someday.;We're leaving!|The pirate says Hodram will eventually understand, then orders her men to withdraw. The change of audience makes the exit immediate.
102|||The crew answer together. The single shout shows how readily they obey.
106|What a strange woman... But she knows how to lead her crew.|a strange woman...;lead her crew.|Hodram calls her strange but admires her command. The praise follows the crew's immediate response to her order.
109|||Gerhard estimates she could command a fleet or two with ease. This remains his opinion, not a claim about ships she already commands.
113|||Hodram reflects on the pirate's pride. The brief echo closes the encounter without explaining her motives.
""",
    180: """
6|||The woman repeats bananas and announces that they are the future. The emphatic prediction starts the joke.
9|||The companion echoes the fruit in disbelief. The short incredulous question gives the woman the next turn.
13|||She argues that bananas taste good enough to become popular. Keep it as her confidence, not a result the game has already confirmed.
17|||The companion remains politely skeptical. The brief reply invites her insistence.
21|||She insists that bananas will catch on because she says so. The repetition keeps her certainty comic.
24|||The companion accepts the decision and asks what to do. The practical question lets her give the order.
27|||She orders him to buy as many bananas as possible. The quantity is open and limited only by what he can buy.
31|||He agrees with a dismissive repetition. The established response suits his skepticism while complying.
35|||She again declares that an age of bananas is beginning and laughs. The dramatic boast is hers before the separate game notice.
38|||The speakerless notice says that bananas may become popular in Seville. Keep the city, commodity and forecast separate from the woman's certainty.
""",
}
review = checked_text(previous.review, {"len(records) == 114": "len(records) == 108"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::the-crown-the-pirate-and-seville", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

