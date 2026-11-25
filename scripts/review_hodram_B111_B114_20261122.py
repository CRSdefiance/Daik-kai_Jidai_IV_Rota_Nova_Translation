"""Review all Santiago, temple and Sphinx exchanges in source order."""

from scripts import pair_hodram_B111_B130_20261122 as paired
from scripts import review_hodram_B91_B93_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = previous.base, paired.ROOT
OUTPUT = ROOT / "B111_B114_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    111: "A woman stops the crew in Seville to tell them about a well-known pilgrimage destination. She offers directions.",
    112: "The priest gives the pilgrims crosses. Hodram notices his looks old but keeps the thought to himself as the priest begins a prayer.",
    113: "The lookout's call changes with the original speaker style. A temple voice answers the party's surprise with an offer and an invitation to debate.",
    114: "The Sphinx asks a familiar riddle, then a second one that uses the first answer as a misdirection. Its rebukes and the crew's startled reactions recur on separate branches.",
}
DECISIONS = {
    111: """
7|||Her brief call gets the crew's attention and asks if they have visited Santiago Cathedral before.
11|||The crew's wordless question lets her explain why she brought up the cathedral. The source CF voice selector stays dynamic.
15|||The long-standing pilgrimage tradition and the cathedral's fame explain her recommendation. The English keeps both without adding a date or rank.
19|Why not go while you're in Seville? I can give you directions.|while you're in Seville?;give you directions.|She suggests a visit while they're in Seville and offers to tell them the way. Her offer leaves the crew to make their own way.
""",
    112: """
5|You're here on pilgrimage, I take it? Please, take one of these crosses to remember your visit.|here on pilgrimage;one of these crosses;remember your visit.|The priest checks that they are pilgrims and offers each of them a cross as a memento. His welcome stays warm and formal.
9|||Hodram notices something before the priest asks what is wrong. The brief spoken reaction gives no explanation away.
13|||The priest politely asks what is the matter. The reply fits his concern without implying he knows what Hodram saw.
17|No... It's nothing. (This is the only cross that looks ancient...)|It's nothing.;looks ancient...)|Hodram dismisses the question aloud. His private thought singles out this cross as unusually old. The parentheses preserve the change in audience.
21|||The current Catholic formula, including Holy Spirit and Amen, fits the priest's formal blessing and retains the original pause.
""",
    113: """
SC1_B113_STYLE_10_0|||The polite ordinary variant calls for the admiral to look. Preserve the wording in both source slots that share this line.
SC1_B113_STYLE_10_28|||The direct version removes the politeness marker and uses a shorter call. Both source slots share it.
SC1_B113_STYLE_10_48|||The familiar variant's idiomatic take a look keeps its casual request without adding familiarity beyond the situation.
SC1_B113_STYLE_10_74|||Have a look is an easy, familiar prompting variant. Preserve the different cadence and the single owner slot.
SC1_B113_STYLE_10_100|||Calling Admiral as its own exclamation carries the stretched address in the Japanese without stylizing the honorific.
SC1_B113_STYLE_10_126|||Do take a look gives this variant a touch of ceremony suited to the original older request form.
29|||The temple voice addresses its visitors directly. The ceremonial opening suits its subsequent offer of power.
33|||The separate startled reaction belongs to the runtime-selected crew voice. Keep both exclamation marks and the dynamic selector.
37|||The speaker promises to lend its power and invites vigorous debate. To your heart's content preserves the invitation's expansiveness.
""",
    114: """
5|||Hodram's short remark conveys his initial awe and gives the Sphinx room to interrupt.
10|||The direct command puts the Sphinx in charge of the exchange. The existing line establishes its formal authority.
14|||The silent question keeps Hodram's reaction separate before the Sphinx poses its riddle.
21|||The traditional riddle keeps the exact sequence of four, two and three legs and its animal premise.
SC1_B114_CHOICE_154_0|||The first answer affirms familiarity and leads to the follow-up question about the animal.
SC1_B114_CHOICE_154_1|||The second answer admits ignorance in the player's voice and keeps its separate fail branch.
SC1_B114_CHOICE_154_2|||The third answer denies the premise. The contraction is natural beside the two shorter answers.
44|||Begone and fool fit the Sphinx's heightened register on the ignorance branch.
48|||The startled cry follows the rejection on this path. Keep the utterance and the dynamic voice.
60|||The same rebuke follows denying the premise. Keep this independent instance in its own branch.
64|||The matching cry follows the separate denial path and keeps the original timing.
77|||The follow-up asks the player to name the animal after they say they know the answer.
SC1_B114_CHOICE_392_0|||Humans works as a concise answer. The Japanese parenthesis clarifies that the crew means people.
SC1_B114_CHOICE_392_1|||The wrong answer explicitly identifies the Sphinx as the addressee and preserves the joke.
SC1_B114_CHOICE_392_2|||The generic alternative reads naturally and preserves the third native slot.
100|||The Sphinx repeats its rebuke when named as the answer. The repeated formula belongs to the response.
104|||The matching alarm remains separate from the other wrong-answer branches.
116|||The familiar rebuke follows the catch-all answer here. Leave its command independent.
120|||The second answer's other failure route ends with the same distinct alarm.
133|||The Sphinx calls its first riddle worn out and requests another answer. The short pause keeps its dismissive voice.
136|||The puzzle keeps 12 people, 32 hands and feet and two canes. Their irrelevance is revealed only after the player answers.
SC1_B114_CHOICE_782_0|||The first numeric response stands for three babies and keeps its original menu position.
SC1_B114_CHOICE_782_1|||The second numeric response stands for four babies and preserves the original correct branch.
SC1_B114_CHOICE_782_2|||The third numeric response stands for five babies and keeps its wrong-answer branch.
156|||The rejection repeats if the player chooses three. This matches the Sphinx's earlier judgments.
160|||The separate short cry stays after the answer three is rejected.
174|||The same rebuke follows the answer five. Preserve the exact separate branch response.
178|||The matching alarm closes the wrong answer five, with the same deliberate repetition.
191|||Gerhard repeats the number of canes and draws the tempting inference about two elderly people. He holds it as a question.
197|We know how many hands and feet are on the floor. The canes don't matter. Older people still have two feet.|hands and feet;The canes don't matter.;have two feet.|Hodram separates the known count from the canes and explains why age does not change the two-feet count.
200|||Gerhard accepts the correction and says the earlier three-legged riddle misled him. The English keeps his rueful realization.
204|Twelve people have 24 feet. That leaves eight hands on the floor. So there are four babies.|have 24 feet.;eight hands;four babies.|Hodram subtracts the feet from the total and reasons from the eight remaining hands to four babies. The answer follows his explanation naturally.
210|||The Sphinx praises the solver and presents a reward without naming the object in this line.
""",
}
review = checked_text(previous.review, {
    "len(records) == 58": "len(records) == 51",
})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::Santiago-and-Sphinx", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

