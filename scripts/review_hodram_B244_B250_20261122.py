"""Review ruins hints and the guild survey exchange across Hodram B244 through B250."""

from scripts import pair_hodram_B241_B260_20261122 as paired
from scripts import review_hodram_B243_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = paired.base, paired.ROOT
OUTPUT = ROOT / "B244_B250_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    244: "A hostess welcomes the returning captain and repeats a sailor's story about a river that carries gold dust. She is taken with the image.",
    245: "A hostess greets the captain and assumes an interest in ancient civilizations. She points out a nearby ruin on a visible hill.",
    246: "A hostess asks whether the captain has seen the pyramids. She offers directions and urges the captain to visit while in town.",
    247: "A hostess welcomes the captain, tells the legend of a nearby treasury, and recommends a visit in the fine weather.",
    248: "The guildmaster asks Hodram to take a survey party across the Atlantic to Rio de Janeiro. He explains how to carry the party and recommends extra funds.",
    249: "Hodram recalls the destination. The guildmaster asks about the survey and repeats its direction from this city.",
    250: "The guildmaster pays the survey expenses and reward. Two notices give the exact money and market-share results. He then suggests visiting the nearby ruins.",
}
DECISIONS = {
    244: """
6|||The hostess is pleased that the captain has come back. The brief welcome has the right warmth.
10|||Her natural question leads to the story of a river, and the material remains gold dust.
14|||The silent question is Hodram's puzzled reaction to the unexpected topic.
18|||She attributes the story to a sailor who visited the New World. Keep the river and its gold dust in his account.
22|||Her wistful question asks Hodram to picture it. Romantic expresses her own response to the idea.
""",
    245: """
7|||The casual greeting keeps the exact given-name substitution.
11|||The hostess shares her interest and points out that the town has ruins. Her question is friendly rather than a challenge.
14|You hadn't heard? They're close by. See that hill? The ruins are right at the top.|They're close by.;See that hill?;right at the top.|She is surprised the captain did not know, then points up the visible hill. Keep the two directions clear.
""",
    246: """
7|||She checks whether the captain has visited the pyramids yet. The direct question invites the brief answer.
11|||Hodram answers plainly, leaving her to recommend going.
15|You have to see them while you're here. I'll tell you how to get there. Go on, have a look!|while you're here.;how to get there.;have a look!|She urges a visit and offers directions. The source gives no promise that she will accompany the captain.
18|||Hodram acknowledges the suggestion and says he will remember it.
""",
    247: """
6|Welcome, FI. It's lovely out again today, isn't it?|again today, isn't it?|The hostess greets the captain by the existing substitution and remarks on another pleasant day.
10|||She asks about the ruins near town, then presents the story of King Solomon's treasury as a rumor.
13|||The short response shows interest and leaves her room to give the suggestion.
17|It's perfect picnic weather today. Why not go take a look?|perfect picnic weather;go take a look?|She suggests an outing because the weather is particularly inviting today. Preserve her playful comparison to a picnic.
""",
    248: """
5|I've got a job I'd like you to do.|I'd like you to do.|The guildmaster asks Hodram to take on a specific job before explaining the assignment.
9|Far to the west across the Atlantic is a village called Rio de Janeiro. I'd like you to take a survey party there.|across the Atlantic;Rio de Janeiro.;a survey party there.|The guildmaster gives the original destination and his request to transport surveyors.
12|||Hodram repeats the term to get clarification. Keep the short reaction before the hiring instruction.
16|Take them aboard as sailors. When you're at the tavern, hire more sailors than usual.|aboard as sailors.;more sailors than usual.|The guildmaster explains the native hiring step and the cover for carrying the survey party. Preserve tavern, sailors, and quantity relative to usual.
20|Across the Atlantic, to the southern part of the New World... That's a long way.|Across the Atlantic,;the New World...;a long way.|Hodram works out the distant region and reacts to the length of the voyage.
24|||The guildmaster says the distance is exactly why he chose to ask Hodram.
28|You'll need funds for the survey, so take a little extra money with you.|funds for the survey,;a little extra money|The guildmaster advises bringing more funds to cover the survey. This is a recommendation, not a grant of advance pay.
""",
    249: """
12|If I remember right, Rio de Janeiro is in the southern part of the New World.|Rio de Janeiro;the New World.|Hodram recalls where the village lies. Keep the whole place name readable.
18|How's the Rio de Janeiro survey coming? It's a long way west, across the Atlantic from here.|Rio de Janeiro;across the Atlantic|The guildmaster asks about the same survey and repeats the direction relative to this town.
""",
    250: """
5|Thanks. Here's your pay and the money to cover your expenses.|Here's your pay;to cover your expenses.|The guildmaster gives both a reward and the money for expenses.
10|||The result panel gives the exact amount of 42,000 gold coins in the established format.
34|||The separate notice says the player's market share in Sofala increased slightly. It gives no percentage.
52|||The guildmaster asks whether the captain has already visited the ruins near town.
55|Legend has it those ruins were once King Solomon's treasury. Go take a look.|Legend has it;King Solomon's treasury.;Go take a look.|The guildmaster attributes the treasury claim to legend and recommends visiting.
""",
}

review = checked_text(previous.review, {"len(records) == 36": "len(records) == 30"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::ruins-and-survey", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
