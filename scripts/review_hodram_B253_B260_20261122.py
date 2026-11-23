"""Review the hostesses' ruins tips and the guild's search for Yuris."""

from scripts import pair_hodram_B241_B260_20261122 as paired
from scripts import review_hodram_B251_B252_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = paired.base, paired.ROOT
OUTPUT = ROOT / "B253_B260_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    253: "A hostess greets the captain and offers a nearby ruins tip she ordinarily withholds from visitors from abroad.",
    254: "A hostess is surprised by the captain's worldwide search for ruins and says her town has none of note.",
    255: "Another hostess welcomes the captain and gives her own version of the answer about locally famous ruins.",
    256: "The guildmaster offers an assignment to find Yuris Huygens. Yuris's people have complained that he seldom comes back from his journeys.",
    257: "A messenger confirms the captain's surname and says the London guild is looking for them.",
    258: "Hodram tries to find Yuris in Syracuse. A man absorbed in the sight of Roman remains turns out to be Yuris himself. He remembers his duties and asks to be taken home. Hodram says they will go to London first.",
    259: "The guildmaster welcomes Yuris back, gives him time to rest, and pays Hodram. Another visitor asks about maps, then insults the guildmaster. Hodram learns about the distant ruins that the maps lead to.",
    260: "Hodram reminds himself to look for Yuris in Syracuse. The guildmaster relays a rumor specifically placing him in the square.",
}
DECISIONS = {
    253: """
7|||The warm greeting retains the given-name substitution in its original role.
10|||The hostess asks about the search and says there are ruins nearby. Her short question stays direct.
13|||She says she usually keeps the ruins to herself when speaking to visitors from abroad. The exception belongs to her offer to tell this captain.
""",
    254: """
6|||The welcome keeps the original given-name substitution and suits the hostess's polite greeting.
9|You're looking for ruins all over the world? Hmm... We don't have any famous ones here.|ruins all over the world?;any famous ones here.|She checks she understood the scale of the search and considers what the town has. The answer is limited to famous ruins.
""",
    255: """
6|||The familiar greeting keeps the exact given-name substitution.
10|You travel the world looking for ruins? I'm afraid we don't have any famous ones here.|looking for ruins?;any famous ones here.|She is surprised by the search and apologetically says her town has no famous ruins. Keep the natural distinction from the other hostess.
""",
    256: """
5|I've got a job for you. Interested in finding someone?|I've got a job for you.;finding someone?|The guildmaster offers the job of finding a particular person and asks whether the captain will take it.
9|||The job is to find a Dutch nobleman called Yuris Huygens. Keep both his approved name and nationality.
12|For a nobleman, he's awfully fond of taking off on long trips. His people say he never comes back to his estate.|taking off on long trips.;his estate.|The guildmaster passes on the complaints and remarks on the contrast with his duties.
16|||The guildmaster says Yuris may have been seen in Syracuse. His trailing delivery preserves the uncertainty.
""",
    257: """
6|||The messenger confirms the surname before saying the London guild has been looking for the captain. Keep the original surname substitution and familiar turn.
""",
    258: """
5|If I remember right, this is the town where that fellow Yuris was seen.|this is the town;that fellow Yuris was seen.|Hodram recalls the reported sighting. He has yet to recognize Yuris by appearance.
8|||The stranger admires ancient Rome. His attention to its beauty sets up Hodram's interruption.
12|||Hodram politely asks whether the stranger knows a man called Yuris. The simple question suits their first meeting.
15|||The stranger continues admiring the ruins, as if he had not heard the question.
19|||Hodram checks whether the man is listening. The hesitation sharpens his impatience.
23|||The stranger says he heard him all along and identifies himself as Yuris. The dry delivery lands the reveal.
27|You are? Now that you mention it, you do carry yourself like a nobleman. Rather elegantly, too...|carry yourself like a nobleman.;Rather elegantly, too...|Hodram is surprised, then recognizes an elegance that could suggest his standing.
31|You've got duties to see to. Your people are upset because their lord went away and never came back.|duties to see to.;went away;never came back.|Hodram reminds him of what his position requires and conveys his people's complaint.
34|Oh, no! I'd forgotten all about my estate! Would you take me back there?|forgotten all about my estate!;take me back there?|Yuris remembers what he neglected and asks for help getting home.
37|||Hodram says they will go to London before sorting out the rest. The reply advances the assignment without promising a different destination.
""",
    259: """
5|Ah, Yuris. What have you been doing all this time? Your people have had a hard time with you away from your duties.|all this time?;away from your duties.|The guildmaster speaks directly to Yuris about his absence and the hardship it caused.
9|||Yuris apologizes, says he loses track of things when traveling, and promises to return right away. Keep both the apology and the promise.
13|Honestly... You must be tired after that journey. Rest here awhile before you go home.|tired after that journey.;before you go home.|The guildmaster is exasperated but offers Yuris time to rest. The invitation softens the rebuke.
17|Oh, I almost forgot. It's a small reward, but please take it.|I almost forgot.;please take it.|The guildmaster interrupts himself to give the captain a modest reward.
21|||The result notice gives the exact amount of 11,000 gold coins.
49|||The next notice records a slight increase in London market share. Preserve the qualitative increase.
60|||The guildmaster excuses himself and turns to someone he thinks is a customer.
64|||The visitor asks whether the maps are sold out. Hey conveys the blunt address without inventing a relationship.
68|||The guildmaster recognizes the returning group and confirms there are no maps left.
71|||The visitor dismisses the shop as useless. The brusque insult sets up the guildmaster's reaction.
75|||The pause separates the insult from the guildmaster snapping back.
79|||The guildmaster blames this exact group for buying the maps. His anger follows the insult.
82|||Hodram asks about the maps. The brief question redirects the conversation to the ruins.
86|Maps to some ruins. A strange bunch has been hanging around there lately. I hear the locals are fed up with them.|Maps to some ruins.;hanging around there lately.;fed up with them.|The guildmaster describes what the maps show and reports the local complaints as hearsay.
90|||Hodram asks if the ruins are nearby. The brief question prompts the distance explanation.
94|They're a long way off, but easy to reach with a map. Trouble is, that lot bought every last one.|easy to reach with a map.;bought every last one.|The guildmaster distinguishes distance from ease of finding the ruins and explains why he can't supply a map.
97|||The guildmaster suggests another town might still have a map. Keep the suggestion uncertain.
100|||Hodram quiets down as he takes in the new lead. The pause leaves it open.
""",
    260: """
12|I'd better go to Syracuse and find this Yuris.|go to Syracuse;find this Yuris.|Hodram reminds himself of the remaining job and the town where he should look.
17|||The guildmaster repeats the report and specifies the square at Syracuse. Keep the location more exact than the earlier town-level clue.
""",
}

review = checked_text(previous.review, {"len(records) == 77": "len(records) == 42"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::hostesses-and-yuris", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
