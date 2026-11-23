"""Review the war notices, Escante and Hayreddin, and Sera's return."""

from collections import Counter

from scripts import review_hodram_B71_B74_20261122 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT, paired = prior.base, prior.ROOT, prior.paired
OUTPUT = ROOT / "B75_B80_contextual_v2.json"
COMBINED = ROOT / "B71_B80_contextual_v2.json"
GLYPHS = {"DK4_MES_B79_R0005"}
CONTEXTS = {
    75: "Maria has come to tell Hodram that the Ottoman navy is attacking. He is unusually direct in thanking her, then objects to the way she addresses him.",
    76: "Two speakerless notices report Escante's letter and declaration of war. Gerhard and Hodram discuss the betrayal and the time Escante gained while they fought Maldonado.",
    77: "Gerhard or Charles brings the king's request to fight. Each reads the same two passages, with ordinary speech around the formal letter.",
    78: "Escante's defeat exposes his plans for the New World. Separate event paths preserve his immediate threat and his bitter opening after defeat. Gerhard reacts to the danger and finds an object on him.",
    79: "Hodram arrives amid rumors of Hayreddin's defeat. The wounded pirate explains why he turned against Pasha, gives away the mark of allegiance, and parts with a blunt warning.",
    80: "Sera returns with people from her homeland to save Hodram. She helps the others leave, insists on remaining aboard, and tells him where to return after he defeats Pasha.",
}
DECISIONS = {
    75: """
25|||Maria uses the runtime surname in a deliberately familiar greeting. It gives Hodram a specific tone to object to later.
29|||Hodram is surprised she came this far and asks why. The existing warmth follows his recognition.
32|||Maria reports the Ottoman navy's major offensive for control of the Mediterranean. The existing sentence keeps the objective clear.
35|||Hodram's startled question follows the unexpected news and precedes his more considered response.
39|I doubt my country will be drawn into the war, but... did you come all this way to warn me?|drawn into the war,;come all this way;to warn me?|Hodram doubts the fighting will reach his country but asks whether Maria came this far on his account.
43|||Maria admits she owes him something. The existing phrasing keeps that acknowledgment casual.
47|||Hodram thanks her plainly for coming. His straightforward gratitude gives Maria a reason to be surprised.
51|(Oh? He's being awfully straightforward...)|being awfully straightforward...)|Maria thinks to herself that he is being unusually direct. Keep the thought in parentheses and the amused pause.
55|Just don't call me 'FA' like that...|'FA';like that...|Hodram objects to Maria's familiar address, using his runtime surname in the quoted phrase. His objection follows a sincere thank-you.
""",
    76: """
6|||The speakerless notice reports receipt of a letter from Escante. Its brief past tense is right for the arrival.
9|||The speakerless notice announces that Escante's forces have declared war. Keep the faction and exclamation.
27|||Hodram's personal suspicion of Escante is confirmed. The familiar idiom already carries his distrust.
40|So Escante betrayed us after all.|betrayed us after all.|Gerhard concludes that Escante betrayed them. The natural past tense keeps the conclusion concise.
43|I saw this coming when I heard what they were really like in a tavern. Still... we're at a serious disadvantage now.|what they were really like;in a tavern.;a serious disadvantage now.|Hodram remembers the tavern account of their true nature. He expected a betrayal and says it now puts his side at a disadvantage.
46|||Gerhard asks what Hodram means by their disadvantage, before Hodram explains the timing.
50|While we were fighting Maldonado, Escante was building up his wealth and power. He did it for a purpose of his own.|we were fighting Maldonado,;wealth and power.;for a purpose of his own.|Escante used the fighting with Maldonado to amass wealth and power for his own undisclosed objective.
53|What purpose? What is he after?|What is he after?|Gerhard presses for the objective after learning why the timing matters.
56|||Hodram says he can guess without revealing the answer. The trailing thought suits the exchange's end.
""",
    77: """
17|||Charles tells the admiral that the king has sent a request to take the field. The form of address and the official request both work.
23|||Hodram is surprised the letter came from the king and asks to hear it. The two questions fit the exchange.
33|Allow me... 'The Ottoman Empire has launched a major offensive. The Christian nations face unprecedented danger.'|launched a major offensive.;The Christian nations;unprecedented danger.'|Gerhard introduces the reading formally. The letter attributes the unprecedented danger to the Ottoman offensive and names the Christian nations it threatens.
36|'For the honor of our armed forces, meet the enemy. Fight to preserve peace in Europe and safeguard trade in the Mediterranean.' That is all.|our armed forces,;meet the enemy.;peace in Europe;safeguard trade;That is all.|Gerhard reads the king's charge to meet the enemy in defense of military honor and protect both European peace and safe Mediterranean trade. His spoken conclusion is outside the quote.
42|Here goes... 'The Ottoman Empire has launched a major offensive. The Christian nations face unprecedented danger.'|launched a major offensive.;The Christian nations;unprecedented danger.'|Charles has his own spoken introduction but reads the same official assessment as Gerhard.
45|'For the honor of our armed forces, meet the enemy. Fight to preserve peace in Europe and safeguard trade in the Mediterranean.' That's all.|our armed forces,;meet the enemy.;peace in Europe;safeguard trade;That's all.|Charles reads the same royal charge, with his own contracted sign-off outside the quote.
52|||Hodram says northern Europe is finally feeling the danger. The idiom carries his wry reaction to the king's call.
""",
    78: """
13|||Escante's initial growl is a speakerless signal of his fury. The existing phonetic growl fits the panel.
17|||Hodram's single exclamation reacts to the sudden sound before Escante speaks.
21|I-I was so close. My empire... I could have taken the New World! If it weren't for you...!|I-I was so close.;the New World!;If it weren't for you...!|Escante stammers over how close he thinks he came to taking the New World. His blame of Hodram caps the outburst.
24|||Hodram recognizes Escante and calls his name. The exclamation fits the sudden confrontation.
28|I'll never hand my empire over to you. Anyone but you... Die!|hand my empire over;Anyone but you...|Escante says Hodram is the last person he would give his empire to and makes the direct threat. His insistence reflects his own ambition.
34|||In the defeat exchange Escante initially addresses Hodram by surname with brittle civility. The existing greeting takes the right tone.
37|||Hodram answers with Escante's name and a pause. Keep his wary response.
41|Well played. You've beaten me completely.|Well played.;beaten me completely.|Escante congratulates Hodram and admits outright defeat. The brief courtesy comes before his fixation on what he almost took.
44|||Hodram lets the acknowledgment hang. Preserve the original standalone ellipsis.
48|Heh... Hehehe... I-I was so close. My empire... I could have taken the New World...|I-I was so close.;taken the New World...|Escante laughs uneasily and stammers over the same thwarted ambition. Preserve the pause into the next line of blame.
51|||Escante blames Hodram for spoiling his plan. The existing fragment is complete as an outburst.
55|||Hodram gives a wordless alarm. The two ASCII exclamation marks match the abrupt interruption.
62|||Gerhard calls out a warning to his admiral. The urgent plain English fits the sudden danger.
66|||Escante has a separate shocked reaction. Its two exclamation marks stay attached to his own speaker.
70|||Escante's strained cry has no clear words. Keep the existing sound in his voice.
74|G-guh... Am I going to die... here?|Am I going to die;here?|Escante struggles to ask if he is going to die here. His disbelief and stumbling breath stay audible.
77|||Escante utters one more sharp cry. The existing grunt ends his turn.
81|||Hodram's quiet pause separates the cries from Gerhard's concern.
85|||Gerhard asks if Hodram is safe and whether he is injured. Both questions remain urgent.
89|||Hodram confirms he is unhurt. His subdued response suits the pause before judging Escante.
93|Escante... What a pitiful man. Did you really think the people of the New World would take you for their king?|What a pitiful man.;the people of the New World;for their king?|Hodram asks if Escante actually believed the people of the New World would accept him as king. The change keeps the pity and the disbelief.
96|||Gerhard notices an unidentified item inside Escante's clothing. Keep the straightforward wording and the existing break before the location.
""",
    79: """
5|...?|...?|Hodram has a tentative wordless question before he asks about the commotion. The ellipsis and question mark use a consistent English glyph style.
10|||Hodram asks about the bustle in town. Keep his opening pause and spontaneous phrasing.
14|I hear the Ottoman navy thrashed Hayreddin. What's left of his pirate fleet is back, and the place is in an uproar.|the Ottoman navy;thrashed Hayreddin.;his pirate fleet;in an uproar.|The port worker reports hearsay about the pirate's defeat and attributes the commotion to the survivors returning.
17|Hayreddin lost?|Hayreddin lost?|Hodram is surprised that the defeated party was Hayreddin. The question echoes the substance of the report.
21|||The speakerless command clears the way. Its one sharp word suits the interruption.
26|||The port worker cries out in recognition and stammers Hayreddin's name. English formality stays in the reaction without adding a title.
29|||Hodram's original double exclamation marks the sudden appearance before an exchange of silence.
33|||Hayreddin first watches in silence. Keep his original two beats.
37|||Hodram's two silent beats are a separate response.
42|||Hayreddin assumes Hodram came to mock him. The existing wording preserves his wounded pride.
45|...You think everything's about you. I'm here on the king's orders to fight the Ottoman Empire.|everything's about you.;the king's orders;the Ottoman Empire.|Hodram tells Hayreddin he takes himself too seriously and states the king's order as his reason for being there.
53|||Hodram asks if the fleet wasn't allied with the Ottomans. The phrasing gives Hayreddin room to explain how the alliance failed.
57|||Hayreddin's silence precedes the explanation of Pasha's demand. Keep the two beats.
61|Pasha commands the Ottoman navy. He wanted our fleet in his offensive. We were allies, but he demanded I bow to him as his vassal.|commands the Ottoman navy.;in his offensive.;We were allies,;as his vassal.|Hayreddin identifies Pasha as the navy's commander and says the proposed incorporation of his pirate fleet came with a demand for personal submission despite their alliance.
64|My father and I worked hard to build that fleet. I wouldn't turn it over to the military. I rose against the Ottomans without hesitation...|My father and I;turn it over;to the military.;without hesitation...|Hayreddin recalls what he and his father put into the fleet and why he immediately rebelled against its incorporation.
67|It went well at first. They had the upper hand. I meant to hold out two or three years and show them the pride of Algiers' pirates.|the upper hand.;two or three years;Algiers' pirates.|Hayreddin says the rebellion initially went well. He intended to hold out for two or three years despite the odds and show his crew's pride.
71|Someone I trusted in my own crew betrayed me. Pasha's forces took us by surprise. Look at me now. Damn it... How can I face my father?|my own crew;by surprise.;Look at me now.;face my father?|He blames a trusted subordinate for betraying him, describes the surprise attack, and expresses shame about facing his father.
75|||Hodram answers with silence. Preserve the original pause after Hayreddin's confession.
79|||Hayreddin says there is no point in telling Hodram any more. The terse existing phrasing fits his pride.
83|Here, take it. That bastard Pasha sent it to mark me as his vassal. I can't stand the sight of it!|That bastard Pasha;as his vassal.;the sight of it!|Hayreddin gives away the unnamed object that was meant as the sign of his submission to Pasha. The insult and disgust remain his.
90|If you lose, at least try not to embarrass yourself.|If you lose,;embarrass yourself.|Hayreddin advises Hodram against a humiliating defeat. The barbed farewell leaves defeat conditional.
""",
    80: """
6|||Hodram catches sight of Sera and calls her name. Keep the double exclamation in this sudden reunion.
10|||Sera calls back to him by his runtime given name with the same urgency.
14|||Hodram's first question is why she is there. The existing punctuation keeps his shock.
18|FI... You were in danger. I heard. My people came with me... to help the king from the legend.|You were in danger.;My people came with me...;the king from the legend.|Sera explains in short beats that she heard of the danger and came with compatriots to help the legendary king. Keep Hodram's controlled given name.
22|||Hodram acknowledges they saved his life and apologizes to everyone. The pause lets him address the group.
26|||Sirwood calls Hodram by his given name and follows it with the same untranslated script he shares with Sera. Retain the exact source-aligned symbol run and the punctuation joining it to the name.
29|Thank you. All of you. Now get out of here, quick. The Ottoman forces won't let this go.|All of you.;get out of here, quick.;won't let this go.|Hodram thanks the group and urges them to flee immediately because the Ottomans will act. The warning stops short of inventing what they will do.
33|||Sera acknowledges Hodram before switching languages to speak with the others.
37|||Sera's five original circle and cross symbols are an untranslated message to her group. Keep the exact sequence and exclamation.
41|||Sirwood answers with a shorter opaque sequence. Preserve the exact symbols and his own speaker control.
45|||Sera reports that the others are leaving. Her existing plain voice connects the unintelligible exchange to Hodram's reply.
49|||Hodram tells Sera she should flee as well. The short instruction makes her later refusal clear.
53|||Sera's pause before answering is deliberate. Preserve the original standalone ellipsis.
57|What's wrong? Come on, hurry.|Come on, hurry.|Hodram notices Sera hasn't moved and presses her to hurry. He doesn't yet know she plans to stay.
61|||Sera refuses to leave in a short sentence. Its simplicity gives the refusal force.
65|What?|What?|Hodram directly reacts to the refusal before she explains where she intends to stay.
69|||Sera says she is staying with him and uses the given-name substitution as the source does. The phrasing suits her plain expression.
72|||Hodram doesn't understand what she is proposing. Keep the direct question and his separate response.
76|||Sera specifies that she means to come aboard. The brief wording keeps her resolve.
83|FI, you'll be king of the seas. I want to see it.|you'll be king of the seas.;I want to see it.|Sera confidently says Hodram will become king of the seas and wants to see it happen. This echoes the earlier farewell.
86|||Hodram rejects the idea and tells her to go home. The pause keeps his reluctance audible.
90|||Sera has already made her decision. The simple existing wording closes the argument on her terms.
94|||Hodram gives her a long silent look before relenting. Preserve its two native ellipsis glyphs.
98|||Hodram calls her stubborn and finally lets her decide. The existing sigh and grudging concession work.
101|||Sera calls him by given name alone to get his attention after he relents.
105|What is it?|What is it?|Hodram asks what she wants to say. The simple question gives her room to pass on a request.
109|||Sera asks him to return to the same town after defeating Pasha. The wording keeps the event as a condition.
112|||Hodram repeats her destination in surprise before she supplies the more specific place.
116|||Sera confirms the town and adds the king's tomb. The incomplete turn leaves Hodram room to ask.
119|||Hodram wonders whether the tomb is the pyramid and asks what she means. Keep the clarification tentative.
123|||Sera says he will understand if he goes. The pause and laconic answer leave the reason for the visit open.
""",
}

review = checked_text(prior.review, {"len(records) == 41": "len(records) == 99"})
scope = prior.scope | globals()
exec(compile(review, __file__ + "::contextual-review", "exec"), scope)


def combine():
    earlier, following = map(base.load, (prior.OUTPUT, OUTPUT))
    for field in ("previous_sha256", "source_packet_sha256", "prior_contextual_receipt_sha256", "review_gates"):
        assert earlier[field] == following[field]
    records = earlier["records"] + following["records"]
    assert len(records) == len({r["id"] for r in records}) == 140
    combined = earlier | dict(records=records, findings=dict(Counter(r["change_class"] for r in records)),
                              prior_hangzhou_draft=str(prior.OUTPUT), prior_hangzhou_sha256=base.digest(prior.OUTPUT))
    base.save(COMBINED, combined)


if __name__ == "__main__":
    scope["main"]()
    combine()
