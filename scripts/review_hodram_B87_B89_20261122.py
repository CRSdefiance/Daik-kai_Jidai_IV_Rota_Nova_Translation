"""Review Janus and Yukihisa's recruitment and the Silla Gold Crown."""

from collections import Counter

from scripts import review_hodram_B81_B84_20261122 as first
from scripts import review_hodram_B85_B86_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT, paired = previous.base, previous.ROOT, previous.paired
OUTPUT = ROOT / "B87_B89_contextual_v1.json"
COMBINED = ROOT / "B81_B89_contextual_v3.json"
GLYPHS = set()
CONTEXTS = {
    87: "Janus asks to join and requests 1,000 gold. The player can accept or decline. After accepting and waiting a day, Hodram learns the money paid for repairs and that Janus was testing him. A speakerless reminder gives the docking and Refit instructions.",
    88: "Gerhard and Charles react to chopsticks. Kurushima and his men stage a collision and demand a fight. Yukihisa intervenes on his own judgment and asks to sail with Hodram to see the world.",
    89: "Hodram finds the Silla Gold Crown ahead of Julian, who wanted it for Mihwa. Julian asks for it and Hodram lets him take it. Gerhard starts to identify Hodram to Julian, who has already left.",
}

DECISIONS = {
    87: """
5|||Janus acknowledges that he's approaching Hodram without warning. Keep the pause before he makes the request.
9|||Hodram waits for him to say what he wants. The short sound suits the opening.
14|||Janus politely asks whether Hodram would hire him. The current question gets straight to the request.
23|||Hodram asks what terms Janus wants, leading directly into the amount.
27|...Then I have one favor to ask. Could you give me 1,000 gold?|one favor to ask.;1,000 gold?|Janus frames the request as a favor and specifies exactly 1,000 gold. Keep the currency and amount unchanged.
SC1_B87_CHOICE_302_0|||Agreed is a clear acceptance of the price at the original first choice. Keep its wording and position.
SC1_B87_CHOICE_302_1|||The second choice declines for lack of that much money. Keep the direct caption and original answer order.
42|||Janus thanks Hodram and says he can finally get the repair done. His excited aside precedes his explanation.
45|Oh, sorry. Could you hold off sailing for just one day?|hold off sailing;for just one day?|Janus corrects himself and asks Hodram to delay departure exactly one day.
48|||Janus gives the port office as the meeting spot on the following day. The existing farewell keeps both details.
55|||Janus says he's been waiting and invites Hodram to see what he wants to show him. His excited welcome works.
58|||Hodram reacts without words to seeing the ship. Keep the single regular exclamation.
62|Thanks to the money you gave me yesterday, the ship's repaired and my debts are paid.|money you gave me yesterday,;my debts are paid.|Janus says the previous day's payment let him finish repairs and repay his debts. Both tasks are complete by this visit.
66|Sorry for testing you like that. If I'm putting my life in an admiral's hands, I want to know what they're made of.|testing you like that.;an admiral's hands,;what they're made of.|Janus apologizes for testing him and explains why he needs to assess the admiral he would trust with his life.
69|||Janus expresses that trust and offers Hodram use of the ship. Keep the voluntary offer.
72|||Hodram asks for a name, leaving just enough ambiguity about whose name for Janus's reply.
76|||Janus assumes he means the ship and gives him permission to name it. The existing question preserves the misunderstanding.
80|I meant yours. You still haven't told me your name.|I meant yours.;told me your name.|Hodram clarifies that he means Janus's name. The direct correction pays off the misunderstanding.
83|||Janus apologizes and explains that he was too excited the previous day to introduce himself.
87|||Janus gives the approved Janus Pasar and expresses his wish to sail with Hodram. The spelling matches the native nameplate.
93|||The speakerless instruction says to take the ship out of the dock before choosing Refit to name it. The sequence and approved menu term are already present.
98|||On refusal Janus accepts the result and says he will try someone else. The existing line does not imply he has been hired.
101|||Hodram leaves the refusal branch with a silent beat. Preserve the single native ellipsis.
""",
    88: """
5|So this is Japan... Things are certainly different here.|So this is Japan...;different here.|Hodram is struck by how unfamiliar the country feels to him. The judgment comes from the visitor's viewpoint.
8|||Gerhard calls Hodram by the runtime given name and points out a man eating with two sticks. Keep his amazement.
19|||Charles supplies the ordinary term chopsticks as something he has heard. The plain name answers Gerhard.
22|||Gerhard reacts with continued surprise. The existing short line stays in his voice.
29|||Kurushima calls out to the outsiders in a rough, challenging way. You lot conveys the contempt without inventing an epithet.
32|||Kurushima claims the visitors have been throwing their weight around in Japan. The accusation and end challenge fit his rough voice.
36|||Hodram observes warily that they seem to want something. The line does not guess their plan.
40|||Gerhard agrees in a few words. Keep his hesitation as they approach.
52|||Charles stammers as the men come close. The short reaction fits his unease rather than making him more assertive.
59|Ow, ow! It hurts, boss!|It hurts, boss!|Kurushima's follower exaggerates his pain and addresses him by role. Keep the repeated cry that starts the performance.
63|||Kurushima theatrically claims the visitors hit his man on purpose and broke his bones. This is his accusation, with no independent confirmation of injury.
67|||Hodram catches the ruse and reacts without speech. Keep the original pause and exclamation.
71|Nonsense! You're the ones who bumped into us!|You're the ones;who bumped into us!|Gerhard rejects their accusation and says who actually bumped into whom. The sharp wording fits the argument.
82|||Charles backs Gerhard up immediately. The emphatic reply works without repeating the claim.
97|||The follower answers Kurushima's command. The brief assent preserves the response to his boss.
102|||Hodram sees the other group has quite a few people. His concern prepares for Charles's admission.
114|||Charles stammers that he can't fight. Keep the reluctance in his own voice.
121|FI and I are more than enough for this rabble.|more than enough;for this rabble.|Gerhard boasts that the two of them are more than enough against the group. Retain the runtime given name and his confidence.
125|Allow me to help!|Allow me to help!|Yukihisa announces his aid in a formal register. The line sounds immediate without dropping his courtesy.
129|||Hodram's three question marks express a silent, sharply puzzled reaction. The original English glyphs already work.
136|||Yukihisa tells Hodram to leave it to him. His quiet pause and short instruction fit the intervention.
140|||The follower challenges a samurai for siding with foreigners. The current question keeps his outrage and the stated role.
144|||Yukihisa insists right and wrong are for him to judge. The formality fits the way he stands apart from either group.
148|||Kurushima calls him insolent and orders his men to act. The two sharp commands support his authority over them.
152|||The follower responds at once to the order. Keep his separate turn.
157|||The follower cries out as Yukihisa strikes. The existing sound conveys surprise without inventing a wound.
161|He got me!|He got me!|The follower groans that he has been beaten. Natural informal English suits his earlier voice.
165|||Kurushima leaves with a threat of payback. The existing wording gives his retreat a clear close.
169|||Yukihisa says he struck with the back of his blade and did not cut the men. Keep the exact distinction.
173|Remarkable... I didn't expect to find someone like you in this island nation.|didn't expect;in this island nation.|Hodram is surprised to encounter someone of his skill in Japan. The line expresses his own earlier expectations.
177|I'm astonished too. That swordplay was extraordinary.|I'm astonished too.;swordplay was extraordinary.|Gerhard shares Hodram's surprise and specifically praises Yukihisa's handling of the sword.
188|||Charles says the speed seems scientifically impossible. The analytical wording distinguishes his voice from Gerhard's.
195|||Yukihisa apologizes formally for what they have seen of his country. The existing apology carries his embarrassment.
198|We're the ones who owe you a bow. You saved us. Thank you.|owe you a bow.;You saved us.|Hodram returns the courtesy, acknowledges the help, and thanks him. Keep the reference to bowing as part of the exchange.
201|||Yukihisa respectfully ventures that they are people who sail all over the world. The conditional phrasing gives him room to ask a favor.
204|||Yukihisa asks if he may travel with them. The polite direct request fits his approach.
207|||He says he wants to see the world. The concise phrasing gives his aspiration weight.
210|||Hodram warns that he may never return to Japan. Keep it as a possibility rather than a condition of joining.
214|||Yukihisa has no intention of returning. His statement about testing himself as a man reflects his stated ambition and historical voice.
217|||Hodram approves the ambition, gives both controlled names, and accepts him in a warm closing. The wording already works.
221|||Yukihisa introduces himself by the full approved Yukihisa Genjo Shiraki. Keep his own name distinct from the short nameplate.
""",
    89: """
11|||Gerhard recognizes the Silla Gold Crown. Keep the approved item name and the pause of recognition.
15|||Hodram remarks on both the weight of its presence and its grace. The two qualities come through naturally.
19|||Gerhard says he can see the appeal even as someone outside the group he expected to want it. The existing wording preserves his stated assumption.
24|||Julian stammers at seeing what Hodram is holding. His unfinished thought leaves Hodram to name him first.
28|You... Julian, was it? You had a head start, but it looks like you got here a little late.|Julian, was it?;had a head start,;a little late.|Hodram recognizes Julian, says he set out first, and observes he arrived just too late.
32|||Julian asks who Hodram is and whether they have met. The brief questions fit his confusion.
35|||Hodram gives his runtime given name and says he heard Julian mention the Silla Gold Crown in the Hangzhou tavern. All particulars are already present.
39|||Hodram says the conversation made him curious enough to look for the crown himself. The existing admission explains why he was there.
43|||Julian takes the loss personally and says the crown was meant as a gift for her. The stammer and unfinished reaction fit.
47|||Hodram is silent before Julian explains why the loss matters so much to him.
51|||Julian worries he will lose face with Mihwa and asks for the crown. The existing words keep his distress and her name.
55|||Gerhard leaves the decision to Hodram. The quiet question is appropriate before his decision.
59|||Hodram agrees to give it up in his usual measured voice.
63|||Julian checks in surprise that Hodram really means it. The short question suits his disbelief.
67|||Hodram offers the crown, says the sailors have no use for it, and lets Julian say he found it himself. Gather dust carries the original idea of letting a treasure go unused.
70|||Julian praises Hodram, promises to repay him someday, and takes his leave in his excitement.
77|||Gerhard starts to introduce Hodram on behalf of the runtime fleet. The unfinished possessive preserves the interruption.
80|He's gone already. I'd like a chance to sit down and talk if we run into him again.|He's gone already.;sit down and talk;run into him again.|Hodram notes Julian has already left and would like a more leisurely conversation if they meet again.
""",
}

review = checked_text(previous.review, {"len(records) == 139": "len(records) == 82"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::contextual-review", "exec"), scope)


def combine():
    drafts = [(mod.OUTPUT, base.load(mod.OUTPUT)) for mod in (first, previous)]
    drafts.append((OUTPUT, base.load(OUTPUT)))
    first_draft = drafts[0][1]
    for _, draft in drafts[1:]:
        for key in ("previous_sha256", "source_packet_sha256", "prior_contextual_receipt_sha256", "review_gates"):
            assert first_draft[key] == draft[key]
    records = [row for _, draft in drafts for row in draft["records"]]
    assert len(records) == len({r["id"] for r in records}) == 297
    report = first_draft | dict(records=records, findings=dict(Counter(r["change_class"] for r in records)),
        component_manuscripts={str(path): base.digest(path) for path, _ in drafts})
    base.save(COMBINED, report)
    print("Combined the 297 contextual decisions.", report["findings"])


if __name__ == "__main__":
    scope["main"]()
    combine()
