"""Review the Malacca monster hunt, its reward, and the lead to ancient ruins."""

from scripts import pair_hodram_B292_B310_20261122 as paired
from scripts import review_hodram_B291_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = paired.base, paired.ROOT
OUTPUT = ROOT / "B292_B293_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    292: "The guildmaster tells Hodram about a fish damaging ships in local waters. Hodram points out that finding it depends on luck. The guildmaster offers to wait.",
    293: "The guildmaster rewards Hodram for defeating the monster, but his aside about there being only one startles the captain. He then shares an unconfirmed jungle lead.",
}
DECISIONS = {
    292: """
5|||The guildmaster is glad Hodram arrived at the right time and introduces a favor in his usual familiar voice.
8|||The guildmaster expects disbelief and then explains the monster keeps appearing in local waters. The phrasing preserves the recurrence.
12|A monster...?|A monster...?|Hodram repeats the unexpected word and hesitates before the guildmaster supplies the fishermen's description.
16|The fishermen call it a monster fish. It takes bites out of ships until they sink.|call it a monster fish.;out of ships;until they sink.|The guildmaster attributes the term to the fishermen and explains how the fish sinks the ships.
19|||The guildmaster notes that the animal has already bitten through several ships this year. Keep the time frame and indefinite tally.
22|I thought you might be able to do something about it. What do you say? Will you take care of it for us?|might be able;do something about it.;What do you say?;take care of it for us?|The guildmaster hopes Hodram can help and asks him to deal with the monster. His questions express an appeal.
25|||Hodram says the encounter depends on luck. It does not promise the guildmaster a quick result.
28|I'll wait as long as it takes. I'm counting on you.|as long as it takes.;I'm counting on you.|The guildmaster says he is willing to wait patiently and asks Hodram to go ahead.
""",
    293: """
5|Incredible! You really did it! I knew you were something special!|You really did it!;something special!|The guildmaster is amazed at the result and praises Hodram with the same coarse enthusiasm.
9|Now let's hope there was only one of them...|there was only one of them...|The guildmaster wonders aloud whether the defeated fish was the only one, setting up Hodram's surprise.
12|||Hodram asks what he just heard. The short pause preserves his reaction to the aside.
16|||The guildmaster brushes off his remark and quickly offers the promised reward.
20|||The result panel gives the exact reward of 70,000 gold coins.
43|||The next notice records a slight increase in the player's Malacca market share.
60|||The guildmaster remembers an interesting rumor and opens a new subject.
63|They say the ruins of an ancient kingdom are still intact in the jungle, far inland from here.|an ancient kingdom;still intact in the jungle,;far inland from here.|The guildmaster says the remains of an ancient kingdom may still be intact in the jungle a long way inland. Preserve the claim as hearsay.
67|Really?|Really?|Hodram asks if the story is true, allowing the guildmaster to clarify that no one has actually found the ruins.
71|No one's found them yet. It's just a rumor, but maybe you'll be the one to find them.|No one's found them yet.;It's just a rumor,;the one to find them.|The guildmaster distinguishes the rumor from any confirmed discovery and suggests Hodram may be able to find the place.
""",
}
review = checked_text(previous.review, {"len(records) == 60": "len(records) == 18"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::malacca-monster-hunt", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
