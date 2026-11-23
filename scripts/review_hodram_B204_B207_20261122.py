"""Review Hodram's inn rescue, rope bargain, and two book encounters."""

from scripts import pair_hodram_B201_B220_20261122 as paired
from scripts import review_hodram_B201_B203_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = paired.base, paired.ROOT
OUTPUT = ROOT / "B204_B207_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    204: "Carlo sees a stranger collapse near the port and has him brought to an inn. He reassures the recovering man, urges him to rest and starts to leave. The stranger insists on giving him a token of thanks, and Carlo accepts.",
    205: "A trader claims the mast rope is worn and offers an unusual replacement at a steep price. Hodram teases him. Carlo haggles until the trader names his floor, then leaves the decision to Hodram. Each branch has separate replies and stat notices.",
    206: "A man hurries past and thrusts a book into Hodram's hands while someone calls after him. Charles learns that it is about glassmaking, encourages Hodram to keep it and asks to read it. Hodram realizes what motivates him.",
    207: "Mikhail and Hodram examine an insect with what looks like a plant growing out of it. An older man identifies the caterpillar fungus and offers a book on medicinal ingredients. When Hodram insists on paying, the older man names a lower amount than Hodram's offer.",
}
DECISIONS = {
    204: """
5|||The speakerless impact cues the man's collapse before Carlo reacts. The single sound word is direct and complete.
9|||Carlo reacts to the impact before seeing how bad the man's condition is. The short exclamation leaves room for the groan.
13|||The man groans in distress before Carlo asks whether he is all right. The trailing pause carries the hesitation.
17|||Carlo asks what happened and whether the man is all right. Both urgent questions belong together.
21|Uh... ugh...||The man struggles to respond and groans again. The two sounds preserve the stammer before he comes around.
25|You're awake.||Carlo gently acknowledges that the man has come to. The conversational contraction suits the change from alarm to reassurance.
29|||The disoriented man asks where he is when he wakes. Retain the pause and the direct question.
33|You're at an inn. You collapsed down at the port, so I had you brought here.|at an inn.;at the port,;had you brought here.|Carlo states where they are, where the man collapsed and that he arranged for someone to bring him here. He does not claim to have carried him personally.
37|Oh. I'm sorry you went to all that trouble.|all that trouble.|The man takes in the explanation and apologizes for inconveniencing Carlo. The gentle acknowledgment fits his politeness.
40|It was no trouble. You still look pretty pale, though. Take it easy for a while.|no trouble.;pretty pale, though.;for a while.|Carlo downplays the help, remarks on the stranger's pallor and urges rest. The ordinary advice gives the man a reason to wonder if he is a doctor.
44|Well, I'd better be going. Take care of yourself.|be going.;Take care of yourself.|Carlo politely excuses himself and wishes the man well. Keep the farewell and the concern in the same turn.
47|Oh, wait! Are you a doctor?|Are you a doctor?|The recovering man calls him back to ask whether he is a physician. Doctor is a natural form of the same profession in speech.
50|No, I'm not.||Carlo denies being a doctor. The short answer makes no claim about a different profession.
54|Oh. This isn't much, but please take it as a thank-you.|take it as a thank-you.|The man understates his token of gratitude and asks Carlo to take it. The offer remains polite.
58|Oh, really, there's no need.|there's no need.|Carlo sincerely declines the token at first. This reply prompts the man to insist.
62|I won't feel right unless you take it. Please.|unless you take it.|The man says he will be uneasy if Carlo refuses. Keep his personal reason and quiet insistence.
65|Well, if you insist. Thank you. Now, take good care of yourself.|if you insist.;take good care of yourself.|Carlo relents, then repeats his concern for the man's health before leaving.
69|I will. Thank you so much.|Thank you so much.|The man agrees to look after himself and thanks Carlo sincerely. I will clearly answers the advice.
72|||The notice identifies Carlo and adds one point of Charm. Keep the exact value in the established notice format.
""",
    205: """
5|||The trader claims the rope for the mast is badly worn. His opinion starts the sales pitch and need not be stated as a fact outside his speech.
8|||Hodram doubts the assessment. The mild reply suits his calm response to the trader's pitch.
12|Oh, it's worn, all right. Why not try this rope instead? They say it has some kind of mysterious power.|try this rope instead?;mysterious power.|The trader insists that the rope is worn and proposes a replacement. Keep the alleged power in reported speech.
15|||Hodram pretends the trader is offering to replace it for free. The dry question sets up the trader's indignation.
19|F-free? Of course not! I'll give you a good price, though. Say, 300,000 coins?|a good price, though.;300,000 coins?|The trader stammers at the idea of a free replacement, claims to be offering a deal and names the original price.
22|||Carlo realizes what the trader is asking and interjects. The repeated alarm and short question tag match his interruption.
25|Special or not, that's a ridiculous price for a mast rope. It's worth 30,000 coins at most.|for a mast rope.;30,000 coins at most.|Carlo says the supposed distinction cannot justify the price of a mast rope. Keep his initial valuation and its upper limit exact.
28|H-hold on! You won't find another one like it anywhere. How about 200,000 coins?|one like it anywhere.;200,000 coins?|The trader is taken aback and defends his price by claiming the rope is one of a kind. His first concession keeps the exact amount.
31|||Carlo counters with a bare 50,000. His terse delivery contrasts with the sales pitch.
35|Hmm... 150,000 coins. Can't you meet me there?|150,000 coins.;meet me there?|The trader names his next offer and asks Carlo to accept it. The appeal follows Carlo's first counter.
38|||Carlo answers only with his new offer. Retain the exact 75,000 without adding a second sales argument.
42|You're wearing me down. All right, 100,000 coins. I can't go any lower.|100,000 coins.;can't go any lower.|The trader gives in to the haggling and states the final minimum. Keep his exasperation and the original amount.
46|||Carlo judges the final price acceptable and passes the purchase decision to the admiral. His hesitation preserves the pacing.
SC1_B205_CHOICE_844_0|||Buy authorizes the final offer. The brevity fits the two-option menu.
SC1_B205_CHOICE_844_1|||Pass declines the offer and leaves the original rope in place on that branch.
60|||Carlo accepts responsibility for finishing the purchase after the decision. The phrasing is friendly and assured.
63|All right. I'll leave it to you.|leave it to you.|Hodram confirms he is entrusting the details to Carlo. The reply follows Carlo's offer to handle them without implying annoyance.
70|All right, bring the rope up on deck, will you?|up on deck, will you?|Carlo switches his attention to the trader and asks him to bring the rope to the deck. The familiar address becomes a conversational request.
74|||The trader acknowledges the purchase with conventional thanks. The stock sales farewell suits his change in tone.
78|||The notice awards the playable captain one point of Charm on purchase. Keep the native given-name slot and exact change.
81|||The notice awards Carlo one point of Wits. The fixed name and stat distinguish this message from the captain's reward.
87|This rope still has some life in it. There's no hurry to replace it.|some life in it.;no hurry to replace it.|Hodram declines because the existing rope can still be used. His practical judgment answers the claim that it needed replacement.
91|||Carlo acknowledges the decision and volunteers to decline the offer. Keep his reply separate from the trader's reaction.
95|||The trader is shocked and complains about being led on. His sharp reply matches the refusal.
98|No, really, I'm sorry. We shouldn't have wasted your time.|I'm sorry.;wasted your time.|Carlo apologizes and asks the trader to excuse them. The second sentence takes responsibility in his own voice.
101|||The refusal branch awards the captain one point of Spirit. Preserve the native given-name slot and the distinct stat.
""",
    206: """
5|||The hurried man gets Hodram's attention with a familiar call. His abrupt opening fits the pursuit.
9|||Hodram reacts to the call in confusion. This first puzzled sound is separate from his reaction to the pursuer.
13|||The man tells Hodram to take the item and use it however he likes. His hurried gift leaves its purpose unexplained.
16|||Hodram's wordless look of confusion buys a beat before the pursuer speaks. Keep the hesitation and question mark.
20|||The pursuer spots the man and yells for him to stop. Both short cries fit his sudden arrival.
23|||Hodram gives another puzzled reaction as the scene changes around him.
27|||The man takes off with a quick farewell. Its casual wording suits his opportunistic handoff.
31|||The pursuer repeats the command to stop. Repetition preserves the urgency of the chase.
35|||Hodram starts to call after them but trails off. The small unfinished reaction preserves his surprise.
39|||Charles asks what Hodram is doing as he comes upon the aftermath. The source address stays Admiral.
43|Someone shoved this into my hands...|into my hands...|Hodram says the item was thrust on him. The unfinished explanation preserves his bewilderment.
47|||Charles asks what the man passed to Hodram. The short question moves the exchange to the object itself.
51|Looks like a book.|Looks like a book.|Hodram tentatively identifies the object. The tentative phrasing gives Charles a reason to look more closely.
55|||Charles reads the established book title aloud. Keep his interest distinct from Hodram's initial guess.
58|Hmm. You might as well keep it.|might as well keep it.|Charles casually recommends keeping the gift. His motive becomes clearer when he asks to see it later.
61|||Hodram hesitates over the unsolicited gift. His unfinished objection sets up Charles's justification.
65|If someone gives you something, you might as well take it.|gives you something,;might as well take it.|Charles argues that a gift is worth accepting. The known situation keeps his maxim from sounding like unsolicited advice.
68|Oh, and let me have a look at it later, will you?|let me have a look;later, will you?|Charles adds his own request to read the book, revealing why he encouraged Hodram to keep it.
72|Ah. So that's what you're after.|what you're after.|Hodram sees the motive behind Charles's advice. The dry recognition closes the joke.
""",
    207: """
5|||Mikhail spots the unfamiliar object and blurts out a question. His alarm contrasts with Hodram's first reply.
9|||Hodram asks what Mikhail is looking at. The plain question hands the next turn back to Mikhail.
13|This, right here.|This, right here.|Mikhail points out the object again. Natural deictic phrasing suits the repetition and the visible discovery.
17|...A bug?|A bug?|Hodram offers a tentative identification. The pause and rising question leave room for Mikhail's observation.
21|But there's something like grass growing out of it.|something like grass;growing out of it.|Mikhail describes what he can see without identifying it as an actual plant.
24|||Hodram briefly agrees that the growth is there. The short response leaves room for the older man to identify it.
28|||The older man supplies the name caterpillar fungus. The established term preserves the cultural detail and answers the question.
31|||Mikhail's wordless surprise follows the unexpected voice and explanation. The punctuation preserves the beat.
35|It's prized as medicine in China.|prized as medicine;in China.|The older man describes how it is valued in China. Keep this as his account of its use.
38|||Hodram repeats the word medicine in surprise. The concise echo fits the preceding explanation.
42|||Mikhail mulls over the use as medicine. His trailing thought is less abrupt than Hodram's question.
46|||The older man confirms his explanation and offers the item. The casual generosity suits his delivery.
50|||Hodram asks what he is being offered. The next line separately identifies the book.
54|It's a book about all sorts of medicinal ingredients.|all sorts of;medicinal ingredients.|The older man describes a book covering a range of materials used in medicine. The wording keeps the scope broad.
57|We can't take it without giving you something for it.|take it without;something for it.|Hodram feels unable to accept the book for free. The ordinary phrasing leads naturally to his offer to pay.
61|||The older man says he no longer needs the book and repeats the gift. Preserve both the reason and the offer.
64|||Hodram still hesitates. The unfinished objection lets the older man draw Mikhail into the exchange.
68|Ho ho ho! Looks like your companion wants it.|your companion wants it.|The older man chuckles and notices Mikhail's interest. Companion preserves the neutral relationship in the source.
71|What? Oh... I only wanted to take a look at the book.|only wanted;take a look at the book.|Mikhail is caught wanting the book and admits his curiosity with a hesitant response.
75|||Hodram offers exactly 1,000 coins for the book. The courteous question suits the shift from a gift to a purchase.
78|Ho ho ho! Then 100 coins will do.|100 coins will do.|The older man laughs and asks for just 100 coins. His lower counteroffer completes the friendly negotiation.
81|||The notice grants the playable captain one point of Charm. Preserve the native name substitution and the stated amount.
""",
}

review = checked_text(previous.review, {"len(records) == 55": "len(records) == 86"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::inn-and-items", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
