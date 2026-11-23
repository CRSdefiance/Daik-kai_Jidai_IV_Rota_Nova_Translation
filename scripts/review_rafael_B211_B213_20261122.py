"""Review the complete Rafael portrait, inn rescue, and rope negotiation scenes."""

from collections import Counter
from types import FunctionType

from scripts import pair_rafael_B211_B220_20261122 as paired
from scripts import review_rafael_B177_B180_20261121 as precedent


base = paired.base
OUTPUT = paired.ROOT / "contextual_decisions_B211_B213_v3.json"
DECISIONS = {
    211: """
5|||Claudio calls Rafael over with the abrupt excitement of someone who has recognized the portrait.
9|||Rafael asks what to look at because he has yet to see what excites Claudio.
14|||Claudio points out the portrait without naming the man yet. Keep his impatient emphasis.
19|||Rafael asks who is in the portrait. Preserve his lack of recognition.
24|||Claudio cannot believe Rafael has never heard of the man. The reaction sets up his enthusiastic introduction.
28|||The blunt answer keeps Rafael's innocence and contrasts with Claudio's excitement.
33|||Keep Rocco Alemkel's established spelling and Claudio's explicit description of him as a legendary navigator.
37|||Rafael's flat acknowledgment deliberately undercuts Claudio's enthusiasm. The next reply quotes it.
42|||Claudio's incredulous repetition leads into the claim that Rocco helped sustain Portugal in its heyday. Keep this as Claudio's praise.
46|So he went to sea long before us.|went to sea long before us.|Rafael takes the legend to mean Rocco was a seafarer before their time. The connection creates no rank or personal tie.
51|||Claudio agrees and begins to add more just as the sound interrupts him.
55|||The speakerless caption reproduces the sudden clatter before anyone identifies the source.
59|||Claudio's pause makes the sudden sound a distinct interruption in the exchange.
63|Huh? Did it come from the portrait? Let's take a look.|Did it come from the portrait?;Let's take a look.|Rafael suspects the sound came from the portrait and proposes investigating. Preserve his uncertainty.
68|||Claudio agrees with a brief stammer after the unexplained sound.
72|||Rafael discovers the book behind the portrait. Keep the surprise and its exact location.
76|||Claudio speculates that Rocco might have written the book. The author is still unknown.
79|||Rafael agrees it is possible and makes a brief sound of effort as he handles the book.
83|Where are you going?||Claudio notices that Rafael is taking the book somewhere and asks where.
87|||Rafael explains that he intends to hand the book over to the innkeeper.
91|What?! You're giving it away? It could be the world's only copy!|You're giving it away?;the world's only copy!|Claudio objects in disbelief and treats the book as a possible one-of-a-kind copy.
95|Come on, of course I am. The portrait belongs to the inn.|The portrait belongs to the inn.|Rafael takes it as obvious that he should hand over a book found behind the inn's portrait.
99|||Claudio stammers and claims the innkeeper has no interest in such a book. It is his guess.
102|||Rafael rejects his reasoning bluntly and keeps his original intention.
107|...||Keep Claudio's pause as he looks for another tactic. Use the ordinary ASCII ellipsis.
111|||Claudio directs Rafael's attention elsewhere just before demanding the book.
115|||Rafael reacts to the apparent alarm and falls for the distraction.
120|||Claudio's short demand is timed to the grab.
124|||Rafael's sharp exclamation follows the grab immediately.
129|||Rafael recognizes what Claudio has done and calls out using his familiar name, Clau.
134|||The innkeeper checks on the disturbance without knowing about the book.
138|||Keep Rafael's halting response as he tries to pass off the disturbance.
142|||The innkeeper accepts the explanation without pressing for more.
146|||The innkeeper's invitation to make himself comfortable is ordinary courtesy to a guest.
150|||Rafael responds politely and thanks the innkeeper.
155|||Rafael lets out a breath and privately expresses frustration with Clau. Keep the inward aside.
""",
    212: """
5|||The speakerless thud signals that somebody fell before Carlo reacts.
9|||Carlo's short exclamation is an immediate startled reaction.
13|||The stranger groans after the fall. No words or identity are supplied.
17|||Carlo asks what happened and whether the stranger is all right. The urgency comes before the quieter inn scene.
21|||The stranger can only groan again before regaining awareness.
25|||Carlo greets the stranger's return to consciousness with a simple observation.
29|||The stranger's pause and question preserve confusion about where they are.
33|You're at the inn. You collapsed at the departure office, so I carried you here.|at the departure office,;carried you here.|Carlo identifies the inn, tells the stranger where they collapsed, and makes the physical act of carrying them explicit.
37|||The stranger acknowledges the explanation and apologizes politely for the trouble.
40|It was no trouble. You look awfully pale, though. You need to rest for a while.|You look awfully pale, though.;You need to rest for a while.|Carlo dismisses the inconvenience, then firmly advises rest because the stranger looks pale.
44|||Carlo prepares to leave and ends with a courteous wish for recovery.
47|||The stranger asks whether he is a doctor. The question supplies no credential.
50|||Carlo simply denies being a doctor, without supplying another title.
54|It's a small token of thanks. Please take it.|a small token of thanks.;Please take it.|The stranger offers an unnamed gift as a modest expression of thanks after learning Carlo is no doctor.
58|Really, there's no need.||Carlo turns down the offer out of courtesy and reassures the stranger again.
62|||The stranger explains why a refusal would leave them uneasy and asks him to accept.
65|Well, if you insist, I'll accept. Take good care of yourself.|if you insist, I'll accept.;Take good care of yourself.|Carlo accepts only after the stranger insists and returns to his concern about their recovery.
69|||The stranger promises to look after their health and closes with sincere thanks.
72|||The speakerless notice names Carlo and reports exactly one point of Charm.
""",
    213: """
5|||The trader claims the mast rope is badly worn. The diagnosis remains the opening sales claim.
8|||Rafael doubts the claim but leaves room for the trader to respond.
12|||The trader insists on the wear, offers his own rope and attributes the mysterious power to what people say.
15|||Rafael asks whether the offer is free before the trader mentions money.
19|N-no! I'll give you a good price. Let's say 300,000 gold?|give you a good price.;Let's say 300,000 gold?|The trader stammers at the idea of a free replacement, promises a deal and names the opening price.
22|||Carlo intervenes with a quick objection and addresses the admiral. The existing wrap keeps the whole question tag together.
25|Special or not, that's a ridiculous price for a mast rope. I'd say 30,000 gold, tops.|for a mast rope.;30,000 gold, tops.|Carlo acknowledges the claimed special quality for argument's sake and sets his initial counteroffer.
28|W-wait! It's one of a kind. How about 200,000 gold?|It's one of a kind.;How about 200,000 gold?|The trader stammers at the counteroffer, claims world uniqueness and comes down to 200,000.
31|||Carlo gives just his 50,000 counteroffer. The bare number makes his poker-faced delivery distinct.
35|Hmm... 150,000 gold. Give me a break here.|150,000 gold.;Give me a break here.|The trader lowers his price again and asks Carlo to give him some room.
38|||Carlo keeps his next counteroffer just as terse, this time at 75,000.
42|Fine, you win. 100,000 gold. I can't go any lower.|100,000 gold.;I can't go any lower.|The trader sounds worn down by the bargaining and presents 100,000 as his floor.
46|||Carlo judges the price reasonable and leaves the decision with the admiral.
860_0|||The first slot takes the final offer. Its direct label is clear after Carlo's question.
860_1|||The second slot passes on the final offer. The refusal branch still follows this slot.
60|||After acceptance Carlo volunteers to handle what remains of the purchase.
63|||Rafael acknowledges his help and leaves the follow-through to him.
73|||Carlo asks the trader to carry the rope to the deck. The familiar address creates no family relationship.
77|||The trader responds with a familiar business courtesy after the deal. It does not require a prior sale.
81|FI's Charm rose by 1!||The accepted deal raises the named captain's Charm by one. Keep the original substitution and keep the short notice consistent with the earlier bargaining scene.
84|||The accepted deal also raises Carlo's Wit by one. Preserve the exact fixed name and stat.
91|||Rafael declines because the existing rope is still usable, independently of whether the new price is fair.
97|||Carlo accepts Rafael's decision and undertakes to turn the trader down.
101|||The trader reacts in disbelief and accuses them of wasting his time after the drawn-out bargaining.
104|No, no. We're really sorry. Please forgive us.|We're really sorry.;Please forgive us.|Carlo acknowledges the inconvenience and appeals for forgiveness after the refusal.
107|FI's Spirit rose by 1!||The refusal increases the named captain's Spirit by one. Keep the original name token and the distinct outcome.
""",
}
WRAPS = {}


