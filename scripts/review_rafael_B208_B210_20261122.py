"""Review the complete bargaining, book-seller, and Namahage encounters."""

from collections import Counter
from types import FunctionType

from scripts import pair_rafael_B201_B220_20261122 as paired
from scripts import review_rafael_B177_B180_20261121 as precedent


base = paired.base
OUTPUT = paired.ROOT / "contextual_decisions_B208_B210_v4.json"
DECISIONS = {
    208: """
5|You've got money, don't you? Heh heh heh...|Heh heh heh...|The seller sizes up Rafael as someone with money. Keep his wheedling opener and telltale laugh.
8|...||Rafael waits to hear the pitch. Use the ASCII pause.
13|I've got something good for you. How about 200,000 gold? Heh heh heh...|200,000 gold?;Heh heh heh...|Keep the item undisclosed, the opening price exact, and the seller's amusement audible.
25|||Fernando objects to the inflated price without claiming to know what is for sale.
218_0|||The first slot accepts the opening price. The short direct label matches the action.
218_1|||The second slot refuses this offer. The bargaining continues in the next beat.
43|||The seller praises the buyer's generosity at his highest price and makes a vague promise about the item.
46|FI's Charm rose by 1!||The purchase raises the named captain's Charm by one. Keep the name token and stat intact. The wording keeps the complete stat notice on one line at the maximum supported name width.
65|All right. How about 100,000 gold? Heh heh heh...|100,000 gold?;Heh heh heh...|After one refusal the seller drops to exactly half his opening price. Use the established gold wording and keep the laugh together.
77|(Admiral, after one refusal, he cut the price in half. He was asking way too much. We can get at least two more cuts.)|after one refusal,;cut the price in half.;He was asking way too much.;at least two more cuts.|Carlo addresses the admiral privately, draws the inference from the immediate drop, and predicts at least two more concessions.
582_0|||The first slot takes the 100,000-coin offer.
582_1|||The second slot refuses the 100,000-coin offer and continues negotiating.
95|||The seller compliments Rafael's bargaining after the first discount and repeats his vague promise.
111|Well then, how about 70,000 gold? Heh heh heh...|70,000 gold?;Heh heh heh...|Preserve this second price drop, the established gold wording and the repeated laugh.
122|||Fernando makes his private suggestion conditional. He would try exactly one more time.
832_0|||The first slot takes the 70,000-coin offer.
832_1|||The second slot refuses the 70,000-coin offer.
140|||The seller hands over the item, repeats its possible use, and laughs.
157|You're tighter with your money than I thought. How about 50,000 gold? Heh heh.|50,000 gold?;Heh heh.|The seller voices his growing surprise at the buyer's frugality. His laugh shortens as his price drops.
175|(I'd hold out one more time.)|hold out one more time.|Julio's private advice is brief and personal. It keeps the single further refusal.
183|(Let's get him to go even lower!)|go even lower!|Yifa urges another concession with the eagerness of someone enjoying the bargaining.
1156_0|||The first slot accepts the 50,000-coin offer.
1156_1|||The second slot passes on this offer. The seller tries again.
202|||The seller praises Rafael's skill and hands over the unnamed item after the longer negotiation.
218|40,000 gold... Heh.|40,000 gold...|Keep the exact offer, the established currency word, the hesitation and the seller's much shorter laugh.
229|||Carlo tentatively says the offer may now be worth taking. Preserve the advice in a private aside.
1370_0|||The first slot accepts the 40,000-coin offer.
1370_1|||The second slot passes on the 40,000-coin offer.
248|||The seller sounds relieved that Rafael is buying after a series of refusals. He hands over the item.
264|Please, just buy it. 30,000 gold.|30,000 gold.|The seller now pleads instead of laughing and offers the last price. Keep the established currency word with the number.
275|||Julio gives his judgment that they have reached the seller's floor.
1588_0|||The first slot accepts the final 30,000-coin offer.
1588_1|||The second slot refuses the final offer and ends this negotiation.
294|Tch. I practically gave it away. At least take good care of it.|take good care of it.|The seller grumbles at the final price and tells the buyer to look after what he bought.
310|Hmph! You wouldn't know a good deal if you saw one!|a good deal|When the sale fails, the seller blames Rafael's judgment. Keep the sting of the retort before he walks away.
314|||The seller gives up and says he will find another buyer.
""",
    209: """
5|||The woman opens by calling Ian handsome. Keep the teasing approach before she makes her pitch.
9|||Ian asks if she means him. His quick question gives her room to make the offer.
14|||The conversational sales pitch already gives the exact asking price and the established gold currency.
17|||Ian asks about the book before deciding whether to buy it.
21|||The sales pitch keeps both figures from the familiar tale, their romance and the book's Indian origin.
24|||Ian asks for the admiral's decision. Preserve his deference before the menu.
230_0|||The first choice buys the book. Keep the direct verb.
230_1|||The second choice turns down the sale.
230_2|||The third leaves the decision to Ian, who has just asked. The brief label addresses him directly.
45|||Ian accepts the sale politely in his own voice.
49|||She wishes Ian a romance like the one in the book. The line also sets up the alternate ending.
53|||Ian politely disclaims interest in the proposed romance after he has bought the book.
57|||She calls that a shame and repeats the compliment, sticking with the playful voice of her first line.
65|||Ian refuses with the courtesy he showed when he asked about the book.
69|||She accepts the refusal and says she will offer it to somebody else.
75|||If Ian lacks the funds, he says he would like to buy it but cannot afford that much.
78|||She absorbs his explanation before he apologizes and she gives him the book.
82|||Ian apologizes for being unable to meet her expectations.
86|||She offers to give him the book outright, reversing the negotiation on this branch.
90|||Ian's sharp surprise breaks his usual composure at the gift.
94|||Her brief laugh and wish for a romance with someone like Ian echo the book's plot and her opening compliment.
98|||Ian falters at her sudden disappearance. Keep the observation at what he experiences.
102|||He briefly considers whether she was a celestial maiden before dismissing his own speculation.
110|||The native notice raises Ian's Charm by one. Keep the approved stat label and his explicit given name.
""",
    210: """
10|||The unseen voice starts its repeated question about badly behaved children. Keep the cadence of the two calls.
14|||The same question repeats verbatim as the encounter continues. Do not vary the repeated formula.
18|||The voice turns its question directly on Yukihisa. Keeping the repeated term carries the ritual rhythm forward.
22|Who's there?!||Yukihisa is startled and calls out for the unseen speaker's identity.
26|||The voice repeats its question, leaving the identity for Yukihisa to infer.
30|||Yukihisa recognizes a namahage. Preserve the cultural term and his pause before recognition.
34|||The voice persists without introducing itself. Keep the third identical directed question.
38|||Yukihisa says he recalls no wrongdoing. His measured denial answers the repeated question.
42|||The unseen voice responds tersely and trails away without explaining the encounter.
49|......||Keep the longer silence as the voice vanishes. Use six ordinary periods for the two source ellipses.
53|||Yukihisa takes it for a dream at this point, before the discovery makes him reconsider.
65|||Angelo's loud alarm abruptly breaks the quiet.
72|||Yukihisa reacts with a short startled interjection before looking.
76|......||Keep the second long wordless reaction as he sees the object. Use matching ASCII punctuation.
80|Strange things do happen.||Yukihisa calmly acknowledges what he sees without explaining what happened.
84|||He says he will give the object to the admiral the next morning. His decision follows the discovery.
95|||Angelo still has no answer and presses him to explain what the object is. Keep the interruption and comic frustration.
""",
}


