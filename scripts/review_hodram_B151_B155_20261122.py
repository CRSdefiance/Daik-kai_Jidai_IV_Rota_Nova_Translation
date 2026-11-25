"""Review the knife, Alexandria summons, Mediterranean map and Abkhaz lead."""

from scripts import pair_hodram_B151_B160_20261122 as paired
from scripts import review_hodram_B131_B132_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base,ROOT = previous.base,paired.ROOT
OUTPUT = ROOT/"B151_B155_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    151: "Hodram and Gerhard pair the knife with a matching sheath. Light flashes from it, and a pattern appears on the blade that Hodram believes is the New World map.",
    152: "A port worker relays word that someone is waiting in Alexandria. Hodram repeats the place in surprise.",
    153: "Hodram is let through to a stranger who awards him an object for commanding the Mediterranean. The stranger withholds details about Sera and points them toward ruins in Turkey.",
    154: "Charles or Yifa suggests using the Brass Lamp to reveal the cloth's design. Hodram tries it and credits whichever crewmate offered the idea.",
    155: "A port worker reports a new Black Sea town. Sera recognizes Abkhaz as her home and asks Hodram to take her there. He starts for it once he understands.",
}
DECISIONS = {
    151: """
5|The Ceremonial Knife and the Sun-Crest Sheath... The sizes match almost too well. It's as if they were made for each other.|the Sun-Crest Sheath...;almost too well.;made for each other.|Hodram observes the nearly exact fit and wonders whether the pieces were originally a pair. Preserve both approved titles.
9|||Gerhard agrees that they may once have been a set. His suggestion remains tentative.
13|Let's see if the knife fits the sheath... What?!|the knife fits the sheath...|Hodram decides to try the fit, then reacts when something unexpected happens. Keep the change of pace.
16|||Gerhard is startled by the sudden light. The brief response comes before Hodram identifies its source.
20|Light from the sheath? It's so bright I can't keep my eyes open!|Light from the sheath?;keep my eyes open!|Hodram identifies the sheath as the possible source and says the light is too bright for him to see.
26|||Hodram wonders what just happened after the light. His unsettled pause leads into Gerhard's discovery.
30|||Gerhard draws attention to the new pattern on the blade. The existing clear observation comes before Hodram explains it.
33|||Hodram identifies the likely New World map but cannot explain how it appeared. Keep his wonder and both distinct thoughts.
""",
    152: """
6|||The port worker says someone has said they will wait for Hodram in Alexandria. No name or reason is given.
9|||Hodram echoes Alexandria in surprise. The brief response leaves the news open.
""",
    153: """
6|||The guard checks the crew's company name through FO and lets them pass. The two short clauses preserve the gatekeeper's manner.
9|To you who rule the Mediterranean, I give this.|rule the Mediterranean,|The stranger presents something to the ruler of the Mediterranean in a ceremonial register. The line leaves the gift unnamed.
12|||Hodram asks who the stranger is. The pause keeps his question politely open.
16|||The stranger identifies himself only as someone who has resisted Ottoman rule for a long time. Leave his name unstated.
27|||Hodram asks if the stranger is the one who helped Sera and the others. The question leaves the claim unconfirmed.
34|You don't need the details. Decipher it, then find the Proof without delay.|don't need the details.;find the Proof without delay.|The stranger sidesteps the question and urges them to decipher the object and search promptly.
45|||The stranger says others escaped Ottoman rule as his group did and directs the crew to ruins in Turkey. The current line keeps the scope of the clue.
""",
    154: """
5|||Hodram is sure the Patterned Cloth has the Mediterranean map but has yet to see it. Preserve the exact item and his trailing thought.
9|It doesn't look like a map as it is.|look like a map|Gerhard observes that they cannot read the cloth as a map in its present state.
19|||Charles suggests trying the Brass Lamp and wonders whether invisible ink might account for the blank result. He presents that as a possibility.
25|||Yifa proposes applying heat with the Brass Lamp in a simpler, more direct turn. Leave the different voices separate.
31|||Hodram acts on the heat suggestion and describes warming the cloth. The pause lets the result appear before anyone explains it.
34|||Gerhard is surprised by the reveal. The short independent reaction carries no new information.
44|||Charles celebrates finding the map. The single exclamation fits his delight.
48|||Hodram credits Charles and states which Proof the map leads to. Keep the exact region and the correct crewmate.
54|I knew it!|I knew it!|Yifa celebrates being right in a casual burst. This is her own reaction on the alternate path.
58|||Hodram credits Yifa in the alternative and names the same Mediterranean destination. Keep the speaker-dependent recognition.
""",
    155: """
5|||The port worker catches Hodram's attention with the original surname substitution. Mr. fits the courteous familiar address.
8|||The worker reports a newly founded town on the Black Sea as a rumor. Keep the region and uncertainty.
11|What's it called?|What's it called?|Hodram asks the new town's name. A direct question fits the informal conversation with the port worker.
15|Abkhaz... I think that was it.|that was it.|The worker thinks he remembers the name but hedges it. Preserve the approved spelling.
19|||Gerhard repeats Abkhaz and says he has never heard of it. The pause follows his attempt to recognize it.
22|||Sera's separate silent exclamation marks her recognition before Hodram asks what is wrong.
26|||Hodram calls her by her given name and invites her to explain the reaction.
30|||Sera addresses Hodram through the original FI and asks him to take her there. The pauses preserve her compact delivery.
33|Sure. Do you know something about it?|know something about it?|Hodram agrees to the trip and asks what she knows. The natural assent gives her room to explain.
36|My country... They're building it again...|They're building it again...|Sera recognizes her homeland and says her people are rebuilding it together. The brief delivery matches her speech.
39|Do you mean it's your home?|it's your home?|Hodram checks that she means her homeland. The question gives her room to confirm it.
43|(She nods.)|(She nods.)|Sera confirms without speaking. A short stage direction makes the action read consistently with her introduction.
47|||Hodram understands that her people are rebuilding a town back home. The inference follows her nod.
50|||Hodram judges the town must be nearby since it is on the Black Sea and tells Sera they're going. His assertion remains a reasonable inference.
53|||Sera's eager assent closes the exchange after Hodram agrees to take her home.
""",
}
review = checked_text(previous.review,{"len(records) == 77":"len(records) == 42"})
scope = previous.scope | globals()
exec(compile(review,__file__+"::the-knife-and-Abkhaz","exec"),scope)


if __name__ == "__main__":
    scope["main"]()

