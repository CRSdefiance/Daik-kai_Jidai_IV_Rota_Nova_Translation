"""Record source-bound editorial decisions for both branches of the sailing lesson."""

from collections import Counter

from scripts import pair_rafael_B177_B180_20261121 as paired
from scripts.review_rafael_east_asia_followup_20261121 import TOKEN


base = paired.base
OUTPUT = paired.ROOT / "contextual_decisions_B180_v2.json"
DECISIONS = """
5|||The shipwright singles out the admiral and invites him to hear a sailing lesson in a casual voice.
8|||Rafael's brief surprise gives the shipwright space to explain why he asked.
13|||The shipwright admits he is bored and jokes that listening would be a kindness.
152_0|||The acceptance politely asks to hear the lesson, with no implication that Rafael already agreed to anything else.
152_1|||The player politely declines in the original second slot.
31|||Janus takes the refusal as confidence in their knowledge and tells the instructor not to underestimate them.
34|||Manuel gives a measured assent to Janus's comment.
46|We know our ships. We hardly need lessons now.||Cesare plainly shares the group's confidence, with a slightly formal insistence appropriate to how he speaks.
52|||The shipwright accepts the refusal, recognizes their experience, and jokes about waiting for a less experienced customer.
63|||The acceptance branch begins by praising Rafael's willingness to listen and predicting he will do well.
66|||The short maxim covers the source's observation that sails are essential to a sailing ship.
69|||The opening identifies square and lateen sails as the exact terms used in the lesson that follows.
72|||The description ties square sails to their crosswise rig without asserting that all crosswise sails have the same shape.
76|||The lesson gives both the configuration's downwind advantage and the limit on setting its angle upwind.
79|||The distinction between the name lateen and the triangular sail it describes stays clear. The nautical explanation contrasts lengthwise and crosswise rigs.
82|You can set a lateen at the ideal angle in a headwind. It won't give you much speed downwind. With me so far?|ideal angle;a headwind.;With me so far?|The shipwright gives the wind tradeoff for the lateen before checking whether the listeners are following.
85|||The transition marks a move from the main sail types to optional sails.
89|||The topsail gets its proper name, small square form, and place high on each mast.
93|||The definition locates the staysail ahead of the mast, then explains why it cannot be fitted ahead of a lateen.
96|||The shipwright gives the sailor's term spritsail, its crosswise position at the bow, and the ship-size limit.
99|||The jigger spanker's name, stern placement, orientation, and large-ship limit remain distinct. A little extra mast is the instructor's comparison.
102|Did you know ships with two masts or more go faster in a wind a bit off to one side than in one straight behind them?|two masts or more;a bit off to one side;straight behind them?|The instructor introduces the two-mast condition and asks about the slightly off-angle wind advantage in plain language.
106|||The shipwright addresses a listener directly and invites a reason before he supplies one.
110|||Manuel deduces the answer from the fore-and-aft arrangement of the masts and maintains his reserved phrasing.
113|||The instructor confirms that a wind from directly behind reaches the rearmost mast well and leaves the forward ones of little use in this example.
116|||The conclusion explains the best direction in the lesson and separately reminds the player to set the sails to match.
120|Ah, I see!||Janus has just understood the example. He responds with recognition instead of giving an order or confirmation.
132|||Cesare admits this is a detail he had overlooked, then says he now understands why it works.
139|||The shipwright thanks his listeners and says he is going back to work, closing the optional lesson.
"""


def main():
    packet = base.load(paired.PAIRED)
    assert packet["candidate_sha256"] == base.digest(paired.parent.ROM)
    assert packet["release_proof_sha256"] == base.digest(paired.parent.RELEASE)
    group, = [g for g in packet["groups"] if g["block"] == 180]
    entries = [line.split("|", 3) for line in DECISIONS.strip().splitlines()]
    records = []
    for row, (key, replacement, protected, reason) in zip(group["records"], entries, strict=True):
        choice = row["selector"] is None
        record_key = row["id"].split("CHOICE_", 1)[1] if choice else str(int(row["id"][-4:]))
        assert key == record_key
        old = " ".join(row["current_English"].split())
        english = replacement or old
        phrases = protected.split(";") if protected else []
        assert reason and all(phrase in english for phrase in phrases)
        assert TOKEN.findall(english) == TOKEN.findall(row["Japanese"]) == TOKEN.findall(old)
        records.append(row | dict(speaker=row["earlier_speaker"], source_meaning=row["earlier_source_meaning"],
            context=row["earlier_context"], kind="typed-choice-label" if choice else "progressive", previous_English=old,
            english=english, protected_phrases=phrases, localization_note=reason,
            decision="revision" if replacement else "retention",
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)))
    assert len(records) == 29 and sum(r["selector"] is None for r in records) == 2
    assert not OUTPUT.exists()
    counts = Counter(r["decision"] for r in records)
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", target_locale="en-US",
        candidate_sha256=packet["candidate_sha256"], paired_source=str(paired.PAIRED),
        paired_source_sha256=base.digest(paired.PAIRED), records=records, findings=dict(counts),
        status="Contextual review complete. Native formatting and registered integration pending."))
    print(f"Reviewed both branches of the optional sailing lesson. {dict(counts)}")


if __name__ == "__main__":
    main()