def main():
    packet = base.load(paired.PAIRED)
    release = base.load(paired.parent.RELEASE)
    assert packet["release_proof_sha256"] == base.digest(paired.parent.RELEASE)
    assert packet["candidate_sha256"] == base.digest(paired.parent.ROM)
    names = {r["actor_ID"]: r["progressive_nameplate"]
             for r in base.load(precedent.prior.CATALOGUE)["source_and_current_default_name_fields"]}
    finding_scope = precedent.from_choices.__globals__ | dict(DECISIONS=DECISIONS)
    from_choices = FunctionType(precedent.from_choices.__code__, finding_scope)
    normalization_scope = precedent.normalize.__globals__ | dict(WRAPS={})
    normalize = FunctionType(precedent.normalize.__code__, normalization_scope)
    records = []
    for group in packet["groups"]:
        if group["block"] not in DECISIONS:
            continue
        for row in from_choices(group):
            item = normalize(row, names)
            item["contextual_speaker"] = row["earlier_speaker"]
            if row["previous_English"] == "……" and row["english"] == "......":
                item["change_class"] = "glyph"
            records.append(item)
    assert len(records) == 77
    assert sum(r["kind"] == "typed-choice-label" for r in records) == 15
    assert sum(r["kind"] == "system-FE" for r in records) == 8
    assert len({r["id"] for r in records}) == len(records)
    counts = Counter(r["change_class"] for r in records)
    assert not OUTPUT.exists()
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=["source", "context", "localization", "naturalness", "formatting"],
        previous_sha256=packet["candidate_sha256"], previous_registry_sha256=release["registry_sha256"],
        source_packet=str(paired.PAIRED), source_packet_sha256=base.digest(paired.PAIRED),
        records=records, findings=dict(counts), new_editorial_credit=0,
        status="Contextual review complete. Stored formatting, gameplay and release checks pending."))
    print(f"Reviewed {len(records)} records. {dict(counts)}")


if __name__ == "__main__":
    main()