def main():
    packet, release = map(base.load, (paired.PAIRED, paired.parent.RELEASE))
    assert packet["release_proof_sha256"] == base.digest(paired.parent.RELEASE)
    assert packet["candidate_sha256"] == base.digest(paired.parent.ROM)
    names = {r["actor_ID"]: r["progressive_nameplate"]
             for r in base.load(precedent.prior.CATALOGUE)["source_and_current_default_name_fields"]}
    from_choices = FunctionType(precedent.from_choices.__code__, precedent.from_choices.__globals__ | dict(DECISIONS=DECISIONS))
    normalize = FunctionType(precedent.normalize.__code__, precedent.normalize.__globals__ | dict(WRAPS=WRAPS))
    records = []
    for group in packet["groups"]:
        if group["block"] in DECISIONS:
            records.extend(normalize(row, names) | dict(contextual_speaker=row["earlier_speaker"])
                           for row in from_choices(group))
    assert len(records) == 81 and len({r["id"] for r in records}) == 81
    assert sum(r["kind"] == "typed-choice-label" for r in records) == 2
    assert sum(r["kind"] == "system-FE" for r in records) == 6
    counts = Counter(r["change_class"] for r in records)
    assert not OUTPUT.exists()
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=["source", "context", "localization", "naturalness", "formatting"],
        previous_sha256=packet["candidate_sha256"], previous_registry_sha256=release["registry_sha256"],
        source_packet=str(paired.PAIRED), source_packet_sha256=base.digest(paired.PAIRED), records=records,
        findings=dict(counts), new_editorial_credit=0,
        status="Contextual review complete. Stored formatting, gameplay and release checks pending."))
    print(f"Reviewed {len(records)} records. {dict(counts)}")


if __name__ == "__main__":
    main()
